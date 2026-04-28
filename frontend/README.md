# Zomato AI - Next.js Frontend

A modern, beautiful frontend for the Zomato AI Restaurant Recommendation System built with Next.js, Tailwind CSS, and Framer Motion.

## 🌐 Live Deployment

- **Frontend**: deployed on Vercel (proxies `/api/recommend` to the backend)
- **Backend**: https://zomato-2-9s48.onrender.com (Flask + gunicorn on Render)

The frontend reads `BACKEND_URL` from the Vercel environment to forward requests; set it to the URL above. The backend is on Render's free tier and may cold-start (~30–60s) after periods of inactivity.

## ✨ Features

- **Modern UI/UX**: Clean, responsive design with Zomato's signature red branding
- **Smooth Animations**: Beautiful transitions and animations using Framer Motion
- **Real-time Recommendations**: Connects to your Flask backend API
- **Interactive Forms**: Intuitive preference selection with icons
- **Rich Restaurant Cards**: Detailed restaurant information with ratings, cuisine, and AI explanations
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Loading States**: Elegant loading indicators while fetching recommendations
- **Error Handling**: User-friendly error messages and feedback

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ installed
- Python backend running (Flask app from phase5)

### Installation

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure environment:**
   The `.env` file is already configured with:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```
   Make sure your Flask backend is running on port 8000.

3. **Start the Flask backend:**
   ```bash
   cd ..
   .venv\Scripts\activate  # On Windows
   python src/phase5/app.py
   ```

4. **Start the Next.js development server:**
   ```bash
   cd frontend
   npm run dev
   ```

5. **Open your browser:**
   Navigate to [http://localhost:3000](http://localhost:3000)

## 📁 Project Structure

```
frontend/
├── app/
│   ├── layout.tsx          # Root layout with metadata
│   ├── page.tsx            # Main page component
│   └── globals.css         # Global styles
├── components/
│   ├── Header.tsx          # App header with branding
│   ├── HeroSection.tsx     # Hero banner with thali image
│   ├── PreferenceForm.tsx  # User preference input form
│   └── RestaurantCard.tsx  # Restaurant recommendation cards
├── public/
│   └── thali.jpg           # Indian thali food image
└── .env                    # Environment variables
```

## 🎨 Design Highlights

### Color Scheme
- **Primary**: Red (#DC2626) - Zomato brand color
- **Secondary**: Orange accents
- **Background**: Clean whites and grays
- **Text**: Dark grays for readability

### Key Components

1. **Header**: Gradient red background with utensil icon
2. **Hero Section**: Showcases the Indian thali image with feature highlights
3. **Preference Form**: 
   - Location dropdown (auto-populated from backend)
   - Budget selector ($, $$, $$$)
   - Cuisine text input
   - Minimum rating (0-5)
   - Additional preferences
   - Number of results (1-10)

4. **Restaurant Cards**:
   - Color-coded ratings (green for 4.5+, yellow for 4.0+, orange for 3.0+)
   - Budget indicators
   - Location and address
   - AI-powered explanation of why each restaurant was recommended

## 🔧 Customization

### Adding More Features

1. **Add search filters**: Modify `PreferenceForm.tsx`
2. **Change colors**: Update Tailwind classes or modify `globals.css`
3. **Add new pages**: Create new files in `app/` directory
4. **Modify API calls**: Update fetch URLs in components

### Environment Variables

- `NEXT_PUBLIC_API_URL`: URL of your Flask backend (default: http://localhost:8000)

##  Enhancing the Frontend

Here are some ideas for future enhancements:

1. **Add restaurant images**: Fetch and display restaurant photos
2. **Map integration**: Show restaurant locations on a map
3. **User authentication**: Save user preferences
4. **Favorites**: Allow users to save favorite restaurants
5. **Dark mode**: Add a dark theme toggle
6. **Share feature**: Share recommendations via social media
7. **Reviews**: Display user reviews for restaurants
8. **Advanced filters**: Add more filtering options (ratings, distance, etc.)

## 🛠️ Tech Stack

- **Next.js 16**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Framer Motion**: Animation library
- **Lucide React**: Beautiful icon library
- **React Hooks**: State management

## 📱 Responsive Design

The frontend is fully responsive and works on:
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (320px - 767px)

## 🤝 Contributing

To enhance this frontend:
1. Make changes to the relevant component files
2. Test locally with `npm run dev`
3. Ensure the backend is running for API integration
4. Test responsiveness on different screen sizes

## 📝 Notes

- The frontend expects the backend to be running on port 8000
- CORS should be enabled in the Flask app for cross-origin requests
- The thali image is displayed in the hero section (from your screenshot)
- All animations use Framer Motion for smooth transitions

## 🐛 Troubleshooting

**Issue**: Can't fetch recommendations
- **Solution**: Make sure the Flask backend is running on port 8000

**Issue**: Localities not loading
- **Solution**: Check if the CSV file exists at `src/phase1/data/processed/clean_zomato_restaurants.csv`

**Issue**: Build errors
- **Solution**: Run `npm install` to ensure all dependencies are installed

## 📄 License

Part of the Zomato AI Restaurant Recommendation System project.
