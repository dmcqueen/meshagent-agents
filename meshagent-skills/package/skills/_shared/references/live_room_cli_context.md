# Live Room CLI Context

Use these rules when a skill runs inside an existing MeshAgent room runtime or room shell.

- Reuse the existing MeshAgent CLI session and room context before asking the user to log in again.
- If `MESHAGENT_ROOM` is present, prefer room-scoped commands and pass `--room "${MESHAGENT_ROOM}"` when the command requires it.
- If `MESHAGENT_ROOM` is already present, do not use room-listing commands as a prerequisite for room-scoped work.
- If authentication is uncertain, test a room-scoped read command first. Do not claim the CLI is unauthenticated until an actual MeshAgent command fails for that reason.
- Treat existing MeshAgent environment variables and active CLI session state as real runtime context to inspect and use.
- Distinguish local authoring files from room-visible runtime files. Room-owned runtime data belongs under `/data`.
- For `meshagent webserver deploy`, local source files are uploaded from the current working directory, while `--website-path` is the room-storage destination.
- Do not treat `/data/...` as the local source root for deployable website files unless the current working directory is already under `/data`.
- Do not treat `/tmp` as the durable room workspace.
- Do not use room file tools against `.` , `/`, or temporary/build paths such as `/tmp`. Use concrete room-visible paths under `/data`, or use shell commands when the task really needs a non-room-local path.
