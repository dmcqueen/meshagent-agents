# Claude Customer Support MeshAgent

## Summary

An agent that uses Anthropic's customer support knowledge work plugin with a nightly docs sync worker

## Long Description

An agent that uses Anthropic's customer support knowledge work plugin with a nightly docs sync worker. It defines 3 runtime agent configuration(s): claude-customer-support-meshagent (ChatBot), claude-customer-support-meshagent (MailBot), claude-customer-support-meshagent (Worker). The workflow is shaped by 5 rule file(s) (draft-response.md, escalate.md, kb-article.md, research.md, triage.md) and 6 skill directory reference(s) (customer-research, escalation, knowledge-management, response-drafting, ticket-triage;, and 1 more). The bundle includes 5 embedded command doc(s) and 5 embedded skill file(s) from the knowledge-work-plugins package. It is configured to run on image reference(s): us-central1-docker.pkg.dev/meshagent-life/meshagent-public/shell-terminal:{SERVER_VERSION}-esgz.

## Install Links

- Dev: https://app.powerboards.life/install?url=https://raw.githubusercontent.com/dmcqueen/meshagent-agents/cb92f24e7cf3e05526f32b6e28df2092f3f21eb9/knowledge-work-plugins/customer-support.docs/agents.dev.yaml
- Prod: https://app.powerboards.com/install?url=https://raw.githubusercontent.com/dmcqueen/meshagent-agents/ebea06f425f8b1a0f6d4013aac027ccba3a153a9/knowledge-work-plugins/customer-support.docs/agents.prod.yaml

## Raw SHA Links

- Dev: https://raw.githubusercontent.com/dmcqueen/meshagent-agents/cb92f24e7cf3e05526f32b6e28df2092f3f21eb9/knowledge-work-plugins/customer-support.docs/agents.dev.yaml
- Prod: https://raw.githubusercontent.com/dmcqueen/meshagent-agents/ebea06f425f8b1a0f6d4013aac027ccba3a153a9/knowledge-work-plugins/customer-support.docs/agents.prod.yaml
