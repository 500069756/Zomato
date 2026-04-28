import { Image } from 'lucide-react';

export default function HeroSection() {
  return (
    <section className="relative bg-gradient-to-br from-red-600 via-red-700 to-orange-600 text-white overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute inset-0" style={{
          backgroundImage: 'url("data:image/svg+xml,%3Csvg width=\'60\' height=\'60\' viewBox=\'0 0 60 60\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cg fill=\'none\' fill-rule=\'evenodd\'%3E%3Cg fill=\'%23ffffff\' fill-opacity=\'1\'%3E%3Cpath d=\'M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z\'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")',
        }} />
      </div>

      <div className="relative max-w-6xl mx-auto px-6 py-16 md:py-24">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          <div className="space-y-6">
            <h2 className="text-4xl md:text-5xl font-bold leading-tight">
              Discover Your Perfect Dining Experience
            </h2>
            <p className="text-lg text-red-100 leading-relaxed">
              Our AI-powered recommendation system analyzes thousands of restaurants to find the perfect match for your cravings, budget, and location.
            </p>
            <div className="flex flex-wrap gap-4">
              <div className="flex items-center gap-2 bg-white/20 backdrop-blur-sm px-4 py-2 rounded-full">
                <span className="text-2xl">🍽️</span>
                <span className="font-semibold">1000+ Restaurants</span>
              </div>
              <div className="flex items-center gap-2 bg-white/20 backdrop-blur-sm px-4 py-2 rounded-full">
                <span className="text-2xl">🤖</span>
                <span className="font-semibold">AI-Powered</span>
              </div>
              <div className="flex items-center gap-2 bg-white/20 backdrop-blur-sm px-4 py-2 rounded-full">
                <span className="text-2xl">⭐</span>
                <span className="font-semibold">Personalized</span>
              </div>
            </div>
          </div>

          {/* Food Image Placeholder */}
          <div className="relative">
            <div className="bg-white/10 backdrop-blur-sm rounded-3xl p-8 border border-white/20 shadow-2xl">
              <div className="aspect-square bg-gradient-to-br from-yellow-100 to-orange-100 rounded-2xl overflow-hidden shadow-inner flex items-center justify-center">
                <img 
                  src="/thali.jpg" 
                  alt="Delicious Indian Thali"
                  className="w-full h-full object-cover"
                  onError={(e) => {
                    (e.target as HTMLImageElement).style.display = 'none';
                    (e.target as HTMLImageElement).parentElement!.innerHTML = `
                      <div class="text-center text-gray-400">
                        <Image class="w-32 h-32 mx-auto mb-4 opacity-50" />
                        <p class="text-lg font-medium">Authentic Indian Cuisine</p>
                      </div>
                    `;
                  }}
                />
              </div>
              <div className="absolute -bottom-4 -right-4 bg-white text-gray-800 px-6 py-3 rounded-2xl shadow-xl">
                <p className="font-bold text-lg">Indian Thali</p>
                <p className="text-sm text-gray-600">Traditional & Delicious</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
