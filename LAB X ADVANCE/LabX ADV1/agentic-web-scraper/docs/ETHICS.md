# Web Scraping Ethics and Legality Guidelines

Important ethical and legal considerations when scraping, to avoid legal issues, IP blocking, or harm to website owners.

## 1. Respect `robots.txt`
- **Always check** `https://[website-domain]/robots.txt` before scraping.
- **Adhere to rules:** if a path is disallowed, do not scrape it.

## 2. Review Terms of Service (ToS)
- If the ToS forbids scraping, scraping is a breach of contract and can lead to Cease and Desist letters or lawsuits.
- The absence of a prohibition does not automatically grant permission.

## 3. Be Polite: Rate Limiting and Delays
- Too many fast requests can look like a Denial-of-Service attack.
- Use delays between pages (this project uses `delay_between_pages` = 2 s).
- Avoid concurrent requests unless you have permission; slow down if the site responds slowly.

## 4. Identify Yourself (User-Agent)
- A descriptive User-Agent lets site admins contact you, e.g. `Mozilla/5.0 (compatible; MyScraper/1.0; mailto:you@example.com)`.
- Do not impersonate Googlebot.

## 5. Transparency
- Be open about scraping activity where possible; never use scraped data for spam or illegal purposes.

## 6. Data Usage and Copyright
- Scraped content is often copyrighted — do not republish or monetize it without permission.
- Fair use is narrow and context-dependent.

## 7. Legal Risks
Scraping has been found unlawful in cases involving breach of ToS, trespass to chattels, copyright infringement, and privacy violations (collecting personal data without consent).

**In summary: act responsibly, respectfully, and legally. When in doubt, ask the site owner.**

> This project targets `books.toscrape.com`, a sandbox site built specifically for scraping practice.
