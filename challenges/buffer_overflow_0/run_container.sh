#!/usr/bin/env bash
# Build and run the fixed challenge image with stdin as its only input channel.
set -euo pipefail

# Resolve this script's folder so it works from any current directory.
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
image="cyb3-buffer-overflow-0:local"

# Build from the challenge files, then run with network and extra privileges removed.
docker build --tag "$image" "$script_dir"
docker run --rm -i \
  --network none \
  --read-only \
  --cap-drop ALL \
  --security-opt no-new-privileges \
  --pids-limit 32 \
  --memory 128m \
  --cpus 1 \
  --user 65534:65534 \
  --tmpfs /tmp:rw,noexec,nosuid,size=8m \
  "$image"
