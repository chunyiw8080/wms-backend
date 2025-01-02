#!/bin/bash
echo "Current directory: $(pwd)"

set -u
: "$CONTAINER_REGISTRY"
: "$VERSION"

docker build -t "$CONTAINER_REGISTRY"/wms-backend:"$VERSION" --file ./deployment/Dockerfile .