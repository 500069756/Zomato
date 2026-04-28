import { NextRequest, NextResponse } from 'next/server';
import path from 'path';
import fs from 'fs';

interface Restaurant {
  restaurant_name: string;
  location: string;
  primary_cuisine: string;
  cuisines: string;
  cost: string;
  budget_label: string;
  rating: number;
  votes: number;
  address: string;
  affordability: string;
  score: number;
}

interface Preferences {
  location: string | null;
  budget: string | null;
  cuisine: string | null;
  minimum_rating: number;
  additional_preferences: string[];
  top_n: number;
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    // Parse preferences
    const preferences: Preferences = {
      location: body.location || null,
      budget: body.budget || null,
      cuisine: body.cuisine || null,
      minimum_rating: parseFloat(body.minimum_rating) || 0,
      additional_preferences: (body.additional_preferences || '')
        .split(',')
        .map((p: string) => p.trim())
        .filter((p: string) => p),
      top_n: parseInt(body.top_n) || 5,
    };

    // Read CSV file
    const csvPath = path.join(process.cwd(), 'data', 'clean_zomato_restaurants.csv');
    
    if (!fs.existsSync(csvPath)) {
      return NextResponse.json(
        { error: 'Data file not found' },
        { status: 500 }
      );
    }

    const csvContent = fs.readFileSync(csvPath, 'utf-8');
    const lines = csvContent.split('\n');
    const header = parseCSVLine(lines[0]);
    
    // Parse all restaurants
    const restaurants: Restaurant[] = [];
    for (let i = 1; i < lines.length; i++) {
      if (lines[i].trim()) {
        const columns = parseCSVLine(lines[i]);
        const restaurant = parseRestaurant(header, columns);
        if (restaurant) {
          restaurants.push(restaurant);
        }
      }
    }

    // Filter based on preferences
    let filtered = restaurants;

    if (preferences.location) {
      filtered = filtered.filter(r => r.location === preferences.location);
    }

    if (preferences.cuisine) {
      filtered = filtered.filter(r => 
        r.cuisines.toLowerCase().includes(preferences.cuisine!.toLowerCase()) ||
        r.primary_cuisine.toLowerCase().includes(preferences.cuisine!.toLowerCase())
      );
    }

    if (preferences.minimum_rating > 0) {
      filtered = filtered.filter(r => r.rating >= preferences.minimum_rating);
    }

    if (preferences.budget) {
      const budgetMap: { [key: string]: number } = {
        'low': 1,
        'medium': 2,
        'high': 3
      };
      const budgetValue = budgetMap[preferences.budget];
      if (budgetValue) {
        filtered = filtered.filter(r => {
          const priceRange = r.budget_label === '$' ? 1 : r.budget_label === '$$' ? 2 : r.budget_label === '$$$' ? 3 : 1;
          return priceRange <= budgetValue;
        });
      }
    }

    // Calculate score and sort
    const maxVotes = Math.max(...filtered.map(r => r.votes), 1);
    filtered = filtered.map(r => ({
      ...r,
      score: r.rating * 0.7 + (r.votes / maxVotes) * 0.3
    }));
    
    filtered.sort((a, b) => b.score - a.score);

    // Get top N results
    const topRestaurants = filtered.slice(0, preferences.top_n);

    // Try to get LLM explanation
    let llmExplanation = null;
    const groqApiKey = process.env.GROQ_API_KEY;

    if (groqApiKey && topRestaurants.length > 0) {
      try {
        const prompt = buildPrompt(topRestaurants, preferences);
        const response = await fetch('https://api.groq.com/openai/v1/responses', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${groqApiKey}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            model: 'openai/gpt-oss-20b',
            input: prompt,
            max_output_tokens: 220,
          }),
          signal: AbortSignal.timeout(30000),
        });

        if (response.ok) {
          const result = await response.json();
          llmExplanation = result.output_text || null;
        }
      } catch (error) {
        console.error('LLM error:', error);
        llmExplanation = 'AI explanation unavailable';
      }
    }

    return NextResponse.json({
      success: true,
      summary: `Found ${topRestaurants.length} restaurants matching your preferences`,
      recommendations: topRestaurants,
      llm_explanation: llmExplanation,
    });

  } catch (error) {
    console.error('Error in recommend API:', error);
    return NextResponse.json(
      { 
        success: false,
        error: 'Failed to generate recommendations' 
      },
      { status: 500 }
    );
  }
}

// Helper function to parse CSV line handling quoted fields
function parseCSVLine(line: string): string[] {
  const result: string[] = [];
  let current = '';
  let inQuotes = false;
  
  for (let i = 0; i < line.length; i++) {
    const char = line[i];
    
    if (char === '"') {
      inQuotes = !inQuotes;
    } else if (char === ',' && !inQuotes) {
      result.push(current);
      current = '';
    } else {
      current += char;
    }
  }
  
  result.push(current);
  return result;
}

// Parse restaurant from CSV columns
function parseRestaurant(header: string[], columns: string[]): Restaurant | null {
  try {
    const getValue = (fieldName: string) => {
      const index = header.findIndex(h => h.trim().toLowerCase() === fieldName.toLowerCase());
      return index >= 0 ? columns[index]?.trim() : '';
    };

    const ratingStr = getValue('rating');
    const votesStr = getValue('votes');

    return {
      restaurant_name: getValue('restaurant_name'),
      location: getValue('location'),
      primary_cuisine: getValue('primary_cuisine'),
      cuisines: getValue('cuisines') || getValue('cuisine_tags'),
      cost: getValue('cost'),
      budget_label: getValue('budget_label'),
      rating: parseFloat(ratingStr) || 0,
      votes: parseInt(votesStr) || 0,
      address: getValue('address'),
      affordability: getValue('affordability'),
      score: 0,
    };
  } catch (error) {
    console.error('Error parsing restaurant:', error);
    return null;
  }
}

// Build prompt for LLM
function buildPrompt(restaurants: Restaurant[], preferences: Preferences): string {
  const lines = [
    'You are an AI assistant that ranks restaurant recommendations.',
    'Use the user preferences and candidate restaurant data to choose the best options.',
    'Provide a ranked list with a short explanation for each.',
    '',
    'User preferences:',
  ];

  if (preferences.location) lines.push(`- location: ${preferences.location}`);
  if (preferences.budget) lines.push(`- budget: ${preferences.budget}`);
  if (preferences.cuisine) lines.push(`- cuisine: ${preferences.cuisine}`);
  lines.push(`- minimum_rating: ${preferences.minimum_rating}`);
  if (preferences.additional_preferences.length > 0) {
    lines.push(`- additional_preferences: ${preferences.additional_preferences.join(', ')}`);
  }

  lines.push('');
  lines.push('Candidate restaurants:');

  restaurants.forEach(r => {
    lines.push(
      `- ${r.restaurant_name} | ${r.primary_cuisine} | ` +
      `Rating: ${r.rating} | Budget: ${r.budget_label} | ` +
      `Location: ${r.location}`
    );
  });

  lines.push('');
  lines.push('Explain why each restaurant is a good fit and provide a final recommendation summary.');

  return lines.join('\n');
}
