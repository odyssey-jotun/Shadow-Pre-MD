# Shadow Pre-MD

Landing site for Zoha Waheed's passion project: a free guide to medical shadowing for high school students, built from her survey of 43 practicing physicians and her review of five peer-reviewed studies.

## Live site

https://odyssey-jotun.github.io/Shadow-Pre-MD/

The repository is public and GitHub Pages serves `main` at root. Pushing to `main` redeploys.

## Pages

| Page | What it is |
| --- | --- |
| `index.html` | StoryBrand landing page: header, problem (three icons with stats), guide (Zoha, first person), plan, proof, call to action |
| `survey.html` | The survey in six numbered sections. Each has a lead paragraph in Zoha's voice, three stat cards, a donut beside a bar chart, and a pull-quote band. Modelled on the survey layout in Deven Patel's mountain biking guide (arbiketrails.com) |
| `results.html` | Every question with the count and share for each answer, plus the split by hosting experience |
| `guide.html` | Holding page for the guide download |

## Editing

`index.html`, `survey.html` and `results.html` are generated. Change the numbers or copy in `build.py`, then run:

    python3 build.py

Styles live in `styles.css`. `guide.html` is hand-written.

## Status

- The guide PDF does not exist yet. Every "Get the free guide" button points to `guide.html`. When the PDF is ready, put it in `downloads/` and point those links at it.
- The three content pages are indexable (`index,follow`, canonical URLs, `sitemap.xml`, open `robots.txt`). Only `guide.html` stays `noindex` because it is a thin holding page; flip it when the PDF ships and add it to the sitemap.
- The survey's raw responses were not available when the site was built. All figures come from the tabulated counts and from the abstract. Questions 2, 3 and 5 on the results page are incomplete for that reason.
- Question wording on the results page follows Zoha's draft question list and should be checked against the final Google Form.
- The abstract is submitted to the 2027 Medical Education Innovation Conference, not yet accepted.
- "Willing to host" is reported as 72% (rated 4 or 5). The abstract's "over 90%" counts ratings of 3 and up.
- Pull quotes credited to Zoha on the survey page are her own words from her brand script. Uncredited bands state a survey finding.

## SEO and performance

- Lighthouse (local, 2026-09-29): 100 in performance, accessibility, best practices and SEO on `index.html`, `survey.html` and `results.html`, mobile and desktop.
- CSS is minified and inlined by `build.py`, so there is no render-blocking stylesheet. Edit `styles.css`, then rebuild.
- Fonts are self-hosted in `fonts/` and subset to the characters the site uses. If copy introduces a new symbol or accented letter, re-subset from the Google Fonts originals or the character will fall back to a system font.
- Each page carries JSON-LD (`WebSite`, `Person`, plus `WebPage` or `Article` and `BreadcrumbList`).
- Headings target searches such as "how to shadow a doctor in high school" and "what to do when shadowing a doctor".
- After a custom domain is added, update `SITE` in `build.py`, `sitemap.xml` and `robots.txt`.
