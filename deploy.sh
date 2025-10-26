#!/bin/bash

echo "🚀 Deploying to production server..."
echo ""

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push origin main

# Deploy to server
echo "🔧 Deploying to server..."
ssh -i ~/.ssh/reads_su_key root@213.171.5.75 "cd /opt/reads-su && git pull origin main && source venv/bin/activate && export DATABASE_URL='postgres://reads_user:reads_password_2024_secure@localhost:5432/reads_su' && export RAILWAY_ENVIRONMENT=production && python manage.py compress --force && python manage.py collectstatic --noinput && systemctl restart reads-su && redis-cli -n 1 FLUSHDB && echo '✅ Deploy completed!'"

echo ""
echo "✅ Deployment completed successfully!"
