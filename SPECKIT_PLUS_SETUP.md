# Instructions for permanent Speckit Plus command access

## Option 1: Add to PowerShell Profile (Recommended for regular use)

1. Find your PowerShell profile path:
   ```powershell
   $PROFILE
   ```

2. Open your PowerShell profile in an editor:
   ```powershell
   notepad $PROFILE
   ```

3. Add the following content to your profile:
   ```powershell
   # Speckit Plus commands
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
       $paths = & ".specify/scripts/powershell/check-prerequisites.ps1" -PathsOnly
       Write-Output "Clarification process would run on current feature"
   }

   function Invoke-Plan { 
       Write-Output "Running planning process..."
       $paths = & ".specify/scripts/powershell/check-prerequisites.ps1" -PathsOnly
       Write-Output "Planning process would run on current feature"
   }

   function Invoke-Tasks { 
       Write-Output "Generating tasks..."
       $paths = & ".specify/scripts/powershell/check-prerequisites.ps1" -PathsOnly
       Write-Output "Task generation would run on current feature"
   }

   function Invoke-ADR { 
       param([string]$Title = "")
       Write-Output "Creating Architecture Decision Record..."
       if ($Title) {
           $filename = $Title -replace ' ', '-' -replace '[^a-zA-Z0-9-]', ''
           $adrPath = "history/adr/$(Get-NextADRNumber)-$filename.md"
           Copy-Item ".specify/templates/adr-template.md" -Destination $adrPath
           Write-Output "Created ADR at $adrPath"
       }
   }

   function Invoke-PHR { 
       param([string]$Title = "", [string]$Stage = "general")
       Write-Output "Creating Prompt History Record..."
       $paths = & ".specify/scripts/powershell/check-prerequisites.ps1" -PathsOnly
       Write-Output "PHR process would run with title: $Title, stage: $Stage"
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
   ```

4. Save the file and restart PowerShell. Now you can use commands like `sp.clarify` from anywhere in your project.

## Option 2: Use the batch file (sp.bat) from this directory

Run commands like:
- `sp clarify`
- `sp plan`
- `sp tasks`
- `sp specify "feature description"`
- `sp adr "decision title"`
- `sp phr`

## Option 3: Dot-source the profile when needed

Run this command when you want to use Speckit Plus commands:
```powershell
. .\speckit-profile.ps1
```

Then you can use commands like `sp.clarify`, `sp.plan`, etc.