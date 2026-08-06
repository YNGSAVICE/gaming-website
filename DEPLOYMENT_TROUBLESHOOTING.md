# 🔧 Deployment Troubleshooting Guide

Complete troubleshooting guide for common deployment issues and how to fix them.

---

## 🆘 Emergency Fixes

### Application Won't Start
**Symptoms:** Deployment status shows "Failed" or "Error"

**Quick Fixes:**
1. **Check Logs**
   ```
   Render Dashboard → Select Service → Logs
   ```

2. **Common Causes:**
   - Missing environment variables
   - Database not initialized
   - Port already in use
   - Python dependencies missing

3. **Solutions:**
   ```bash
   # Check all environment variables are set
   env | grep FLASK
   env | grep DATABASE
   env | grep OPENWEATHER
   
   # Restart the application
   # Render: Dashboard → Manual Restart
   ```

---

## 🗄️ Database Issues

### "Database Connection Refused"

**Cause:** Database not running or credentials wrong

**Fix:**
1. **Verify Database Exists**
   - Render Dashboard → Select Database
   - Check status = "Available"
   - Wait 2-3 minutes if just created

2. **Check DATABASE_URL Format**
   ```
   Should be: postgresql://user:password@host:5432/dbname
   Not: postgres://... (old format)
   ```

3. **Verify Credentials**
   ```bash
   # In Render dashboard, copy the exact connection string
   # Paste into DATABASE_URL environment variable
   ```

4. **Test Connection**
   ```bash
   psql $DATABASE_URL -c "SELECT 1"
   ```

---

## 🌐 API & Network Issues

### "OpenWeather API Not Working"

**Symptoms:** Weather dashboard shows "API Error" or no data

**Fix:**

1. **Verify API Key**
   ```bash
   # Check if key is set
   curl "https://api.openweathermap.org/data/2.5/weather?q=London&appid=$OPENWEATHER_API_KEY"
   ```

2. **Common Issues:**
   - ❌ API key not activated (wait 10 minutes after signup)
   - ❌ Free tier rate limit exceeded (1000 calls/day)
   - ❌ Wrong API endpoint (use 2.5, not 3.0 for free tier)
   - ❌ Missing `&appid=` parameter

3. **Solution:**
   ```bash
   # Get API key from: https://openweathermap.org/api
   # Add to Render: Environment → OPENWEATHER_API_KEY
   # Wait 10 minutes for activation
   # Test: https://your-app.onrender.com/api/weather/current?city=London
   ```

---

## 🐳 Docker & Container Issues

### "Docker Image Build Failed"

**Symptoms:** Deploy shows "Build failed"

**Fix:**

1. **Check Build Logs**
   - Render Dashboard → Logs → Build Logs tab

2. **Common Build Errors:**
   - ❌ Missing `requirements.txt` → Add it
   - ❌ Syntax error in Dockerfile → Fix it
   - ❌ Missing dependencies → Update requirements.txt

3. **Test Locally**
   ```bash
   docker build -f Dockerfile.prod -t gaming-website .
   docker run -p 5000:5000 gaming-website
   ```

---

## 🚀 Deployment Issues

### "Deployment Hangs or Takes Too Long"

**Cause:** Large dependencies, network issues, or database migrations

**Fix:**

1. **Check Progress**
   - Render Dashboard → Deployments tab
   - Watch the live logs

2. **Common Slow Items:**
   - First time: pulling base Python image (~2 min)
   - Installing dependencies (~3 min)
   - Running migrations (~1 min)
   - Total: 5-10 minutes normal

3. **If Stuck > 15 minutes:**
   - Render Dashboard → Cancel Deployment
   - Check logs for specific error
   - Fix and redeploy

---

### "Deployment Succeeds But App Shows Old Code"

**Cause:** Browser cache or Render cache

**Fix:**

1. **Clear Browser Cache**
   - Press `Ctrl+Shift+Delete` (Windows/Linux)
   - Press `Cmd+Shift+Delete` (Mac)
   - Clear "Cached images and files"

2. **Hard Refresh**
   - Press `Ctrl+F5` (Windows/Linux)
   - Press `Cmd+Shift+R` (Mac)

3. **Verify New Code Deployed**
   ```bash
   curl https://your-app.onrender.com/api/version
   # Should return latest commit hash
   ```

---

## 🌍 Domain & SSL Issues

### "Custom Domain Not Working"

**Symptoms:** Domain points to Render but shows error

**Fix:**

1. **Check DNS Propagation**
   ```bash
   nslookup your-domain.com
   # Should show Render's IP/CNAME
   ```

2. **Verify Render Settings**
   - Render Dashboard → Settings → Custom Domains
   - Confirm domain is added

3. **Update DNS Records**
   - At your domain registrar (GoDaddy, Namecheap, etc.)
   - Add CNAME record:
     ```
     Name: @ (or subdomain)
     Value: gaming-website-xxxxx.onrender.com
     TTL: 3600
     ```

---

## 🔄 GitHub Actions Issues

### "GitHub Actions Workflow Failing"

**Symptoms:** Workflow shows ❌ in GitHub Actions tab

**Fix:**

1. **Check Logs**
   - Repository → Actions tab
   - Click failed workflow
   - Expand job and see error

2. **Common Issues:**
   - ❌ Tests failing → Fix tests locally first
   - ❌ Dependencies missing → Update requirements.txt
   - ❌ Secrets not set → Add to repo secrets

3. **Add Missing Secret**
   ```
   GitHub → Settings → Secrets and Variables → Actions
   New Repository Secret:
   Name: RENDER_DEPLOY_HOOK
   Value: <paste-your-render-deploy-hook-url>
   ```

4. **Re-run Workflow**
   - GitHub → Actions → Failed Workflow
   - Click "Re-run jobs" button

---

### "Deploy Hook URL Not Working"

**Symptoms:** Deployment doesn't trigger from GitHub

**Fix:**

1. **Get Correct Hook URL**
   - Render Dashboard → Service → Settings
   - Scroll to "Deploy Hook"
   - Copy full URL

2. **Update GitHub Secret**
   - GitHub → Settings → Secrets and Variables
   - Edit RENDER_DEPLOY_HOOK
   - Paste new URL

3. **Test Hook Manually**
   ```bash
   curl -X POST <your-deploy-hook-url>
   # Should trigger deployment in Render
   ```

---

## ✅ Verification Checklist

After fixing an issue, verify:

- [ ] App loads without errors
- [ ] All features work (clock, weather, games)
- [ ] API endpoints respond correctly
- [ ] Database queries return data
- [ ] No console errors (F12)
- [ ] Logs show successful operations
- [ ] Response times are acceptable
- [ ] HTTPS works and shows secure
- [ ] Mobile view works
- [ ] Tests pass locally

---

## 📝 Performance Tips

1. **Enable Caching**
   ```python
   from flask_caching import Cache
   cache = Cache(app, config={'CACHE_TYPE': 'simple'})
   ```

2. **Optimize Database**
   ```bash
   # Add indexes to frequently queried columns
   psql $DATABASE_URL -c "CREATE INDEX idx_column ON table(column);"
   ```

3. **Use CDN** (optional)
   - Cloudflare (free)
   - AWS CloudFront (paid)

---

**Still having issues?**

1. Check Render documentation: https://render.com/docs
2. Check Flask documentation: https://flask.palletsprojects.com
3. Review full guide: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
4. Open GitHub issue with error details

Good luck! 🚀
