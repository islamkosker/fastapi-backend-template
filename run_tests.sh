#!/bin/bash
set -e

# Run the test stack with Docker Compose and .env.test
docker compose -f docker-compose.test.yml --env-file .env.test up --build --abort-on-container-exit

# Get the exit code of the backend_test container
test_exit_code=$(docker inspect backend_test --format='{{.State.ExitCode}}')

# Copy the test report from the container to the host (if it exists)
docker cp backend_test:/backend/report.xml ./report.xml || echo "No report.xml found."

# Clean up containers and volumes
docker compose -f docker-compose.test.yml --env-file .env.test down -v

# Exit with the test container's exit code (for CI/CD)
exit $test_exit_code 