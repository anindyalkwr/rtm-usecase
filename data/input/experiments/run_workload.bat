@echo off
setlocal

:: --- Configuration ---
set "CONFIGMAP_FILE=k8s\sensor-producer-configmap.yaml"
set "DEPLOYMENT_FILE=k8s\sensor-producer-deployment.yaml"
set "DEPLOYMENT_NAME=sensor-producer"
set "TOTAL_WORKLOAD_MINUTES=30"
set "RAMP_PHASE_DURATION_MINUTES=10"
set "STEADY_PHASE_DURATION_MINUTES=10"
set "RAMP_STEP_INTERVAL_SECONDS=120" :: 2 minutes

:: --- Main Script ---

echo Starting Kubernetes Workload Script for %DEPLOYMENT_NAME%
echo Total workload duration: %TOTAL_WORKLOAD_MINUTES% minutes.
echo.

:: --- Phase 1: Initial Setup ---
echo --- Phase 1: Initial Setup ---
echo Applying %CONFIGMAP_FILE%...
kubectl apply -f %CONFIGMAP_FILE%
if errorlevel 1 (
    echo ERROR: Failed to apply ConfigMap. Exiting.
    goto :eof
)

echo Applying %DEPLOYMENT_FILE%...
kubectl apply -f %DEPLOYMENT_FILE%
if errorlevel 1 (
    echo ERROR: Failed to apply Deployment. Exiting.
    goto :eof
)

:: Initial scale to 1 producer
echo.
echo Scaling %DEPLOYMENT_NAME% to 1 replicas...
kubectl scale deployment %DEPLOYMENT_NAME% --replicas=1
if errorlevel 1 (
    echo ERROR: Failed to scale deployment. Exiting.
    goto :eof
)
echo Scale command sent.
echo.
echo Waiting for %RAMP_STEP_INTERVAL_SECONDS% seconds...
timeout /t %RAMP_STEP_INTERVAL_SECONDS% /nobreak >nul
:: --- Phase 2: Ramp Up (0-10 minutes) ---
echo.
echo --- Phase 2: Ramp Up (0-%RAMP_PHASE_DURATION_MINUTES% minutes) ---
echo Starting with 1 producer, doubling every 2 minutes.

echo.
echo Scaling %DEPLOYMENT_NAME% to 2 replicas...
kubectl scale deployment %DEPLOYMENT_NAME% --replicas=2
if errorlevel 1 (echo ERROR: Failed to scale deployment. Exiting. & goto :eof)
echo Scale command sent.
echo.
echo Waiting for %RAMP_STEP_INTERVAL_SECONDS% seconds...
timeout /t %RAMP_STEP_INTERVAL_SECONDS% /nobreak >nul
echo.
echo Scaling %DEPLOYMENT_NAME% to 4 replicas...
kubectl scale deployment %DEPLOYMENT_NAME% --replicas=4
if errorlevel 1 (echo ERROR: Failed to scale deployment. Exiting. & goto :eof)
echo Scale command sent.
echo.
echo Waiting for %RAMP_STEP_INTERVAL_SECONDS% seconds...
timeout /t %RAMP_STEP_INTERVAL_SECONDS% /nobreak >nul
echo.
echo Scaling %DEPLOYMENT_NAME% to 8 replicas...
kubectl scale deployment %DEPLOYMENT_NAME% --replicas=8
if errorlevel 1 (echo ERROR: Failed to scale deployment. Exiting. & goto :eof)
echo Scale command sent.
echo.
echo Waiting for %RAMP_STEP_INTERVAL_SECONDS% seconds...
timeout /t %RAMP_STEP_INTERVAL_SECONDS% /nobreak >nul
echo.
echo Scaling %DEPLOYMENT_NAME% to 16 replicas...
kubectl scale deployment %DEPLOYMENT_NAME% --replicas=16
if errorlevel 1 (echo ERROR: Failed to scale deployment. Exiting. & goto :eof)
echo Scale command sent.
echo.
echo Waiting for %RAMP_STEP_INTERVAL_SECONDS% seconds...
timeout /t %RAMP_STEP_INTERVAL_SECONDS% /nobreak >nul
echo.
echo Scaling %DEPLOYMENT_NAME% to 32 replicas...
kubectl scale deployment %DEPLOYMENT_NAME% --replicas=32
if errorlevel 1 (echo ERROR: Failed to scale deployment. Exiting. & goto :eof)
echo Scale command sent.
echo Reached 32 replicas.
echo.
echo Waiting for %RAMP_STEP_INTERVAL_SECONDS% seconds...
timeout /t %RAMP_STEP_INTERVAL_SECONDS% /nobreak >nul
:: --- Phase 3: Steady State (10-20 minutes) ---
echo.
echo --- Phase 3: Steady State (%RAMP_PHASE_DURATION_MINUTES%-%STEADY_PHASE_DURATION_MINUTES% minutes) ---
echo Maintaining 32 producers for %STEADY_PHASE_DURATION_MINUTES% minutes.
echo.
echo Waiting for 600 seconds...
timeout /t 600 /nobreak >nul
:: --- Phase 4: Ramp Down (20-30 minutes) ---
echo.
echo --- Phase 4: Ramp Down (%RAMP_PHASE_DURATION_MINUTES%-%TOTAL_WORKLOAD_MINUTES% minutes) ---
echo Ramping down producers.

echo.
echo Scaling %DEPLOYMENT_NAME% to 16 replicas...
kubectl scale deployment %DEPLOYMENT_NAME% --replicas=16
if errorlevel 1 (echo ERROR: Failed to scale deployment. Exiting. & goto :eof)
echo Scale command sent.
echo.
echo Waiting for %RAMP_STEP_INTERVAL_SECONDS% seconds...
timeout /t %RAMP_STEP_INTERVAL_SECONDS% /nobreak >nul
echo.
echo Scaling %DEPLOYMENT_NAME% to 8 replicas...
kubectl scale deployment %DEPLOYMENT_NAME% --replicas=8
if errorlevel 1 (echo ERROR: Failed to scale deployment. Exiting. & goto :eof)
echo Scale command sent.
echo.
echo Waiting for %RAMP_STEP_INTERVAL_SECONDS% seconds...
timeout /t %RAMP_STEP_INTERVAL_SECONDS% /nobreak >nul
echo.
echo Scaling %DEPLOYMENT_NAME% to 4 replicas...
kubectl scale deployment %DEPLOYMENT_NAME% --replicas=4
if errorlevel 1 (echo ERROR: Failed to scale deployment. Exiting. & goto :eof)
echo Scale command sent.
echo.
echo Waiting for %RAMP_STEP_INTERVAL_SECONDS% seconds...
timeout /t %RAMP_STEP_INTERVAL_SECONDS% /nobreak >nul
echo.
echo Scaling %DEPLOYMENT_NAME% to 2 replicas...
kubectl scale deployment %DEPLOYMENT_NAME% --replicas=2
if errorlevel 1 (echo ERROR: Failed to scale deployment. Exiting. & goto :eof)
echo Scale command sent.
echo.
echo Waiting for %RAMP_STEP_INTERVAL_SECONDS% seconds...
timeout /t %RAMP_STEP_INTERVAL_SECONDS% /nobreak >nul
echo.
echo Scaling %DEPLOYMENT_NAME% to 1 replicas...
kubectl scale deployment %DEPLOYMENT_NAME% --replicas=1
if errorlevel 1 (echo ERROR: Failed to scale deployment. Exiting. & goto :eof)
echo Scale command sent.
echo Ramped down to 1 producer.
echo.
echo Waiting for %RAMP_STEP_INTERVAL_SECONDS% seconds...
timeout /t %RAMP_STEP_INTERVAL_SECONDS% /nobreak >nul
echo.
echo --- Workload Complete ---
echo The %TOTAL_WORKLOAD_MINUTES%-minute workload for %DEPLOYMENT_NAME% has finished.
echo The deployment is currently scaled to 1 replica.
echo.

:: --- Optional Cleanup Prompt ---
echo Do you want to delete the deployment and configmap? (y/n)
set /p DELETE_CHOICE="Enter your choice: "
if /i "%DELETE_CHOICE%"=="y" (
    echo Deleting %DEPLOYMENT_NAME% deployment...
    kubectl delete -f %DEPLOYMENT_FILE%
    echo Deleting %DEPLOYMENT_NAME% configmap...
    kubectl delete -f %CONFIGMAP_FILE%
    echo Cleanup complete.
) else (
    echo Skipping cleanup. You can manually delete them later if needed.
)

echo Script finished.
endlocal
pause
