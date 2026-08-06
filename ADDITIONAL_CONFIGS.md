# 📋 Additional Configuration Files

Optional advanced configuration files for production deployment.

---

## GitHub Actions Workflow

The `.github/workflows/ci-deploy.yml` file provides:

✅ **Automated Testing**
- Runs pytest on every push
- Checks code quality with flake8
- PostgreSQL test database
- Coverage reporting

✅ **Docker Build**
- Builds production Docker image
- Pushes to GitHub Container Registry
- Multi-stage build optimization
- Automatic caching

✅ **Security Scanning**
- Trivy vulnerability scanner
- Automatic SARIF reports
- GitHub Security alerts

✅ **Automatic Deployment**
- Triggers Render deployment on push to main
- Creates GitHub Deployments
- Status notifications

---

## Health Check Endpoint

Add to your Flask app:

```python
import os
from datetime import datetime

@app.route('/health')
def health():
    """Health check endpoint for monitoring"""
    try:
        # Check database connection
        db.session.execute("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "version": os.getenv("APP_VERSION", "unknown"),
        "database": db_status,
        "environment": os.getenv("FLASK_ENV", "unknown")
    }, 200 if db_status == "healthy" else 503
```

---

## Setup Checklist

For production deployment:

- [ ] Configure GitHub Actions (automatic)
- [ ] Add RENDER_DEPLOY_HOOK secret to GitHub
- [ ] Set up Render with PostgreSQL
- [ ] Configure environment variables
- [ ] Test health check endpoint
- [ ] Enable monitoring in Render
- [ ] Set up custom domain (optional)
- [ ] Test all features
- [ ] Set up backups

---

**Need help?** See:
- [QUICKSTART_DEPLOY.md](QUICKSTART_DEPLOY.md) - Fast deployment guide
- [DEPLOYMENT_TROUBLESHOOTING.md](DEPLOYMENT_TROUBLESHOOTING.md) - Common issues
- [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) - Full deployment guide
