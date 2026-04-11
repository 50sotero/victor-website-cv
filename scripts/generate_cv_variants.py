#!/usr/bin/env python3

from __future__ import annotations

import html
import re
from pathlib import Path
from typing import Any, Callable, cast

import yaml


ROOT = Path(__file__).resolve().parent.parent
CONTENT_PATH = ROOT / "data" / "content.yaml"
OUTPUT_DIR = ROOT / "artifacts" / "cv-variants"
JsonDict = dict[str, Any]
JsonList = list[JsonDict]

PAGE_CSS = """
  :root {
    --space-1: 0.25rem;
    --space-2: 0.5rem;
    --space-3: 0.75rem;
    --space-4: 1rem;
    --space-5: 1.5rem;
    --space-6: 2rem;
    --space-7: 2.75rem;
    --space-8: 4rem;
    --radius-sm: 0.5rem;
    --radius-md: 0.9rem;
    --radius-lg: 1.35rem;
    --radius-xl: 2rem;
    --shadow-soft: 0 24px 60px rgba(15, 23, 42, 0.12);
    --shadow-edge: 0 0 0 1px rgba(15, 23, 42, 0.08);
    --font-sans: 'Avenir Next', 'Segoe UI', 'Helvetica Neue', sans-serif;
    --font-serif: 'Iowan Old Style', 'Palatino Linotype', 'Book Antiqua', Georgia, serif;
    --font-display: 'Baskerville', 'Times New Roman', serif;
    --font-mono: 'SFMono-Regular', 'Cascadia Code', 'JetBrains Mono', monospace;
    --paper: #ffffff;
    --paper-alt: #f7f6f2;
    --ink: #111827;
    --muted: #5b6472;
    --line: rgba(15, 23, 42, 0.12);
    --accent: #0f766e;
    --accent-strong: #134e4a;
    --accent-soft: rgba(15, 118, 110, 0.14);
    --canvas: #ebe9e2;
  }

  * {
    box-sizing: border-box;
  }

  html {
    background: var(--canvas);
  }

  body {
    margin: 0;
    min-height: 100vh;
    padding: 24px;
    background: var(--canvas);
    color: var(--ink);
    font-family: var(--font-sans);
    line-height: 1.45;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  a {
    color: inherit;
    text-decoration: none;
  }

  p,
  ul,
  ol,
  h1,
  h2,
  h3,
  h4 {
    margin: 0;
  }

  ul {
    padding-left: 1.15rem;
  }

  li + li {
    margin-top: 0.28rem;
  }

  .document {
    width: min(100%, 210mm);
    min-height: 297mm;
    margin: 0 auto;
    background: var(--paper);
    box-shadow: var(--shadow-soft), var(--shadow-edge);
    position: relative;
    overflow: hidden;
  }

  .document-inner {
    position: relative;
    min-height: 297mm;
  }

  .eyebrow {
    font-size: 0.72rem;
    letter-spacing: 0.24em;
    text-transform: uppercase;
    color: var(--accent-strong);
  }

  .section-title {
    display: flex;
    align-items: center;
    gap: var(--space-3);
    margin-bottom: var(--space-4);
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--accent-strong);
  }

  .section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--line);
  }

  .stack-lg,
  .stack-md,
  .stack-sm,
  .stack-xs {
    display: grid;
  }

  .stack-lg {
    gap: var(--space-5);
  }

  .stack-md {
    gap: var(--space-4);
  }

  .stack-sm {
    gap: var(--space-3);
  }

  .stack-xs {
    gap: var(--space-2);
  }

  .muted {
    color: var(--muted);
  }

  .lede {
    font-size: 1rem;
    color: var(--muted);
  }

  .kicker {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
    padding: 0.4rem 0.75rem;
    border-radius: 999px;
    background: var(--accent-soft);
    color: var(--accent-strong);
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
  }

  .fact-list,
  .contact-list,
  .inline-list,
  .meta-list,
  .chip-list {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-2);
    padding-left: 0;
    list-style: none;
  }

  .fact-list li,
  .contact-list li,
  .inline-list li,
  .meta-list li,
  .chip-list li {
    margin: 0;
  }

  .pill,
  .chip,
  .metric,
  .contact-pill {
    border: 1px solid var(--line);
    border-radius: 999px;
    padding: 0.44rem 0.72rem;
    background: rgba(255, 255, 255, 0.84);
  }

  .chip {
    font-size: 0.78rem;
    background: var(--paper-alt);
  }

  .metric {
    min-width: 8rem;
    border-radius: var(--radius-md);
  }

  .metric strong {
    display: block;
    font-size: 1.3rem;
    margin-bottom: var(--space-1);
  }

  .metric span {
    display: block;
    color: var(--muted);
    font-size: 0.82rem;
  }

  .contact-pill {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
    font-size: 0.82rem;
  }

  .summary p + p {
    margin-top: var(--space-3);
  }

  .entry {
    display: grid;
    gap: var(--space-3);
    padding-bottom: var(--space-4);
    border-bottom: 1px solid var(--line);
    page-break-inside: avoid;
  }

  .entry:last-child {
    border-bottom: none;
    padding-bottom: 0;
  }

  .entry-head {
    display: flex;
    justify-content: space-between;
    gap: var(--space-4);
    align-items: flex-start;
  }

  .entry-company {
    font-size: 1.05rem;
    font-weight: 800;
  }

  .entry-role {
    margin-top: var(--space-1);
    color: var(--muted);
    font-weight: 600;
  }

  .entry-meta {
    display: grid;
    gap: var(--space-1);
    justify-items: end;
    text-align: right;
    color: var(--muted);
    font-size: 0.82rem;
    white-space: nowrap;
  }

  .entry-body {
    display: grid;
    gap: var(--space-3);
  }

  .entry-description {
    color: var(--muted);
  }

  .entry-highlights {
    margin: 0;
    color: var(--ink);
  }

  .entry-tech {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-2);
    list-style: none;
    padding: 0;
  }

  .entry-tech li {
    margin: 0;
    padding: 0.28rem 0.62rem;
    border-radius: 999px;
    background: var(--accent-soft);
    color: var(--accent-strong);
    font-size: 0.74rem;
    font-weight: 700;
    letter-spacing: 0.03em;
  }

  .project-card,
  .panel,
  .skill-card,
  .mini-card {
    border: 1px solid var(--line);
    border-radius: var(--radius-lg);
    padding: var(--space-4);
    background: rgba(255, 255, 255, 0.86);
    page-break-inside: avoid;
  }

  .project-card h3,
  .skill-card h3,
  .panel h3,
  .mini-card h3 {
    font-size: 1rem;
    margin-bottom: var(--space-2);
  }

  .project-impact {
    margin-top: var(--space-3);
    font-weight: 700;
    color: var(--accent-strong);
  }

  .skill-category {
    display: grid;
    gap: var(--space-3);
  }

  .skill-category h3 {
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }

  .skill-meter {
    display: grid;
    gap: 0.38rem;
  }

  .skill-meter-head {
    display: flex;
    justify-content: space-between;
    gap: var(--space-3);
    font-size: 0.82rem;
  }

  .skill-meter-track {
    height: 0.45rem;
    border-radius: 999px;
    background: rgba(15, 23, 42, 0.08);
    overflow: hidden;
  }

  .skill-meter-fill {
    height: 100%;
    border-radius: inherit;
    background: linear-gradient(90deg, var(--accent), var(--accent-strong));
  }

  .two-col,
  .three-col,
  .grid-cards,
  .grid-sidebar,
  .grid-projects {
    display: grid;
    gap: var(--space-5);
  }

  .two-col {
    grid-template-columns: minmax(0, 1fr) minmax(16rem, 0.72fr);
  }

  .three-col {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  .grid-cards {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .grid-projects {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .grid-sidebar {
    grid-template-columns: minmax(15rem, 0.78fr) minmax(0, 1.22fr);
  }

  .timeline {
    position: relative;
    display: grid;
    gap: var(--space-4);
    padding-left: var(--space-5);
  }

  .timeline::before {
    content: '';
    position: absolute;
    left: 0.42rem;
    top: 0.35rem;
    bottom: 0.35rem;
    width: 2px;
    background: linear-gradient(180deg, var(--accent), transparent 100%);
  }

  .timeline-item {
    position: relative;
  }

  .timeline-item::before {
    content: '';
    position: absolute;
    left: calc(-1 * var(--space-5) + 0.15rem);
    top: 0.45rem;
    width: 0.65rem;
    height: 0.65rem;
    border-radius: 999px;
    background: var(--accent);
    box-shadow: 0 0 0 0.28rem var(--paper), 0 0 0 0.4rem var(--accent-soft);
  }

  .compact-table {
    width: 100%;
    border-collapse: collapse;
  }

  .compact-table td {
    padding: 0.44rem 0;
    vertical-align: top;
    border-bottom: 1px solid var(--line);
  }

  .compact-table tr:last-child td {
    border-bottom: none;
  }

  .compact-table td:first-child {
    width: 8.5rem;
    font-weight: 700;
    color: var(--accent-strong);
  }

  .formal-rule {
    height: 1px;
    background: var(--line);
  }

  .small {
    font-size: 0.82rem;
  }

  .micro {
    font-size: 0.74rem;
  }

  .uppercase {
    text-transform: uppercase;
    letter-spacing: 0.14em;
  }

  @page {
    size: A4;
    margin: 10mm;
  }

  @media print {
    html,
    body {
      background: #fff;
      padding: 0;
    }

    .document {
      width: auto;
      min-height: auto;
      box-shadow: none;
      margin: 0;
    }

    .document-inner {
      min-height: auto;
    }

    .ats-minimal .stack-lg,
    .ats-minimal .stack-md,
    .ats-minimal .stack-sm,
    .ats-minimal .stack-xs,
    .ats-minimal .grid-cards,
    .ats-minimal .grid-projects {
      display: block !important;
    }

    .ats-minimal .stack-lg > * + *,
    .ats-minimal .stack-md > * + *,
    .ats-minimal .stack-sm > * + *,
    .ats-minimal .stack-xs > * + *,
    .ats-minimal .grid-cards > * + *,
    .ats-minimal .grid-projects > * + * {
      margin-top: var(--space-4) !important;
    }
  }

  @media (max-width: 960px) {
    body {
      padding: 0;
    }

    .document {
      width: 100%;
      border-radius: 0;
    }

    .two-col,
    .three-col,
    .grid-cards,
    .grid-sidebar,
    .grid-projects {
      grid-template-columns: 1fr;
    }
  }
"""


def esc(value: object) -> str:
    return html.escape(str(value or ""))


def lines_to_paragraphs(text: str) -> str:
    parts = [
        block.strip()
        for block in str(text or "").strip().split("\n\n")
        if block.strip()
    ]
    return "".join(f"<p>{esc(part)}</p>" for part in parts)


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def format_role(role: str, via: str | None) -> str:
    if via:
        return f'{esc(role)} <span class="muted">({esc(via)})</span>'
    return esc(role)


def render_contacts(personal: JsonDict, class_name: str = "contact-list") -> str:
    items: list[str] = [
        f'<li><span class="contact-pill">{esc(personal["email"])}</span></li>',
        f'<li><span class="contact-pill">{esc(personal["location"])}</span></li>',
        f'<li><a class="contact-pill" href="{esc(personal["linkedin"])}">LinkedIn</a></li>',
        f'<li><a class="contact-pill" href="{esc(personal["github"])}">GitHub</a></li>',
    ]
    whatsapp = personal.get("whatsapp", {})
    for number in whatsapp.get("numbers", []):
        items.append(
            f'<li><a class="contact-pill" href="tel:{esc(number.get("tel", ""))}">{esc(number.get("label", "Phone"))}: {esc(number.get("display", ""))}</a></li>'
        )
    return f'<ul class="{class_name}">' + "".join(items) + "</ul>"


def render_summary(summary: str, title: str = "Professional Summary") -> str:
    return (
        '<section class="stack-sm">'
        f'<div class="section-title">{esc(title)}</div>'
        f'<div class="summary lede">{lines_to_paragraphs(summary)}</div>'
        "</section>"
    )


def render_experience(
    entries: JsonList, *, timeline: bool = False, dense: bool = False
) -> str:
    wrapper_class = "timeline" if timeline else "stack-lg"
    blocks = []
    for item in entries:
        company = esc(item.get("company", ""))
        role = format_role(item.get("role", ""), item.get("via"))
        date = esc(
            f"{item.get('start_date', '')} - {item.get('end_date', '')}".strip(" -")
        )
        location = esc(item.get("location", ""))
        description = item.get("description")
        description_html = (
            f'<p class="entry-description">{esc(description)}</p>'
            if description
            else ""
        )
        highlights = "".join(
            f"<li>{esc(point)}</li>" for point in item.get("highlights", [])
        )
        tech = "".join(f"<li>{esc(name)}</li>" for name in item.get("tech_stack", []))
        entry_class = "entry timeline-item" if timeline else "entry"
        if dense:
            entry_class += " small"
        blocks.append(
            f'''
            <article class="{entry_class}">
              <div class="entry-head">
                <div>
                  <h3 class="entry-company">{company}</h3>
                  <div class="entry-role">{role}</div>
                </div>
                <div class="entry-meta">
                  <span>{date}</span>
                  <span>{location}</span>
                </div>
              </div>
              <div class="entry-body">
                {description_html}
                <ul class="entry-highlights">{highlights}</ul>
                <ul class="entry-tech">{tech}</ul>
              </div>
            </article>
            '''
        )
    return (
        '<section class="stack-sm">'
        '<div class="section-title">Professional Experience</div>'
        f'<div class="{wrapper_class}">{"".join(blocks)}</div>'
        "</section>"
    )


def render_projects(projects: JsonList, *, cards: bool = True) -> str:
    items = []
    for project in projects:
        tech = "".join(
            f'<li class="chip">{esc(name)}</li>' for name in project.get("tech", [])
        )
        class_name = "project-card" if cards else "entry"
        items.append(
            f'''
            <article class="{class_name}">
              <h3>{esc(project.get("name", ""))}</h3>
              <p class="muted">{esc(project.get("description", ""))}</p>
              <p class="project-impact">{esc(project.get("impact", ""))}</p>
              <ul class="chip-list">{tech}</ul>
            </article>
            '''
        )
    container_class = "grid-projects" if cards else "stack-md"
    return (
        '<section class="stack-sm">'
        '<div class="section-title">Selected Projects</div>'
        f'<div class="{container_class}">{"".join(items)}</div>'
        "</section>"
    )


def render_skills(
    skills: JsonList, *, meters: bool = False, compact: bool = False
) -> str:
    blocks = []
    for category in skills:
        if meters:
            items = "".join(
                f"""
                <div class="skill-meter">
                  <div class="skill-meter-head"><span>{esc(item.get("name", ""))}</span><span class="muted">{esc(item.get("level", ""))}%</span></div>
                  <div class="skill-meter-track"><div class="skill-meter-fill" style="width: {esc(item.get("level", 0))}%"></div></div>
                </div>
                """
                for item in category.get("items", [])
            )
        else:
            items = (
                '<ul class="chip-list">'
                + "".join(
                    f'<li class="chip">{esc(item.get("name", ""))}</li>'
                    for item in category.get("items", [])
                )
                + "</ul>"
            )
        card_class = "skill-card" if not compact else "panel small"
        blocks.append(
            f'<article class="{card_class}"><h3>{esc(category.get("category", ""))}</h3>{items}</article>'
        )
    container_class = "stack-sm" if compact else "grid-cards"
    return (
        '<section class="stack-sm">'
        '<div class="section-title">Skills & Tools</div>'
        f'<div class="{container_class}">{"".join(blocks)}</div>'
        "</section>"
    )


def render_education(items: JsonList) -> str:
    rows = []
    for item in items:
        meta_bits = [
            item.get("degree", ""),
            item.get("field", ""),
            item.get("location", ""),
            item.get("dates", ""),
        ]
        meta = " · ".join(esc(bit) for bit in meta_bits if bit)
        rows.append(
            f'<article class="mini-card"><h3>{esc(item.get("institution", ""))}</h3><p class="muted">{meta}</p></article>'
        )
    return (
        '<section class="stack-sm"><div class="section-title">Education</div><div class="stack-sm">'
        + "".join(rows)
        + "</div></section>"
    )


def render_certifications(items: JsonList) -> str:
    rows = "".join(
        f'<li class="pill"><strong>{esc(item.get("name", ""))}</strong><br><span class="muted small">{esc(item.get("issuer", ""))}</span></li>'
        for item in items
    )
    return (
        '<section class="stack-sm"><div class="section-title">Certifications</div><ul class="chip-list">'
        + rows
        + "</ul></section>"
    )


def render_languages(items: JsonList) -> str:
    rows = "".join(
        f'<li class="pill"><strong>{esc(item.get("name", ""))}</strong><br><span class="muted small">{esc(item.get("level", ""))}</span></li>'
        for item in items
    )
    return (
        '<section class="stack-sm"><div class="section-title">Languages</div><ul class="chip-list">'
        + rows
        + "</ul></section>"
    )


def render_publications(items: JsonList) -> str:
    if not items:
        return ""
    cards = "".join(
        f'<article class="mini-card"><h3>{esc(item.get("title", ""))}</h3><p class="muted">{esc(item.get("venue", ""))} · {esc(item.get("year", ""))}</p><p class="small"><a href="{esc(item.get("url", "#"))}">{esc(item.get("url", ""))}</a></p></article>'
        for item in items
    )
    return (
        '<section class="stack-sm"><div class="section-title">Publication</div><div class="stack-sm">'
        + cards
        + "</div></section>"
    )


def render_profile_facts(data: JsonDict) -> str:
    personal = data["personal"]
    metrics = [
        ("Current role", personal["title"]),
        ("Base", personal["location"]),
        ("Signature stack", personal["tagline"]),
    ]
    cards = "".join(
        f'<li class="metric"><strong>{esc(label)}</strong><span>{esc(value)}</span></li>'
        for label, value in metrics
    )
    return '<ul class="fact-list">' + cards + "</ul>"


def executive_split(data: JsonDict) -> str:
    personal = data["personal"]
    return f"""
    <div class="document executive-split">
      <div class="document-inner" style="padding: var(--space-7);">
        <div class="two-col">
          <div class="stack-lg">
            <div class="stack-md">
              <span class="kicker">Executive split</span>
              <div class="stack-sm">
                <div class="eyebrow">Victor Sotero</div>
                <h1 style="font-size: 3.3rem; line-height: 0.95;">{esc(personal["title"])}</h1>
                <p class="lede">{esc(personal["tagline"])}</p>
              </div>
              {render_profile_facts(data)}
            </div>
            {render_summary(data["summary"])}
            {render_experience(data["experience"])}
          </div>
          <aside class="stack-lg">
            <section class="panel stack-sm">
              <div class="section-title">Contact</div>
              {render_contacts(personal)}
            </section>
            {render_projects(data["projects"])}
            {render_skills(data["skills"], meters=True)}
            {render_education(data["education"])}
            {render_certifications(data["certifications"])}
            {render_languages(data["languages"])}
          </aside>
        </div>
      </div>
    </div>
    """


def editorial_single_column(data: JsonDict) -> str:
    personal = data["personal"]
    return f'''
    <div class="document editorial-single" style="--paper:#faf6ef; --paper-alt:#f2ece2; --canvas:#d8d0c2; --accent:#a16207; --accent-strong:#713f12; --accent-soft:rgba(161, 98, 7, 0.12);">
      <div class="document-inner" style="padding: var(--space-8) var(--space-7); font-family: var(--font-serif);">
        <header class="stack-md" style="border-bottom: 3px solid var(--ink); padding-bottom: var(--space-6); margin-bottom: var(--space-6);">
          <span class="eyebrow">Editorial single-column</span>
          <div class="three-col" style="align-items:end;">
            <div style="grid-column: span 2;" class="stack-sm">
              <h1 style="font-family: var(--font-display); font-size: 4rem; line-height: 0.92; font-weight: 600;">Victor Sotero</h1>
              <p style="font-size: 1.35rem; max-width: 38rem;">{esc(personal["title"])} shaping resilient data systems across automotive, retail, finance, and cloud transformation.</p>
            </div>
            <div class="stack-xs small">
              <div>{esc(personal["location"])}</div>
              <div>{esc(personal["email"])}</div>
              <div><a href="{esc(personal["linkedin"])}">LinkedIn</a></div>
              <div><a href="{esc(personal["github"])}">GitHub</a></div>
            </div>
          </div>
        </header>
        <main class="stack-lg">
          {render_summary(data["summary"], title="Opening note")}
          {render_experience(data["experience"])}
          {render_projects(data["projects"], cards=False)}
          <div class="two-col">
            <div class="stack-lg">
              {render_skills(data["skills"])}
            </div>
            <div class="stack-lg">
              {render_education(data["education"])}
              {render_certifications(data["certifications"])}
              {render_languages(data["languages"])}
              {render_publications(data.get("publications", []))}
            </div>
          </div>
        </main>
      </div>
    </div>
    '''


def technical_dense(data: JsonDict) -> str:
    personal = data["personal"]
    return f"""
    <div class="document technical-dense" style="--paper:#f7fafc; --paper-alt:#edf2f7; --canvas:#cbd5e1; --accent:#0f766e; --accent-strong:#134e4a;">
      <div class="document-inner" style="padding: var(--space-6); font-family: var(--font-mono);">
        <header class="panel stack-md" style="border-radius: var(--radius-xl); background: linear-gradient(135deg, #0f172a, #134e4a); color: white; border: none;">
          <div class="eyebrow" style="color: rgba(255,255,255,0.72);">Technical dense</div>
          <div class="two-col" style="grid-template-columns: 1.4fr 0.8fr; gap: var(--space-4);">
            <div class="stack-sm">
              <h1 style="font-size: 2.3rem; line-height: 1;">{esc(personal["name"])}</h1>
              <p style="font-size: 1rem; color: rgba(255,255,255,0.82);">{esc(personal["title"])}</p>
              <p class="small" style="color: rgba(255,255,255,0.76);">{esc(personal["tagline"])}</p>
            </div>
            <div class="stack-xs small" style="justify-self:end; text-align:right; color: rgba(255,255,255,0.78);">
              <div>{esc(personal["location"])}</div>
              <div>{esc(personal["email"])}</div>
              <div>linkedin / github / whatsapp</div>
            </div>
          </div>
        </header>
        <main class="stack-lg" style="margin-top: var(--space-5);">
          <section class="panel stack-sm">
            <div class="section-title">System profile</div>
            <div class="summary small">{lines_to_paragraphs(data["summary"])}</div>
          </section>
          <div class="grid-sidebar">
            <div class="stack-md">
              {render_experience(data["experience"], dense=True)}
              {render_projects(data["projects"], cards=False)}
            </div>
            <div class="stack-md">
              {render_skills(data["skills"], meters=True, compact=True)}
              <section class="panel stack-sm">
                <div class="section-title">Reference data</div>
                <table class="compact-table small">
                  <tr><td>Location</td><td>{esc(personal["location"])}</td></tr>
                  <tr><td>Email</td><td>{esc(personal["email"])}</td></tr>
                  <tr><td>LinkedIn</td><td>{esc(personal["linkedin"])}</td></tr>
                  <tr><td>GitHub</td><td>{esc(personal["github"])}</td></tr>
                </table>
              </section>
              {render_education(data["education"])}
              {render_certifications(data["certifications"])}
              {render_languages(data["languages"])}
            </div>
          </div>
        </main>
      </div>
    </div>
    """


def project_first(data: JsonDict) -> str:
    personal = data["personal"]
    return f"""
    <div class="document project-first" style="--paper:#fffdfa; --paper-alt:#f8efe4; --canvas:#f0ddd0; --accent:#c2410c; --accent-strong:#7c2d12; --accent-soft:rgba(194, 65, 12, 0.12);">
      <div class="document-inner">
        <header style="padding: var(--space-7); background: radial-gradient(circle at top right, rgba(194,65,12,0.22), transparent 40%), linear-gradient(180deg, #fff1e8, #fffdfa); border-bottom: 1px solid var(--line);">
          <div class="stack-md">
            <span class="kicker">Project-first</span>
            <div class="two-col" style="grid-template-columns: 1.3fr 0.7fr; align-items:end;">
              <div class="stack-sm">
                <h1 style="font-size: 3.5rem; line-height: 0.96;">{esc(personal["name"])}</h1>
                <p style="font-size: 1.2rem; max-width: 36rem;">{esc(personal["title"])}</p>
                <p class="lede">A portfolio-forward CV centered on flagship data platform work and measurable enterprise impact.</p>
              </div>
              <div class="stack-xs">{render_contacts(personal, class_name="contact-list")}</div>
            </div>
          </div>
        </header>
        <main style="padding: var(--space-7);" class="stack-lg">
          {render_projects(data["projects"])}
          <div class="two-col">
            <div class="stack-lg">
              {render_experience(data["experience"])}
            </div>
            <div class="stack-lg">
              {render_summary(data["summary"], title="Profile")}
              {render_skills(data["skills"])}
              {render_education(data["education"])}
              {render_certifications(data["certifications"])}
              {render_languages(data["languages"])}
            </div>
          </div>
        </main>
      </div>
    </div>
    """


def ats_minimal(data: JsonDict) -> str:
    personal = data["personal"]
    return f"""
    <div class="document ats-minimal" style="--paper:#ffffff; --paper-alt:#ffffff; --canvas:#d4d4d4; --ink:#111111; --muted:#444444; --line:#c9c9c9; --accent:#111111; --accent-strong:#111111; --accent-soft:rgba(17,17,17,0.05);">
      <div class="document-inner" style="padding: 22mm 18mm; font-family: 'Trebuchet MS', var(--font-sans);">
        <header class="stack-sm" style="padding-bottom: var(--space-4); border-bottom: 2px solid var(--ink);">
          <h1 style="font-size: 2rem;">{esc(personal["name"])}</h1>
          <p style="font-size: 1rem; font-weight: 700;">{esc(personal["title"])}</p>
          <p class="small">{esc(personal["location"])} · {esc(personal["email"])} · {esc(personal["linkedin"])} · {esc(personal["github"])}</p>
        </header>
        <main class="stack-lg" style="margin-top: var(--space-5);">
          {render_summary(data["summary"])}
          {render_experience(data["experience"], dense=True)}
          {render_projects(data["projects"], cards=False)}
          {render_skills(data["skills"], compact=True)}
          {render_education(data["education"])}
          {render_certifications(data["certifications"])}
          {render_languages(data["languages"])}
          {render_publications(data.get("publications", []))}
        </main>
      </div>
    </div>
    """


def consulting_timeline(data: JsonDict) -> str:
    personal = data["personal"]
    return f"""
    <div class="document consulting-timeline" style="--paper:#fcfcfb; --paper-alt:#f1f5f9; --canvas:#dbe4ea; --accent:#0369a1; --accent-strong:#0f3a53; --accent-soft:rgba(3,105,161,0.12);">
      <div class="document-inner" style="padding: var(--space-7);">
        <header class="stack-md" style="margin-bottom: var(--space-6);">
          <span class="kicker">Consulting timeline</span>
          <div class="two-col" style="grid-template-columns: 1.1fr 0.9fr; align-items:start;">
            <div class="stack-sm">
              <h1 style="font-size: 3rem;">{esc(personal["name"])}</h1>
              <p style="font-size: 1.15rem;">{esc(personal["title"])}</p>
              <div class="summary lede"><p>Senior consultant perspective highlighting engagements, migration programs, governance work, and multi-client delivery through product and services organizations.</p></div>
            </div>
            <div class="panel stack-sm">
              <div class="section-title">Contact</div>
              {render_contacts(personal)}
            </div>
          </div>
        </header>
        <main class="grid-sidebar">
          <aside class="stack-lg">
            {render_summary(data["summary"], title="Consulting brief")}
            {render_skills(data["skills"], meters=True)}
            {render_projects(data["projects"], cards=False)}
          </aside>
          <section class="stack-lg">
            {render_experience(data["experience"], timeline=True)}
            <div class="grid-cards">
              {render_education(data["education"])}
              {render_certifications(data["certifications"])}
            </div>
            <div class="grid-cards">
              {render_languages(data["languages"])}
              {render_publications(data.get("publications", []))}
            </div>
          </section>
        </main>
      </div>
    </div>
    """


def sidebar_cards(data: JsonDict) -> str:
    personal = data["personal"]
    return f"""
    <div class="document sidebar-cards" style="--paper:#fbfbfd; --paper-alt:#eef2ff; --canvas:#d7d8ef; --accent:#4338ca; --accent-strong:#312e81; --accent-soft:rgba(67,56,202,0.14);">
      <div class="document-inner" style="display:grid; grid-template-columns: 17rem 1fr; min-height:297mm;">
        <aside style="background: linear-gradient(180deg, #312e81, #4338ca 55%, #6d28d9); color:white; padding: var(--space-6); display:grid; gap: var(--space-5); align-content:start;">
          <div class="stack-sm">
            <div class="eyebrow" style="color: rgba(255,255,255,0.66);">Sidebar cards</div>
            <h1 style="font-size: 2.3rem; line-height: 0.95;">Victor Sotero</h1>
            <p style="color: rgba(255,255,255,0.82);">{esc(personal["title"])}</p>
          </div>
          <div class="stack-sm small" style="color: rgba(255,255,255,0.84);">
            <div>{esc(personal["location"])}</div>
            <div>{esc(personal["email"])}</div>
            <div>{esc(personal["linkedin"])}</div>
            <div>{esc(personal["github"])}</div>
          </div>
          <section class="stack-sm">
            <div class="uppercase micro" style="color: rgba(255,255,255,0.7);">Strengths</div>
            <ul class="chip-list">{"".join(f'<li class="chip" style="background: rgba(255,255,255,0.12); border-color: rgba(255,255,255,0.16); color: white;">{esc(item.get("name", ""))}</li>' for category in data["skills"] for item in category.get("items", [])[:2])}</ul>
          </section>
          {render_languages(data["languages"])}
          {render_certifications(data["certifications"])}
        </aside>
        <main style="padding: var(--space-6);" class="stack-lg">
          {render_summary(data["summary"])}
          {render_experience(data["experience"])}
          {render_projects(data["projects"])}
          {render_skills(data["skills"])}
          <div class="grid-cards">
            {render_education(data["education"])}
            {render_publications(data.get("publications", []))}
          </div>
        </main>
      </div>
    </div>
    """


def dark_statement(data: JsonDict) -> str:
    personal = data["personal"]
    return f"""
    <div class="document dark-statement" style="--paper:#08111f; --paper-alt:#0f1c2f; --canvas:#030712; --ink:#e6edf6; --muted:#9db0c9; --line:rgba(230,237,246,0.14); --accent:#22d3ee; --accent-strong:#67e8f9; --accent-soft:rgba(34,211,238,0.12); color: var(--ink);">
      <div class="document-inner" style="padding: var(--space-7); background: radial-gradient(circle at top right, rgba(34,211,238,0.16), transparent 28%), radial-gradient(circle at bottom left, rgba(103,232,249,0.12), transparent 36%), var(--paper);">
        <header class="stack-md" style="padding: var(--space-6); border: 1px solid var(--line); border-radius: var(--radius-xl); background: rgba(15, 28, 47, 0.86); backdrop-filter: blur(16px);">
          <span class="kicker">Dark statement</span>
          <h1 style="font-size: 3.7rem; line-height: 0.92; letter-spacing: -0.05em;">{esc(personal["name"])}</h1>
          <p style="font-size: 1.25rem; max-width: 42rem; color: var(--muted);">{esc(personal["title"])} building governed, scalable data platforms with a bias for production clarity and enterprise trust.</p>
          {render_contacts(personal)}
        </header>
        <main class="stack-lg" style="margin-top: var(--space-6);">
          <div class="grid-sidebar">
            <div class="stack-lg">
              {render_summary(data["summary"])}
              {render_projects(data["projects"])}
              {render_education(data["education"])}
            </div>
            <div class="stack-lg">
              {render_experience(data["experience"])}
              {render_skills(data["skills"], meters=True)}
              <div class="grid-cards">
                {render_certifications(data["certifications"])}
                {render_languages(data["languages"])}
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
    """


def compact_grid(data: JsonDict) -> str:
    personal = data["personal"]
    return f"""
    <div class="document compact-grid" style="--paper:#f9fafb; --paper-alt:#eef2f5; --canvas:#d8dee4; --accent:#0f766e; --accent-strong:#134e4a; --accent-soft:rgba(15,118,110,0.12);">
      <div class="document-inner" style="padding: var(--space-6);">
        <header class="grid-cards" style="margin-bottom: var(--space-5); align-items:stretch;">
          <section class="panel stack-md" style="grid-column: span 2;">
            <span class="kicker">Compact grid</span>
            <div class="two-col" style="grid-template-columns: 1.2fr 0.8fr; gap: var(--space-4);">
              <div class="stack-sm">
                <h1 style="font-size: 2.8rem; line-height: 0.96;">{esc(personal["name"])}</h1>
                <p>{esc(personal["title"])}</p>
                <p class="small muted">{esc(personal["tagline"])}</p>
              </div>
              <div>{render_contacts(personal)}</div>
            </div>
          </section>
        </header>
        <main class="grid-cards">
          <section class="panel stack-sm">{render_summary(data["summary"])}</section>
          <section class="panel stack-sm">{render_skills(data["skills"], meters=True)}</section>
          <section class="panel stack-sm" style="grid-column: span 2;">{render_projects(data["projects"])}</section>
          <section class="panel stack-sm" style="grid-column: span 2;">{render_experience(data["experience"], dense=True)}</section>
          <section class="panel stack-sm">{render_education(data["education"])}</section>
          <section class="panel stack-sm">{render_certifications(data["certifications"])}{render_languages(data["languages"])}{render_publications(data.get("publications", []))}</section>
        </main>
      </div>
    </div>
    """


def european_formal(data: JsonDict) -> str:
    personal = data["personal"]
    return f"""
    <div class="document european-formal" style="--paper:#fffefb; --paper-alt:#f6f1e9; --canvas:#ddd5c8; --accent:#8b5e34; --accent-strong:#5f3b20; --accent-soft:rgba(139,94,52,0.12);">
      <div class="document-inner" style="padding: 20mm 18mm; border: 14px solid #efe5d6; font-family: var(--font-serif);">
        <header class="stack-md">
          <div class="eyebrow">European formal</div>
          <div class="two-col" style="grid-template-columns: 1fr 0.86fr; align-items:start; gap: var(--space-6);">
            <div class="stack-sm">
              <h1 style="font-family: var(--font-display); font-size: 3.2rem; line-height: 0.94; font-weight: 500;">Victor Sotero</h1>
              <p style="font-size: 1.12rem;">{esc(personal["title"])}</p>
              <div class="formal-rule"></div>
              <div class="summary lede">{lines_to_paragraphs(data["summary"])}</div>
            </div>
            <div class="panel">
              <table class="compact-table small">
                <tr><td>Location</td><td>{esc(personal["location"])}</td></tr>
                <tr><td>Email</td><td>{esc(personal["email"])}</td></tr>
                <tr><td>LinkedIn</td><td>{esc(personal["linkedin"])}</td></tr>
                <tr><td>GitHub</td><td>{esc(personal["github"])}</td></tr>
              </table>
            </div>
          </div>
        </header>
        <main class="stack-lg" style="margin-top: var(--space-6);">
          <div class="two-col" style="grid-template-columns: 1.2fr 0.8fr;">
            <div class="stack-lg">
              {render_experience(data["experience"])}
              {render_projects(data["projects"], cards=False)}
            </div>
            <aside class="stack-lg">
              {render_skills(data["skills"], meters=True)}
              {render_education(data["education"])}
              {render_certifications(data["certifications"])}
              {render_languages(data["languages"])}
              {render_publications(data.get("publications", []))}
            </aside>
          </div>
        </main>
      </div>
    </div>
    """


VARIANTS: list[tuple[str, str, Callable[[JsonDict], str]]] = [
    ("executive-split", "Executive Split", executive_split),
    ("editorial-single-column", "Editorial Single Column", editorial_single_column),
    ("technical-dense", "Technical Dense", technical_dense),
    ("project-first", "Project First", project_first),
    ("ats-minimal", "ATS Minimal", ats_minimal),
    ("consulting-timeline", "Consulting Timeline", consulting_timeline),
    ("sidebar-cards", "Sidebar Cards", sidebar_cards),
    ("dark-statement", "Dark Statement", dark_statement),
    ("compact-grid", "Compact Grid", compact_grid),
    ("european-formal", "European Formal", european_formal),
]


def document_html(title: str, variant_key: str, body_html: str) -> str:
    return f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{esc(title)} | Victor Sotero</title>
    <meta name="generator" content="scripts/generate_cv_variants.py" />
    <style>{PAGE_CSS}</style>
  </head>
  <body data-variant="{esc(variant_key)}">{body_html}</body>
</html>
'''


def main() -> None:
    data = cast(JsonDict, yaml.safe_load(CONTENT_PATH.read_text(encoding="utf-8")))
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for variant_key, variant_title, renderer in VARIANTS:
        content = document_html(variant_title, variant_key, renderer(data))
        output_path = OUTPUT_DIR / f"{variant_key}.html"
        output_path.write_text(content, encoding="utf-8")
        print(f"generated {output_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
