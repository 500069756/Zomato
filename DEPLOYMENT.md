# Vercel Deployment Guide - Zomato AI Restaurant Recommender

## 📋 Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Push your code to GitHub
3. **Groq API Key**: Get from [console.groq.com](https://console.groq.com/)

## 🚀 Deployment Steps

### Option 1: Deploy via Vercel CLI (Recommended)

#### Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

#### Step 2: Login to Vercel
```bash
vercel login
```

#### Step 3: Deploy to Vercel
```bash
cd c:\Users\bansa\Downloads\zomato
vercel
```

Follow the prompts:
- **Set up and deploy**: Yes
- **Which scope**: Choose your account
- **Link to existing project**: No
- **Project name**: zomato-ai-recommender (or your choice)
- **Directory**: ./frontend
- **Override settings**: No

#### Step 4: Set Environment Variables
After first deployment, set environment variables:

```bash
vercel env add GROQ_API_KEY
```

Enter your Groq API key when prompted.

#### Step 5: Deploy to Production
```bash
vercel --prod
```

### Option 2: Deploy via Vercel Dashboard (GitHub Integration)

#### Step 1: Push to GitHub
```bash
cd c:\Users\bansa\Downloads\zomato
git init
git add .
git commit -m "Initial commit for Vercel deployment"
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

#### Step 2: Import to Vercel
1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click **"Add New..."** → **"Project"**
3. Import your GitHub repository
4. Configure project:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `next build`
   - **Output Directory**: `.next`

#### Step 3: Add Environment Variables
In Vercel Dashboard → Your Project → Settings → Environment Variables:
- Add `GROQ_API_KEY` with your Groq API key

#### Step 4: Deploy
Click **"Deploy"**

## 🔧 Project Structure for Vercel

```
zomato/
├── frontend/                 # Next.js app (deployed to Vercel)
│   ├── app/
│   │   └── api/              # Next.js API routes (serverless)
│   │       ├── localities/   # GET /api/localities
│   │       │   └── route.ts
│   │       └── recommend/    # POST /api/recommend
│   │           └── route.ts
│   ├── data/                 # Restaurant data (CSV)
│   ├── components/           # React components
│   ├── package.json
│   └── .env.example          # Environment variables template
├── vercel.json               # Vercel configuration
└── .env.example             # Environment variables template
```

## 📡 API Endpoints

After deployment, your API will be available at:
- `https://your-project.vercel.app/api/localities` (GET)
- `https://your-project.vercel.app/api/recommend` (POST)

## 🔐 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `NEXT_PUBLIC_API_URL` | API base URL (use `/api` for production) | Yes |
| `GROQ_API_KEY` | Groq API key for AI explanations | Yes |

## ⚙️ Configuration Files

### vercel.json
Configures builds and routes:
- Next.js frontend builds
- Python serverless functions for API
- Route mappings

### requirements.txt
No Python dependencies needed - all API routes use TypeScript/Node.js

## 🧪 Local Testing

### Test Frontend Locally
```bash
cd frontend
npm run dev
```
Visit: http://localhost:3000

### Test Python API Locally
Since we're using Next.js API routes (TypeScript), they run automatically with the dev server:
```bash
cd frontend
npm run dev
```
The API routes will be available at http://localhost:3000/api/*

## 🐛 Troubleshooting

### Build Fails
- Check that all dependencies are in `package.json`
- Ensure `requirements.txt` has all Python packages
- Check Vercel build logs in dashboard

### API Returns 500 Error
- Verify `GROQ_API_KEY` is set in Vercel environment variables
- Check that `data/clean_zomato_restaurants.csv` exists in the frontend directory
- Review function logs in Vercel dashboard
- Check browser console for error details

### Data File Not Found
Ensure the CSV file is in `frontend/data/`:
```bash
ls frontend/data/clean_zomato_restaurants.csv
```
If missing, copy it from the source:
```bash
cp src/phase1/data/processed/clean_zomato_restaurants.csv frontend/data/
```

### CORS Issues
Next.js API routes handle CORS automatically. If issues persist, add CORS headers to API responses.

## 📊 Post-Deployment

### Custom Domain
1. Go to Vercel Dashboard → Your Project → Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed

### Monitoring
- View real-time logs: `vercel logs`
- Check deployment status in dashboard
- Monitor function execution times

### Performance Optimization
- Enable Edge Functions for faster response times
- Add caching headers to API responses
- Optimize CSV data size

## 🔄 Continuous Deployment

When connected to GitHub, Vercel automatically deploys on every push to main branch.

### Preview Deployments
Every pull request gets a unique preview URL for testing.

### Production Deployments
Push to main branch or run:
```bash
vercel --prod
```

## 📝 Important Notes

1. **Serverless Function Limits**: 
   - Max execution time: 10 seconds (Hobby), 60 seconds (Pro)
   - Max memory: 1024 MB
   
2. **File Size Limits**:
   - Serverless function bundle: 50 MB
   - CSV data file should be optimized if large
   - Consider using a database for very large datasets

3. **Cold Starts**:
   - Node.js functions may have cold start delays
   - Consider keeping functions warm with periodic calls

4. **Environment Variables**:
   - Never commit `.env.local` to Git
   - Use Vercel dashboard for production env vars
   - Add `GROQ_API_KEY` in Vercel dashboard

## 🎯 Next Steps

1. Test the deployed application
2. Set up custom domain (optional)
3. Monitor performance and logs
4. Iterate based on user feedback

## 📞 Support

- [Vercel Documentation](https://vercel.com/docs)
- [Next.js Documentation](https://nextjs.org/docs)
- [Next.js API Routes](https://nextjs.org/docs/app/building-your-application/routing/route-handlers)

---

**Happy Deploying! 🚀**
