# AdugboInsure - Quick Start Guide

Get the AdugboInsure website running in minutes.

## 🎯 5-Minute Setup

### Prerequisites
- Node.js 18+ ([Download](https://nodejs.org))
- npm (comes with Node.js)
- A code editor (VS Code recommended)

### 1. Install Dependencies (2 min)

```bash
cd adugboinsure
npm install
```

### 2. Run Development Server (1 min)

```bash
npm run dev
```

Output:
```
   ▲ Next.js 15.5.14
   - Local:        http://localhost:3000
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### 3. Explore the Site (2 min)

- **Home** `/` - Hero section & value prop
- **Coverage** `/coverage` - Plans & details
- **Enrollment** `/enrollment` - Sign-up form
- **FAQ** `/faq` - Common questions
- **About** `/about` - Company info
- **Contact** `/contact` - Support info

## 🛠️ Customize Your Content

### Update Company Info

**File:** `components/Footer.tsx`
```typescript
<span>💚</span>
<span>AdugboInsure</span>
```

Change the emoji and company name.

### Update Colors

**File:** `tailwind.config.ts`
```javascript
colors: {
  primary: {
    600: "#0284c7",  // Change this
  },
  secondary: {
    500: "#10b981",  // And this
  },
}
```

### Update Hero Section

**File:** `components/Hero.tsx`
```typescript
<h1 className="text-4xl sm:text-5xl md:text-6xl font-bold text-neutral-900 leading-tight mb-6">
  Health Insurance{" "}
  <span className="text-primary-600">Made Simple</span>
</h1>
```

### Update Phone/Email

**File:** `components/Footer.tsx`
```typescript
<a href="tel:0800-INSURE-1" className="hover:text-secondary-400">
  📞 0800-INSURE-1
</a>
```

Change to your actual contact details.

## 🚀 Deploy to Production

### Option 1: Vercel (1 click - Recommended)

1. Push to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. Go to [vercel.com/new](https://vercel.com/new)

3. Click "Import Git Repository"

4. Select your GitHub repo

5. Click "Deploy"

Done! ✅ Your site is live.

### Option 2: Vercel CLI

```bash
npm install -g vercel
vercel login
vercel --prod
```

Follow the prompts.

### Option 3: Netlify

1. Connect GitHub repo
2. Set build command: `npm run build`
3. Set publish directory: `.next`
4. Deploy

## 📖 Project Structure

```
adugboinsure/
├── app/
│   ├── page.tsx          ← Home page
│   ├── layout.tsx        ← Layout for all pages
│   ├── globals.css       ← Global styles
│   ├── coverage/
│   ├── enrollment/
│   ├── faq/
│   ├── about/
│   └── contact/
├── components/           ← Reusable components
│   ├── Hero.tsx
│   ├── CoverageHighlights.tsx
│   ├── Navigation.tsx
│   └── Footer.tsx
├── public/              ← Images, icons, etc.
├── package.json
└── README.md
```

## 🎨 Common Customizations

### Change the Logo

Add your logo to `public/logo.png`, then update `components/Navigation.tsx`:

```typescript
<img src="/logo.png" alt="Logo" width={40} height={40} />
```

### Add a New Page

Create `app/newpage/page.tsx`:

```typescript
export const metadata = {
  title: "New Page - AdugboInsure",
  description: "Description here",
};

export default function NewPage() {
  return (
    <section className="py-16 sm:py-24">
      <div className="section-container">
        <h1 className="section-title">Welcome!</h1>
      </div>
    </section>
  );
}
```

It automatically routes to `/newpage`.

### Connect a Form to Email

Update `components/EnrollmentForm.tsx`:

```typescript
const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();
  
  // Send to your backend
  const response = await fetch('/api/enroll', {
    method: 'POST',
    body: JSON.stringify(formData),
  });
  
  if (response.ok) {
    setSubmitted(true);
  }
};
```

## 🧪 Testing

### Mobile Responsive

Right-click → "Inspect" → Device emulation (Ctrl+Shift+M)

Test breakpoints:
- 320px (mobile)
- 768px (tablet)
- 1024px (desktop)

### Browser Testing

- Chrome
- Safari
- Firefox
- Edge

### Performance

```bash
npm run build
```

Check output for bundle size. Good if under 150KB (JS).

## 📚 Useful Commands

```bash
npm run dev       # Development server
npm run build     # Production build
npm start         # Run production build locally
npm run lint      # Check code quality
npm install       # Install dependencies
npm update        # Update packages
```

## 🐛 Troubleshooting

**Port 3000 already in use:**
```bash
npm run dev -- -p 3001
```

**Build errors:**
```bash
rm -rf .next
npm run build
```

**Clear cache:**
```bash
npm cache clean --force
rm -rf node_modules
npm install
npm run build
```

## 📦 Next Steps

1. ✅ Customize content
2. ✅ Test locally
3. ✅ Deploy to Vercel
4. ✅ Set up custom domain
5. ✅ Connect email service
6. ✅ Add Google Analytics
7. ✅ Submit to search engines

## 📚 Learn More

- [Next.js Docs](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com)
- [React](https://react.dev)
- [Vercel Docs](https://vercel.com/docs)

## ✨ Pro Tips

- Use `<Link>` from `next/link` for internal navigation (faster)
- Tailwind utilities: `sm:`, `md:`, `lg:` for responsive design
- Use emoji for icons (saves requests)
- Keep color scheme consistent
- Test on mobile before deploying

## 🎉 You're Ready!

Your AdugboInsure website is ready to launch.

```bash
npm run dev
```

Happy building! 🚀

---

**Questions?** Check README.md or DEPLOYMENT.md for more details.
