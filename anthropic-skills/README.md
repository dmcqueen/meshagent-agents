# Anthropic Skills Image

## Summary

A MeshAgent Claude skills agent that loads Anthropic’s published skills; this README also includes instructions to build the tiny `/skills` image mount.

## Description

This agent lets you use all of Anthropic’s published skills inside a MeshAgent agent. On first install it copies the skills into the room at `/data/skills`, so they’re editable. The agent then loads every `skill.md` it finds there, which means you can evolve or customize the skills over time directly in the room and the agent will pick them up.

It runs with the shell tool, script tool, web search, storage tool, and memory enabled, so it can execute commands, write files, and refine skills as your workflow changes.

## Build The Skills Image

1. Clone the Anthropic skills repo.

```bash
git clone https://github.com/anthropics/skills.git
cd skills
```

2. Create a scratch Dockerfile in the repo root.

```Dockerfile
FROM scratch
COPY skills/ /skills/
```

3. Build and push the image.

```bash
docker buildx build . \
  -t "<REGISTRY>/<NAMESPACE>/<IMAGE_NAME>:<TAG>" \
  --platform linux/amd64 \
  --push
```

## What The Build Arguments Mean

- `<REGISTRY>`: Container registry host (for example `docker.io`, `ghcr.io`, `us-west1-docker.pkg.dev`).
- `<NAMESPACE>`: Your registry account or organization name.
- `<IMAGE_NAME>`: The repository name for the image.
- `<TAG>`: A version label (for example `latest`, `2026-03-03`).
- `docker buildx build .`: Builds from the current directory using Buildx.
- `-t`: Tags the image with the full name.
- `--platform linux/amd64`: Builds a Linux AMD64 image.
- `--push`: Pushes the built image to the registry.

### Docker Hub Note

For Docker Hub you can omit the registry and just use:

```bash
docker buildx build . \
  -t "<NAMESPACE>/<IMAGE_NAME>:<TAG>" \
  --platform linux/amd64 \
  --push
```

## Update The Image Mount

Update the image mount in `anthropic-skills/agents.prod.yaml` to point at the image you pushed:

- `container.storage.images.image: <REGISTRY>/<NAMESPACE>/<IMAGE_NAME>:<TAG>`

If you prefer, you can keep using the prebuilt image already referenced there:

- `docker.io/tulamasterman/anthropic-skills:latest`
