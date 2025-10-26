@echo off
echo Deploying to production server...
echo.

REM Push to GitHub
git push origin main

REM Deploy to server using plink (PuTTY) with password
echo y | plink -ssh root@213.171.5.75 -pw "p,-iVfmLCQ3EiK" "cd /opt/reads-su && git pull origin main && source venv/bin/activate && export DATABASE_URL='postgres://reads_user:reads_password_2024_secure@localhost:5432/reads_su' && export RAILWAY_ENVIRONMENT=production && python manage.py compress --force && python manage.py collectstatic --noinput && systemctl restart reads-su && redis-cli -n 1 FLUSHDB && echo 'Deploy completed successfully!'"

echo.
echo ✅ Deployment completed!
pause
