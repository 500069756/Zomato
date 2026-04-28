import { Utensils } from 'lucide-react';

export default function Header() {
  return (
    <header className="bg-gradient-to-r from-red-600 to-red-700 text-white py-8 shadow-lg">
      <div className="max-w-6xl mx-auto px-6">
        <div className="flex items-center justify-center gap-4 mb-3">
          <Utensils className="w-10 h-10" />
          <h1 className="text-4xl font-bold tracking-tight">
            Zomato AI
          </h1>
        </div>
        <p className="text-center text-red-100 text-lg max-w-2xl mx-auto">
          Discover perfect restaurants with AI-powered recommendations tailored to your preferences
        </p>
      </div>
    </header>
  );
}
