#!/bin/bash

set -u
: "$CONTAINER_NAME"
: "$EXPOSED_PORT"
: "$CONTAINER_PORT"
: "$CONTAINER_REGISTRY"
: "$REGISTRY_NAMESPACE"
: "$VERSION"
: "$SERVER_USER"
: "$SERVER_IP"

ssh -o StrictHostKeyChecking=no "$SERVER_USER"@"$SERVER_IP" << EOF
sudo docker stop "$CONTAINER_NAME" || true
sudo docker rm "$CONTAINER_NAME" || true
sudo docker pull "$CONTAINER_REGISTRY"/"$REGISTRY_NAMESPACE"/wms-backend:"$VERSION"
if [ $? -ne 0 ]; then
    echo "Failed to pull docker image to the server"
    exit 1
fi
sudo docker run -d --name "$CONTAINER_NAME" -p "$EXPOSED_PORT":"$CONTAINER_PORT" "$CONTAINER_REGISTRY"/"$REGISTRY_NAMESPACE"/wms-backend:"$VERSION"
if [ $? -ne 0]; then
    echo "Failed to run docker container"
    exit 1
fi
EOF