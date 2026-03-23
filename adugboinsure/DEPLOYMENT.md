# AdugboInsure Deployment Guide

Complete instructions for deploying the AdugboInsure website to production.

## ✅ Pre-Deployment Checklist

- [ ] All pages tested locally (`npm run dev`)
- [ ] Build passes without errors (`npm run build`)
- [ ] Content reviewed and updated
- [ ] Contact information verified
- [ ] Social links updated
- [ ] Analytics tracking code ready
- [ ] Email service configured
- [ ] Domain registered or ready

## 🚀 Deploy to Vercel (Recommended)

Vercel is the easiest way to deploy Next.js apps. It offers:
- **Zero configuration** deployment
- **Automatic SSL/HTTPS**
- **Global CDN** for fast loading worldwide
- **Preview deployments** for PRs
- **Environment variables** management
- **Analytics & monitoring**

### Option 1: GitHub Integration (Best)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial AdugboInsure website"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/adugboinsure.git
   git push -u origin main
   ```

2. **Connect to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Click "Import Git Repository"
   - Paste your GitHub repo URL
   - Click "Import"

3. **Configure & Deploy**
   - Framework: Next.js (auto-detected)
   - Build Command: `npm run build`
   - Output Directory: `.next`
   - Click "Deploy"

4. **Custom Domain**
   - In Vercel dashboard → Project Settings → Domains
   - Add your domain (e.g., adugboinsure.com)
   - Follow DNS configuration instructions

### Option 2: Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   vercel
   ```

4. **Production Deployment**
   ```bash
   vercel --prod
   ```

### Option 3: Direct GitHub Connection

1. Go to [vercel.com/new](https://vercel.com/new)
2. Select "Next.js" template
3. Enter your GitHub repo URL
4. Follow the wizard

## 🌐 Alternative Hosting Options

### Netlify

1. Push to GitHub
2. Go to [netlify.com](https://netlify.com)
3. Click "Add new site" → "Import an existing project"
4. Choose GitHub, select repo
5. Build settings (auto-detected):
   - Build command: `npm run build`
   - Publish directory: `.next`
6. Deploy

### AWS Amplify

1. Create AWS account
2. Install AWS CLI
3. Configure credentials: `aws configure`
4. Deploy:
   ```bash
   npm install -g @aws-amplify/cli
   amplify init
   amplify publish
   ```

### DigitalOcean App Platform

1. Push to GitHub
2. Create App on [DigitalOcean](https://cloud.digitalocean.com)
3. Connect GitHub repo
4. Auto-detects Next.js
5. Deploy

## 📦 Production Build & Testing

### Local Production Build

```bash
# Build
npm run build

# Test production build locally
npm start
```

Open http://localhost:3000 in your browser to test.

### Build Analysis

Check bundle size:
```bash
npm install --save-dev @next/bundle-analyzer
```

Update `next.config.ts`:
```typescript
import bundleAnalyzer from "@next/bundle-analyzer";

const withBundleAnalyzer = bundleAnalyzer({
  enabled: process.env.ANALYZE === "true",
});

export default withBundleAnalyzer({
  // ... your next config
});
```

Run analysis:
```bash
ANALYZE=true npm run build
```

## 🔧 Environment Variables

Create `.env.production.local` for production-only variables:

```env
NEXT_PUBLIC_API_URL=https://api.adugboinsure.com
NEXT_PUBLIC_GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX
CONTACT_EMAIL_SERVICE_API_KEY=your_api_key_here
```

Set these in Vercel:
1. Project Settings → Environment Variables
2. Add each variable
3. Select which environments (Preview, Production)
4. Redeploy

## 📊 Performance Optimization

### Image Optimization

Already using Next.js Image component. Make sure all images:
- Are optimized PNG/JPG
- Use proper aspect ratios
- Include alt text for accessibility

### Code Splitting

Next.js automatically code-splits pages. Verify:
```bash
npm run build
```

Look for separate chunks for each page in build output.

### Caching Headers

Set in `vercel.json`:
```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=3600, stale-while-revalidate=86400"
        }
      ]
    }
  ]
}
```

## 🔐 Security Best Practices

1. **HTTPS Only** - Vercel auto-enables
2. **Security Headers** - Already set in Tailwind/Next.js
3. **Content Security Policy** - Add to headers
4. **Rate Limiting** - Configure in backend API
5. **Input Validation** - Always validate on backend
6. **Secrets Management** - Use environment variables

## 📈 Analytics & Monitoring

### Google Analytics

1. Create Google Analytics 4 property
2. Get measurement ID (starts with `G-`)
3. Add to `.env.local`:
   ```env
   NEXT_PUBLIC_GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX
   ```

4. Install gtag:
   ```bash
   npm install @next/third-parties
   ```

5. Update `app/layout.tsx`:
   ```typescript
   import { GoogleAnalytics } from '@next/third-parties/google'
   
   export default function RootLayout() {
     return (
       <html>
         <body>
           {/* ... */}
           <GoogleAnalytics gaId={process.env.NEXT_PUBLIC_GOOGLE_ANALYTICS_ID} />
         </body>
       </html>
     )
   }
   ```

### Vercel Analytics

Built-in! View in Vercel dashboard:
- Page views
- Real User Monitoring (RUM)
- Core Web Vitals
- Performance metrics

## 🐛 Monitoring & Errors

### Sentry Integration (Error Tracking)

1. Create Sentry account
2. Create Next.js project
3. Install:
   ```bash
   npm install @sentry/nextjs
   ```

4. Initialize (follow Sentry wizard)

## 🔄 Continuous Deployment

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Vercel

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm run build
      - uses: vercel/action@v4
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
```

## 📱 Mobile Testing

Test on:
- iPhone (Safari)
- Android (Chrome)
- Tablet devices
- Desktop (various browsers)

Use Chrome DevTools for device emulation.

## 🎯 Form Backend Integration

Current forms log to console. To make them functional:

### Option 1: Serverless Functions (Vercel)

Create `app/api/enroll/route.ts`:

```typescript
import { NextRequest, NextResponse } from 'next/server';
import nodemailer from 'nodemailer';

export async function POST(request: NextRequest) {
  try {
    const data = await request.json();
    
    // Validate data
    if (!data.email || !data.fullName) {
      return NextResponse.json(
        { error: 'Missing required fields' },
        { status: 400 }
      );
    }
    
    // Send email
    const transporter = nodemailer.createTransport({
      // Configure your email service
    });
    
    await transporter.sendMail({
      from: 'noreply@adugboinsure.com',
      to: data.email,
      subject: 'Welcome to AdugboInsure!',
      html: `<p>Thank you for enrolling, ${data.fullName}!</p>`
    });
    
    // Save to database
    // await saveToDatabase(data);
    
    return NextResponse.json({ success: true });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to process enrollment' },
      { status: 500 }
    );
  }
}
```

### Option 2: External Service (SendGrid, Mailgun)

Use their APIs directly from your serverless function.

### Option 3: Backend API

Call your existing backend API from the Vercel function.

## 📋 Post-Deployment

- [ ] Test all forms on production
- [ ] Verify mobile responsiveness
- [ ] Check Core Web Vitals
- [ ] Test contact forms
- [ ] Verify email notifications
- [ ] Check analytics tracking
- [ ] Test 404 page
- [ ] Verify sitemap.xml
- [ ] Submit to Google Search Console
- [ ] Submit to Bing Webmaster Tools

## 🚨 Troubleshooting

### Build Fails on Vercel

1. Check build logs in Vercel dashboard
2. Ensure `package-lock.json` is committed
3. Check Node.js version compatibility
4. Verify environment variables

### Slow Performance

1. Check bundle size: `ANALYZE=true npm run build`
2. Optimize images
3. Enable gzip compression
4. Use Vercel Analytics to identify bottlenecks

### Deployment Stuck

1. Cancel current deployment
2. Push new commit to trigger rebuild
3. Check network connectivity
4. Verify GitHub token permissions

## 📞 Support

- **Vercel Support**: support@vercel.com
- **Next.js Docs**: https://nextjs.org/docs
- **Deploy Button**: [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/YOUR_USERNAME/adugboinsure)

---

**Ready to go live?** Deploy now and watch your site reach the world! 🌍
