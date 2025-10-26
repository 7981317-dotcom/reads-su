# Deploy script for reads.su
Write-Host "🚀 Deploying to production server..." -ForegroundColor Cyan
Write-Host ""

# Push to GitHub
Write-Host "📤 Pushing to GitHub..." -ForegroundColor Yellow
git push origin main

# Create SSH password file (temporary)
$password = "p,-iVfmLCQ3EiK"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force

# Deploy command
$deployCommand = @"
cd /opt/reads-su && git pull origin main && source venv/bin/activate && export DATABASE_URL='postgres://reads_user:reads_password_2024_secure@localhost:5432/reads_su' && export RAILWAY_ENVIRONMENT=production && python manage.py compress --force && python manage.py collectstatic --noinput && systemctl restart reads-su && redis-cli -n 1 FLUSHDB && echo '✅ Deploy completed!'
"@

Write-Host "🔧 Deploying to server..." -ForegroundColor Yellow

# Use SSH with password (requires sshpass or plink)
$env:SSHPASS = $password
ssh root@213.171.5.75 $deployCommand

Write-Host ""
Write-Host "✅ Deployment completed successfully!" -ForegroundColor Green
