#!/bin/bash

set -u
: "CONTAINER_NAME"
: "EXPOSED_PORT"
: "CONTAINER_PORT"
: "CONTAINER_REGISTRY"
: "VERSION"

ssh -o StrictHostKeyChecking=no user@server_ip << EOF
docker stop "$CONTAINER_NAME" || true
docker rm "$CONTAINER_NAME" || true
docker pull "$CONTAINER_REGISTRY"/wms-backend:"$VERSION"
if [ $? -ne 0 ]; then
    echo "Failed to pull docker image to the server"
    exit 1
fi
docker run -d --name "$CONTAINER_NAME" -p "$EXPOSED_PORT":"$CONTAINER_PORT" "$CONTAINER_REGISTRY"/wms-backend:"$VERSION"
if [ $? -ne 0]; then
    echo "Failed to run docker container"
    exit 1
fi
EOF