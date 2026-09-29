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
| `guide.html` | Guide landing page: what is inside, the worksheets, and the download |
| `downloads/shadowing-a-doctor-guide.pdf` | The 12-page guide |

## Editing

`index.html`, `guide.html`, `survey.html` and `results.html` are generated. Change the numbers or copy in `build.py`, then run:

    python3 build.py

Styles live in `styles.css`.

## Status

- The guide exists as of 2026-09-29. Every "Get the free guide" button downloads the PDF.
- All four pages are indexable (`index,follow`, canonical URLs, `sitemap.xml`, open `robots.txt`).
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

## Photos

Every page's hero is a photograph of people. This is a standing rule: no data panels or graphics in the hero.

| File | Used on | Source |
| --- | --- | --- |
| `images/hero-student-doctor-*.webp` | Home hero | Unsplash `i8dHi584lFs`, Unsplash licence (free, no credit required) |
| `images/hero-reviewing-scan-*.webp` | Results hero | Unsplash `5VkNa1LrS8A`, Unsplash licence (free, no credit required) |
| `images/hero-zoha-*.webp`, `images/zoha-*.webp` | Survey hero, About section | Zoha's own photo |

The two stock photos are stand-ins showing young adults, the closest free match to a student shadowing a doctor. No free photo of a high school student in scrubs was found. Replace them with photos of Zoha shadowing if she has any.

## The guide PDF

Source is in `guide-src/`. To rebuild:

    cd guide-src
    python3 guide.py
    NODE_PATH=/Users/marcgray/odyssey/node_modules node render.mjs

`guide.py` holds all twelve pages. Each page is a fixed Letter sheet whose blocks share the spare height, so no page ends with a hole. `render.mjs` prints the PDF and reports each page's shared gap: under 10px is too full, over 30px is too empty.

What in the guide comes from where:

- Survey figures, charts, and the two quoted lines come from Zoha's survey and brand script.
- The reflection advice on page 11 follows her literature review.
- The practical advice (where to look, the email and phone scripts, dress code, privacy rules, observation prompts, questions, thank-you note) is standard shadowing practice written up for this guide. It is not drawn from her survey. Zoha should read it and change anything that does not match her experience.
- Photos: Unsplash `Pd4lRfKo16U` (cover), `hRRx2byCaLo` (page 7), `TRE4BJelfLk` (page 9), `DbCfSrTnflA` (page 10), plus Zoha's own photo.
