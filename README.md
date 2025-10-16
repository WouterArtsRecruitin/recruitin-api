# 🚀 Recruitin Labour Market Intelligence API

Flask API voor het verwerken van Jotform submissions en het genereren van arbeidsmarkt analyses.

## 📋 Features

- ✅ Jotform webhook handler
- ✅ Health check endpoint
- ✅ CORS enabled
- ✅ Production-ready logging
- ✅ Error handling
- ✅ Render.com deployment config

## 🔗 Endpoints

### `GET /`
API home met documentatie

### `GET /health`
Health check voor monitoring

### `POST /webhook/jotform`
Webhook voor Jotform submissions

**Expected payload:**
```json
{
  "rawRequest": "{\"submissionID\":\"...\",\"answers\":{...}}"
}
```

## 🚀 Deployment

### Render.com (Recommended)

1. Push naar GitHub
2. Connect repo in Render dashboard
3. Auto-deploy from `render.yaml`

### Manual Deploy

```bash
pip install -r requirements.txt
gunicorn app:app
```

## 🔗 Jotform Setup

1. Open form settings: https://www.jotform.com/form-designer/252881347421054
2. Go to "Settings" → "Integrations" → "Webhooks"
3. Add webhook URL: `https://your-api.onrender.com/webhook/jotform`
4. Select "Send as JSON"
5. Save

## 📊 Environment Variables

- `PORT`: Server port (default: 5000)
- `DEBUG`: Debug mode (default: false)

## 🧪 Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python app.py

# Test webhook
curl -X POST http://localhost:5000/webhook/jotform \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'rawRequest={"submissionID":"test123"}'
```

## 📞 Support

Contact: Recruitin Development Team
