# Frontend - Next.js Weather App

## Quick Start

1. Install dependencies:
```bash
npm install
```

2. Setup environment:
```bash
# .env.local is already created
# Verify NEXT_PUBLIC_API_URL points to your backend
```

3. Run development server:
```bash
npm run dev
```

4. Open `http://localhost:3000`

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx        # Root layout
│   ├── page.tsx          # Home page
│   ├── page.module.css   # Page styles
│   └── globals.css       # Global styles
├── components/           # React components
│   ├── WeatherCard.tsx
│   ├── DailyForecast.tsx
│   └── LocationSearch.tsx
├── lib/                  # Utilities
│   ├── api.ts           # API client
│   └── utils.ts         # Helper functions
├── types/               # TypeScript types
│   └── weather.ts
└── public/              # Static assets
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint

## Styling

This project uses **CSS Modules** instead of Tailwind CSS for:
- More control over styles
- Better performance
- Easier customization
- Modern CSS features (variables, grid, flexbox)

## Features

- ✅ Server-side rendering with Next.js App Router
- ✅ TypeScript for type safety
- ✅ CSS Modules for scoped styling
- ✅ Responsive design
- ✅ Dark/Light theme
- ✅ Geolocation support
- ✅ Favorite locations
- ✅ Real-time weather data

## Deployment

Deploy to Vercel with one click or follow the deployment guide in the main README.
