# Deploy Flask Backend to Render.com

## Steps:

1. **Go to** https://render.com
2. **Sign up/Login** with GitHub
3. **Click "New +"** → **"Web Service"**
4. **Connect your repository**: `https://github.com/500069756/Zomato`
5. **Configure**:
   - **Name**: `zomato-ai-backend`
   - **Region**: Choose nearest to your users
   - **Branch**: `main`
   - **Root Directory**: Leave blank (root)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn src.phase5.app:app`
   - **Instance Type**: Free

6. **Add Environment Variables**:
   - `GROQ_API_KEY`: Your Groq API key
   - `FLASK_DEBUG`: `false`

7. **Click "Create Web Service"**

## Access Your API:
- URL: `https://zomato-ai-backend.onrender.com`
- Endpoints:
  - `GET /api/health`
  - `GET /api/localities`
  - `POST /api/recommend`

## Update Frontend:
After deployment, update your frontend `.env`:
```
NEXT_PUBLIC_API_URL=https://zomato-ai-backend.onrender.com
```
