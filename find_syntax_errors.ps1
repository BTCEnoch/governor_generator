# ======================================================================
# SYNTAX ERROR FINDER - Governor Generator Project Phase 3
# ======================================================================
# Purpose: Find and report Python syntax errors across the project
# Method: Use Python AST parser to validate each file

Write-Host "SYNTAX ERROR FINDER - Starting Phase 3" -ForegroundColor Yellow
Write-Host "============================================================"

# Initialize counters
$totalFiles = 0
$syntaxErrors = 0
$errorFiles = @()

Write-Host "Scanning for Python files..." -ForegroundColor Blue

# Get all Python files, excluding backup directories
$pythonFiles = Get-ChildItem -Path "." -Recurse -Filter "*.py" | 
    Where-Object { $_.FullName -notmatch "backup|__pycache__|\.git" } |
    Sort-Object FullName

$totalFiles = $pythonFiles.Count
Write-Host "Found $totalFiles Python files to check for syntax errors" -ForegroundColor Blue

if ($totalFiles -eq 0) {
    Write-Host "No Python files found!" -ForegroundColor Red
    exit 1
}

# Create a temporary Python script to check syntax
$syntaxChecker = @"
import ast
import sys
import os

def check_syntax(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to parse the AST
        ast.parse(content, filename=file_path)
        return True, None
    except SyntaxError as e:
        return False, f"Line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, f"Error: {str(e)}"

if __name__ == "__main__":
    file_path = sys.argv[1]
    success, error = check_syntax(file_path)
    if not success:
        print(f"SYNTAX_ERROR:{file_path}:{error}")
        sys.exit(1)
    else:
        print(f"OK:{file_path}")
        sys.exit(0)
"@

# Write the syntax checker to a temporary file
$checkerPath = "temp_syntax_checker.py"
Set-Content -Path $checkerPath -Value $syntaxChecker -Encoding UTF8

Write-Host "Checking syntax of each file..." -ForegroundColor Blue
Write-Host ""

# Process each file
foreach ($file in $pythonFiles) {
    $relativePath = $file.FullName.Replace($PWD.Path, "").TrimStart("\")
    
    try {
        # Run the syntax checker
        $result = python $checkerPath $file.FullName 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ $relativePath" -ForegroundColor Green
        } else {
            Write-Host "  ❌ $relativePath" -ForegroundColor Red
            
            # Parse the error details
            if ($result -match "SYNTAX_ERROR:(.+):(.+)") {
                $errorDetail = $matches[2]
                Write-Host "     Error: $errorDetail" -ForegroundColor Red
                $errorFiles += @{
                    File = $relativePath
                    Error = $errorDetail
                }
                $syntaxErrors++
            } else {
                Write-Host "     Unknown error: $result" -ForegroundColor Red
                $errorFiles += @{
                    File = $relativePath
                    Error = "Unknown error: $result"
                }
                $syntaxErrors++
            }
        }
        
    } catch {
        Write-Host "  ⚠️ $relativePath - Could not check: $($_.Exception.Message)" -ForegroundColor Yellow
    }
    
    # Progress indicator
    $processedFiles = $pythonFiles.IndexOf($file) + 1
    if ($totalFiles -gt 0) {
        $progress = [math]::Round(($processedFiles / $totalFiles) * 100, 1)
        Write-Progress -Activity "Checking syntax" -Status "$processedFiles/$totalFiles files checked" -PercentComplete $progress
    }
}

# Clean up temporary file
Remove-Item -Path $checkerPath -Force

Write-Host ""
Write-Host "PHASE 3 COMPLETE - Syntax Check Summary:" -ForegroundColor Green
Write-Host "=================================================="
Write-Host "Total files checked: $totalFiles" -ForegroundColor White
Write-Host "Files with syntax errors: $syntaxErrors" -ForegroundColor Red
Write-Host ""

if ($syntaxErrors -gt 0) {
    Write-Host "FILES WITH SYNTAX ERRORS:" -ForegroundColor Red
    Write-Host "========================="
    
    foreach ($errorFile in $errorFiles) {
        Write-Host "  📄 $($errorFile.File)" -ForegroundColor Red
        Write-Host "     └─ $($errorFile.Error)" -ForegroundColor Yellow
        Write-Host ""
    }
    
    Write-Host "NEXT STEPS:" -ForegroundColor Cyan
    Write-Host "1. Fix the syntax errors listed above" -ForegroundColor White
    Write-Host "2. Re-run this script to verify fixes" -ForegroundColor White
    Write-Host "3. Proceed to basic functionality testing" -ForegroundColor White
    
} else {
    Write-Host "🎉 SUCCESS: No syntax errors found!" -ForegroundColor Green
    Write-Host "All Python files have valid syntax." -ForegroundColor Green
    Write-Host ""
    Write-Host "Ready to proceed to Phase 4 (Basic Functionality Testing)" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "Phase 3 Complete - Syntax Error Detection" -ForegroundColor Green 