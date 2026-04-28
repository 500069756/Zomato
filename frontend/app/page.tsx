'use client';

import { useState } from 'react';
import Header from '@/components/Header';
import HeroSection from '@/components/HeroSection';
import PreferenceForm from '@/components/PreferenceForm';
import RestaurantCard from '@/components/RestaurantCard';
import { AlertCircle, CheckCircle, Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';

interface Preferences {
  location: string;
  budget: string;
  cuisine: string;
  minimum_rating: string;
  additional_preferences: string;
  top_n: string;
}

interface Restaurant {
  restaurant_name: string;
  cuisine: string;
  location: string;
  rating: number;
  budget_label: string;
  explanation: string;
  address?: string;
}

export default function Home() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [summary, setSummary] = useState<string | null>(null);
  const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async (preferences: Preferences) => {
    setIsLoading(true);
    setError(null);
    setSuccess(null);
    setSummary(null);
    setRestaurants([]);
    setHasSearched(true);

    try {
      const response = await fetch('/api/recommend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...preferences,
          minimum_rating: parseFloat(preferences.minimum_rating),
          top_n: parseInt(preferences.top_n),
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || data.fallback_message || 'Unable to fetch recommendations.');
        return;
      }

      if (!data.success) {
        setError(data.fallback_message || 'No matching restaurants found.');
        return;
      }

      setSuccess(data.warning ? `Warning: ${data.warning}` : 'Recommendations loaded successfully!');
      setSummary(data.summary);
      setRestaurants(data.recommendations || []);
    } catch (err) {
      setError('Unable to reach the recommendation service. Please make sure the backend is running.');
      console.error('Fetch error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100">
      <Header />
      <HeroSection />

      <main className="max-w-6xl mx-auto px-6 py-12 space-y-12">
        {/* Form Section */}
        <section>
          <PreferenceForm onSearch={handleSearch} isLoading={isLoading} />
        </section>

        {/* Results Section */}
        {hasSearched && (
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="space-y-8"
          >
            {/* Status Messages */}
            {error && (
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="bg-red-50 border-l-4 border-red-500 p-6 rounded-r-xl shadow-md flex items-start gap-4"
              >
                <AlertCircle className="w-6 h-6 text-red-500 flex-shrink-0 mt-1" />
                <div>
                  <h3 className="font-bold text-red-800 text-lg">Error</h3>
                  <p className="text-red-700 mt-1">{error}</p>
                </div>
              </motion.div>
            )}

            {success && (
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="bg-green-50 border-l-4 border-green-500 p-6 rounded-r-xl shadow-md flex items-start gap-4"
              >
                <CheckCircle className="w-6 h-6 text-green-500 flex-shrink-0 mt-1" />
                <div>
                  <h3 className="font-bold text-green-800 text-lg">Success</h3>
                  <p className="text-green-700 mt-1">{success}</p>
                </div>
              </motion.div>
            )}

            {/* Summary */}
            {summary && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100"
              >
                <h3 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-3">
                  <span className="text-3xl">📊</span>
                  Summary
                </h3>
                <p className="text-gray-700 leading-relaxed text-lg">{summary}</p>
              </motion.div>
            )}

            {/* Restaurant Cards */}
            {restaurants.length > 0 && (
              <div>
                <h3 className="text-3xl font-bold text-gray-800 mb-6 flex items-center gap-3">
                  <span className="text-4xl">🍽️</span>
                  Recommended Restaurants
                  <span className="text-lg font-normal text-gray-500">
                    ({restaurants.length} found)
                  </span>
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {restaurants.map((restaurant, index) => (
                    <RestaurantCard
                      key={index}
                      restaurant={restaurant}
                      index={index}
                    />
                  ))}
                </div>
              </div>
            )}

            {/* Loading State */}
            {isLoading && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="flex flex-col items-center justify-center py-16 space-y-4"
              >
                <Loader2 className="w-16 h-16 text-red-600 animate-spin" />
                <p className="text-xl font-semibold text-gray-700">
                  Finding the perfect restaurants for you...
                </p>
                <p className="text-gray-500">
                  Our AI is analyzing thousands of options
                </p>
              </motion.div>
            )}

            {/* No Results */}
            {!isLoading && hasSearched && restaurants.length === 0 && !error && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="text-center py-16 space-y-4"
              >
                <div className="text-6xl">🔍</div>
                <h3 className="text-2xl font-bold text-gray-800">No Restaurants Found</h3>
                <p className="text-gray-600 text-lg">
                  Try adjusting your preferences to get more results
                </p>
              </motion.div>
            )}
          </motion.section>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12 mt-20">
        <div className="max-w-6xl mx-auto px-6 text-center">
          <div className="flex items-center justify-center gap-3 mb-4">
            <span className="text-3xl">🍽️</span>
            <h3 className="text-2xl font-bold">Zomato AI</h3>
          </div>
          <p className="text-gray-400">
            Powered by AI • Making dining decisions easier
          </p>
          <p className="text-gray-500 text-sm mt-4">
            © 2026 Zomato AI Restaurant Recommendations
          </p>
        </div>
      </footer>
    </div>
  );
}
