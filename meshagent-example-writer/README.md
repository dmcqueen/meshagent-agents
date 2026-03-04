# MeshAgent Example Writer

## Summary

An OpenAI Codex based agent for developer tasks inside MeshAgent rooms. The agent has access to the MeshAgent SDKs and special instructions for how to create tutorials based on the MeshAgent CLI and SDKs.

## Description

This agent runs OpenAI Codex in a shell-enabled MeshAgent container so it can execute commands and inspect or edit files in `/data`. It has the web fetch tool enabled for pulling in reference material, includes the MeshAgent SDK at `/src/meshagent-sdk`, and follows build rules like copying sources into `/build` and returning outputs to `/data`.

## Install Links

- Prod: https://app.powerboards.com/install?url=https://raw.githubusercontent.com/dmcqueen/meshagent-agents/e8ebef1caab6d9e0cf61e934992b21f41a6e04d9/meshagent-example-writer/agents.prod.yaml

## Raw SHA Links

- Prod: https://raw.githubusercontent.com/dmcqueen/meshagent-agents/e8ebef1caab6d9e0cf61e934992b21f41a6e04d9/meshagent-example-writer/agents.prod.yaml
