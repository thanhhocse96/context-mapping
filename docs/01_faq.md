# FAQ

## Is context-mapping an Agent Harness?

No. `context-mapping` is not an Agent Harness.

An Agent Harness is usually the runtime/control layer for agents:

- how agents run
- which tools agents can call
- task execution loops
- memory/session orchestration
- permissions, retries, and automation

`context-mapping` is the project memory and governance layer for Agentic Engineering:

- what the code currently exposes
- why the system is designed that way
- what constraints must not be broken
- which tensions are unresolved
- what milestone is active
- what evidence proves a slice is done

An Agent Harness answers:

```text
How does the agent operate?
```

`context-mapping` answers:

```text
What must the agent know before it operates, and what must it not violate?
```

They can work together:

- Agent Harness drives execution.
- `context-mapping` supplies project context, intent, constraints, milestone scope, and tension tracking.

The nearest concept is:

```text
context-mapping is a context governance layer for Agentic Engineering workflows.
```

It helps humans and agents share the same project memory without relying on long chat history or fragile assumptions.

## Is context-mapping the same as Agentic Engineering?

No. It is part of an Agentic Engineering workflow, but it is not the whole workflow.

Agentic Engineering usually focuses on making agents act effectively:

- task decomposition
- tool use
- planning and execution loops
- test and CI feedback
- multi-agent or automated coding workflows

`context-mapping` focuses on making agents understand correctly before they act:

- project intent
- design decisions
- invariants and constraints
- unresolved tensions
- milestone scope
- evidence that a slice is done

In short:

```text
Agentic Engineering:
  How do agents act effectively?

context-mapping:
  What must agents know before acting, and what must they not violate?
```

The key difference is that `context-mapping` does not try to make agents more autonomous.
It tries to make agents less likely to guess.

It turns human design intent into repo artifacts:

- `.context/GLOBAL.md`
- `.context/*.md`
- `.context/TENSIONS*.md`
- `AGENTS.md`
- milestone docs

That makes it an epistemic and governance layer for Agentic Engineering: the agent still codes, tests, and uses tools, but it does so inside a project memory with explicit constraints and decision history.
