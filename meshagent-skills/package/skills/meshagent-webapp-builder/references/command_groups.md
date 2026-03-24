# MeshAgent Webapp Builder CLI references

The primary packaged CLI routing reference lives at:

- `skills/meshagent-cli-operator/references/command_groups.md`

Open that shared file for the actual command-family routing details. This local wrapper
exists so `meshagent-webapp-builder` can point to package-local references without
sending the model to live `meshagent --help` by default.
