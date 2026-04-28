import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const projectRoot = join(__dirname, '..');
const csvPath = join(projectRoot, 'data', 'clean_zomato_restaurants.csv');
const outPath = join(projectRoot, 'data', 'localities.json');

function parseCsvLine(line) {
  const cells = [];
  let cur = '';
  let inQuotes = false;
  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    if (ch === '"') {
      inQuotes = !inQuotes;
    } else if (ch === ',' && !inQuotes) {
      cells.push(cur);
      cur = '';
    } else {
      cur += ch;
    }
  }
  cells.push(cur);
  return cells;
}

const csv = readFileSync(csvPath, 'utf-8');
const lines = csv.split(/\r?\n/);
const header = parseCsvLine(lines[0]);
const locationIdx = header.findIndex((h) => h.trim().toLowerCase() === 'location');
if (locationIdx === -1) {
  throw new Error('location column not found in CSV header');
}

const seen = new Set();
for (let i = 1; i < lines.length; i++) {
  const line = lines[i];
  if (!line.trim()) continue;
  const value = parseCsvLine(line)[locationIdx]?.trim();
  if (value) seen.add(value);
}

const localities = [...seen].sort((a, b) => a.localeCompare(b));
writeFileSync(outPath, JSON.stringify(localities, null, 2) + '\n');
console.log(`Wrote ${localities.length} localities to ${outPath}`);
