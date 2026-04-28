# Quick Start Guide - Zomato AI with Next.js Frontend

## 🎯 Overview

You now have a modern Next.js frontend for your Zomato AI Restaurant Recommendation System! The frontend features:

- ✨ Beautiful Zomato-themed UI with red branding
- 🍽️ Indian thali image in the hero section (from your screenshot)
- 🎨 Smooth animations with Framer Motion
- 📱 Fully responsive design
- ⚡ Real-time API integration with your Flask backend

## 🚀 How to Run

### Step 1: Start the Flask Backend

Open a **new terminal** and run:

```powershell
cd c:\Users\bansa\Downloads\zomato
.venv\Scripts\activate
python src/phase5/app.py
```

The backend will start on **http://localhost:8000**

### Step 2: Start the Next.js Frontend

The frontend is already running! If you need to restart it:

```powershell
cd c:\Users\bansa\Downloads\zomato\frontend
npm run dev
```

The frontend runs on **http://localhost:3000**

### Step 3: Open Your Browser

Click the preview button in your IDE or navigate to:
**http://localhost:3000**

## 📋 What's Been Created

### New Files & Folders

```
frontend/                           # Next.js application
├── app/
│   ├── layout.tsx                  # Root layout
│   ├── page.tsx                    # Main page with all components
│   └── globals.css                 # Global styles with custom scrollbar
├── components/
│   ├── Header.tsx                  # Red gradient header
│   ├── HeroSection.tsx             # Hero with thali image
│   ├── PreferenceForm.tsx          # Interactive form
│   └── RestaurantCard.tsx          # Beautiful restaurant cards
├── public/
│   └── thali.jpg                   # Your Indian thali image
├── .env                            # API configuration
└── README.md                       # Detailed documentation
```

### Modified Files

- `src/phase5/app.py` - Added CORS support for cross-origin requests
- `requirements.txt` - Added flask-cors dependency

## 🎨 Features

### 1. Modern Header
- Gradient red background (Zomato branding)
- Utensil icon
- Clear title and description

### 2. Hero Section
- Beautiful gradient background
- Indian thali image from your screenshot
- Feature highlights (1000+ Restaurants, AI-Powered, Personalized)

### 3. Interactive Preference Form
- **Location**: Dropdown populated from backend
- **Budget**: Low ($), Medium ($$), High ($$$)
- **Cuisine**: Text input (e.g., Chinese, Italian, Indian)
- **Minimum Rating**: Number input (0-5)
- **Additional Preferences**: Text input
- **Number of Results**: 1-10

### 4. Beautiful Restaurant Cards
- Color-coded ratings:
  - 🟢 Green: 4.5+ stars
  - 🟡 Yellow: 4.0-4.4 stars
  - 🟠 Orange: 3.0-3.9 stars
  - 🔴 Red: Below 3.0
- Budget indicators ($, $$, $$$)
- Location and address
- AI-powered explanation box

### 5. Status Messages
- Success messages (green)
- Error messages (red)
- Loading animations
- Empty state handling

## 🔧 Key Technologies

- **Next.js 16** - React framework with App Router
- **TypeScript** - Type-safe code
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Smooth animations
- **Lucide React** - Beautiful icons

## 📝 API Configuration

The frontend connects to your backend at:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

API Endpoints used:
- `GET /api/localities` - Fetch available locations
- `POST /api/recommend` - Get restaurant recommendations

## 🎯 Usage Flow

1. User opens http://localhost:3000
2. Sees beautiful hero section with thali image
3. Fills out preference form
4. Clicks "Get AI Recommendations"
5. Frontend calls Flask backend API
6. Backend returns recommendations with AI explanations
7. Frontend displays beautiful animated cards

## ️ Customization Tips

### Change Colors
Edit Tailwind classes in components or add custom colors in `globals.css`

### Add Features
- New form fields: Edit `PreferenceForm.tsx`
- New card elements: Edit `RestaurantCard.tsx`
- New pages: Create files in `app/` directory

### Modify API Calls
Update fetch URLs in:
- `components/PreferenceForm.tsx` (line 35)
- `app/page.tsx` (line 47)

## 🐛 Troubleshooting

### Backend Not Responding
```powershell
# Check if backend is running
curl http://localhost:8000/api/health

# Start backend if not running
python src/phase5/app.py
```

### Frontend Not Loading Localities
1. Check if backend is running
2. Verify CSV exists at: `src/phase1/data/processed/clean_zomato_restaurants.csv`
3. Check browser console for errors

### CORS Errors
- flask-cors is installed and configured
- Restart the backend after CORS changes

### Build Errors
```powershell
cd frontend
npm install
npm run dev
```

## 📱 Responsive Breakpoints

- **Desktop**: 1200px+
- **Tablet**: 768px - 1199px
- **Mobile**: 320px - 767px

##  Next Steps

To enhance the frontend further:

1. **Add Restaurant Images**: Fetch and display photos
2. **Map Integration**: Show locations on Google Maps
3. **User Authentication**: Save preferences
4. **Favorites**: Bookmark restaurants
5. **Dark Mode**: Toggle between light/dark themes
6. **Social Sharing**: Share recommendations
7. **Reviews**: Display user reviews
8. **Advanced Filters**: Distance, open hours, etc.

## 💡 Tips

- The frontend auto-reloads when you edit files
- Check browser DevTools (F12) for debugging
- Use React DevTools extension for component inspection
- Test on different screen sizes using browser DevTools

## 📞 Support

If you need help:
1. Check the detailed README in `frontend/README.md`
2. Look at component files for inline documentation
3. Check browser console for errors
4. Verify backend is running on port 8000

---

**Enjoy your modern Zomato AI frontend! 🎉**
