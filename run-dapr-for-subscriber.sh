dapr run \
    --app-id process-job \
    --app-port 6002 \
    --dapr-http-port 3602 \
    --app-protocol grpc \
    --components-path ./components \
    -- python process_job.py
