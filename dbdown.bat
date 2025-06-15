@echo off

echo "[STEP]: Stopping Docker containers..."
docker-compose down -v
if EXIST "Repository\data_log" (
    echo "[STATUS]: Removing data_log directory..."
    rmdir /s /q "Repository\data_log"
)

echo "[STATUS]: Successfully removed containers and data."