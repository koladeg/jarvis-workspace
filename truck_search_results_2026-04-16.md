# Truck search results — 2026-04-16

Search brief:
- Brands: HOWO, DAF, IVECO
- Configuration: 4x2 flatbed
- Max age: under 15 years
- Max price: £4,000 per truck
- Locations: Germany, UK, Netherlands

## Method used
- Tried live extraction with `agent-browser` on AutoScout24 and eBay.
- AutoScout24 was blocked by Cloudflare challenge before usable truck listings could be extracted.
- eBay UK search pages were accessible and yielded usable search-result text.
- Truck1 returned placeholder / challenge-style responses and TrucksCorner returned JS/403 blocking. No Apify tool was available in this environment, so CAPTCHA/anti-bot bypass could not be completed here.

## Source status
- **AutoScout24**: blocked by Cloudflare challenge. No reliable listing extraction completed.
- **eBay UK**: usable.
- **Truck1.eu**: status 202 placeholder, no listings extracted.
- **TrucksCorner**: 403 / JS required.

## Strict matches found

### 1) IVECO EUROCARGO 140 E22 EURO 5, 4X2, 14 TONNE FLATBED
- Source: eBay UK
- URL: https://www.ebay.co.uk/itm/326775823163
- Price: £3,450.00
- Year: not visible on accessible search snippet
- Mileage: not visible on accessible search snippet
- Specs seen: 4x2, 14 tonne, flatbed, Euro 5, Iveco Eurocargo 140 E22
- Location: UK only filter applied on search results
- Notes: This is the clearest strict hit against the requested configuration.

## Near matches / possible leads
These matched brand + price and were flatbed/dropside related, but one or more required fields were not fully visible from the accessible result text.

### 2) 2019 Iveco Eurocargo 75-160 4.5 21FT DROPSIDE LORRY 7.5 TON TRUCK FLATBED
- Source: eBay UK
- URL: https://www.ebay.co.uk/itm/236415428199
- Price: £1.20
- Year: 2019
- Mileage: not visible on accessible search snippet
- Specs seen: 21FT, dropside, truck flatbed, 7.5 ton, Iveco Eurocargo 75-160
- Location: UK only filter applied on search results
- Notes: Strong flatbed lead, but 4x2 was not shown in the accessible result text and £1.20 appears to be a placeholder classified-ad price.

### 3) Iveco Eurocargo 7.5 Ton Flatbed Scaffold Truck
- Source: eBay UK
- URL: https://www.ebay.co.uk/itm/157828838923
- Price: £1,200.00
- Year: not visible on accessible search snippet
- Mileage: not visible on accessible search snippet
- Specs seen: 7.5 ton, flatbed, scaffold truck
- Location: UK only filter applied on search results
- Notes: Looks relevant, but 4x2 and exact year were not visible from the accessible search result.

## DAF review
I found several DAF results under the eBay UK £4,000 filter, but none of the accessible listings clearly met the full strict requirement of **under 15 years + 4x2 + flatbed**.

Relevant DAF links checked:
- 2019 DAF LF 230 18 TON GROSS 4X2 with Hyvalift Skip Gear — https://www.ebay.co.uk/itm/187831295284
  - Price not exposed in accessible snippet from this pass
  - Rejected as strict match: 4x2 shown, but not a flatbed listing
- 2016 DAF CF 75.330 26T FLATBED WITH MOFFETT ATTACHMENTS — https://www.ebay.co.uk/itm/327055476111
  - Price not exposed in accessible snippet from this pass
  - Rejected as strict match: flatbed shown, but 4x2 not shown
- DAF LF55 SCAFFOLD TRUCK, LOW MILES — https://www.ebay.co.uk/itm/267634024509
  - Price: £3,850.00
  - Year not shown in accessible snippet
  - Rejected as strict match: scaffold body suggests relevance, but year and 4x2/flatbed details were not explicit

## HOWO review
- eBay UK search for `HOWO flatbed truck` with UK-only and under-£4,000 filters returned **0 results**.
- No HOWO matches were extracted from accessible AutoScout24 / Truck1 / TrucksCorner paths.

## Netherlands / Germany review
- AutoScout24 extraction for Germany / Netherlands failed at Cloudflare challenge stage.
- Truck1 and TrucksCorner were blocked / inaccessible in this environment.
- No confirmed Germany or Netherlands strict matches could be extracted from accessible pages during this run.

## Key limitations
- **Mileage was not exposed** on the accessible eBay search-result snippets.
- **AutoScout24 direct extraction failed** due to anti-bot challenge.
- **Truck1 / TrucksCorner** could not be bypassed in this environment because no Apify path/tool was available here.
- Several eBay classified ads show placeholder prices such as **£1.20**, so those should be manually verified.

## Best current shortlist
1. **IVECO EUROCARGO 140 E22 EURO 5, 4X2, 14 TONNE FLATBED** — https://www.ebay.co.uk/itm/326775823163 — £3,450.00
2. **2019 Iveco Eurocargo 75-160 4.5 21FT DROPSIDE LORRY 7.5 TON TRUCK FLATBED** — https://www.ebay.co.uk/itm/236415428199 — £1.20 placeholder / verify manually
3. **Iveco Eurocargo 7.5 Ton Flatbed Scaffold Truck** — https://www.ebay.co.uk/itm/157828838923 — £1,200.00
