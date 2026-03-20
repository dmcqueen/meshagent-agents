# Mailbox-backed sender pattern

Use this flow for room-hosted contact forms that send outbound mail.

## Rules

- Reuse an existing mailbox for the room when it already fits the workflow.
- If no suitable mailbox exists, create a collision-resistant address derived from the room and workflow purpose.
- Treat `409` on mailbox creation as a candidate collision, not proof that the exact address is available to use.
- If mailbox inspection returns `403`, try another candidate before asking the user for mailbox access help.
- Use the exact mailbox address returned by the CLI as the `From` address.
- Use the visitor email only as `Reply-To` when present.
- Do not synthesize sender addresses such as `contact-form@<mail-domain>`.
- Do not invent sender env vars such as `FROM_ADDRESS`, `MAIL_FROM`, `SMTP_FROM`, or `MESHAGENT_PARTICIPANT_NAME`.

## Minimal CLI flow

1. `meshagent mailbox list --room "$MESHAGENT_ROOM"`
2. If needed, try one or more collision-resistant `meshagent mailbox create` candidates.
3. Write the successful mailbox address into the handler configuration.
4. Re-test a valid form submission after deploy.

## SMTP configuration

When the handler uses direct SMTP, use only the runtime defaults that exist in `meshagent.agents.mail_common`:

- `SMTP_USERNAME`
- `SMTP_PASSWORD`
- `SMTP_HOSTNAME`
- `SMTP_PORT`

The mailbox address is still the sender identity. SMTP username and password do not define the `From` address.

## Failure interpretation

- `SMTPDataError`, `550`, `553`, or similar after the form renders successfully usually means sender authorization is still wrong.
- A live site with this failure is not complete.
