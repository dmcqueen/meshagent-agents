# Verification checklist

Use this before claiming a room-hosted contact form is done.

## Website

- `webserver.yaml` uses `host: 0.0.0.0`
- route source paths are relative and live under the current working directory
- public URL uses the correct managed suffix for the active API environment
- live `GET /` returns `200`

## Form behavior

- invalid `POST` returns `400` and renders a validation message
- valid `POST` reaches the success path and does not raise `500`
- if the task requires outbound email, valid `POST` reaches provider acceptance rather than stopping at `SMTPDataError`, `550`, or `553`
- a working form page plus a failing valid `POST` is not a completed contact-form workflow

## Diagnosis

- `500` first: inspect handler import, template rendering, and runtime exceptions
- `502` first: inspect `host`, bind port, and route-to-service wiring
- mailbox `409` plus mailbox read `403`: treat that candidate as unavailable and try another one
- mailbox exists but valid `POST` fails with a runtime exception: inspect the actual send path before blaming mailbox queue creation
