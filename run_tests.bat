@echo off
setlocal

set "ROOT=%~dp0"
set "PYTHON=%ROOT%..\.venv\Scripts\python.exe"
if not exist "%PYTHON%" set "PYTHON=python"

set FAILURES=0

echo [1/4] Web tests
"%PYTHON%" -m pytest tests\web
if errorlevel 1 set /a FAILURES+=1

echo [2/4] API tests
"%PYTHON%" -m pytest tests\api
if errorlevel 1 set /a FAILURES+=1

echo [3/4] Contract tests
echo Running serially because mobile contract flows share the same emulator state.
"%PYTHON%" -m pytest tests\contract
if errorlevel 1 set /a FAILURES+=1

echo [4/4] Mobile tests
echo Running after contract tests to avoid emulator state collisions.
"%PYTHON%" -m pytest tests\mobile
if errorlevel 1 set /a FAILURES+=1

if %FAILURES% neq 0 (
  echo.
  echo Test run finished with %FAILURES% failing suite^(s^).
  exit /b 1
)

echo.
echo All suites passed.
exit /b 0
