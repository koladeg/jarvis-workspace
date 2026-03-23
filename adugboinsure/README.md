# AdugboInsure - Community Health Insurance Platform

A modern, responsive website for AdugboInsure, a community-based health insurance platform serving Nigerian families with affordable, reliable health coverage starting at ₦15,000/year.

## ✨ Features

- **🏥 Multi-page Platform**: Home, Coverage, Enrollment, FAQ, About, Contact
- **📱 Mobile-First Design**: Optimized for diverse device access in the Nigerian market
- **💳 Enrollment System**: Simple, fast sign-up forms with plan selection
- **📊 Coverage Details**: Interactive plan comparison and detailed coverage information
- **⚡ Fast & Responsive**: Next.js 15 with React and Tailwind CSS for blazing-fast performance
- **♿ Accessible**: WCAG-compliant UI with semantic HTML
- **🎨 Professional Design**: Warm, trustworthy color scheme suitable for health/insurance space
- **🌍 Vercel-Ready**: Deploy instantly with zero configuration

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm

### Installation

```bash
# Clone the repository
cd adugboinsure

# Install dependencies
npm install

# Start development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the app.

## 📦 Build for Production

```bash
# Build the project
npm run build

# Start production server
npm start
```

## 🌐 Deploy to Vercel

### Option 1: Direct Vercel CLI
```bash
npm install -g vercel
vercel
```

### Option 2: GitHub Integration
1. Push this repository to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Create a new project and connect your GitHub repo
4. Vercel will auto-detect Next.js and deploy

### Option 3: Vercel Dashboard
1. Visit [vercel.com/new](https://vercel.com/new)
2. Select "Next.js" template
3. Clone this repository URL
4. Deploy

## 📁 Project Structure

```
adugboinsure/
├── app/                      # Next.js app directory
│   ├── page.tsx             # Home page
│   ├── layout.tsx           # Root layout
│   ├── globals.css          # Global styles
│   ├── coverage/            # Coverage details page
│   ├── enrollment/          # Enrollment form page
│   ├── faq/                 # FAQ page
│   ├── about/               # About page
│   └── contact/             # Contact page
├── components/              # Reusable React components
│   ├── Navigation.tsx       # Header/navigation
│   ├── Hero.tsx             # Hero section
│   ├── CoverageHighlights.tsx
│   ├── CoverageDetail.tsx
│   ├── EnrollmentForm.tsx
│   ├── FAQSection.tsx
│   ├── AboutSection.tsx
│   ├── ContactSection.tsx
│   ├── CTASection.tsx
│   ├── WhyChooseUs.tsx
│   └── Footer.tsx
├── public/                  # Static assets (logos, icons)
├── package.json             # Dependencies and scripts
├── tsconfig.json            # TypeScript configuration
├── next.config.ts           # Next.js configuration
├── tailwind.config.ts       # Tailwind CSS configuration
├── postcss.config.mjs       # PostCSS configuration
└── vercel.json             # Vercel deployment config
```

## 🎨 Design & Colors

### Color Palette
- **Primary**: Sky Blue (#0284c7) - Professional, trustworthy
- **Secondary**: Emerald Green (#10b981) - Health, wellness
- **Accent**: Amber (#f59e0b) - Action, emphasis
- **Neutral**: Gray scale (50-900) - Text, backgrounds

### Responsive Breakpoints
- Mobile: 0px - 640px
- Tablet: 641px - 1024px
- Desktop: 1025px+

## 📄 Pages Overview

### Home (`/`)
- Hero section with key value proposition (₦15,000/year)
- Coverage highlights (6 main categories)
- Why choose us (stats & benefits)
- Call-to-action for enrollment

### Coverage (`/coverage`)
- Interactive plan selector (Individual, Family, Premium Family)
- Detailed plan comparison table
- Complete feature breakdowns
- CTA buttons linking to enrollment

### Enrollment (`/enrollment`)
- Form with fields: name, email, phone, plan selection
- Plan-dependent family member fields
- Terms & conditions acceptance
- Success confirmation screen

### FAQ (`/faq`)
- Expandable accordion with 10 common questions
- Topics: coverage, costs, claims, enrollment, policies
- Quick contact CTA
- Mobile-friendly interaction

### About (`/about`)
- Mission statement
- Core values (Compassion, Integrity, Innovation)
- Impact statistics
- Leadership team (with placeholders)
- Community commitment details

### Contact (`/contact`)
- Contact form (name, email, subject, message)
- Direct contact methods: phone, email, address
- Support hours & response times
- Interactive form submission

## 🔧 Customization

### Update Branding
Edit these files to personalize:
- `tailwind.config.ts` - Colors and theme
- `app/layout.tsx` - Site title and metadata
- `components/Navigation.tsx` - Logo and nav links
- `components/Footer.tsx` - Company info

### Add Content
- Pages are in `app/[page]/page.tsx`
- Components are in `components/`
- Styling uses Tailwind utility classes

### Environment Variables
Create a `.env.local` file for any backend integrations:
```
NEXT_PUBLIC_API_URL=https://api.example.com
```

## 📱 Responsive Design

All pages are tested and optimized for:
- Mobile (320px - 640px)
- Tablet (641px - 1024px)
- Desktop (1025px+)

Uses mobile-first approach with breakpoints:
- `sm:` for 640px+
- `md:` for 1024px+
- `lg:` for 1280px+

## ⚙️ Scripts

```bash
npm run dev      # Start development server
npm run build    # Build for production
npm start        # Start production server
npm run lint     # Run ESLint
```

## 🔐 Security & Performance

- ✅ TypeScript for type safety
- ✅ Next.js built-in optimizations (Image, Font, etc.)
- ✅ Semantic HTML for accessibility
- ✅ No external scripts in core flow
- ✅ Mobile-first performance

## 📊 SEO

- Proper meta tags and title on each page
- Semantic HTML structure
- Mobile-responsive design
- Fast Core Web Vitals (Next.js optimized)
- Schema markup ready (can be added)

## 🚢 Deployment Checklist

- [ ] Update company info in `Footer.tsx`
- [ ] Set proper phone numbers and emails
- [ ] Customize colors in `tailwind.config.ts`
- [ ] Add real team photos in About section
- [ ] Connect enrollment form to backend
- [ ] Set up analytics (Google Analytics, etc.)
- [ ] Configure email service for contact forms
- [ ] Test on mobile devices
- [ ] Test on various browsers
- [ ] Set up SSL/HTTPS (Vercel handles this)

## 🤝 Integration Notes

The forms (enrollment, contact) currently log to console. To make them functional:

### Backend Integration
1. Add API endpoint for form submissions
2. Update form `onSubmit` handlers in components
3. Connect to email service (SendGrid, Mailgun, etc.)
4. Set up database for member data

### Example (Enrollment Form):
```typescript
const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();
  const response = await fetch('/api/enroll', {
    method: 'POST',
    body: JSON.stringify(formData),
  });
  // Handle response
};
```

## 📞 Support & Next Steps

- **Design Improvements**: Add testimonials, case studies
- **Features**: Member dashboard, claims tracking, payment gateway
- **Content**: Blog, resources, health tips
- **Integrations**: Payment processors, SMS notifications, mobile app

## 📄 License

All code and design assets are proprietary to AdugboInsure.

---

**Ready to launch?** Deploy to Vercel with one click:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/adugboinsure)

---

Built with ❤️ for Nigerian communities
