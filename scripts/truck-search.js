#!/usr/bin/env node

/**
 * Truck Listings Scraper
 * Searches multiple platforms for matching trucks
 * Posts to Telegram + Notion every 2-3 days at 11 PM WAT
 */

const https = require('https');
const http = require('http');
const { execSync } = require('child_process');

// Search specs
const SPECS = {
  makes: ['HOWO', 'DAF', 'IVECO'],
  maxPrice: 4000, // GBP
  maxAge: 10,
  minHp: 380,
  bodyType: 'flatbed',
  axleConfig: '4x2',
  regions: ['Germany', 'UK', 'Netherlands']
};

const PLATFORMS = {
  ebayMotors: 'https://www.ebay.co.uk/sch/Trucks-Commercial-Vehicles/6022/i.html',
  autoScout24: 'https://www.autoscout24.com/lst/trucks',
  autoline: 'https://www.autoline.com/en',
};

async function fetchUrl(url) {
  return new Promise((resolve, reject) => {
    const protocol = url.startsWith('https') ? https : http;
    protocol.get(url, { 
      headers: { 'User-Agent': 'Mozilla/5.0' },
      timeout: 5000
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    }).on('error', reject);
  });
}

async function searchEbayMotors() {
  // eBay Motors trucks in UK
  const url = `${PLATFORMS.ebayMotors}?_nkw=HOWO+DAF+IVECO+flatbed+truck`;
  console.log('📍 Searching eBay Motors...');
  try {
    const data = await fetchUrl(url);
    // Parse HTML for truck listings
    const listings = [];
    // Basic regex extraction (limited without DOM parser)
    const prices = data.match(/£[\d,]+/g) || [];
    return { platform: 'eBay Motors', url, count: prices.length };
  } catch (err) {
    console.error('❌ eBay Motors error:', err.message);
    return null;
  }
}

async function searchAutoline() {
  // Autoline truck search
  const url = `${PLATFORMS.autoline}?make=HOWO,DAF,IVECO&category=trucks`;
  console.log('📍 Searching Autoline...');
  try {
    const data = await fetchUrl(url);
    return { platform: 'Autoline', url, status: 'connected' };
  } catch (err) {
    console.error('❌ Autoline error:', err.message);
    return null;
  }
}

async function postToTelegram(message) {
  // Uses OpenClaw's message tool (called via main session)
  console.log('\n📤 Message ready for Telegram:');
  console.log(message);
  return true;
}

async function updateNotion(trucks) {
  // Would integrate with Notion API here
  console.log(`\n💾 Ready to save ${trucks.length} trucks to Notion`);
  return true;
}

async function runSearch() {
  console.log('🚛 TRUCK SCAN STARTED');
  console.log(`⏰ ${new Date().toISOString()}`);
  console.log(`📋 Specs: ${SPECS.makes.join(', ')} | Max £${SPECS.maxPrice} | <${SPECS.maxAge} years\n`);

  const results = await Promise.all([
    searchEbayMotors(),
    searchAutoline(),
  ]);

  const foundResults = results.filter(r => r);
  console.log(`\n✅ Connected to ${foundResults.length} platforms`);

  // Build Telegram message
  const message = `🚛 TRUCK SCAN - ${new Date().toLocaleDateString()}

${foundResults.map(r => 
  `✅ ${r.platform}\n🔗 ${r.url}`
).join('\n\n')}

Search specs: ${SPECS.makes.join('/')} | Max £${SPECS.maxPrice} | <${SPECS.maxAge} yrs
Next scan: in 2-3 days`;

  await postToTelegram(message);
  console.log('\n✨ Scan complete');
}

// Run search
runSearch().catch(console.error);
