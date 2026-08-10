#!/usr/bin/env node
const { chromium } = require('/home/claw/.npm-global/lib/node_modules/openclaw/node_modules/playwright-core');

async function main() {
  const siteId = process.argv[2];
  const url = process.argv[3];
  if (!siteId || !url) {
    throw new Error('usage: render_company_jobs.js <siteId> <url>');
  }

  const browser = await chromium.launch({
    executablePath: '/home/claw/.local/bin/google-chrome',
    headless: true,
  });

  try {
    const page = await browser.newPage();
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(3000);

    let jobs = [];
    if (siteId === 'kuda-careers') {
      jobs = await page.$$eval('.career-job-list', els =>
        els.map((el, index) => {
          const bits = (el.innerText || '')
            .split('\n')
            .map(s => s.trim())
            .filter(Boolean);
          return {
            index,
            role: bits[0] || '',
            location: bits[1] || '',
            jobType: bits[2] || '',
          };
        })
      );
    } else if (siteId === 'chowdeck-careers') {
      jobs = await page.$$eval('a[href^="/careers/"]', els =>
        els.map((el, index) => {
          const card = el.closest('div[class]');
          const section = el.parentElement?.parentElement;
          const parentText = section?.innerText || '';
          const lines = parentText
            .split('\n')
            .map(s => s.trim())
            .filter(Boolean);
          return {
            index,
            role: (el.textContent || '').trim(),
            href: el.href,
            department: lines[1] || '',
            location: lines.find(line => /\(|remote|lagos|abuja|ibadan/i.test(line)) || '',
            jobType: lines[lines.length - 1] || '',
          };
        })
      );
    } else if (siteId === 'arbeitnow-english-germany') {
      jobs = await page.$$eval('a[href*="/jobs/companies/"]', els => {
        const seen = new Set();
        return els
          .map((el, index) => {
            const href = el.href || '';
            const text = (el.textContent || '').trim();
            if (!href || !text || !/engineer|developer|devops|data|frontend|backend|software|mobile|react|qa|product/i.test(text)) {
              return null;
            }
            const card = el.closest('li') || el.closest('article') || el.parentElement?.parentElement?.parentElement;
            const lines = (card?.innerText || '')
              .split('\n')
              .map(s => s.trim())
              .filter(Boolean);
            const company = lines[1] || '';
            const salary = lines.find(line => /€|eur/i.test(line)) || '';
            const location = lines.find(line => /berlin|munich|münchen|hamburg|cologne|frankfurt|stuttgart|remote|germany|düsseldorf|dusseldorf|leipzig|bremen|bonn|dresden|hannover|hanover/i.test(line)) || 'Germany';
            const key = `${href}::${text}`;
            if (seen.has(key)) return null;
            seen.add(key);
            return {
              index,
              role: text,
              company,
              href,
              salary,
              location,
              description: (card?.innerText || '').trim(),
            };
          })
          .filter(Boolean);
      });
    } else if (siteId === 'berlinstartupjobs-engineering') {
      jobs = await page.$$eval('.bjs-jlid__wrapper', els =>
        els.map((el, index) => {
          const roleEl = el.querySelector('h4 a[href*="/engineering/"]');
          if (!roleEl) return null;
          const role = (roleEl.textContent || '').trim();
          const href = roleEl.href || '';
          const company = (el.querySelector('.bjs-jlid__b')?.textContent || '').trim();
          const tags = Array.from(el.querySelectorAll('.links-box a'))
            .map(node => (node.textContent || '').trim())
            .filter(Boolean);
          const description = (el.querySelector('.bjs-jlid__description')?.textContent || el.innerText || '').trim();
          const location = tags.find(tag => /remote/i.test(tag)) ? 'Berlin / Remote' : 'Berlin, Germany';
          return {
            index,
            role,
            company,
            href,
            location,
            tags,
            description,
          };
        }).filter(Boolean)
      );
    } else if (siteId === 'wearedevelopers-germany') {
      jobs = await page.$$eval('.wad4-job-card.wad4-job-card--large', els =>
        els.map((el, index) => {
          const roleEl = el.querySelector('a.wad4-job-card__link');
          if (!roleEl) return null;
          const lines = (el.innerText || '')
            .split('\n')
            .map(s => s.trim())
            .filter(Boolean);
          const role = (roleEl.textContent || '').trim();
          const href = roleEl.href || '';
          const company = (el.querySelector('.wad4-job-card__logo-img')?.alt || lines[1] || '').trim();
          const location = lines.find(line => /, Germany$|Remote/i.test(line)) || 'Germany';
          const salary = lines.find(line => /€\s*\d|\d+\s*[–-]\s*\d+K|\d+\s*[–-]\s*\d+\s*€/i.test(line)) || '';
          return {
            index,
            role,
            company,
            href,
            location,
            salary,
            description: lines.join(' | '),
          };
        }).filter(Boolean)
      );
    } else if (siteId === 'pegel-visa-berlin') {
      jobs = await page.$$eval('a.after\\:absolute', els =>
        els.map((el, index) => {
          const href = el.href || '';
          const role = (el.textContent || '').trim();
          if (!href.includes('/jobs/') || !role) return null;
          const card = el.closest('article') || el.closest('li') || el.parentElement?.parentElement;
          const lines = (card?.innerText || '')
            .split('\n')
            .map(s => s.trim())
            .filter(Boolean);
          const company = lines[1] || '';
          const location = lines.find(line => /berlin/i.test(line)) || 'Berlin, Germany';
          return {
            index,
            role,
            company,
            href,
            location,
            description: lines.join(' | '),
          };
        }).filter(Boolean)
      );
    } else if (siteId === 'jobriver-germany-it') {
      const searchUrls = [
        'https://jobriver.de/en/jobs?q=Frontend+Developer',
        'https://jobriver.de/en/jobs?q=Backend+Developer',
        'https://jobriver.de/en/jobs?q=Full-Stack+Developer',
        'https://jobriver.de/en/jobs?q=DevOps+Engineer',
        'https://jobriver.de/en/jobs?q=Mobile+Developer',
        'https://jobriver.de/en/jobs?q=Data+Engineer',
        'https://jobriver.de/en/jobs?q=QA+%2F+Test+Engineer',
      ];

      const collected = [];
      for (const searchUrl of searchUrls) {
        await page.goto(searchUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
        await page.waitForTimeout(2000);
        const pageJobs = await page.$$eval('a.card-link', els =>
          els.map((el, index) => {
            const lines = (el.innerText || '')
              .split('\n')
              .map(s => s.trim())
              .filter(Boolean);
            const filtered = lines.filter(line => !/^PREMIUM$/i.test(line));
            const role = filtered[0] || '';
            const company = filtered[1] || '';
            const locationBits = filtered.slice(2, 5);
            return {
              index,
              role,
              company,
              href: el.href || '',
              location: locationBits.join(' | ') || 'Germany',
              description: filtered.join(' | '),
            };
          }).filter(item => item && item.role && item.href)
        );
        collected.push(...pageJobs);
      }
      jobs = collected;
    }

    process.stdout.write(JSON.stringify(jobs));
  } finally {
    await browser.close();
  }
}

main().catch(err => {
  console.error(String(err && err.stack || err));
  process.exit(1);
});
