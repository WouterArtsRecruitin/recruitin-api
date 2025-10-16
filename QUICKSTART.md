# 🚀 QUICKSTART - Deploy in 15 Minutes

## ✅ PRE-FLIGHT CHECKLIST

You have:
- [x] Jotform API Key
- [x] Brave Search API Key
- [x] Notion API Key
- [x] GitHub Token
- [x] Cloudflare API Token
- [x] Render API Token

All systems GO! 🎯

---

## 📦 STEP 1: PREPARE CODE (2 min)

```bash
# 1. Create project directory
mkdir labour-market-intelligence
cd labour-market-intelligence

# 2. Copy these files from /tmp:
cp /tmp/labour-market-intelligence-mcp.py .
cp /tmp/app.py .
cp /tmp/requirements.txt .
cp /tmp/render.yaml .
cp /tmp/.gitignore .
cp /tmp/LABOUR_MARKET_INTELLIGENCE_README.md README.md

# 3. Create .env file (NEVER COMMIT!)
cat > .env << 'EOF'
JOTFORM_API_KEY=2189378edb821cfa9d6ddbb920038eea
BRAVE_SEARCH_API_KEY=your_brave_api_key_here
NOTION_API_KEY=your_notion_api_key_here
GITHUB_TOKEN=your_github_token_here
CLOUDFLARE_API_TOKEN=your_cloudflare_token_here
RENDER_API_TOKEN=your_render_token_here
EOF
```

---

## 🔧 STEP 2: TEST LOCALLY (3 min)

```bash
# Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Test MCP directly
python3 labour-market-intelligence-mcp.py
# → Should show: ✅ ALL TESTS PASSED!

# Test Flask API
python3 app.py
# → Server running on http://localhost:5000

# Test API endpoint (in another terminal)
curl http://localhost:5000/health
# → {"status": "healthy"}
```

---

## 📝 STEP 3: CREATE JOTFORM (5 min)

```bash
# 1. Go to: https://www.jotform.com/myforms
# 2. Click "Create Form"
# 3. Add these fields:
#    - Email (required)
#    - Job Title (text, required)
#    - Location (text, required)
#    - Upload Jobdigger PDF (file upload, .pdf, 10MB max)
#    - Upload LinkedIn TI PDF (file upload, .pdf, 10MB max)
#    - Vacancy Text (long text)
#    - Vacancy URL (url)
#    - Report Type (dropdown: Executive/Standard/Extensive/Action Plan)
#
# 4. Settings → Integrations → Webhooks
#    Add: https://labour-intel-parser.onrender.com/webhook/jotform
#    (Will add after deployment)
#
# 5. Settings → Notifications
#    Email: artsrecruitin@gmail.com
#
# 6. Publish form
# 7. Copy form URL
```

**Your form will be at:** `https://form.jotform.com/YOUR_FORM_ID`

---

## 🌐 STEP 4: DEPLOY TO RENDER (3 min)

```bash
# 1. Initialize git repo
git init
git add .
git commit -m "Initial commit - Labour Market Intelligence"

# 2. Create GitHub repo
# Go to: https://github.com/new
# Name: labour-market-intelligence
# Visibility: Private
# Create repository

# 3. Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/labour-market-intelligence.git
git branch -M main
git push -u origin main

# 4. Deploy on Render
# Go to: https://dashboard.render.com
# Click "New Web Service"
# Connect GitHub repo: labour-market-intelligence
# Name: labour-intel-parser
# Region: Frankfurt (EU)
# Branch: main
# Root Directory: (leave empty)
# Build Command: pip install -r requirements.txt
# Start Command: gunicorn --bind 0.0.0.0:$PORT --timeout 120 app:app
# Plan: Starter ($7/month)
# 
# Environment Variables (add these):
#   BRAVE_SEARCH_API_KEY=BSAW_h04juedQeMi6BwPvPLlfST4vC3
#   JOTFORM_API_KEY=2189378edb821cfa9d6ddbb920038eea
#   NOTION_API_KEY=ntn_N921362306116pa5KHYRvt3AScWH3y2K87Hf4bMwi2x5R3
#
# Click "Create Web Service"
```

**Your API will be at:** `https://labour-intel-parser.onrender.com`

---

## 🗄️ STEP 5: SETUP NOTION DATABASE (2 min)

```bash
# 1. Open Notion
# 2. Create new page: "Labour Market Intelligence"
# 3. Add database: /database
# 4. Name it: "Market Reports"
# 5. Add properties:
#    - Job Title (Title) - auto-created
#    - Location (Text)
#    - Status (Select: Processing, Completed, Failed)
#    - Confidence (Number, %)
#    - Vacancy Count (Number)
#    - Median Salary (Number, €)
#    - Submitted By (Email)
#    - Created At (Created time) - auto-created
#
# 6. Click "..." → Add connections → Select your integration
#    (Or create integration at: https://www.notion.so/my-integrations)
#
# 7. Copy database ID from URL:
#    notion.so/YOUR_WORKSPACE/DATABASE_ID?v=...
#                           ^^^^^^^^^ Copy this part
```

---

## 🔗 STEP 6: CONNECT JOTFORM WEBHOOK (1 min)

```bash
# 1. Go back to Jotform → Form Settings
# 2. Integrations → Webhooks
# 3. Edit webhook URL to:
#    https://labour-intel-parser.onrender.com/webhook/jotform
# 4. Save
# 5. Test webhook (Submit test form)
```

---

## ✅ STEP 7: TEST END-TO-END (2 min)

```bash
# 1. Submit Jotform:
#    - Job Title: "Test Engineer"
#    - Location: "Amsterdam"
#    - Upload: Your Jobdigger PDF
#
# 2. Check Render logs:
#    https://dashboard.render.com → labour-intel-parser → Logs
#    → Should see: "Submission received"
#
# 3. Check Notion database:
#    → New row should appear
#
# 4. Test API directly:
curl -X POST https://labour-intel-parser.onrender.com/parse/jobdigger \
  -H "Content-Type: application/json" \
  -d '{"pdf_path": "/path/to/jobdigger.pdf"}'
```

---

## 🎉 YOU'RE LIVE!

**Next steps:**
1. ✅ Test with real Jobdigger PDF
2. ✅ Check report quality
3. ✅ Refine skills extraction
4. ✅ Add more data sources (CBS, UWV)
5. ✅ Build Vercel dashboard (optional)

---

## 🆘 TROUBLESHOOTING

### Render deployment fails
```bash
# Check logs:
render logs labour-intel-parser

# Common issues:
# - Missing requirements.txt → Check file exists
# - Wrong Python version → render.yaml specifies 3.11
# - Environment vars missing → Add in Render dashboard
```

### Jotform webhook not working
```bash
# Test webhook manually:
curl -X POST https://labour-intel-parser.onrender.com/webhook/jotform \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'rawRequest={"submissionID":"test","answers":{}}'

# Should return: {"success": true}
```

### PDF parsing errors
```bash
# Check PDF format:
# - Must be valid PDF
# - Max 10MB
# - Not encrypted
# - Not scanned image (needs OCR)

# Test locally first:
python3 labour-market-intelligence-mcp.py
```

---

## 📊 MONITORING

**Render Dashboard:**
- https://dashboard.render.com
- Check: Logs, Metrics, Health

**Jotform Submissions:**
- https://www.jotform.com/myforms
- See all submissions

**Notion Database:**
- Check for new reports
- Export to Pipedrive if needed

---

## 💰 COST TRACKING

| Service | Cost/Month | Usage Limit |
|---------|-----------|-------------|
| Render Starter | $7 | Always-on, 512MB RAM |
| Jotform Bronze | €34 | 100 forms/month |
| Brave Search | €30 | 3,000 searches |
| Notion | €0 | Unlimited |
| GitHub | €0 | Private repos OK |
| **TOTAL** | **€71/month** | |

**Per report cost:** €0.71 (at 100 reports/month)

---

## 🔐 SECURITY REMINDER

**After setup, IMMEDIATELY:**
1. Delete all API keys from chat history
2. Regenerate all tokens
3. Use 1Password/Bitwarden for storage
4. Enable 2FA on all services
5. Never commit .env to git

---

## 📞 SUPPORT

Questions? Issues?
- Check logs first (Render dashboard)
- Test API endpoints (curl commands above)
- GitHub Issues: (create repo issues)
- Email: artsrecruitin@gmail.com

---

**⏱️ Total setup time:** ~15 minutes  
**🎯 Result:** Fully automated labour market intelligence system!

Let's go! 🚀
