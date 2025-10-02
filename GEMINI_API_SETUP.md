# 🤖 Gemini API Setup Guide

This guide will help you get your **FREE** Google Gemini API key to enable AI-powered SEO analysis.

---

## ⏱️ Quick Setup (5 minutes)

### Step 1: Get Your Free Gemini API Key

1. **Go to Google AI Studio:**
   - Visit: https://aistudio.google.com/apikey
   - Sign in with your Google account

2. **Create API Key:**
   - Click **"Create API Key"** button
   - Select **"Create API key in new project"** (or use existing project)
   - Copy the API key (starts with `AIza...`)

   ⚠️ **IMPORTANT:** Save this key somewhere safe! You won't be able to see it again.

---

### Step 2: Add API Key to Config

1. **Open `config.py`** in your project folder

2. **Replace placeholder:**
   ```python
   # Find this line:
   GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"

   # Replace with your actual key:
   GEMINI_API_KEY = "AIzaSyC_YOUR_ACTUAL_KEY_HERE"
   ```

3. **Save the file**

---

### Step 3: Test AI Features

Run the test script to verify it works:

```bash
python ai_engine.py
```

You should see:
```
✅ Gemini AI Engine initialized successfully
✅ AI Engine is ready!
```

---

## 🎯 What AI Features Will You Get?

Once configured, the SEO Auditor will provide:

### 1. **AI Content Quality Analysis**
- E-E-A-T signals detection (Experience, Expertise, Authoritativeness, Trust)
- Search intent matching (informational/transactional/navigational/commercial)
- Content depth analysis
- Keyword naturalness scoring
- Content gap identification

### 2. **AI Personalized Action Plan**
- 30/60/90-day roadmap
- Quick wins identification
- Prioritized tasks with impact estimates
- Tool recommendations
- Content strategy suggestions

---

## 💰 Pricing (Gemini 2.5 Flash)

**Good news:** Gemini 2.5 Flash is **EXTREMELY CHEAP**!

| Usage | Cost per Audit |
|-------|----------------|
| Input (1M tokens) | **$0.000075 per 1k tokens** |
| Output (65k tokens) | **$0.00030 per 1k tokens** |

**Typical audit cost: $0.01 - $0.03** 🎉

**Free tier:**
- 1,500 requests per day
- 1 million tokens per minute

➡️ **Translation:** You can run ~50 audits per day **COMPLETELY FREE**

---

## 🔧 Troubleshooting

### Issue 1: "AI not available - check API key"

**Cause:** API key is missing or invalid

**Fix:**
1. Check `config.py` has your real API key (not placeholder)
2. Verify key starts with `AIza...`
3. Make sure there are no extra spaces or quotes

---

### Issue 2: "403 Forbidden" or "Permission Denied"

**Cause:** API key restrictions in Google Cloud Console

**Fix:**
1. Go to: https://console.cloud.google.com/apis/credentials
2. Click on your API key
3. Under "API restrictions":
   - Select **"Don't restrict key"**
   - OR add **"Generative Language API"** to allowed APIs
4. Save changes
5. Wait 1-2 minutes for changes to propagate

---

### Issue 3: "Quota exceeded"

**Cause:** You've exceeded free tier limits

**Fix:**
1. Wait for quota to reset (resets daily)
2. OR upgrade to paid tier (still very cheap!)
3. OR disable AI temporarily:
   ```python
   # In config.py:
   ENABLE_AI_ANALYSIS = False
   ```

---

## 🛡️ Security Best Practices

### ✅ DO:
- Keep your API key private (don't share on GitHub)
- Add `config.py` to `.gitignore` if sharing code
- Use environment variables in production:
  ```python
  import os
  GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'YOUR_GEMINI_API_KEY_HERE')
  ```

### ❌ DON'T:
- Commit API keys to public repositories
- Share keys in screenshots or videos
- Use the same key for multiple public projects

---

## 🔄 Disable AI Features (Optional)

If you want to run audits **without AI** (saves API calls):

1. Open `config.py`
2. Set:
   ```python
   ENABLE_AI_ANALYSIS = False
   ```
3. Audits will still work, but skip AI insights

---

## 📚 Additional Resources

- **Gemini API Documentation:** https://ai.google.dev/gemini-api/docs
- **Pricing Calculator:** https://ai.google.dev/pricing
- **API Console:** https://console.cloud.google.com/apis/credentials
- **Community Forum:** https://discuss.ai.google.dev/

---

## ✅ Verification Checklist

- [ ] Created Gemini API key at https://aistudio.google.com/apikey
- [ ] Added key to `config.py`
- [ ] Ran `python ai_engine.py` successfully
- [ ] Saw "✅ AI Engine is ready!" message
- [ ] Ready to run AI-powered audits! 🚀

---

**Need help?** Check our troubleshooting section or open an issue on GitHub.

**Questions about costs?** The free tier is generous enough for personal use and small agencies. You'd need to run 500+ audits per day to hit limits.
