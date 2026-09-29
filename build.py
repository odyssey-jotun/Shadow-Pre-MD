#!/usr/bin/env python3
"""Builds index.html, survey.html and results.html from the survey data below.

Run: python3 build.py
Every number on the site comes from DATA, so a correction is made once here.
"""
from html import escape

N = 43
HOSTS, NEVER = 27, 16

# ---------------------------------------------------------------- data
BARRIERS = [  # label, total, never-hosts (of 16), hosts (of 27)
    ("Lack of physician time", 34, 12, 22),
    ("Lack of formal shadowing structure", 24, 10, 14),
    ("Patient privacy and confidentiality", 22, 9, 13),
    ("Hospital or institutional policies", 22, 12, 10),
    ("Liability or administrative concerns", 19, 9, 10),
    ("Difficulty coordinating schedules", 18, 5, 13),
    ("Student preparedness and professionalism", 15, 9, 6),
    ("Uncertainty about what students may do", 12, 5, 7),
]
BARRIERS_OTHER = ("Other", 3)
FISHER = {  # two-sided Fisher exact p, never-hosts vs previous hosts
    "Lack of physician time": 0.706,
    "Lack of formal shadowing structure": 0.542,
    "Patient privacy and confidentiality": 0.755,
    "Hospital or institutional policies": 0.027,
    "Liability or administrative concerns": 0.341,
    "Difficulty coordinating schedules": 0.348,
    "Student preparedness and professionalism": 0.045,
    "Uncertainty about what students may do": 0.737,
}
RESOURCES = [
    ("Student orientation program or handbook", 28),
    ("Clear institutional guidelines on what students may observe", 26),
    ("Suggested questions or discussion topics", 19),
    ("Short physician guide for supervising students", 17),
    ("Pre-shadowing educational materials", 17),
    ("Professionalism expectations", 16),
    ("HIPAA and confidentiality training", 14),
    ("Structured shadowing schedule", 12),
    ("Mentorship guidance", 12),
]
FACTORS = [
    ("Direct observation of patient care", 30),
    ("Ability to ask questions", 22),
    ("Interaction with physicians", 19),
    ("Career guidance", 17),
    ("Understanding clinical reasoning", 15),
    ("Structured educational activities", 15),
    ("Exposure to different specialties", 14),
    ("Exposure to medical procedures", 8),
    ("Research project involvement", 8),
    ("Mentorship or relationship with a physician", 7),
]
SPECIALTY = [
    ("Internal medicine or subspecialty", 24),
    ("Surgery or surgical subspecialty", 8),
    ("Family medicine", 3),
    ("Pediatrics or pediatric subspecialty", 3),
    ("Emergency medicine", 0),
    ("Other or not tabulated", 5),
]
SETTING = [  # reported as percentages in the abstract
    ("Government or VA hospital", 30),
    ("Community hospital", 23),
    ("Private practice", 21),
    ("Academic medical center", 18),
]
USEFUL = [0, 1, 10, 9, 23]   # ratings 1..5
LIKELY = [1, 2, 9, 8, 23]
RHO = [("All 43 physicians", 0.40, "p = .008"),
       ("Previous hosts (27)", 0.12, "p = .55"),
       ("Never hosted (16)", 0.63, "p = .009")]


def pct(n, d=N):
    return round(100 * n / d)


# ---------------------------------------------------------------- pieces
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,500;6..72,600;6..72,700'
         '&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">')


def head(title, desc):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<!-- TEMPORARY: noindex until the guide PDF is published. Flip to "index,follow" at launch. -->
<meta name="robots" content="noindex,nofollow">
<meta name="theme-color" content="#F4F7F9">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
{FONTS}
<link rel="stylesheet" href="styles.css">
</head>
<body>

<a class="skip" href="#main">Skip to content</a>
"""


def nav(current):
    items = [("index.html", "Home"), ("survey.html", "The Survey"), ("results.html", "The Results"),
             ("index.html#about", "About")]
    lis = []
    for href, label in items:
        cur = ' aria-current="page"' if href == current else ""
        lis.append(f'      <li><a href="{href}"{cur}>{label}</a></li>')
    return f"""<nav class="site" aria-label="Primary">
  <div class="wrap">
    <a class="wordmark" href="index.html">Shadow <span>Pre-MD</span></a>
    <ul>
{chr(10).join(lis)}
    </ul>
    <a href="guide.html" class="nav-cta">Get the Guide</a>
  </div>
</nav>
"""


FOOT = """
<footer>
  <div class="wrap">
    <span>Shadow Pre-MD, a project by Zoha Waheed</span>
    <ul>
      <li><a href="index.html">Home</a></li>
      <li><a href="survey.html">The Survey</a></li>
      <li><a href="results.html">The Results</a></li>
      <li><a href="guide.html">The Guide</a></li>
    </ul>
  </div>
</footer>

</body>
</html>
"""


def bars(rows, d=N, hl=(), muted=(), show_n=True):
    out = ['<ul class="bars">']
    for label, n in rows:
        p = pct(n, d)
        cls = " hl" if label in hl else (" muted" if label in muted else "")
        cls = f' class="{cls.strip()}"' if cls else ""
        of = f"{n} of {d}" if show_n else ""
        out.append(f'  <li{cls} title="{escape(label)}: {n} of {d} ({p}%)">'
                   f'<div class="lab"><span>{escape(label)}</span><span class="val">{of}<b>{p}%</b></span></div>'
                   f'<div class="track"><span class="fill" style="width:{max(p, 0)}%"></span></div></li>')
    out.append("</ul>")
    return "\n".join(out)


def pbars(rows):
    """Bars for values that were reported only as percentages."""
    out = ['<ul class="bars">']
    for label, p in rows:
        out.append(f'  <li title="{escape(label)}: {p}%">'
                   f'<div class="lab"><span>{escape(label)}</span><span class="val"><b>{p}%</b></span></div>'
                   f'<div class="track"><span class="fill" style="width:{p}%"></span></div></li>')
    out.append("</ul>")
    return "\n".join(out)


LEGEND = ('<ul class="legend" aria-label="Legend">'
          '<li><span class="mk never"></span>Never hosted a student (16)</li>'
          '<li><span class="mk host"></span>Has hosted a student (27)</li></ul>')


def dumbbell(rows):
    rows = sorted(rows, key=lambda r: (r[2] / NEVER - r[3] / HOSTS), reverse=True)
    out = [LEGEND, '<ul class="dumb">']
    for label, _t, nv, hs in rows:
        a, b = 100 * nv / NEVER, 100 * hs / HOSTS
        lo, hi = min(a, b), max(a, b)
        gap = round(a - b)
        sign = "+" if gap > 0 else ("−" if gap < 0 else "")
        out.append(
            f'  <li title="{escape(label)}: never hosted {round(a)}%, has hosted {round(b)}%">'
            f'<div class="lab"><span>{escape(label)}</span><span class="gap">gap<b>{sign}{abs(gap)} pts</b></span></div>'
            f'<div class="rail"><span class="link" style="left:{lo:.1f}%;width:{hi - lo:.1f}%"></span>'
            f'<span class="pt host" style="left:{b:.1f}%"></span><span class="pt never" style="left:{a:.1f}%"></span></div>'
            f'<div class="nums"><span>Never hosted: {round(a)}% ({nv} of {NEVER})</span>'
            f'<span>Has hosted: {round(b)}% ({hs} of {HOSTS})</span></div></li>')
    out.append("</ul>")
    out.append('<div class="axis" aria-hidden="true"><span>0%</span><span>25%</span><span>50%</span><span>75%</span><span>100%</span></div>')
    return "\n".join(out)


def columns(dist, lo_label, hi_label):
    top = max(dist)
    mean = sum((i + 1) * n for i, n in enumerate(dist)) / sum(dist)
    high = dist[3] + dist[4]
    out = [f'<p class="mean"><b>{mean:.2f}</b>average out of 5. {high} of {N} ({pct(high)}%) chose 4 or 5.</p>',
           '<ul class="cols">']
    for i, n in enumerate(dist):
        cls = ' class="lo"' if i < 3 else ""
        out.append(f'  <li{cls} title="Rating {i + 1}: {n} of {N}"><span class="c">{n}</span>'
                   f'<span class="b" style="height:{100 * n / top * 0.82:.1f}%"></span></li>')
    out.append("</ul>")
    out.append('<ul class="cols-x" aria-hidden="true">' + "".join(f"<li>{i}</li>" for i in range(1, 6)) + "</ul>")
    out.append(f'<div class="cols-ends"><span>{lo_label}</span><span>{hi_label}</span></div>')
    return "\n".join(out)


def waffle():
    cells = ['<li class="never"></li>'] * NEVER + ["<li></li>"] * HOSTS
    return ('<ul class="waffle" role="img" aria-label="43 physicians: 27 had hosted a high school student, 16 never had">'
            + "".join(cells) + "</ul>")


def rho_bars():
    out = ['<ul class="bars">']
    for label, r, p in RHO:
        cls = ' class="hl"' if r > 0.6 else (' class="muted"' if r < 0.2 else "")
        out.append(f'  <li{cls} title="{label}: rho {r:.2f}, {p}">'
                   f'<div class="lab"><span>{label}</span><span class="val">{p}<b>&rho; = {r:.2f}</b></span></div>'
                   f'<div class="track"><span class="fill" style="width:{r * 100:.0f}%"></span></div></li>')
    out.append("</ul>")
    out.append('<div class="axis" aria-hidden="true"><span>0 (no link)</span><span>0.5</span><span>1.0 (perfect)</span></div>')
    return "\n".join(out)


ARROW = ('<span class="arrow" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
         'stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h15M13 6l6 6-6 6"/></svg></span>')


def pairs():
    rows = [("Student preparedness", 15, "Student orientation handbook", 28),
            ("Hospital or institutional policies", 22, "Clear guidelines on what students may observe", 26),
            ("Privacy and confidentiality", 22, "HIPAA and confidentiality training", 14),
            ("No formal shadowing structure", 24, "Structured shadowing schedule", 12)]
    out = ['<ul class="pairs">']
    for b, bn, r, rn in rows:
        out.append(f'  <li><div class="side"><span class="k">Barrier named</span>'
                   f'<span class="v"><b>{pct(bn)}%</b>{b}</span></div>{ARROW}'
                   f'<div class="side res"><span class="k">Resource requested</span>'
                   f'<span class="v"><b>{pct(rn)}%</b>{r}</span></div></li>')
    out.append("</ul>")
    return "\n".join(out)


def group_table():
    rows = sorted(BARRIERS, key=lambda r: (r[2] / NEVER - r[3] / HOSTS), reverse=True)
    out = ['<div class="tablewrap"><table class="data">',
           '<caption class="sr-only">Barriers named by physicians who had never hosted a student and by those who had</caption>',
           "<thead><tr><th>Barrier</th><th>Never hosted</th><th>Has hosted</th><th>Gap</th><th>Fisher exact p</th></tr></thead><tbody>"]
    for label, _t, nv, hs in rows:
        a, b = 100 * nv / NEVER, 100 * hs / HOSTS
        g = round(a - b)
        sign = "+" if g > 0 else ("−" if g < 0 else "")
        p = FISHER[label]
        cls = ' class="sig"' if p < 0.05 else ""
        out.append(f"<tr{cls}><td>{escape(label)}</td><td>{round(a)}% ({nv})</td><td>{round(b)}% ({hs})</td>"
                   f"<td>{sign}{abs(g)} pts</td><td>{('%.3f' % p).lstrip('0')}</td></tr>")
    out.append("</tbody></table></div>")
    return "\n".join(out)


CHECK = ('<svg viewBox="0 0 24 24" fill="none" stroke="#F2A77E" stroke-width="2.4" stroke-linecap="round" '
         'stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>')

ICON_CLOCK = ('<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" '
              'stroke-linejoin="round" aria-hidden="true"><circle cx="24" cy="26" r="15"/><path d="M24 17v9l6 4"/>'
              '<path d="M19 5h10M24 5v6M37 13l3-3"/></svg>')
ICON_MAP = ('<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true"><rect x="10" y="8" width="28" height="34" rx="4"/>'
            '<path d="M18 8V5h12v3"/><path d="M17 19h4M17 27h4M17 35h4"/>'
            '<path d="M27 19h4M27 27h4M27 35h4" stroke-dasharray="1.5 4"/></svg>')
ICON_LOCK = ('<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" '
             'stroke-linejoin="round" aria-hidden="true"><path d="M24 4l16 6v12c0 10-6.5 17.5-16 22C14.5 39.500 8 32 8 22V10z"/>'
             '<rect x="17" y="21" width="14" height="11" rx="2.5"/><path d="M20 21v-3a4 4 0 018 0v3"/></svg>')


def refs(items, heading="Works cited", band=True):
    lis = "\n".join(f'      <li id="r{i + 1}">{t}</li>' for i, t in enumerate(items))
    return f"""
<section class="refs{' band' if band else ''}" id="sources">
  <div class="wrap">
    <div class="section-head" style="margin-bottom:22px">
      <span class="eyebrow">Sources</span>
      <h2>{heading}</h2>
    </div>
    <ol>
{lis}
    </ol>
  </div>
</section>
"""


R_WAHEED = ('Waheed, Z. S. (2026). <em>Physician perspectives on high school shadowing: Barriers, educational value, '
            'and opportunities for standardization</em>. Cross-sectional survey of 43 practicing physicians. '
            'Abstract submitted to the 2027 Medical Education Innovation Conference.')
R_MANN = ('Mann, K., Gordon, J., &amp; MacLeod, A. (2009). Reflection and reflective practice in health professions '
          'education: A systematic review. <em>Advances in Health Sciences Education, 14</em>(4), 595&ndash;621. '
          '<a class="src" href="https://doi.org/10.1007/s10459-007-9090-2" target="_blank" rel="noopener noreferrer">'
          'https://doi.org/10.1007/s10459-007-9090-2</a>')
R_MAF = ('Mafinejad, M. K., Ebrahimpour, F., Sayarifard, A., Shahbazi, F., &amp; Gruppen, L. (2022). Reflection on '
         "near-peer shadowing program: Impact on operating room student's perception of their future profession. "
         '<em>BMC Medical Education, 22</em>. <a class="src" href="https://doi.org/10.1186/s12909-022-03891-w" '
         'target="_blank" rel="noopener noreferrer">https://doi.org/10.1186/s12909-022-03891-w</a>')
R_ESTES = ('Estes, M., et al. (2026). From fly on the wall to future colleagues: Best practice recommendations for '
           'medical student shadowing programs. <em>AEM Education and Training, 10</em>(3). '
           '<a class="src" href="https://doi.org/10.1002/aet2.70214" target="_blank" rel="noopener noreferrer">'
           'https://doi.org/10.1002/aet2.70214</a>')
R_KITSIS = ('Kitsis, E. A., &amp; Goldsammler, M. (2013). Physician shadowing: A review of the literature and proposal '
            'for guidelines. <em>Academic Medicine, 88</em>(1), 102&ndash;110. '
            '<a class="src" href="https://doi.org/10.1097/ACM.0b013e318277d5b2" target="_blank" rel="noopener noreferrer">'
            'https://doi.org/10.1097/ACM.0b013e318277d5b2</a>')
R_BAV = ('Baveja, Fonkeu, &amp; Kelly. (2024). The value of medical shadowing for high school students: A '
         'three-dimensional view. <em>Medical Teacher, 46</em>(4), 584&ndash;589. '
         '<a class="src" href="https://doi.org/10.1080/0142159X.2023.2243024" target="_blank" rel="noopener noreferrer">'
         'https://doi.org/10.1080/0142159X.2023.2243024</a>')
R_KEN = ("Kendrick, Withey, Batson, Wright, &amp; O'Rourke. (2020). Predictors of satisfying and impactful clinical "
         'shadowing experiences for underrepresented minority high school students interested in healthcare careers. '
         '<em>Journal of the National Medical Association, 112</em>(4), 381&ndash;386. '
         '<a class="src" href="https://doi.org/10.1016/j.jnma.2020.04.007" target="_blank" rel="noopener noreferrer">'
         'https://doi.org/10.1016/j.jnma.2020.04.007</a>')


def c(n):
    return f'<a class="cite" href="#r{n}"><span class="sr-only">See reference </span>{n}</a>'


# ---------------------------------------------------------------- index
def index():
    b = dict((l, t) for l, t, *_ in BARRIERS)
    time_n, struct_n, pol_n = b["Lack of physician time"], b["Lack of formal shadowing structure"], b["Hospital or institutional policies"]
    likely_hi = LIKELY[3] + LIKELY[4]
    handbook = RESOURCES[0][1]
    return head("Shadow Pre-MD | A Free Shadowing Guide for High School Students",
                "A free guide to medical shadowing for high school students, built from a survey of 43 practicing physicians and five peer-reviewed studies.") + nav("index.html") + f"""
<main id="main">

<header class="hero">
  <div class="wrap split">
    <div>
      <span class="eyebrow">A free guide for high school students considering medicine</span>
      <h1>Make every shadowing day count.</h1>
      <p class="lede">Shadow Pre-MD shows students how to prepare for a day with a physician, what to watch for, and which questions to ask. It is built on what 43 practicing physicians said about the students they host.</p>
      <div class="btn-row">
        <a href="guide.html" class="btn">Get the free guide</a>
        <a href="survey.html" class="btn ghost">See the survey</a>
      </div>
    </div>
    <aside class="hero-panel" aria-label="Headline survey findings">
      <span class="eyebrow">What 43 physicians said</span>
      <ul class="hp-rows">
        <li><div class="top"><span class="n">{pct(likely_hi)}%</span><span class="t">would likely host a high school student if the right resources were in place</span></div><div class="track"><span class="fill" style="width:{pct(likely_hi)}%"></span></div></li>
        <li><div class="top"><span class="n">{pct(handbook)}%</span><span class="t">want students to arrive with an orientation handbook</span></div><div class="track"><span class="fill" style="width:{pct(handbook)}%"></span></div></li>
        <li><div class="top"><span class="n">{pct(FACTORS[1][1])}%</span><span class="t">said the ability to ask questions is what makes shadowing meaningful</span></div><div class="track"><span class="fill" style="width:{pct(FACTORS[1][1])}%"></span></div></li>
      </ul>
      <p class="src">Source: physician survey, 2026. <a href="results.html">See every answer</a></p>
    </aside>
  </div>
</header>

<section id="problem" class="band">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">The problem</span>
      <h2>Why a shadowing spot is so hard to get and so easy to waste</h2>
      <p>Most high schoolers interested in medicine email physician after physician for a single day in a clinic. Many come away frustrated by how few chances exist and disappointed by how little the day taught them. Physicians explained why.{c(1)}</p>
    </div>
    <div class="cards">
      <div class="card problem">
        <div class="icon">{ICON_CLOCK}</div>
        <p class="num">{pct(time_n)}%</p>
        <h3>Physicians are out of time</h3>
        <p>Time was the barrier physicians named most. A doctor with a full clinic has few minutes left to explain what a student is watching.</p>
        <p class="of">{time_n} of {N} physicians</p>
      </div>
      <div class="card problem">
        <div class="icon">{ICON_MAP}</div>
        <p class="num">{pct(struct_n)}%</p>
        <h3>Nobody wrote the playbook</h3>
        <p>More than half said no formal shadowing structure exists, so each visit gets improvised by a physician and a student who have never done it together.</p>
        <p class="of">{struct_n} of {N} physicians</p>
      </div>
      <div class="card problem">
        <div class="icon">{ICON_LOCK}</div>
        <p class="num">{pct(pol_n)}%</p>
        <h3>Hospital rules block the door</h3>
        <p>Half pointed to institutional policies, and just as many to patient privacy. Unclear rules make it safer for a physician to say no.</p>
        <p class="of">{pol_n} of {N} physicians, for each</p>
      </div>
    </div>
    <p class="punch">A student who is serious about medicine shouldn't have to email physicians endlessly with no hope of an answer.</p>
    <p>Students who never get a useful look at the work stay unsure about medicine, and they never form a strong picture of themselves as a physician.</p>
  </div>
</section>

<section id="control">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">What a student can change</span>
      <h2>Preparation is the one barrier a student controls</h2>
      <p>No student can give a doctor more hours or rewrite a hospital's policies. Showing up ready is different. It is also what worries the physicians who have never said yes.{c(1)}</p>
    </div>
    <div class="charts">
      <figure class="chart">
        <h3>Who worries about student preparedness</h3>
        <p class="sub">Share naming it as a barrier, by hosting experience</p>
        <ul class="bars">
          <li class="hl" title="Never hosted: 9 of 16 (56%)"><div class="lab"><span>Physicians who have never hosted</span><span class="val">9 of 16<b>56%</b></span></div><div class="track"><span class="fill" style="width:56%"></span></div></li>
          <li title="Has hosted: 6 of 27 (22%)"><div class="lab"><span>Physicians who have hosted</span><span class="val">6 of 27<b>22%</b></span></div><div class="track"><span class="fill" style="width:22%"></span></div></li>
        </ul>
        <p class="foot">Small groups, so treat the gap as a lead worth testing (Fisher exact p = .045).</p>
      </figure>
      <figure class="chart">
        <h3>What physicians asked for most</h3>
        <p class="sub">Top requested resources, all 43 physicians</p>
        {bars(RESOURCES[:4])}
      </figure>
    </div>
    <div class="btn-row"><a href="results.html" class="btn ghost">See every question and answer</a></div>
  </div>
</section>

<section id="about" class="band">
  <div class="wrap split flip">
    <div class="about-photo">
      <img src="images/zoha.webp" width="1000" height="1250" alt="Zoha, standing outdoors in a light blue shirt with pine trees and hills behind her" loading="lazy" decoding="async">
    </div>
    <div class="about-text">
      <span class="eyebrow">About the guide</span>
      <h2>Meet Zoha</h2>
      <p class="name-line">I'm Zoha Waheed, and I went through the same search.</p>
      <p>I walked into my first endocrinology clinic knowing little more than what Google had told me the week before. Since then I have shadowed seven physicians across endocrinology, rheumatology, pulmonology, and infectious disease. Even once I had those opportunities, I found it difficult to get the most out of them.</p>
      <p>So I went looking for answers. I read five peer-reviewed studies on clinical shadowing, surveyed 43 practicing physicians about what helps and what gets in the way, and submitted my findings as a research abstract to the 2027 Medical Education Innovation Conference. I put what I learned into this guide so the next student can walk in prepared.</p>
    </div>
  </div>
  <div class="wrap">
    <ul class="strip">
      <li><span class="n">7</span><span class="t">physicians shadowed across four specialties</span></li>
      <li><span class="n">5</span><span class="t">peer-reviewed studies reviewed</span></li>
      <li><span class="n">43</span><span class="t">practicing physicians surveyed</span></li>
    </ul>
  </div>
</section>

<section id="plan">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">The plan</span>
      <h2>Three steps to a shadowing day that counts</h2>
      <p>You have done the hard part if a physician has said yes. Here is how to make the day worth it.</p>
    </div>
    <ol class="steps">
      <li>
        <h3>Download the free guide</h3>
        <p>It costs nothing. Save it before your first day in the clinic.</p>
      </li>
      <li>
        <h3>Follow each step</h3>
        <p>Work through the guide one step at a time.</p>
      </li>
      <li>
        <h3>Get more from your shadowing</h3>
        <p>Walk out knowing more about medicine and about whether you want it.</p>
      </li>
    </ol>
    <div class="promise">
      <span class="eyebrow">My promise</span>
      <p>If you read through the guide and follow its steps, you will take away something useful from your shadowing.</p>
    </div>
    <div class="btn-row">
      <a href="guide.html" class="btn">Get the free guide</a>
    </div>
  </div>
</section>

<section id="value" class="band">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">What makes shadowing meaningful</span>
      <h2>Physicians rank questions far above procedures</h2>
      <p>I asked physicians which factors matter most to a student's experience. Watching patient care and asking about it came out on top. Seeing a procedure landed near the bottom.{c(1)}</p>
    </div>
    <figure class="chart">
      <h3>Factors physicians called most important</h3>
      <p class="sub">Share of 43 physicians selecting each factor</p>
      {bars(FACTORS, hl=("Ability to ask questions",), muted=("Exposure to medical procedures",))}
    </figure>
    <p class="note">The takeaway for a student: a quiet clinic day with a physician who answers questions is worth more than a dramatic one in the operating room.</p>
  </div>
</section>

<section id="habits">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">What the studies found</span>
      <h2>Three habits the research backs</h2>
      <p>The guide also leans on published studies of students in clinical settings. These findings came up again and again.</p>
    </div>
    <div class="cards">
      <div class="card">
        <h3>Write about each day</h3>
        <p>Keep a journal or take notes while you shadow. Written reflection helps students analyze what they saw and spot what they still need to learn.{c(2)}{c(3)}</p>
      </div>
      <div class="card">
        <h3>Ask your questions</h3>
        <p>Students who take the initiative and ask, instead of staying silent, get more value from the experience.{c(4)}</p>
      </div>
      <div class="card">
        <h3>Know the plan for the day</h3>
        <p>Shadowing works better when the student is introduced to the team and the patients, and a clear structure is set from the start.{c(4)}</p>
      </div>
    </div>
  </div>
</section>

<section id="why" class="band">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Why this guide exists</span>
      <h2>Physicians want to teach. They need students who come ready.</h2>
    </div>
    <div class="explain">
      <p>A shadowing day is your first real look at the career you are thinking about giving your life to. Physicians want to give you that look. In the survey, {likely_hi} of {N} said they would likely host a student if the right resources existed, and {USEFUL[3] + USEFUL[4]} of {N} rated standardized shadowing guidelines as highly useful.</p>
      <p>Their days are short on time, and their hospitals have given them no structure to follow. That is why the student who arrives prepared, asks good questions, and writes down what they saw gets so much more out of the same day. Shadow Pre-MD shows you how to be that student.</p>
    </div>
  </div>
</section>

<section class="after">
  <div class="wrap split">
    <div>
      <span class="eyebrow">After a good shadowing experience</span>
      <h2>From frustrated to certain about what comes next</h2>
      <p>I started this search disappointed and frustrated. A day used well can settle the question you came in with.</p>
      <div class="btn-row">
        <a href="guide.html" class="btn light">Get the free guide</a>
      </div>
    </div>
    <ul class="outcomes">
      <li>{CHECK}<span>Make up your mind about medicine.</span></li>
      <li>{CHECK}<span>Find a specialty you can see yourself in.</span></li>
      <li>{CHECK}<span>Learn what a physician's day-to-day life looks like.</span></li>
      <li>{CHECK}<span>Bring a sharper focus to the rest of your schooling.</span></li>
    </ul>
  </div>
</section>

<section class="closing">
  <div class="wrap">
    <h2>Make your next shadowing day count</h2>
    <p>The guide is free. Read it before you walk into the clinic.</p>
    <div class="btn-row">
      <a href="guide.html" class="btn">Get the free guide</a>
    </div>
  </div>
</section>
{refs([R_WAHEED, R_MANN, R_MAF, R_ESTES])}
</main>
""" + FOOT


# ---------------------------------------------------------------- survey
def sec(num, title, kicker, lead):
    return f"""<div class="sec-head">
      <span class="sec-num" aria-hidden="true">{num}</span>
      <div><h2>{title}</h2><p class="kicker">{kicker}</p></div>
    </div>
    <p class="lead">{lead}</p>"""


def stats(items):
    tones = ("rust", "teal", "gold")
    out = ['<ul class="stats">']
    for i, (n, t) in enumerate(items):
        out.append(f'  <li class="{tones[i % 3]}"><span class="n">{n}</span><span class="t">{t}</span></li>')
    out.append("</ul>")
    return "\n".join(out)


def donut(segments, center, caption, label):
    """segments: [(name, count, colour)]. Drawn clockwise from 12 o'clock."""
    total = sum(n for _, n, _ in segments)
    r, circ = 54, 2 * 3.14159265 * 54
    arcs, legend, off = [], [], 0.0
    for name, n, col in segments:
        length = circ * n / total
        arcs.append(f'<circle cx="70" cy="70" r="{r}" fill="none" stroke="{col}" stroke-width="22" '
                    f'stroke-dasharray="{max(length - 2.5, 0):.2f} {circ - max(length - 2.5, 0):.2f}" '
                    f'stroke-dashoffset="{-off:.2f}"/>')
        legend.append(f'<li><span class="sw" style="background:{col}"></span>{name} ({n})</li>')
        off += length
    return (f'<div class="donut"><svg viewBox="0 0 140 140" role="img" aria-label="{label}">'
            f'<g transform="rotate(-90 70 70)">{"".join(arcs)}</g></svg>'
            f'<div class="mid"><span class="n">{center}</span><span class="t">{caption}</span></div></div>'
            f'<ul class="legend center">{"".join(legend)}</ul>')


def quote(text, who=""):
    cite = f"<cite>{who}</cite>" if who else ""
    return f'<blockquote class="band-quote"><p>{text}</p>{cite}</blockquote>'


DK, MID, GREY = "#0F4C5C", "#008A9E", "#A9B9C1"


def survey():
    useful_hi = USEFUL[3] + USEFUL[4]
    likely_hi = LIKELY[3] + LIKELY[4]
    b = dict((l, (t, nv, hs)) for l, t, nv, hs in BARRIERS)
    time_n = b["Lack of physician time"][0]
    return head("The Physician Survey | Shadow Pre-MD",
                "What 43 practicing physicians said about hosting high school students: the barriers, the resources they want, and what makes shadowing meaningful.") + nav("survey.html") + f"""
<main id="main">

<header class="page-hero">
  <div class="wrap">
    <span class="eyebrow">The physician survey</span>
    <h1>I asked 43 physicians why shadowing is so hard to get right</h1>
    <p class="lede">Students can't fix a problem nobody has measured. So I surveyed practicing physicians about what stops them from hosting high schoolers, what makes a shadowing day worth it, and what would help. Here is what they told me.</p>
    <div class="btn-row">
      <a href="guide.html" class="btn">Get the free guide</a>
      <a href="results.html" class="btn ghost">See every question and answer</a>
    </div>
  </div>
</header>

<section class="band" id="open">
  <div class="wrap">
    {sec("01", "The Door Is Open", "Physicians want to teach",
         "Most of the physicians I surveyed want students in their clinics. More than half chose the highest possible rating when I asked how likely they would be to host a student with the right support. The willingness is already there. Everything around it is missing.")}
    {stats([(f"{pct(likely_hi)}%", "would likely host a high school student if the right resources were available."),
            (f"{pct(useful_hi)}%", "rated standardized shadowing guidelines a 4 or 5 out of 5 for usefulness."),
            (f"{LIKELY[4]} of {N}", "chose the top rating of 5 on each of the two questions.")])}
    <div class="charts duo">
      <figure class="chart">
        <h3>Likelihood of hosting with resources</h3>
        <p class="sub">Rating out of 5, all 43 physicians</p>
        {donut([("Rating 5", LIKELY[4], DK), ("Rating 4", LIKELY[3], MID), ("Rating 3 or lower", sum(LIKELY[:3]), GREY)],
               f"{pct(likely_hi)}%", "rated 4 or 5", "72 percent of physicians rated their likelihood of hosting a 4 or 5")}
      </figure>
      <figure class="chart">
        <h3>Usefulness of standardized guidelines</h3>
        <p class="sub">Number of physicians choosing each rating</p>
        {columns(USEFUL, "Not useful", "Very useful")}
      </figure>
    </div>
    {quote("High school students shouldn't have to endlessly email physicians with no hope of finding any shadowing opportunities.", "Zoha Waheed")}
  </div>
</section>

<section id="barriers">
  <div class="wrap">
    {sec("02", "What Stands in the Way", "Time, structure, and red tape",
         "When I asked what gets in the way, time came first. A physician with a full clinic has few minutes to spare. Look past time, though, and the next four barriers all describe the same gap: no program to follow, unclear hospital policies, and no guidance on privacy or liability. A well-built program can close that gap.")}
    {stats([(f"{pct(time_n)}%", f"named lack of physician time, the most common barrier ({time_n} of {N})."),
            (f"{pct(24)}%", "said no formal shadowing structure exists for them to follow."),
            ("22 + 22", "named hospital policies and patient privacy, tied for third.")])}
    <div class="charts duo">
      <figure class="chart">
        <h3>The leading barrier</h3>
        <p class="sub">Physicians naming lack of time</p>
        {donut([("Named time", time_n, "#C2571F"), ("Did not", N - time_n, GREY)],
               f"{pct(time_n)}%", "short on time", "79 percent of physicians named lack of time as a barrier")}
      </figure>
      <figure class="chart">
        <h3>Every barrier physicians named</h3>
        <p class="sub">Share of 43 physicians selecting each</p>
        {bars([(l, t) for l, t, *_ in BARRIERS] + [BARRIERS_OTHER], hl=("Lack of physician time",), muted=("Other",))}
      </figure>
    </div>
    {quote("The four most common barriers after time all come down to missing rules and structure, and that is a problem someone can solve.")}
  </div>
</section>

<section class="band" id="never">
  <div class="wrap">
    {sec("03", "Who Stays Out", "The 16 physicians who have never hosted",
         "Sixteen of the physicians I surveyed had never hosted a high school student. They are the doctors students most need to reach, so I looked at what holds them back. Hospital policies and doubts about student preparedness worried them far more than they worried experienced hosts.")}
    {stats([("75%", "of never-hosts named hospital policies, against 37% of experienced hosts."),
            ("56%", "of never-hosts named student preparedness, against 22% of experienced hosts."),
            ("3.50", "average likelihood of hosting among never-hosts, against 4.56 for experienced hosts.")])}
    <figure class="chart">
      <h3>Barriers by hosting experience</h3>
      <p class="sub">Share of each group naming the barrier, sorted by the size of the gap</p>
      {dumbbell(BARRIERS)}
      <p class="foot">Only the top two gaps reach p &lt; .05 on a Fisher exact test (policies p = .027, preparedness p = .045), and no correction was made for running eight comparisons.</p>
    </figure>
    <div class="charts" style="margin-top:20px">
      <figure class="chart">
        <h3>Guidelines and willingness to host</h3>
        <p class="sub">Spearman correlation, by group</p>
        {rho_bars()}
      </figure>
      <figure class="chart">
        <h3>Likelihood of hosting with resources</h3>
        <p class="sub">Average rating out of 5, by group</p>
        <ul class="bars">
          <li class="hl" title="Never hosted: 3.50"><div class="lab"><span>Never hosted</span><span class="val"><b>3.50</b></span></div><div class="track"><span class="fill" style="width:70%"></span></div></li>
          <li title="Has hosted: 4.56"><div class="lab"><span>Has hosted</span><span class="val"><b>4.56</b></span></div><div class="track"><span class="fill" style="width:91.2%"></span></div></li>
        </ul>
        <p class="foot">Both groups rated guidelines about equally useful (4.13 and 4.33).</p>
      </figure>
    </div>
    {quote("Among physicians who had never hosted a student, the ones who saw the most value in clear guidelines were the most willing to say yes.")}
  </div>
</section>

<section id="meaning">
  <div class="wrap">
    {sec("04", "What Makes a Day Meaningful", "Questions over procedures",
         "Students often assume the best shadowing day is the one with the most dramatic procedure. Physicians see it differently. They told me the value comes from watching patient care up close and asking about it.")}
    {stats([(f"{FACTORS[0][1]} of {N}", "chose direct observation of patient care as a top factor."),
            (f"{FACTORS[1][1]} of {N}", "chose the ability to ask questions."),
            (f"{FACTORS[7][1]} of {N}", "chose exposure to medical procedures.")])}
    <div class="charts duo">
      <figure class="chart">
        <h3>The top factor</h3>
        <p class="sub">Physicians choosing direct observation</p>
        {donut([("Chose it", FACTORS[0][1], MID), ("Did not", N - FACTORS[0][1], GREY)],
               f"{pct(FACTORS[0][1])}%", "direct observation", "70 percent of physicians chose direct observation of patient care")}
      </figure>
      <figure class="chart">
        <h3>Factors physicians called most important</h3>
        <p class="sub">Share of 43 physicians selecting each</p>
        {bars(FACTORS, hl=("Ability to ask questions",), muted=("Exposure to medical procedures",))}
      </figure>
    </div>
    {quote("Even with shadowing opportunities, it was difficult to find a way to maximize their usefulness.", "Zoha Waheed")}
  </div>
</section>

<section class="band" id="asked">
  <div class="wrap">
    {sec("05", "What Physicians Asked For", "Prepared students and clear rules",
         "I asked physicians what would make hosting easier. Their top answer was a student who arrives already oriented. That answer is why Shadow Pre-MD exists. Preparation is the one part of this problem a student can solve alone.")}
    {stats([(f"{pct(RESOURCES[0][1])}%", "asked for a student orientation program or handbook."),
            (f"{pct(RESOURCES[1][1])}%", "asked for clear institutional guidelines on what students may observe."),
            (f"{pct(RESOURCES[2][1])}%", "asked for suggested questions or discussion topics.")])}
    <div class="charts duo">
      <figure class="chart">
        <h3>The top request</h3>
        <p class="sub">Physicians asking for a student handbook</p>
        {donut([("Asked for it", RESOURCES[0][1], DK), ("Did not", N - RESOURCES[0][1], GREY)],
               f"{pct(RESOURCES[0][1])}%", "want a handbook", "65 percent of physicians asked for a student orientation handbook")}
      </figure>
      <figure class="chart">
        <h3>Every resource physicians requested</h3>
        <p class="sub">Share of 43 physicians selecting each</p>
        {bars(RESOURCES, hl=("Student orientation program or handbook",))}
      </figure>
    </div>
    <h3 class="sub-h">Each barrier, beside the resource meant to solve it</h3>
    {pairs()}
    {quote("I promise if you read through our guide and follow its steps, you will be able to take away something useful from your shadowing.", "Zoha Waheed")}
  </div>
</section>

<section id="sample">
  <div class="wrap">
    {sec("06", "Who Answered", "Read these numbers with care",
         "I want these results read honestly. Forty-three physicians is enough to see patterns and too few to speak for every doctor. Most of my respondents practiced internal medicine, and physicians who answer a survey about shadowing may already care more about teaching.")}
    {stats([(f"{N}", "practicing physicians completed the survey."),
            (f"{HOSTS}", "had hosted a high school student before."),
            (f"{NEVER}", "had never hosted one.")])}
    <div class="charts">
      <figure class="chart">
        <h3>Hosting experience</h3>
        <p class="sub">Each mark is one physician</p>
        {LEGEND}
        {waffle()}
      </figure>
      <figure class="chart">
        <h3>Specialty</h3>
        <p class="sub">Number of physicians, out of 43</p>
        {bars(SPECIALTY, muted=("Other or not tabulated",))}
      </figure>
    </div>
    <ul class="limits" style="margin-top:20px">
      <li><h3>Small sample</h3><p>43 physicians can describe patterns. They cannot stand in for all physicians.</p></li>
      <li><h3>Weighted toward internal medicine</h3><p>24 of 43 respondents practiced internal medicine, and several specialties had three or fewer.</p></li>
      <li><h3>Who chose to answer</h3><p>Physicians willing to fill out a survey about shadowing may already care more about teaching students.</p></li>
      <li><h3>Stated intentions</h3><p>Saying you would host a student is different from hosting one.</p></li>
      <li><h3>One point in time</h3><p>A cross-sectional survey measures beliefs on one day and cannot establish cause.</p></li>
      <li><h3>Checkbox limits</h3><p>Some questions asked for up to three choices, and the form did not enforce the limit, so those counts are descriptive.</p></li>
    </ul>
  </div>
</section>

<section class="after glance">
  <div class="wrap">
    <span class="eyebrow">The survey in one glance</span>
    <h2>Physicians are willing. Students can meet them halfway.</h2>
    <ul class="glance-grid">
      <li><span class="n">{pct(time_n)}%</span><span class="t">named lack of time as a barrier</span></li>
      <li><span class="n">{pct(likely_hi)}%</span><span class="t">would likely host with the right resources</span></li>
      <li><span class="n">{pct(RESOURCES[0][1])}%</span><span class="t">asked for a student orientation handbook</span></li>
      <li><span class="n">{pct(FACTORS[1][1])}%</span><span class="t">said asking questions makes shadowing meaningful</span></li>
    </ul>
    <div class="btn-row">
      <a href="guide.html" class="btn light">Get the free guide</a>
      <a href="results.html" class="btn ghost on-dark">See every question and answer</a>
    </div>
  </div>
</section>
{refs([R_WAHEED, R_KITSIS, R_BAV, R_KEN], heading="The abstract and its background reading", band=False)}
</main>
""" + FOOT


# ---------------------------------------------------------------- results
def q(num, title, kind, body, foot=""):
    foot = f'\n      <p class="foot">{foot}</p>' if foot else ""
    return f"""
    <figure class="chart stack" id="q{num}">
      <span class="qnum">Question {num}</span>
      <h3>{title}</h3>
      <p class="sub">{kind}</p>
      {body}{foot}
    </figure>"""


def results():
    qs = []
    qs.append(q(1, "What is your medical specialty?", "One answer. Number of physicians out of 43.",
                bars(SPECIALTY, muted=("Other or not tabulated",)),
                "Five responses fell into other specialties or were not broken out."))
    qs.append(q(2, "Does your field involve procedures?", "One answer.",
                pbars([("Yes", 85), ("No", 15)]),
                "Reported in the abstract as a percentage."))
    qs.append(q(3, "What is your practice setting?", "One answer.",
                pbars(SETTING), "Reported in the abstract as percentages. The remaining 8% fell into other settings."))
    qs.append(q(4, "Have you ever supervised a high school student for a medical shadowing experience?", "One answer. Number of physicians out of 43.",
                bars([("Yes", HOSTS), ("No", NEVER)])))
    qs.append(q(5, "What activities do you typically allow high school students to participate in?", "Select all that apply.",
                pbars([("Discuss medical cases with the physician", 78), ("Observe patient encounters", 70)]),
                "Only the two leading activities have been tabulated for this question."))
    qs.append(q(6, "Which factors are most important for making a student's shadowing experience meaningful?",
                "Choose up to three. Share of 43 physicians selecting each.",
                bars(FACTORS), "The form did not enforce the limit of three, so some physicians chose more."))
    qs.append(q(7, "What are the biggest barriers to providing a meaningful shadowing experience?",
                "Select all that apply. Share of 43 physicians selecting each.",
                bars([(l, t) for l, t, *_ in BARRIERS] + [BARRIERS_OTHER], muted=("Other",))))
    qs.append(q(8, "Which resources would make it easier to provide a high-quality shadowing experience?",
                "Select all that apply. Share of 43 physicians selecting each.",
                bars(RESOURCES)))
    qs.append(q(9, "How useful would standardized guidelines for high school shadowing be?", "Scale from 1 to 5.",
                columns(USEFUL, "Not useful", "Very useful")))
    qs.append(q(10, "How likely would you be to host a high school student if appropriate resources were available?", "Scale from 1 to 5.",
                columns(LIKELY, "Not likely", "Very likely"),
                "40 of 43 (93%) chose 3 or higher. The stricter count of 4 or 5 is used across this site."))
    return head("Every Question and Answer | Shadow Pre-MD",
                "Question-by-question results from a survey of 43 practicing physicians on high school medical shadowing.") + nav("results.html") + f"""
<main id="main">

<header class="page-hero">
  <div class="wrap">
    <span class="eyebrow">The results</span>
    <h1>Every question, and how 43 physicians answered</h1>
    <p class="lede">Each chart below shows one survey question with the count and share for every answer. The second half breaks the answers down by whether the physician had hosted a student before.</p>
    <div class="btn-row">
      <a href="survey.html" class="btn ghost">Read the five findings</a>
      <a href="guide.html" class="btn">Get the free guide</a>
    </div>
  </div>
</header>

<section class="band" id="all">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">All 43 physicians</span>
      <h2>Question by question</h2>
      <p>Percentages are out of all 43 respondents unless the chart says otherwise.</p>
    </div>
{''.join(qs).replace('<figure class="chart stack" id="q1">', '<figure class="chart" id="q1">', 1)}
  </div>
</section>

<section id="groups">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">By hosting experience</span>
      <h2>How the two groups answered</h2>
      <p>{HOSTS} physicians had hosted a high school student and {NEVER} never had. Splitting the answers shows what keeps physicians from hosting for the first time.</p>
    </div>
    <figure class="chart">
      <span class="qnum">Question 7, by group</span>
      <h3>Barriers named by each group</h3>
      <p class="sub">Share of each group naming the barrier, sorted by the size of the gap</p>
      {dumbbell(BARRIERS)}
      {group_table()}
      <p class="foot">Shaded rows reach p &lt; .05. Eight comparisons were run with no correction, so these are leads to test in a larger sample.</p>
    </figure>
    <div class="charts" style="margin-top:20px">
      <figure class="chart">
        <span class="qnum">Question 9, by group</span>
        <h3>Usefulness of standardized guidelines</h3>
        <p class="sub">Average rating out of 5</p>
        <ul class="bars">
          <li class="hl" title="Never hosted: 4.13"><div class="lab"><span>Never hosted</span><span class="val"><b>4.13</b></span></div><div class="track"><span class="fill" style="width:82.6%"></span></div></li>
          <li title="Has hosted: 4.33"><div class="lab"><span>Has hosted</span><span class="val"><b>4.33</b></span></div><div class="track"><span class="fill" style="width:86.6%"></span></div></li>
        </ul>
      </figure>
      <figure class="chart">
        <span class="qnum">Question 10, by group</span>
        <h3>Likelihood of hosting with resources</h3>
        <p class="sub">Average rating out of 5</p>
        <ul class="bars">
          <li class="hl" title="Never hosted: 3.50"><div class="lab"><span>Never hosted</span><span class="val"><b>3.50</b></span></div><div class="track"><span class="fill" style="width:70%"></span></div></li>
          <li title="Has hosted: 4.56"><div class="lab"><span>Has hosted</span><span class="val"><b>4.56</b></span></div><div class="track"><span class="fill" style="width:91.2%"></span></div></li>
        </ul>
      </figure>
    </div>
    <figure class="chart stack">
      <span class="qnum">Questions 9 and 10 together</span>
      <h3>Link between guideline usefulness and willingness to host</h3>
      <p class="sub">Spearman correlation, by group</p>
      {rho_bars()}
      <p class="foot">Physicians who found guidelines more useful were more willing to host, and the link was strongest among those who had never hosted.</p>
    </figure>
    <div class="btn-row">
      <a href="guide.html" class="btn">Get the free guide</a>
      <a href="survey.html" class="btn ghost">Read the five findings</a>
    </div>
  </div>
</section>
{refs([R_WAHEED], heading="Source")}
</main>
""" + FOOT


if __name__ == "__main__":
    for name, fn in (("index.html", index), ("survey.html", survey), ("results.html", results)):
        with open(name, "w") as f:
            f.write(fn())
        print("wrote", name)
