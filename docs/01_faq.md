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
