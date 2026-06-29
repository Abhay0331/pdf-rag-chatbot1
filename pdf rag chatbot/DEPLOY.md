# Deployment Guide for Vercel

## Prerequisites

1. **Vercel Account**: Sign up at https://vercel.com
2. **Groq API Key** (Free tier available): https://console.groq.com
3. **OpenAI API Key**: https://platform.openai.com/api-keys (for embeddings)

## Step 1: Get API Keys

### Groq (Free LLM)
- Go to https://console.groq.com
- Sign up/Login
- Create an API key
- Copy it

### OpenAI (Embeddings)
- Go to https://platform.openai.com/api-keys
- Create a new API key
- Copy it
- **Note**: Small embeddings requests are cheap (~$0.02 per 1M tokens)

## Step 2: Push Code to GitHub

```powershell
# Initialize git if not already done
git init

# Add all files
git add .

# Commit
git commit -m "Update for Vercel deployment with Groq + OpenAI"

# Push to GitHub (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/pdf-rag-chatbot.git
git branch -M main
git push -u origin main
```

## Step 3: Deploy to Vercel

### Option A: Via Vercel CLI (Fastest)
```powershell
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel --prod
```

### Option B: Via Vercel Web Dashboard
1. Go to https://vercel.com/dashboard
2. Click "Add New" → "Project"
3. Import your GitHub repository
4. Click "Deploy"

## Step 4: Set Environment Variables in Vercel

After deployment:

1. Go to your Vercel project dashboard
2. Click "Settings" → "Environment Variables"
3. Add these variables:

| Key | Value |
|-----|-------|
| `GROQ_API_KEY` | Your Groq API key |
| `OPENAI_API_KEY` | Your OpenAI API key |
| `CHROMA_DB_PATH` | `/tmp/chroma_db` |
| `TEMPERATURE` | `0.4` |

4. Click "Save"
5. Go to "Deployments" and redeploy (or manually trigger a redeployment)

## Step 5: Test Your Deployment

1. Visit your Vercel URL (e.g., `https://pdf-rag-chatbot.vercel.app`)
2. Upload a PDF
3. Ask a question about the PDF

## Troubleshooting

### Error: "GROQ_API_KEY environment variable is required"
- Verify the API key is set in Vercel Settings → Environment Variables
- Redeploy after setting the variable

### Error: "OPENAI_API_KEY environment variable is required"
- Same as above

### Cold Start Issues
- Vercel serverless may take a few seconds on first request
- Subsequent requests are faster

### PDF Upload Fails
- Vercel has a 50MB request size limit
- Ensure PDFs are under 50MB
- For larger PDFs, use a storage solution like AWS S3

## Local Development (Optional)

To test locally before deploying:

1. Copy `.env.example` to `.env`
2. Fill in your API keys
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python app.py`
5. Visit `http://localhost:5000`

## Cost Estimation

- **Groq**: Free tier with reasonable limits (~100 requests/day)
- **OpenAI Embeddings**: ~$0.02 per 1M tokens (very cheap)
- **Vercel**: Free tier includes this deployment
- **Total Monthly Cost**: $0-2 for light usage, $5-10 for moderate usage

## Production Considerations

- Use HTTPS (Vercel provides this automatically)
- Consider adding authentication/rate limiting for public access
- Monitor API usage in Groq and OpenAI dashboards
- Set up alerts for API key leaks
commit changes in git as well
