# 🎯 SIMPLE DEPLOYMENT GUIDE
## After Autonomous Script Attempt

**Status:** ✅ Project files created locally!
**Location:** `/root/labour-market-intelligence/`

API keys had rate limiting, so here's the **super simple manual deployment**:

---

## ✅ WHAT'S ALREADY DONE

- ✅ All files created
- ✅ Git repository initialized
- ✅ .env file configured
- ✅ Project structure ready

**You just need to:**
1. Push to GitHub (2 min)
2. Deploy to Render (5 min)
3. Create Jotform (5 min)

---

## 🚀 STEP 1: PUSH TO GITHUB (2 min)

```bash
cd /root/labour-market-intelligence

# Create repo on GitHub.com
# Go to: https://github.com/new
# Name: labour-market-intelligence
# Private: Yes
# Create repository

# Push code (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/labour-market-intelligence.git
git branch -M main
git push -u origin main
```

**Or use GitHub CLI:**
```bash
gh repo create labour-market-intelligence --private --source=. --remote=origin --push
```

---

## 🚀 STEP 2: DEPLOY TO RENDER (5 min)

### Option A: Via Dashboard (Easiest)

1. Go to https://dashboard.render.com
2. Click **"New Web Service"**
3. Connect your GitHub repo
4. Settings:
   - **Name:** `labour-intel-parser`
   - **Region:** Frankfurt
   - **Branch:** main
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn --bind 0.0.0.0:$PORT --timeout 120 app:app`
   - **Plan:** Starter ($7/month)

5. Add Environment Variables:
   ```
   BRAVE_SEARCH_API_KEY=BSAW_h04juedQeMi6BwPvPLlfST4vC3
   JOTFORM_API_KEY=2189378edb821cfa9d6ddbb920038eea
   NOTION_API_KEY=ntn_N921362306116pa5KHYRvt3AScWH3y2K87Hf4bMwi2x5R3
   ```

6. Click **"Create Web Service"**

7. Wait 5 minutes for deployment

8. Test: `https://your-service.onrender.com/health`

### Option B: Via Render CLI

```bash
# Install Render CLI
npm install -g render-cli

# Login
render login

# Deploy
render deploy
```

---

## 📝 STEP 3: CREATE JOTFORM (5 min)

1. Go to https://www.jotform.com/myforms
2. Click **"Create Form"**
3. Add these fields:
   - Email (required)
   - Job Title (text, required)
   - Location (text, required)
   - Upload Jobdigger PDF (file, optional)
   - Upload LinkedIn TI PDF (file, optional)
   - Vacancy Text (textarea, optional)
   - Vacancy URL (url, optional)
   - Report Type (dropdown: Executive/Standard/Extensive/Action Plan)

4. **Settings → Integrations → Webhooks**
   - Add: `https://your-service.onrender.com/webhook/jotform`

5. **Settings → Notifications**
   - Email: artsrecruitin@gmail.com

6. Publish form

7. Copy form URL

---

## 🗄️ STEP 4: SETUP NOTION (5 min)

1. Open Notion
2. Create new page: **"Labour Market Intelligence"**
3. Add database: `/database`
4. Add properties:
   - **Job Title** (Title)
   - **Location** (Text)
   - **Status** (Select: Processing, Completed, Failed)
   - **Confidence** (Number, %)
   - **Vacancy Count** (Number)
   - **Median Salary** (Number, €)
   - **Submitted By** (Email)
   - **Created At** (Created time)

5. Share with integration:
   - Click "..." → Add connections
   - Select your integration
   - Or create at: https://www.notion.so/my-integrations

6. Copy database ID from URL

---

## ✅ TEST END-TO-END (2 min)

```bash
# 1. Test API health
curl https://your-service.onrender.com/health

# Should return: {"status": "healthy"}

# 2. Submit test form
# Go to your Jotform URL
# Fill out test data
# Submit

# 3. Check Render logs
# Dashboard → your-service → Logs
# Should see: "Submission received"

# 4. Check Notion database
# Should see new entry

# 5. Test with real PDF
# Upload your Jobdigger PDF via form
# Wait 2-3 minutes
# Check Notion for report
```

---

## 🎉 YOU'RE LIVE!

After these steps:
- ✅ Code on GitHub
- ✅ API running on Render
- ✅ Form live on Jotform
- ✅ Database ready in Notion
- ✅ All webhooks configured

**Total time:** 15-20 minutes

---

## 💡 QUICK TIPS

### Test locally first:
```bash
cd /root/labour-market-intelligence
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py

# In another terminal:
curl http://localhost:5000/health
```

### Use ngrok for webhook testing:
```bash
ngrok http 5000
# Copy ngrok URL to Jotform webhook
```

### Update code after deployment:
```bash
cd /root/labour-market-intelligence
git add .
git commit -m "Update: description"
git push
# Render auto-deploys!
```

---

## 🆘 NEED HELP?

**Check logs:**
- Render: Dashboard → Service → Logs
- Jotform: Submissions page
- Local: Terminal output

**Common issues:**
- Render build fails → Check requirements.txt
- Webhook not working → Verify URL in Jotform
- PDF parsing errors → Check PDF format

**Ask Claude:**
- Share error messages
- Show API responses
- Include logs

---

## 📊 WHAT YOU GET

After deployment:
- **API Endpoints:**
  - `/health` - Health check
  - `/parse/jobdigger` - Parse Jobdigger PDF
  - `/scrape/indeed` - Scrape Indeed data
  - `/deepdive` - Full market analysis
  - `/report/generate` - Generate report
  - `/webhook/jotform` - Jotform webhook

- **Automated Workflow:**
  1. User submits Jotform
  2. Webhook triggers API
  3. PDFs parsed automatically
  4. Market data scraped
  5. Report generated
  6. Stored in Notion
  7. User notified via email

- **Cost:** €71/month (~€0.71 per report)

---

## 🎯 NEXT STEPS

After deployment:
1. Test with your Jobdigger PDF
2. Check report quality
3. Refine extractors if needed
4. Add CBS/UWV data sources
5. Build dashboard (optional)

---

**📦 All files ready at:** `/root/labour-market-intelligence/`

**🚀 Let's deploy manually - it's only 15 minutes!**

Type "MANUAL DEPLOY" when ready to start step-by-step! 👊
