# Image-Backed Service Iteration

Use these rules when iterating on a MeshAgent service whose runtime should be packaged into a container image instead of being edited live in room storage.

- This pattern is for service-style runtime changes, not the default for `meshagent webserver deploy` file-backed sites.
- Prefer image-backed iteration when the service has non-trivial runtime dependencies, repeated code changes, or a meaningful need to contain changes and revert them quickly.
- Build images inside the room with `meshagent room container image build ...` when the source context is already in room or mounted storage.
- Use explicit, versioned image tags for every candidate build. Prefer release-candidate tags such as `4.2-rc1`, `4.2-rc2`, `4.2-rc3`, and reserve the plain release tag `4.2` for the image that has passed verification.
- Do not overwrite a single floating tag and call that rollback-ready.
- Keep the last known good plain release tag available. There is no native service rollback command; rollback means updating the service spec back to the previous known-good release tag.
- If the runtime has cheap unit or smoke tests that can run during image build, bake them into the image build path so a broken candidate image never becomes deployable.
- After building an image, verify it exists with `meshagent room container image list ...` before updating the service to reference it.
- Update the service declaratively so `container.image` points at the new candidate image tag first.
- After the service update, verify both service/runtime health and the actual user-facing surface. A successful image build and service update are not enough.
- Only add or move the plain release tag after the corresponding `-rcN` candidate image has passed the required verification.
- Do not roll back automatically just because a candidate image failed verification. Leave the rollback as an explicit user-controlled action unless the user asked for automatic rollback behavior.
- If the user asks to roll back, update the service back to the previous known-good plain release tag instead of guessing among unverified candidate tags.
- Use `meshagent room container image save ...` only when you need to archive or export a built image. It is not the normal rollback mechanism.
- When image-backed iteration is the chosen path, avoid mixing it with ad hoc live-file edits to the same service runtime in the same pass.
