'use client';

import { useState, useEffect } from 'react';
import { MapPin, DollarSign, UtensilsCrossed, Star, SlidersHorizontal, List } from 'lucide-react';

interface PreferenceFormProps {
  onSearch: (preferences: Preferences) => void;
  isLoading: boolean;
}

interface Preferences {
  location: string;
  budget: string;
  cuisine: string;
  minimum_rating: string;
  additional_preferences: string;
  top_n: string;
}

export default function PreferenceForm({ onSearch, isLoading }: PreferenceFormProps) {
  const [localities, setLocalities] = useState<string[]>([]);
  const [preferences, setPreferences] = useState<Preferences>({
    location: '',
    budget: '',
    cuisine: '',
    minimum_rating: '4.0',
    additional_preferences: '',
    top_n: '5',
  });

  useEffect(() => {
    loadLocalities();
  }, []);

  const loadLocalities = async () => {
    try {
      const response = await fetch('/api/localities');
      if (response.ok) {
        const data = await response.json();
        setLocalities(data.localities || []);
      }
    } catch (error) {
      console.error('Failed to load localities:', error);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(preferences);
  };

  const handleChange = (field: keyof Preferences, value: string) => {
    setPreferences(prev => ({ ...prev, [field]: value }));
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
      <div className="flex items-center gap-3 mb-6">
        <SlidersHorizontal className="w-6 h-6 text-red-600" />
        <h2 className="text-2xl font-bold text-gray-800">Your Preferences</h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Location */}
        <div className="space-y-2">
          <label className="flex items-center gap-2 text-sm font-semibold text-gray-700">
            <MapPin className="w-4 h-4 text-red-500" />
            Location
          </label>
          <select
            value={preferences.location}
            onChange={(e) => handleChange('location', e.target.value)}
            className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-red-500 focus:outline-none transition-colors bg-gray-50"
          >
            <option value="">Select a location</option>
            {localities.map((locality) => (
              <option key={locality} value={locality}>
                {locality}
              </option>
            ))}
          </select>
        </div>

        {/* Budget */}
        <div className="space-y-2">
          <label className="flex items-center gap-2 text-sm font-semibold text-gray-700">
            <DollarSign className="w-4 h-4 text-red-500" />
            Budget
          </label>
          <select
            value={preferences.budget}
            onChange={(e) => handleChange('budget', e.target.value)}
            className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-red-500 focus:outline-none transition-colors bg-gray-50"
          >
            <option value="">Any</option>
            <option value="low">Low ($)</option>
            <option value="medium">Medium ($$)</option>
            <option value="high">High ($$$)</option>
          </select>
        </div>

        {/* Cuisine */}
        <div className="space-y-2">
          <label className="flex items-center gap-2 text-sm font-semibold text-gray-700">
            <UtensilsCrossed className="w-4 h-4 text-red-500" />
            Cuisine
          </label>
          <input
            type="text"
            value={preferences.cuisine}
            onChange={(e) => handleChange('cuisine', e.target.value)}
            placeholder="e.g., Chinese, Italian, Indian"
            className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-red-500 focus:outline-none transition-colors bg-gray-50"
          />
        </div>

        {/* Minimum Rating */}
        <div className="space-y-2">
          <label className="flex items-center gap-2 text-sm font-semibold text-gray-700">
            <Star className="w-4 h-4 text-red-500" />
            Minimum Rating
          </label>
          <input
            type="number"
            value={preferences.minimum_rating}
            onChange={(e) => handleChange('minimum_rating', e.target.value)}
            step="0.1"
            min="0"
            max="5"
            className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-red-500 focus:outline-none transition-colors bg-gray-50"
          />
        </div>

        {/* Additional Preferences */}
        <div className="space-y-2 md:col-span-2">
          <label className="text-sm font-semibold text-gray-700">
            Additional Preferences
          </label>
          <input
            type="text"
            value={preferences.additional_preferences}
            onChange={(e) => handleChange('additional_preferences', e.target.value)}
            placeholder="e.g., family-friendly, quick service, outdoor seating"
            className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-red-500 focus:outline-none transition-colors bg-gray-50"
          />
        </div>

        {/* Top N */}
        <div className="space-y-2">
          <label className="flex items-center gap-2 text-sm font-semibold text-gray-700">
            <List className="w-4 h-4 text-red-500" />
            Number of Results
          </label>
          <input
            type="number"
            value={preferences.top_n}
            onChange={(e) => handleChange('top_n', e.target.value)}
            min="1"
            max="10"
            className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-red-500 focus:outline-none transition-colors bg-gray-50"
          />
        </div>
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className="w-full mt-8 bg-gradient-to-r from-red-600 to-red-700 text-white py-4 rounded-xl font-bold text-lg hover:from-red-700 hover:to-red-800 transition-all shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isLoading ? (
          <span className="flex items-center justify-center gap-2">
            <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            Finding Perfect Restaurants...
          </span>
        ) : (
          'Get AI Recommendations'
        )}
      </button>
    </form>
  );
}
