#!/bin/bash
echo "Current directory: $(pwd)"

set -u
: "$CONTAINER_REGISTRY"
: "$VERSION"
: "$REGISTRY_NAMESPACE"
: "$CONTAINER_PORT"

docker build -t "$CONTAINER_REGISTRY"/"$REGISTRY_NAMESPACE"/wms-backend:"$VERSION" --build-arg CONTAINER_PORT="$CONTAINER_PORT" --file ./deployment/Dockerfile .