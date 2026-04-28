'use client';

import { MapPin, Star, DollarSign, Info } from 'lucide-react';
import { motion } from 'framer-motion';

interface Restaurant {
  restaurant_name: string;
  cuisine: string;
  location: string;
  rating: number;
  budget_label: string;
  explanation: string;
  address?: string;
}

interface RestaurantCardProps {
  restaurant: Restaurant;
  index: number;
}

export default function RestaurantCard({ restaurant, index }: RestaurantCardProps) {
  const getRatingColor = (rating: number) => {
    if (rating >= 4.5) return 'text-green-600 bg-green-50';
    if (rating >= 4.0) return 'text-yellow-600 bg-yellow-50';
    if (rating >= 3.0) return 'text-orange-600 bg-orange-50';
    return 'text-red-600 bg-red-50';
  };

  const getBudgetDisplay = (budget: string | null | undefined) => {
    if (!budget) return 'Not specified';
    switch (budget.toLowerCase()) {
      case 'low': return '$';
      case 'medium': return '$$';
      case 'high': return '$$$';
      default: return budget;
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1, duration: 0.5 }}
      className="bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden border border-gray-100 group"
    >
      {/* Card Header with Gradient */}
      <div className="bg-gradient-to-r from-red-50 to-orange-50 p-6 border-b border-red-100">
        <div className="flex items-start justify-between mb-2">
          <h3 className="text-xl font-bold text-gray-800 group-hover:text-red-600 transition-colors">
            {restaurant.restaurant_name}
          </h3>
          <div className={`flex items-center gap-1 px-3 py-1 rounded-full font-bold ${getRatingColor(restaurant.rating)}`}>
            <Star className="w-4 h-4 fill-current" />
            {restaurant.rating ? restaurant.rating.toFixed(1) : 'N/A'}
          </div>
        </div>
        <p className="text-gray-600 text-sm flex items-center gap-2">
          <UtensilsIcon className="w-4 h-4" />
          {restaurant.cuisine || 'Not specified'}
        </p>
      </div>

      {/* Card Body */}
      <div className="p-6 space-y-4">
        <div className="flex items-start gap-3">
          <MapPin className="w-5 h-5 text-red-500 mt-1 flex-shrink-0" />
          <div>
            <p className="font-semibold text-gray-700">{restaurant.location || 'Not specified'}</p>
            {restaurant.address && (
              <p className="text-sm text-gray-500 mt-1">{restaurant.address}</p>
            )}
          </div>
        </div>

        <div className="flex items-center gap-3">
          <DollarSign className="w-5 h-5 text-green-500" />
          <span className="font-semibold text-gray-700">
            {getBudgetDisplay(restaurant.budget_label)} - {restaurant.budget_label ? restaurant.budget_label.charAt(0).toUpperCase() + restaurant.budget_label.slice(1) : 'Not specified'}
          </span>
        </div>

        <div className="bg-blue-50 border-l-4 border-blue-400 p-4 rounded-r-lg">
          <div className="flex items-start gap-2">
            <Info className="w-5 h-5 text-blue-500 mt-0.5 flex-shrink-0" />
            <div>
              <p className="text-sm font-semibold text-blue-800 mb-1">Why this restaurant?</p>
              <p className="text-sm text-blue-700 leading-relaxed">
                {restaurant.explanation || 'Matches your preferences based on location, cuisine, and other criteria.'}
              </p>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}

function UtensilsIcon({ className }: { className?: string }) {
  return (
    <svg 
      className={className} 
      viewBox="0 0 24 24" 
      fill="none" 
      stroke="currentColor" 
      strokeWidth="2" 
      strokeLinecap="round" 
      strokeLinejoin="round"
    >
      <path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2" />
      <path d="M7 2v20" />
      <path d="M21 15V2v0a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7" />
    </svg>
  );
}
