@echo off
REM Run the test stack with Docker Compose and .env.test
call docker compose -f docker-compose.test.yml --env-file .env.test up --build --abort-on-container-exit

REM Get the exit code of the backend_test container
for /f %%i in ('docker inspect backend_test --format="{{.State.ExitCode}}"') do set test_exit_code=%%i

REM Copy the test report from the container to the host (if it exists)
docker cp backend_test:/backend/report.xml .\report.xml 2>nul
if errorlevel 1 echo No report.xml found.

REM Clean up containers and volumes
call docker compose -f docker-compose.test.yml --env-file .env.test down -v

REM Exit with the test container's exit code (for CI/CD)
exit /b %test_exit_code% 