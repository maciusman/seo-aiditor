# 🔑 How to Get Free API Keys (2 minutes)

SEO AIditor requires Google API keys to function. Don't worry - they're completely FREE and take only 2 minutes to get!

---

## 1. Google Gemini API Key (Required) ⭐

### Why needed?
Powers AI analysis: content quality, site type detection, holistic insights, strategic recommendations.

### How to get it:

1. **Go to:** https://aistudio.google.com/apikey
2. **Sign in** with your Google account
3. Click **"Create API Key"**
4. Choose **"Create API key in new project"** (or select existing project)
5. **Copy the key** (starts with `AIza...`)
6. **Paste into SEO AIditor** when prompted

### Free tier limits:
- ✅ **5 requests per minute**
- ✅ **25 requests per day**
- ✅ **1M token context window**

**Need more?** Upgrade to paid tier: $7 per 1M tokens for unlimited use.

---

## 2. PageSpeed Insights API Key (Optional) 📊

### Why needed?
Enables detailed Performance tab with:
- Lighthouse scores (Performance, Accessibility, Best Practices, SEO)
- Core Web Vitals (LCP, FID, CLS)
- Optimization opportunities with time savings
- Full PageSpeed Insights report link

**Without PSI key:** You'll still get basic performance metrics, but no detailed Performance tab.

### How to get it:

1. **Go to:** https://console.cloud.google.com/apis/library/pagespeedonline.googleapis.com
2. **Select or create** a Google Cloud project
3. Click **"Enable"** on PageSpeed Insights API
4. Go to **Credentials**: https://console.cloud.google.com/apis/credentials
5. Click **"Create Credentials"** → **"API Key"**
6. **Copy the key**
7. *(Optional)* Click **"Restrict Key"** → Select "PageSpeed Insights API" for security
8. **Paste into SEO AIditor**

### Free tier limits:
- ✅ **25,000 requests per day**
- ✅ **Unlimited requests per minute**

**PSI is very generous** - you likely won't hit the limit.

---

## 🔒 Security & Privacy

### Where are keys stored?

**By default:** `sessionStorage` (browser session only)
- Keys are deleted when you close the browser tab
- Most secure option
- You'll need to re-enter keys on next visit

**Optional:** `localStorage` (persistent)
- Check ☑️ "Remember keys in this browser"
- Keys saved until you clear browser data
- **Only use on trusted, personal devices!**

### Important:
- ✅ Keys stored **only in YOUR browser** (client-side)
- ✅ Keys sent to server **only during analysis** (HTTPS recommended)
- ✅ Keys **never logged** or saved on server
- ✅ Keys **never visible** to SEO AIditor developers
- ❌ Never share your API keys publicly
- ❌ Don't commit keys to GitHub

---

## ❓ Troubleshooting

### "Invalid Gemini API key"

**Possible causes:**
- Key not copied fully (must start with `AIza...`)
- Key not activated yet (wait 1-2 minutes after creation)
- API not enabled in Google Cloud Console

**Solution:**
1. Go back to https://aistudio.google.com/apikey
2. Copy the ENTIRE key (should be ~39 characters)
3. Try creating a new key if problem persists

### "Rate limit exceeded - Gemini API"

**What happened:** Free tier limit = 5 requests per minute

**Solution:**
- Wait 60 seconds before next analysis
- OR upgrade your Gemini plan at https://ai.google.dev/pricing

### "PageSpeed API error" / "PSI timeout"

**Don't worry!** PSI key is optional.

**What you'll miss:**
- Detailed Performance tab
- Lighthouse category scores
- Core Web Vitals breakdown
- Optimization opportunities list

**What still works:**
- All other analysis (Technical, On-Page, Content, etc.)
- Basic performance score (mobile)
- AI recommendations
- Issue detection

**Solution:**
- Continue without PSI key (basic analysis)
- OR get PSI key following steps above

### Keys not saving / keep asking for keys

**Check:**
- Is "Remember keys" checkbox checked?
- Did you clear browser cache/cookies?
- Are you in Private/Incognito mode? (use regular browser)

**Solution:**
- Re-enter keys
- Check "Remember keys in this browser"
- Make sure cookies/localStorage enabled in browser

---

## 💰 Cost Breakdown (2025)

| Service | Free Tier | Paid Tier |
|---------|-----------|-----------|
| **Gemini API** | 5 req/min, 25/day | $7 per 1M tokens |
| **PageSpeed Insights** | 25K req/day | Free forever |
| **SEO AIditor hosting** | $0 (PythonAnywhere free) | $5/mo (HTTPS upgrade) |

**Total cost for typical use:** **$0/month** 🎉

**Heavy use (100+ audits/day):** ~$10-20/month (Gemini paid tier)

---

## 🎯 Quick Start Checklist

- [ ] Get Gemini API key → https://aistudio.google.com/apikey
- [ ] (Optional) Get PSI API key → https://console.cloud.google.com
- [ ] Open SEO AIditor
- [ ] Enter API keys when prompted
- [ ] Choose "Remember keys" if on personal device
- [ ] Run your first audit! 🚀

---

## 📞 Need Help?

- **GitHub Issues:** https://github.com/maciusman/seo-aiditor/issues
- **Gemini API Docs:** https://ai.google.dev/gemini-api/docs
- **PageSpeed API Docs:** https://developers.google.com/speed/docs/insights/v5/get-started

---

**Ready to go?** [Open SEO AIditor](../) and paste your keys! 🎉
