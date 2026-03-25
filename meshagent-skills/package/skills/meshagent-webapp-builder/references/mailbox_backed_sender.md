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
- Do not treat mailbox creation alone as proof that the contact form has a working outbound send path.
- Do not treat a missing queue in generic queue inspection as proof that mailbox creation failed. A contact form may still be broken for other reasons.

## Minimal CLI flow

1. `meshagent mailbox list --room "$MESHAGENT_ROOM"`
2. If needed, try one or more collision-resistant `meshagent mailbox create` candidates.
3. Choose the send path deliberately:
   - prefer the room mail path for normal contact forms
   - use direct SMTP only if the runtime has already proven SMTP configuration or the user asked for raw SMTP
4. Write the successful mailbox address into the handler configuration.
5. Re-test a valid form submission after deploy.

## SMTP configuration

When the handler uses direct SMTP, use only the runtime defaults that exist in `meshagent.agents.mail_common`:

- `SMTP_USERNAME`
- `SMTP_PASSWORD`
- `SMTP_HOSTNAME`
- `SMTP_PORT`

The mailbox address is still the sender identity. SMTP username and password do not define the `From` address.
If those runtime defaults are not actually present, do not keep the contact form on a direct-SMTP design just because the mailbox exists.

## Failure interpretation

- `SMTPDataError`, `550`, `553`, or similar after the form renders successfully usually means sender authorization is still wrong.
- A live site with this failure is not complete.
