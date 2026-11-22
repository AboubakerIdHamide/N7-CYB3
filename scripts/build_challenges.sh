#!/bin/sh
# Build only the three fixed local images used by the CYB-3 runner.
set -eu

docker build --pull=false -t cyb3-buffer-overflow-0:local challenges/buffer_overflow_0
docker build --pull=false -t cyb3-integer-wrap:local challenges/integer_wrap
docker build --pull=false -t cyb3-path-traversal:local challenges/path_traversal
