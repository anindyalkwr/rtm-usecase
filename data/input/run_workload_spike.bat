@echo off
setlocal

:: --- Configuration ---
set "CONFIGMAP_FILE=k8s\sensor-producer-configmap.yaml"
set "DEPLOYMENT_FILE=k8s\sensor-producer-deployment.yaml"
set "DEPLOYMENT_NAME=sensor-producer"
set "SPIKE_DURATION_MINUTES=600"
set "STEADY_PRODUCERS=64"

:: --- Main Script ---

echo Starting Kubernetes Spike Test Script for %DEPLOYMENT_NAME%
echo Spike duration: %SPIKE_DURATION_MINUTES% minutes.
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

:: Scale to initial number of producers
echo.
echo Scaling %DEPLOYMENT_NAME% to %STEADY_PRODUCERS% replicas...
kubectl scale deployment %DEPLOYMENT_NAME% --replicas=%STEADY_PRODUCERS%
if errorlevel 1 (
    echo ERROR: Failed to scale deployment. Exiting.
    goto :eof
)
echo Scale command sent.
echo.
echo Maintaining %STEADY_PRODUCERS% producers for %SPIKE_DURATION_MINUTES% seconds...
timeout /t %SPIKE_DURATION_MINUTES% /nobreak >nul

:: --- Phase 2: Ramp Down to Zero ---
echo.
echo --- Phase 2: Scaling Down to Zero ---
echo Scaling %DEPLOYMENT_NAME% to 0 replicas...
kubectl scale deployment %DEPLOYMENT_NAME% --replicas=0
if errorlevel 1 (
    echo ERROR: Failed to scale deployment to zero.
) else (
    echo Scale command sent. Deployment scaled to zero.
)

echo.
echo --- Spike Test Complete ---
echo The %SPIKE_DURATION_MINUTES%-minute spike test for %DEPLOYMENT_NAME% has finished.
echo The deployment is currently scaled to 0 replicas.
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