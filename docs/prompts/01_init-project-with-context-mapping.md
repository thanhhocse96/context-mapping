# Prompt: Init Project With Context Mapping

Use this prompt when initializing a separate application repo to use `context-mapping`.

Assumptions:

- The application repo is the current working directory.
- The `context-mapping` tool repo is available at `../context-mapping` relative to the application repo.
- The dev environment is WSL Debian.
- Python dependencies should run inside a `.venv` managed from WSL Debian.

````text
You are initializing this project to use context-mapping.

Important paths and environment:

- Application repo: current working directory
- context-mapping tool repo: ../context-mapping
- Dev environment: WSL Debian
- Python environment: .venv, created and used from WSL Debian

Follow this workflow strictly.

1. Inspect the application repo first

Read:

- README.md if it exists
- AGENTS.md if it exists
- .gitignore if it exists
- existing .context/ files if they exist
- package/build config relevant to the stack

Do not overwrite existing project instructions or context files without reporting what already exists.

Detect the governance root before creating milestone or tension files:

- If the current repo contains multiple apps, packages, plugins, services, or deployable projects, treat the repo root as one program governance root.
- Root `.context/MILESTONES.md` is the only milestone source of truth.
- Root `.context/TENSIONS_OPEN.md`, `.context/TENSIONS_ACTIVE.md`, and `.context/TENSIONS_HISTORY.md` are the only tension system.
- Subprojects use `Area:` or tags to scope work. Do not create `apps/<name>/.context/MILESTONES.md`, `plugins/<name>/.context/MILESTONES.md`, or package-local `TENSIONS_*.md`.
- A subproject may keep an implementation checklist in its README or issue tracker, but it must not redefine roadmap authority.
- Only create separate governance files if the subproject is already its own repository or the human explicitly approves a governance split.

2. Confirm local environment shape

If `.local/ENVIRONMENT.md` exists, read it first.

If it does not exist, create `.local/ENVIRONMENT.md` with non-secret machine-local setup details for this project:

```text
# Local Environment

# Do not commit this file. It is ignored by git.

PROJECT_ROOT_WINDOWS=
PROJECT_ROOT_WSL=
CONTEXT_MAPPING_ROOT_WINDOWS=
CONTEXT_MAPPING_ROOT_WSL=../context-mapping

WSL_DISTRO=Debian
PYTHON_VENV_PATH_WSL=.venv

CONTEXT_GEN_BUILD_CMD=.venv/bin/python ../context-mapping/cli.py build . --quiet
CONTEXT_GEN_CHECK_CMD=.venv/bin/python ../context-mapping/cli.py check-consistency .
CONTEXT_GEN_LOAD_EXAMPLE_CMD=.venv/bin/python ../context-mapping/cli.py load <module_path> . --include-manual

NOTES=
```

Also ensure `.local/` is listed in `.gitignore`.

Do not put credentials in committed docs.

3. Prepare the WSL Debian Python environment

Use WSL Debian.

If the project is inside the Linux filesystem, create/use project-local `.venv`:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

If the project is on a Windows mount such as `/mnt/c/...` or `/mnt/d/...`, ask the human whether to:

- keep the requested project-local `.venv`, or
- use a venv in the Linux filesystem such as `~/.venvs/<project-name>`.

Do not create a `.venv` on a Windows mount without confirming this choice.

Install context-mapping dependencies into the active project `.venv` from the tool repo:

```bash
python -m pip install --upgrade pip
python -m pip install -r ../context-mapping/requirements.txt
```

If optional commands are needed, install optional dependencies only after explaining why.

4. Initialize context files

From the application repo, run:

```bash
.venv/bin/python ../context-mapping/cli.py build . --quiet
```

If using an already active WSL venv, this is also acceptable:

```bash
python ../context-mapping/cli.py build . --quiet
```

If build reports no source files, explain whether the project uses an unsupported language or whether source files are outside the parser scope.

5. Add or update project AGENTS.md

If AGENTS.md does not exist, create one with:

- instruction to read `.context/GLOBAL.md`
- instruction to load relevant module context with `../context-mapping/cli.py load <module_path> . --include-manual`
- instruction to read `.context/TENSIONS_OPEN.md` if present
- instruction that monorepo/multi-project milestones and tensions live at the governance root, while subprojects use `Area:` or tags
- instruction that `.local/ENVIRONMENT.md` is machine-local and must not be committed
- instruction that `[manual]` sections must not be overwritten

If AGENTS.md exists, add only the missing context-mapping protocol. Preserve existing project-specific rules.

6. Verify

Run:

```bash
.venv/bin/python ../context-mapping/cli.py check-consistency .
.venv/bin/python ../context-mapping/cli.py build . --quiet
```

If using an already active WSL venv, use:

```bash
python ../context-mapping/cli.py check-consistency .
python ../context-mapping/cli.py build . --quiet
```

7. Report back

Summarize:

- files created or changed
- which path was treated as the governance root
- whether `.context/GLOBAL.md` exists
- which modules were detected
- whether any tension files exist
- any unsupported language/parser gaps
- the exact command to load context for the first useful module

Do not commit anything unless the human explicitly asks.
````
