# Verify Setup Script

Write-Host "Verifying Self-Healing CI/CD Agent Setup..." -ForegroundColor Cyan
Write-Host ""

# Check if backend is running
Write-Host "1. Checking backend..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "   Backend is running!" -ForegroundColor Green
    }
} catch {
    Write-Host "   Backend is NOT running!" -ForegroundColor Red
    Write-Host "   Start it with: .\start-backend.ps1" -ForegroundColor Yellow
}

Write-Host ""

# Check if dashboard is accessible
Write-Host "2. Checking dashboard..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3000" -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "   Dashboard is accessible!" -ForegroundColor Green
    }
} catch {
    Write-Host "   Dashboard is NOT accessible!" -ForegroundColor Red
    Write-Host "   Start it with: .\start-dashboard.ps1" -ForegroundColor Yellow
}

Write-Host ""

# Check API endpoints
Write-Host "3. Checking API endpoints..." -ForegroundColor Yellow
try {
    $stats = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/stats"
    Write-Host "   API is working!" -ForegroundColor Green
    Write-Host "   Total Pipelines: $($stats.total_pipelines)" -ForegroundColor Cyan
    Write-Host "   Total Failures: $($stats.total_failures)" -ForegroundColor Cyan
    Write-Host "   Total Fixes: $($stats.total_fixes)" -ForegroundColor Cyan
    Write-Host "   Success Rate: $($stats.success_rate)%" -ForegroundColor Cyan
} catch {
    Write-Host "   API is not responding!" -ForegroundColor Red
}

Write-Host ""

# Check .env configuration
Write-Host "4. Checking configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    $envContent = Get-Content ".env" -Raw
    
    if ($envContent -match "GITHUB_TOKEN=github_pat_" -or $envContent -match "GITHUB_TOKEN=ghp_") {
        Write-Host "   GitHub token configured!" -ForegroundColor Green
    } else {
        Write-Host "   GitHub token NOT configured!" -ForegroundColor Red
        Write-Host "   Add your token to .env file" -ForegroundColor Yellow
    }
    
    if ($envContent -match "OPENAI_API_KEY=sk-") {
        Write-Host "   OpenAI API key configured!" -ForegroundColor Green
    } else {
        Write-Host "   OpenAI API key NOT configured!" -ForegroundColor Red
        Write-Host "   Add your key to .env file" -ForegroundColor Yellow
    }
} else {
    Write-Host "   .env file not found!" -ForegroundColor Red
}

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Summary
Write-Host "Next Steps:" -ForegroundColor Green
Write-Host "1. Open browser: http://localhost:3000" -ForegroundColor White
Write-Host "2. Create a test failure (see TEST_FAILURE_GUIDE.md)" -ForegroundColor White
Write-Host "3. Wait 30 seconds for agent to detect it" -ForegroundColor White
Write-Host "4. Check dashboard for results!" -ForegroundColor White
Write-Host ""
