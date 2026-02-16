# v4.5.0 Golden State Restoration Script
Write-Host "🔧 Restoring v4.5.0 Golden State..." -ForegroundColor Cyan

# Fix 1: Language Configuration
Write-Host "✅ Fixing LANGUAGE_CONFIGURED..." -ForegroundColor Green
(Get-Content .env) -replace "LANGUAGE_CONFIGURED='False'", "LANGUAGE_CONFIGURED='ID'" | Set-Content .env

# Fix 2: Broker List (Optional)
Write-Host "✅ Removing IC Markets from broker list..." -ForegroundColor Green
(Get-Content src\localization.py) -replace 'IC Markets', 'RoboForex' -replace 'icmarkets.com', 'roboforex.com' | Set-Content src\localization.py

Write-Host "✅ Restoration Complete!" -ForegroundColor Green
Write-Host "🔄 Please restart the application: python src/gui.py" -ForegroundColor Yellow
