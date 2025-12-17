# Speckit Plus Aliases Setup for PowerShell
#
# This script defines PowerShell aliases for Speckit Plus commands
# that can be run from anywhere in the project.

# Define all Speckit Plus commands as PowerShell functions
function Invoke-Specify {
    param([string]$Description = "")
    $specDir = "specs/$(Get-NextFeatureNumber)-$(if ($Description) { $Description } else { 'new-feature' })"
    $specDir = $specDir -replace ' ', '-' -replace '[^a-zA-Z0-9-]', ''
    New-Item -ItemType Directory -Path $specDir -Force
    Copy-Item ".specify/templates/spec-template.md" -Destination "$specDir/spec.md"
    Copy-Item ".specify/templates/checklist-template.md" -Destination "$specDir/checklist.md"
    Write-Output "Created specification structure in $specDir"
}

function Invoke-Clarify {
    Write-Output "Running clarification process..."

    # Get paths and check prerequisites
    $pathsJson = & ".specify/scripts/powershell/check-prerequisites.ps1" -Json -PathsOnly | Out-String | ConvertFrom-Json

    # Check if feature directory exists
    if (-not (Test-Path $pathsJson.FEATURE_DIR -PathType Container)) {
        Write-Output "ERROR: Feature directory not found: $($pathsJson.FEATURE_DIR)"
        Write-Output "Run /sp.specify first to create the feature structure."
        return
    }

    # Check if spec.md exists
    if (-not (Test-Path $pathsJson.FEATURE_SPEC -PathType Leaf)) {
        Write-Output "ERROR: spec.md not found in $($pathsJson.FEATURE_DIR)"
        Write-Output "Run /sp.specify first to create the feature specification."
        return
    }

    # Read the feature specification
    $specContent = Get-Content $pathsJson.FEATURE_SPEC -Raw

    Write-Output "Feature specification found:"
    Write-Output "  Path: $($pathsJson.FEATURE_SPEC)"
    Write-Output "  Size: $(Get-Item $pathsJson.FEATURE_SPEC | Select-Object -ExpandProperty Length) bytes"

    # Show basic details about the spec
    $lines = $specContent -split "`n"
    $titleLine = $lines | Where-Object { $_ -match "^#.*" } | Select-Object -First 1
    if ($titleLine) {
        Write-Output "  Title: $($titleLine.TrimStart('# '))"
    }

    # Count important sections
    $sections = ($lines | Where-Object { $_ -match "^##.*" }).Count
    Write-Output "  Sections: $sections"

    # Check for common required elements
    $hasAcceptance = $specContent -match "(?i)acceptance criteria"
    $hasDescription = $specContent -match "(?i)description"
    $hasRequirements = $specContent -match "(?i)requirements"

    $acceptanceResult = if ($hasAcceptance) { 'Yes' } else { 'No' }
    Write-Output "  Has acceptance criteria: $acceptanceResult"
    $descriptionResult = if ($hasDescription) { 'Yes' } else { 'No' }
    Write-Output "  Has description: $descriptionResult"
    $requirementsResult = if ($hasRequirements) { 'Yes' } else { 'No' }
    Write-Output "  Has requirements: $requirementsResult"

    # Check if research.md exists and show its status
    $hasResearch = Test-Path $pathsJson.RESEARCH -PathType Leaf
    $researchResult = if ($hasResearch) { 'Yes' } else { 'No' }
    Write-Output "  Has research: $researchResult"

    # Check if plan.md exists and show its status
    $hasPlan = Test-Path $pathsJson.IMPL_PLAN -PathType Leaf
    $planResult = if ($hasPlan) { 'Yes' } else { 'No' }
    Write-Output "  Has implementation plan: $planResult"

    Write-Output ""
    Write-Output "Clarification process completed for feature: $($pathsJson.FEATURE_DIR)"
}

function Invoke-Plan {
    Write-Output "Running planning process..."

    # Get paths and check prerequisites
    $pathsJson = & ".specify/scripts/powershell/check-prerequisites.ps1" -Json -PathsOnly | Out-String | ConvertFrom-Json

    # Check if feature directory exists
    if (-not (Test-Path $pathsJson.FEATURE_DIR -PathType Container)) {
        Write-Output "ERROR: Feature directory not found: $($pathsJson.FEATURE_DIR)"
        Write-Output "Run /sp.specify first to create the feature structure."
        return
    }

    # Check if spec.md exists
    if (-not (Test-Path $pathsJson.FEATURE_SPEC -PathType Leaf)) {
        Write-Output "ERROR: spec.md not found in $($pathsJson.FEATURE_DIR)"
        Write-Output "Run /sp.specify first to create the feature specification."
        return
    }

    # Read the feature specification
    $specContent = Get-Content $pathsJson.FEATURE_SPEC -Raw

    # Generate plan based on the specification
    Write-Output "Generating implementation plan for: $($pathsJson.FEATURE_DIR)"

    # Check if plan.md already exists
    if (Test-Path $pathsJson.IMPL_PLAN -PathType Leaf) {
        Write-Output "Plan already exists at: $($pathsJson.IMPL_PLAN)"
        $overwrite = Read-Host "Do you want to overwrite it? (y/N)"
        if ($overwrite -ne 'y') {
            Write-Output "Plan generation cancelled."
            return
        }
    }

    # Copy the plan template
    $templatePath = Join-Path (Get-Location) ".specify/templates/plan-template.md"
    if (Test-Path $templatePath) {
        Copy-Item $templatePath $pathsJson.IMPL_PLAN
        Write-Output "Created implementation plan at: $($pathsJson.IMPL_PLAN)"
    } else {
        # Create a basic plan file if template doesn't exist
        $planContent = "# Implementation Plan

Feature: $($pathsJson.FEATURE_DIR)

## Overview
Brief overview of the implementation approach for this feature.

## Architecture
- System components
- Data flow
- External dependencies

## Implementation Steps
1. Step 1
2. Step 2
3. Step 3

## Testing Strategy
How the feature will be tested.

## Risks & Mitigations
Potential risks and how to address them.

## Success Criteria
How to verify the feature is working as expected.

"
        Set-Content -Path $pathsJson.IMPL_PLAN -Value $planContent
        Write-Output "Created basic implementation plan at: $($pathsJson.IMPL_PLAN)"
    }
}

function Invoke-Tasks {
    Write-Output "Generating tasks..."

    # Get paths and check prerequisites
    $pathsJson = & ".specify/scripts/powershell/check-prerequisites.ps1" -Json -PathsOnly | Out-String | ConvertFrom-Json

    # Check if feature directory exists
    if (-not (Test-Path $pathsJson.FEATURE_DIR -PathType Container)) {
        Write-Output "ERROR: Feature directory not found: $($pathsJson.FEATURE_DIR)"
        Write-Output "Run /sp.specify first to create the feature structure."
        return
    }

    # Check if spec.md exists
    if (-not (Test-Path $pathsJson.FEATURE_SPEC -PathType Leaf)) {
        Write-Output "ERROR: spec.md not found in $($pathsJson.FEATURE_DIR)"
        Write-Output "Run /sp.specify first to create the feature specification."
        return
    }

    # Check if plan.md exists
    if (-not (Test-Path $pathsJson.IMPL_PLAN -PathType Leaf)) {
        Write-Output "ERROR: plan.md not found in $($pathsJson.FEATURE_DIR)"
        Write-Output "Run /sp.plan first to create the implementation plan."
        return
    }

    # Read the feature specification and plan
    $specContent = Get-Content $pathsJson.FEATURE_SPEC -Raw
    $planContent = Get-Content $pathsJson.IMPL_PLAN -Raw

    Write-Output "Generating task list for: $($pathsJson.FEATURE_DIR)"

    # Check if tasks.md already exists
    if (Test-Path $pathsJson.TASKS -PathType Leaf) {
        Write-Output "Tasks already exist at: $($pathsJson.TASKS)"
        $overwrite = Read-Host "Do you want to overwrite it? (y/N)"
        if ($overwrite -ne 'y') {
            Write-Output "Task generation cancelled."
            return
        }
    }

    # Copy the tasks template
    $templatePath = Join-Path (Get-Location) ".specify/templates/tasks-template.md"
    if (Test-Path $templatePath) {
        Copy-Item $templatePath $pathsJson.TASKS
        Write-Output "Created task list at: $($pathsJson.TASKS)"
    } else {
        # Create a basic tasks file if template doesn't exist
        $tasksContent = "# Implementation Tasks

Feature: $($pathsJson.FEATURE_DIR)

## Overview
Task breakdown for implementing the feature based on the specification and plan.

## Tasks

### 1. Setup and Environment
- [ ] Task 1: Setup development environment
- [ ] Task 2: Install dependencies
- [ ] Task 3: Configure project structure

### 2. Core Implementation
- [ ] Task 4: Implement core functionality
- [ ] Task 5: Add required features
- [ ] Task 6: Integrate with existing systems

### 3. Testing
- [ ] Task 7: Write unit tests
- [ ] Task 8: Write integration tests
- [ ] Task 9: Perform manual testing

### 4. Documentation
- [ ] Task 10: Update documentation
- [ ] Task 11: Write usage examples
- [ ] Task 12: Create user guides

### 5. Deployment
- [ ] Task 13: Prepare for deployment
- [ ] Task 14: Deploy to staging
- [ ] Task 15: Deploy to production

"
        Set-Content -Path $pathsJson.TASKS -Value $tasksContent
        Write-Output "Created basic task list at: $($pathsJson.TASKS)"
    }
}

function Invoke-ADR {
    param([string]$Title = "")
    Write-Output "Creating Architecture Decision Record..."

    if (-not $Title) {
        Write-Output "ERROR: ADR title is required."
        Write-Output "Usage: sp.adr 'Title of the decision'"
        return
    }

    # Create history/adr directory if it doesn't exist
    $adrDir = Join-Path (Get-Location) "history/adr"
    New-Item -ItemType Directory -Path $adrDir -Force | Out-Null

    # Generate filename with incremented number
    $nextNumber = Get-NextADRNumber
    $filename = "$nextNumber-$($Title -replace ' ', '-' -replace '[^a-zA-Z0-9-]', '').md"
    $adrPath = Join-Path $adrDir $filename

    # Check if ADR already exists
    if (Test-Path $adrPath -PathType Leaf) {
        Write-Output "ERROR: ADR already exists at: $adrPath"
        return
    }

    # Copy the ADR template if it exists
    $templatePath = Join-Path (Get-Location) ".specify/templates/adr-template.md"
    if (Test-Path $templatePath) {
        Copy-Item $templatePath $adrPath
        Write-Output "Created ADR at: $adrPath"
    } else {
        # Create a basic ADR template if one doesn't exist
        $adrContent = "# $nextNumber. $Title

Date: $(Get-Date -Format 'yyyy-MM-dd')

## Status

Proposed | Accepted | Rejected | Deprecated | Superseded by [ADR-000](000-example.md)

## Context

What is the issue that we're seeing that is motivating this decision or change?

## Decision

What is the change that we're proposing and documenting?

## Consequences

What becomes easier or more difficult to do because of this change?

"
        Set-Content -Path $adrPath -Value $adrContent
        Write-Output "Created ADR at: $adrPath"
    }
}

function Invoke-PHR {
    param([string]$Title = "", [string]$Stage = "general")
    Write-Output "Creating Prompt History Record..."

    # Get current date in ISO format
    $dateIso = Get-Date -Format "yyyy-MM-dd"

    # Get the current branch to determine the feature
    $currentBranch = git rev-parse --abbrev-ref HEAD 2>$null
    if ($LASTEXITCODE -ne 0) {
        # If not in git repo, use the latest feature
        $specsPath = Join-Path (Get-Location) "specs"
        $latestFeature = ""
        $highest = 0
        if (Test-Path $specsPath) {
            Get-ChildItem -Path $specsPath -Directory | ForEach-Object {
                if ($_.Name -match '^(\d{3})-') {
                    $num = [int]$matches[1]
                    if ($num -gt $highest) {
                        $highest = $num
                        $latestFeature = $_.Name
                    }
                }
            }
        }
        $currentBranch = if ($latestFeature) { $latestFeature } else { "general" }
    }

    # Determine output directory based on stage and feature
    $outputDir = if ($Stage -eq "constitution") {
        "history/prompts/constitution"
    } elseif ($Stage -ne "general") {
        "history/prompts/$currentBranch"
    } else {
        "history/prompts/general"
    }

    # Create the directory if it doesn't exist
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null

    # Generate a unique ID by looking at existing files
    $existingFiles = Get-ChildItem -Path $outputDir -File -Filter "*.prompt.md" | Select-Object -ExpandProperty Name
    $maxId = 0
    foreach ($file in $existingFiles) {
        if ($file -match '^(\d+)-') {
            $id = [int]$matches[1]
            if ($id -gt $maxId) {
                $maxId = $id
            }
        }
    }
    $newId = $maxId + 1

    # Generate filename
    $slug = if ($Title) { $Title -replace ' ', '-' -replace '[^a-zA-Z0-9-]', '' } else { "general-$newId" }
    $filename = "$newId-$slug.$Stage.prompt.md"
    $outputPath = Join-Path $outputDir $filename

    # Generate PHR content
    $phrContent = "---
ID: $newId
TITLE: $Title
STAGE: $Stage
DATE_ISO: $dateIso
SURFACE: agent
MODEL: (best known)
FEATURE: $currentBranch
BRANCH: $currentBranch
USER: $env:USERNAME
COMMAND: (current command)
LABELS: []
LINKS:
  SPEC: null
  TICKET: null
  ADR: null
  PR: null
FILES_YAML: []
TESTS_YAML: []
PROMPT_TEXT: (user input would go here)
RESPONSE_TEXT: (assistant response would go here)
OUTCOME: (outcome of the interaction)
EVALUATION: (evaluation of the outcome)
---

# Prompt History Record: $newId - $Title

## Summary
Brief summary of the interaction and outcome.

## Details
Detailed description of the interaction.

## Next Steps
What should happen next based on this interaction.

"
    Set-Content -Path $outputPath -Value $phrContent
    Write-Output "Created Prompt History Record: $outputPath"
}

function Get-NextFeatureNumber {
    $specsPath = Join-Path (Get-Location) "specs"
    if (Test-Path $specsPath) {
        $dirs = Get-ChildItem -Path $specsPath -Directory
        $maxNum = 0
        foreach ($dir in $dirs) {
            if ($dir.Name -match '^(\d{3})-') {
                $num = [int]$matches[1]
                if ($num -gt $maxNum) {
                    $maxNum = $num
                }
            }
        }
        return "{0:D3}" -f ($maxNum + 1)
    }
    return "001"
}

function Get-NextADRNumber {
    $adrPath = Join-Path (Get-Location) "history/adr"
    if (Test-Path $adrPath) {
        $files = Get-ChildItem -Path $adrPath -File -Filter "*.md"
        $maxNum = 0
        foreach ($file in $files) {
            if ($file.Name -match '^(\d+)-') {
                $num = [int]$matches[1]
                if ($num -gt $maxNum) {
                    $maxNum = $num
                }
            }
        }
        return ($maxNum + 1)
    }
    return 1
}

# Create aliases for all Speckit Plus commands
Set-Alias -Name sp.specify -Value Invoke-Specify
Set-Alias -Name sp.clarify -Value Invoke-Clarify
Set-Alias -Name sp.plan -Value Invoke-Plan
Set-Alias -Name sp.tasks -Value Invoke-Tasks
Set-Alias -Name sp.adr -Value Invoke-ADR
Set-Alias -Name sp.phr -Value Invoke-PHR