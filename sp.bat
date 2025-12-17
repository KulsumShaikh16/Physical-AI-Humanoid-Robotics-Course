@echo off
REM Speckit Plus Windows Batch File
REM This file provides a simple way to run Speckit Plus commands on Windows

if "%1"=="" (
    echo Usage: sp ^<command^> [options]
    echo.
    echo Available commands:
    echo   sp clarify       - Run clarification process
    echo   sp plan          - Run planning process
    echo   sp tasks         - Generate tasks
    echo   sp specify       - Create a new feature specification
    echo   sp adr ^<title^>  - Create an Architecture Decision Record
    echo   sp phr           - Create a Prompt History Record
    goto :eof
)

if "%1"=="clarify" (
    powershell -Command ". .\speckit-profile.ps1; sp.clarify"
    goto :eof
)

if "%1"=="plan" (
    powershell -Command ". .\speckit-profile.ps1; sp.plan"
    goto :eof
)

if "%1"=="tasks" (
    powershell -Command ". .\speckit-profile.ps1; sp.tasks"
    goto :eof
)

if "%1"=="specify" (
    powershell -Command ". .\speckit-profile.ps1; sp.specify"
    goto :eof
)

if "%1"=="adr" (
    powershell -Command ". .\speckit-profile.ps1; sp.adr '%2'"
    goto :eof
)

if "%1"=="phr" (
    powershell -Command ". .\speckit-profile.ps1; sp.phr"
    goto :eof
)

echo Unknown command: %1
echo Use 'sp' without arguments to see help.