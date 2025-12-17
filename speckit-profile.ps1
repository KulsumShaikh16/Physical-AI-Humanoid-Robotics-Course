# Speckit Plus Profile for PowerShell
#
# This script loads Speckit Plus aliases and functions for the current project.
# You can either:
# 1. Dot-source this file manually: . .\speckit-profile.ps1
# 2. Add it to your PowerShell profile to load automatically

# Get the current directory and check if we're in a Speckit Plus project
$specifyDir = ".specify"
if (Test-Path $specifyDir) {
    Write-Output "Speckit Plus project detected. Loading aliases..."
    
    # Import the Speckit Plus functions
    . .\setup-speckit-aliases.ps1
    
    Write-Output "Speckit Plus commands are now available:"
    Write-Output "  sp.specify - Create a new feature specification"
    Write-Output "  sp.clarify - Clarify the current feature"
    Write-Output "  sp.plan - Generate an implementation plan"
    Write-Output "  sp.tasks - Generate implementation tasks"
    Write-Output "  sp.adr - Create an Architecture Decision Record"
    Write-Output "  sp.phr - Create a Prompt History Record"
    
    Write-Output ""
    Write-Output "You can now use commands like: sp.clarify, sp.plan, sp.tasks, etc."
} else {
    Write-Output "Error: Not in a Speckit Plus project directory (no .specify folder found)"
}