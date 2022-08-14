dapr run \
    --app-id hasura \
    --app-port 8080 \
    --dapr-http-port 3601 \
    --app-protocol http \
    --components-path ./components
