# 🚀 Vercel Deployment Guide for DealFlowAI

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Your code should be on GitHub
3. **Vercel CLI** (optional): `npm i -g vercel`

## Environment Variables

Set these environment variables in your Vercel dashboard:

```env
DEBUG=False
SECRET_KEY=your-production-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,.vercel.app,.now.sh
DATABASE_URL=sqlite:///db.sqlite3
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,https://*.vercel.app,https://*.now.sh
ML_MODEL_PATH=ml_models
EMBEDDING_MODEL=all-MiniLM-L6-v2
VECTOR_DIMENSION=384
```

## Deployment Steps

### Option 1: Vercel Dashboard (Recommended)

1. **Connect Repository**
   - Go to [vercel.com/dashboard](https://vercel.com/dashboard)
   - Click "New Project"
   - Import your GitHub repository: `TanmaySingh007/DealFlowAI`

2. **Configure Project**
   - **Framework Preset**: Other
   - **Root Directory**: `./` (leave empty)
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Output Directory**: `staticfiles`
   - **Install Command**: `pip install -r requirements.txt`

3. **Environment Variables**
   - Add all environment variables listed above
   - Set `SECRET_KEY` to a secure random string

4. **Deploy**
   - Click "Deploy"
   - Wait for build to complete

### Option 2: Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   vercel
   ```

4. **Follow prompts**
   - Link to existing project or create new
   - Set environment variables
   - Deploy

## Important Notes

### Database Limitations
- Vercel uses serverless functions
- SQLite database is read-only in production
- Consider using external database for full functionality

### Static Files
- Static files are served via WhiteNoise
- Files are collected during build
- No file uploads in production

### ML Models
- Large ML models may cause timeout
- Consider using external ML services
- Models are downloaded during build

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Check Python version (3.9)
   - Verify all dependencies in requirements.txt
   - Check environment variables

2. **Import Errors**
   - Ensure all packages are in requirements.txt
   - Check PYTHONPATH setting

3. **Static Files Not Loading**
   - Verify STATIC_ROOT setting
   - Check WhiteNoise configuration
   - Ensure collectstatic runs during build

4. **Database Errors**
   - SQLite is read-only on Vercel
   - Use external database for write operations
   - Consider using Vercel Postgres

### Performance Optimization

1. **Reduce Bundle Size**
   - Remove unused dependencies
   - Use lighter ML models
   - Optimize static files

2. **Caching**
   - Enable Vercel caching
   - Use CDN for static files
   - Implement API caching

3. **Monitoring**
   - Use Vercel Analytics
   - Monitor function execution time
   - Check error logs

## Production Checklist

- [ ] Environment variables set
- [ ] DEBUG=False
- [ ] Secure SECRET_KEY
- [ ] Static files collected
- [ ] Database migrations applied
- [ ] CORS settings configured
- [ ] Security headers enabled
- [ ] Error logging configured
- [ ] Performance monitoring enabled

## Support

For issues with Vercel deployment:
- Check Vercel documentation
- Review build logs
- Contact Vercel support
- Check GitHub issues

---

**DealFlowAI on Vercel** - AI-Powered Investment Analysis Platform 