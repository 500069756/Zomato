import { NextRequest, NextResponse } from 'next/server';
import path from 'path';
import fs from 'fs';

export async function GET(request: NextRequest) {
  try {
    // Read the CSV file
    const csvPath = path.join(process.cwd(), 'data', 'clean_zomato_restaurants.csv');
    
    if (!fs.existsSync(csvPath)) {
      return NextResponse.json(
        { error: 'Data file not found' },
        { status: 500 }
      );
    }

    const csvContent = fs.readFileSync(csvPath, 'utf-8');
    const lines = csvContent.split('\n');
    
    // Parse CSV to extract unique localities
    const header = lines[0].split(',');
    const locationIndex = header.findIndex(h => h.trim().toLowerCase() === 'location');
    
    if (locationIndex === -1) {
      return NextResponse.json(
        { error: 'Location column not found in CSV' },
        { status: 500 }
      );
    }

    const localities = new Set<string>();
    for (let i = 1; i < lines.length; i++) {
      if (lines[i].trim()) {
        // Handle CSV with quotes
        const columns = parseCSVLine(lines[i]);
        if (columns[locationIndex]) {
          const location = columns[locationIndex].trim();
          if (location) {
            localities.add(location);
          }
        }
      }
    }

    const sortedLocalities = Array.from(localities).sort();

    return NextResponse.json({ localities: sortedLocalities });
  } catch (error) {
    console.error('Error fetching localities:', error);
    return NextResponse.json(
      { error: 'Failed to fetch localities' },
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
