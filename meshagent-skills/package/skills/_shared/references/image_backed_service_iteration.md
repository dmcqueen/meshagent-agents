# Image-Backed Service Iteration

Use these rules when iterating on a MeshAgent service whose runtime should be packaged into a container image instead of being edited live in room storage.

- This pattern is for `candidate` and `release` deployment modes on service-style runtimes, not the default for `dev` file-backed previews.
- In `dev` mode, the priority is fast iteration on behavior. A file-backed preview can be acceptable if the user has not asked for rollback-ready or release-ready packaging.
- In `candidate` mode, the runtime under test must already be image-backed. Build, tag, deploy, and verify a specific `-rcN` image.
- Unless the user explicitly asked to replace the existing runtime, a `candidate` deploy should use a separate service identity and separate candidate route so the current dev or stable site keeps serving its existing URL.
- If the user does not specify release-candidate names, derive them deterministically from the current dev or stable runtime:
  - image tag: start at `1.0-rc1` for the first release line, then increment the `rc` number within the active line
  - candidate service: `<base-service>-rc`
  - candidate hostname label: `<base-host>-rc`
- In `release` mode, promote a previously verified candidate to the plain stable tag. Do not treat an unverified `-rcN` image as the release.
- Prefer image-backed iteration when the service has non-trivial runtime dependencies, repeated code changes, or a meaningful need to contain changes and revert them quickly.
- Build images inside the room with `meshagent room container image build ...` when the source context is already in room or mounted storage.
- Use explicit, versioned image tags for every candidate build. Prefer release-candidate tags such as `4.2-rc1`, `4.2-rc2`, `4.2-rc3`, and reserve the plain release tag `4.2` for the image that has passed verification.
- Do not overwrite a single floating tag and call that rollback-ready.
- A meaningful shift in the user's primary iteration goal starts a new release line. The last verified plain release tag from the previous goal remains the rollback target while the new goal proceeds through fresh `-rcN` candidates.
- For a continued release line, increment `rc` numbers instead of inventing a new service or hostname family. Keep the candidate service and candidate hostname stable while the image tag advances from `-rc1` to `-rc2`, `-rc3`, and so on unless the user explicitly wants a different naming scheme.
- Keep the last known good plain release tag available. There is no native service rollback command; rollback means updating the service spec back to the previous known-good release tag.
- If the runtime has cheap unit or smoke tests that can run during image build, bake them into the image build path so a broken candidate image never becomes deployable.
- After building an image, verify it exists with `meshagent room container image list ...` before updating the service to reference it.
- Update the service declaratively so `container.image` points at the new candidate image tag first.
- For candidate testing, update or create the candidate service, not the current dev or stable service, unless the user explicitly asked for in-place replacement.
- After the service update, verify both service/runtime health and the actual user-facing surface. A successful image build and service update are not enough.
- A candidate route should be treated as a test URL, not as the main release URL.
- Only add or move the plain release tag after the corresponding `-rcN` candidate image has passed the required verification.
- Candidate testing is the deploy-in-room verification path. Do not call a candidate a release just because it was built and deployed into the room.
- Do not roll back automatically just because a candidate image failed verification. Leave the rollback as an explicit user-controlled action unless the user asked for automatic rollback behavior.
- If the user asks to roll back, update the service back to the previous known-good plain release tag instead of guessing among unverified candidate tags.
- Use `meshagent room container image save ...` only when you need to archive or export a built image. It is not the normal rollback mechanism.
- When image-backed iteration is the chosen path, avoid mixing it with ad hoc live-file edits to the same service runtime in the same pass.
