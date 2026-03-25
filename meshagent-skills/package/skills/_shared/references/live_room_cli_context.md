# Live Room CLI Context

Use these rules when a skill runs inside an existing MeshAgent room runtime or room shell.

- Reuse the existing MeshAgent CLI session and room context before asking the user to log in again.
- If `MESHAGENT_ROOM` is present, prefer room-scoped commands and pass `--room "${MESHAGENT_ROOM}"` when the command requires it.
- If `MESHAGENT_ROOM` is already present, do not use room-listing commands as a prerequisite for room-scoped work.
- If the user already named the room or the current runtime clearly implies the room, do not use broad project or room listing commands as a prerequisite for room-scoped work.
- If authentication is uncertain, test a room-scoped read command first. Do not claim the CLI is unauthenticated until an actual MeshAgent command fails for that reason.
- For room-scoped workflows, do not use `meshagent auth whoami`, `meshagent project list`, or unfiltered `meshagent rooms list` as the primary readiness test.
- A `403` from a broad project-scoped or room-listing command does not by itself prove that a narrower room-scoped workflow is blocked. Retry with the narrowest relevant room-scoped read path first.
- Good first probes are commands such as `meshagent room service list --room <ROOM_NAME>`, `meshagent room queue size --room <ROOM_NAME> --queue <QUEUE_NAME>`, or `meshagent room agent list-toolkits --room <ROOM_NAME>` depending on the workflow.
- Treat existing MeshAgent environment variables and active CLI session state as real runtime context to inspect and use.
- Distinguish local authoring files from room-visible runtime files. Room-owned runtime data belongs under `/data`.
- If the user asks to write or create a file in the room and does not provide a more specific room-visible path, default to the room storage root under `/data`, for example `/data/<filename>`.
- Do not default room file writes to `.`, the current working directory, or other ad hoc paths when the request is clearly about a room-visible file.
- For `meshagent webserver deploy`, local source files are uploaded from the current working directory, while `--website-path` is the room-storage destination.
- Do not treat `/data/...` as the local source root for deployable website files unless the current working directory is already under `/data`.
- Do not treat `/tmp` as the durable room workspace.
- Do not use room file tools against `.` , `/`, or temporary/build paths such as `/tmp`. Use concrete room-visible paths under `/data`, or use shell commands when the task really needs a non-room-local path.
