#!/bin/bash
echo "Current directory: $(pwd)"

set -u
: "$CONTAINER_REGISTRY"
: "$VERSION"
: "$REGISTRY_NAMESPACE"

docker build -t "$CONTAINER_REGISTRY"/"$REGISTRY_NAMESPACE"/wms-backend:"$VERSION" --file ./deployment/Dockerfile .