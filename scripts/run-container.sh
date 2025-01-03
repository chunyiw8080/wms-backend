#!/bin/bash

set -u
: "$CONTAINER_NAME"
: "$EXPOSED_PORT"
: "$CONTAINER_REGISTRY"
: "$REGISTRY_NAMESPACE"
: "$VERSION"
: "$SERVER_USER"
: "$SERVER_IP"
: "$SERVER_PORT"
: "$REGISTRY_PW"
: "$REGISTRY_UN"
: "$DB_HOST"
: "$DB_USER"
: "$DB_PASSWORD"
: "$DB_NAME"
: "$DB_PORT"
: "$TOKEN_SECRET_KEY"

ssh -p "$SERVER_PORT" -T -o StrictHostKeyChecking=no "$SERVER_USER"@"$SERVER_IP" << EOF
sudo docker stop "$CONTAINER_NAME" || true
sudo docker rm "$CONTAINER_NAME" || true
sudo echo "$REGISTRY_PW" | docker login "$CONTAINER_REGISTRY" --username "$REGISTRY_UN" --password-stdin
sudo docker pull "$CONTAINER_REGISTRY"/"$REGISTRY_NAMESPACE"/wms-backend:"$VERSION"
if [ $? -ne 0 ]; then
    echo "Failed to pull docker image to the server"
    exit 1
fi
sudo docker run \
  -d \
  --name "$CONTAINER_NAME" \
  -p "$EXPOSED_PORT":8000 \
  --network bridge \
  -e DB_HOST="$DB_HOST" \
  -e DB_USER="$DB_USER" \
  -e DB_PASSWORD="$DB_PASSWORD" \
  -e DB_NAME="$DB_NAME" \
  -e DB_PORT="$DB_PORT" \
  -e TOKEN_SECRET_KEY="$TOKEN_SECRET_KEY" \
  "$CONTAINER_REGISTRY"/"$REGISTRY_NAMESPACE"/wms-backend:"$VERSION"
if [ $? -ne 0 ]; then
    echo "Failed to run docker container"
    exit 1
fi
EOF
# sudo docker run -d --name "$CONTAINER_NAME" -p "$EXPOSED_PORT":8000  --network bridge "$CONTAINER_REGISTRY"/"$REGISTRY_NAMESPACE"/wms-backend:"$VERSION"