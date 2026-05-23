"""
PowerShell parser: extract script parameters, functions, and command bridges using
the official PowerShell AST parser.

This parser intentionally does not use regex for syntax extraction. It shells out to
PowerShell and calls System.Management.Automation.Language.Parser.ParseFile.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import base64
from pathlib import Path

from schema import FunctionInfo, ModuleContext, ParserPlugin, register_plugin


_SKIP_DIRS = {
    ".git",
    ".context",
    "__pycache__",
    "node_modules",
    "vendor",
    "reports",
    "tests/generated",
}

_COMMON_CMDLETS = {
    "add-member", "compare-object", "convertfrom-json", "convertto-json",
    "copy-item", "export-csv", "foreach-object", "format-list", "format-table",
    "get-childitem", "get-command", "get-content", "get-date", "get-item",
    "get-itemproperty", "get-location", "get-process", "get-service",
    "import-csv", "join-path", "measure-object", "move-item", "new-item",
    "new-object", "out-file", "out-null", "read-host", "remove-item",
    "remove-itemproperty", "rename-item", "select-object", "set-content",
    "set-itemproperty", "set-location", "sort-object", "split-path",
    "start-process", "start-sleep", "test-path", "where-object", "write-error",
    "write-host", "write-output", "write-progress", "write-warning",
}

_PS_AST_HELPER = r"""
$ErrorActionPreference = 'Stop'
$path = $script:ContextPowerShellFile
if (-not $path) { throw 'CONTEXT_PS_FILE is not set.' }

$tokens = $null
$errors = $null
$ast = [System.Management.Automation.Language.Parser]::ParseFile($path, [ref]$tokens, [ref]$errors)

function Convert-CommentText {
    param([string]$Text)
    if ($null -eq $Text) { return '' }
    return ($Text -replace '^\s*#\s?', '').Trim()
}

function Get-DocComment {
    param([int]$Line)

    $comments = @($tokens | Where-Object {
        $_.Kind -eq 'Comment' -and $_.Extent.EndLineNumber -lt $Line
    } | Sort-Object { $_.Extent.EndLineNumber } -Descending)

    $lines = New-Object System.Collections.Generic.List[string]
    $expected = $Line - 1

    foreach ($comment in $comments) {
        if ($comment.Extent.EndLineNumber -ne $expected) { break }
        $lines.Insert(0, (Convert-CommentText $comment.Text))
        $expected = $comment.Extent.StartLineNumber - 1
    }

    $joined = (($lines | Where-Object { $_ }) -join ' ')
    return $joined
}

function Convert-ParamAst {
    param($Param)
    if ($null -eq $Param) { return '' }
    return $Param.Extent.Text.Trim()
}

$scriptParams = @()
if ($ast.ParamBlock) {
    foreach ($param in $ast.ParamBlock.Parameters) {
        $scriptParams += (Convert-ParamAst $param)
    }
}

$functions = @()
$functionAsts = @($ast.FindAll({
    param($node)
    $node -is [System.Management.Automation.Language.FunctionDefinitionAst]
}, $true))

foreach ($fn in $functionAsts) {
    $params = @()
    if ($fn.Parameters) {
        foreach ($param in $fn.Parameters) {
            $params += (Convert-ParamAst $param)
        }
    }
    elseif ($fn.Body -and $fn.Body.ParamBlock) {
        foreach ($param in $fn.Body.ParamBlock.Parameters) {
            $params += (Convert-ParamAst $param)
        }
    }

    $functions += [pscustomobject]@{
        Name = $fn.Name
        Line = $fn.Extent.StartLineNumber
        Params = $params
        DocComment = (Get-DocComment $fn.Extent.StartLineNumber)
    }
}

$commands = @()
$commandAsts = @($ast.FindAll({
    param($node)
    $node -is [System.Management.Automation.Language.CommandAst]
}, $true))

foreach ($cmd in $commandAsts) {
    $name = $cmd.GetCommandName()
    if ($name -and $commands -notcontains $name) {
        $commands += $name
    }
}

$usingStatements = @()
$usingAsts = @($ast.FindAll({
    param($node)
    $node -is [System.Management.Automation.Language.UsingStatementAst]
}, $true))

foreach ($using in $usingAsts) {
    $usingStatements += $using.Extent.Text.Trim()
}

$parseErrors = @()
foreach ($err in @($errors)) {
    $parseErrors += [pscustomobject]@{
        Message = $err.Message
        Line = $err.Extent.StartLineNumber
    }
}

[pscustomobject]@{
    ScriptParams = $scriptParams
    Functions = $functions
    Commands = $commands
    UsingStatements = $usingStatements
    ParseErrors = $parseErrors
} | ConvertTo-Json -Depth 8 -Compress
"""


def _candidate_backends() -> list[list[str]]:
    backends: list[list[str]] = []
    for exe in ("pwsh", "powershell"):
        found = shutil.which(exe)
        if found:
            backends.append([found])

    windows_powershell = Path("/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe")
    if windows_powershell.exists():
        backends.append([str(windows_powershell)])

    return backends


def _run_powershell_ast(path: Path) -> dict:
    backends = _candidate_backends()
    if not backends:
        raise RuntimeError(
            "No PowerShell AST backend found. Install PowerShell 7 (`pwsh`) or run on Windows PowerShell."
        )

    last_error = ""
    for backend in backends:
        backend_path = _path_for_backend(path, backend[0])
        path_literal = backend_path.replace("'", "''")
        helper = f"$script:ContextPowerShellFile = '{path_literal}'\n{_PS_AST_HELPER}"
        encoded_helper = base64.b64encode(helper.encode("utf-16-le")).decode("ascii")
        cmd = backend + ["-NoProfile", "-ExecutionPolicy", "Bypass", "-EncodedCommand", encoded_helper]
        try:
            completed = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
        except OSError as exc:
            last_error = str(exc)
            continue

        stdout = _decode_powershell_output(completed.stdout)
        stderr = _decode_powershell_output(completed.stderr)

        if completed.returncode == 0 and stdout.strip():
            return json.loads(stdout)

        last_error = stderr.strip() or stdout.strip()

    raise RuntimeError(f"PowerShell AST parse failed for {path}: {last_error}")


def _path_for_backend(path: Path, backend: str) -> str:
    path_text = str(path)
    if backend.endswith("powershell.exe") and path_text.startswith("/mnt/"):
        parts = path_text.split("/")
        if len(parts) >= 4 and len(parts[2]) == 1:
            drive = parts[2].upper()
            rest = "\\".join(parts[3:])
            return f"{drive}:\\{rest}"
    return path_text


def _decode_powershell_output(data: bytes) -> str:
    if not data:
        return ""
    if data.startswith(b"\xff\xfe") or data.startswith(b"\xfe\xff"):
        for encoding in ("utf-16", "utf-16-le", "utf-16-be"):
            try:
                return data.decode(encoding)
            except UnicodeDecodeError:
                continue
    if b"\x00" in data[:80]:
        try:
            return data.decode("utf-16-le")
        except UnicodeDecodeError:
            pass
    for encoding in ("utf-8-sig", "utf-8", "cp1252"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def _script_function_from_params(path: Path, data: dict) -> FunctionInfo | None:
    params = data.get("ScriptParams", []) or []
    if not params:
        return None
    return FunctionInfo(
        name=path.stem,
        is_public=True,
        is_async=False,
        params=[str(p) for p in params],
        return_type=None,
        doc_comment=None,
        line=1,
    )


def parse_powershell_file(path: Path):
    data = _run_powershell_ast(path)

    functions: list[FunctionInfo] = []
    script_fn = _script_function_from_params(path, data)
    if script_fn:
        functions.append(script_fn)

    for item in data.get("Functions", []) or []:
        functions.append(FunctionInfo(
            name=item.get("Name", ""),
            is_public=True,
            is_async=False,
            params=[str(p) for p in item.get("Params", []) or []],
            return_type=None,
            doc_comment=item.get("DocComment") or None,
            line=int(item.get("Line", 1) or 1),
        ))

    imports = [str(x) for x in data.get("UsingStatements", []) or []]
    commands = [str(x) for x in data.get("Commands", []) or []]
    errors = data.get("ParseErrors", []) or []
    return functions, imports, commands, errors


def parse_powershell_directory(dir_path: Path, project_root: Path) -> ModuleContext:
    rel = str(dir_path.relative_to(project_root))
    ctx = ModuleContext(path=rel, language="powershell")

    files = sorted(
        list(dir_path.glob("*.ps1")) +
        list(dir_path.glob("*.psm1")) +
        list(dir_path.glob("*.psd1"))
    )
    parse_error_imports: list[str] = []
    parsed_files = []

    for file_path in files:
        ctx.source_files.append(str(file_path.relative_to(project_root)))
        functions, imports, commands, errors = parse_powershell_file(file_path)
        parsed_files.append((functions, imports, commands, errors, file_path))
        ctx.public_functions.extend(functions)

    function_names = {fn.name.lower() for fn in ctx.public_functions}

    for functions, imports, commands, errors, file_path in parsed_files:
        for imp in imports:
            if imp not in ctx.imports:
                ctx.imports.append(imp)
        for cmd in commands:
            cmd_lower = cmd.lower()
            is_project_function = cmd_lower in function_names
            is_external_tool = "." in cmd or "-" not in cmd
            if (is_project_function or is_external_tool) and cmd_lower not in _COMMON_CMDLETS and cmd not in ctx.tauri_commands:
                ctx.tauri_commands.append(cmd)
        for err in errors:
            message = err.get("Message", "Parse error")
            line = err.get("Line", "?")
            parse_error_imports.append(f"# Parse error in {file_path.name}:{line}: {message}")

    for err in parse_error_imports:
        if err not in ctx.imports:
            ctx.imports.append(err)

    return ctx


def _is_skipped(path: Path) -> bool:
    normalized_parts = set(path.parts)
    if normalized_parts & _SKIP_DIRS:
        return True
    normalized = str(path).replace("\\", "/")
    return any(f"/{skip}/" in normalized for skip in _SKIP_DIRS if "/" in skip)


def _find_powershell_dirs(root: Path) -> list[Path]:
    dirs: list[Path] = []
    for pattern in ("*.ps1", "*.psm1", "*.psd1"):
        for ps_file in root.rglob(pattern):
            if _is_skipped(ps_file.relative_to(root)):
                continue
            if ps_file.parent not in dirs:
                dirs.append(ps_file.parent)
    return sorted(dirs)


register_plugin(ParserPlugin(
    language="powershell",
    extensions=[".ps1", ".psm1", ".psd1"],
    find_dirs=_find_powershell_dirs,
    parse_dir=parse_powershell_directory,
    skip_dirs=_SKIP_DIRS,
    ipc_label="PowerShell Commands / External Tools",
))
