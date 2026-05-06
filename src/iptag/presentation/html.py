"""Render a classified transcription to a standalone HTML file."""

import json
from html import escape
from pathlib import Path
from typing import Optional

from iptag.classifier.config import CategoriesConfig
from iptag.presentation.colors import css_class, html_color
from iptag.transcriptions.models import TranscriptionData

_BASE_CSS = """
body { font-family: -apple-system, system-ui, sans-serif; max-width: 960px;
       margin: 2rem auto; padding: 0 1rem; line-height: 1.6; color: #222; }
h1 { font-size: 1.2rem; color: #555; font-weight: normal; }

/* Filter bar */
.filters { margin: 1rem 0; display: flex; flex-wrap: wrap; gap: 0.6rem; }
.filter-card { background: #f5f5f5; border-radius: 8px; padding: 0.5rem 0.75rem;
               min-width: 180px; max-width: 260px; }
.filter-card label { cursor: pointer; user-select: none; display: flex;
                     align-items: center; gap: 0.4rem; font-weight: 600; }
.cat-desc { font-size: 0.75em; color: #777; font-style: italic;
            margin-top: 0.15rem; line-height: 1.3; }
.threshold-row { display: flex; align-items: center; gap: 0.4rem;
                 margin-top: 0.35rem; }
.threshold-row input[type=range] { flex: 1; cursor: pointer; accent-color: #555; }
.thresh-val { font-size: 0.75em; color: #555; width: 2.5em; text-align: right; }

/* Transcript */
.transcript { padding: 1rem; border: 1px solid #e0e0e0; border-radius: 6px;
              white-space: pre-wrap; }
mark { padding: 0.05rem 0.15rem; border-radius: 3px;
       border-bottom: 2px solid rgba(0,0,0,0.2); cursor: default; }
mark.muted { background: transparent !important; border-bottom-color: transparent;
             color: #999; }
mark .extras { font-size: 0.75em; color: #555; font-style: italic;
               margin-left: 0.25rem; }

/* Summary table */
table { border-collapse: collapse; margin-top: 1rem; width: 100%; max-width: 600px; }
th, td { padding: 0.3rem 0.75rem; text-align: left; border-bottom: 1px solid #eee; }
th { font-weight: 600; }
.swatch { display: inline-block; width: 0.9rem; height: 0.9rem;
          border-radius: 2px; margin-right: 0.4rem; vertical-align: middle; }
.cat-row { cursor: pointer; }
.cat-row:hover { background: #fafafa; }
.caret { color: #aaa; user-select: none; text-align: center; width: 1.5rem; }
.cat-name-cell .cat-desc { font-size: 0.75em; color: #888; font-style: italic; }
.phrases-row { background: #fafafa; }
.phrases-row.hidden { display: none; }
.phrase-list { margin: 0.4rem 0; padding-left: 1.2rem; list-style: disc; }
.phrase-list li { padding: 0.15rem 0; font-size: 0.9em; }
.phrase-list li .score { display: inline-block; width: 3rem; font-weight: 600;
                         color: #444; font-variant-numeric: tabular-nums; }
.phrase-list li.empty { color: #aaa; font-style: italic; list-style: none; }
"""

_JS_TEMPLATE = """
(function() {
  var phrases = /*__PHRASES_JSON__*/;
  var cats = /*__CATS_JSON__*/;

  var catMap = {};
  cats.forEach(function(c) { catMap[c.name] = c; });

  function escHtml(s) {
    return String(s)
      .replace(/&/g,'&amp;').replace(/</g,'&lt;')
      .replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

  function getThreshold(name) {
    var el = document.querySelector('input[type=range][data-name="'+name+'"]');
    return el ? parseFloat(el.value) : catMap[name].threshold;
  }

  function isEnabled(name) {
    var sel = '.filter-card[data-name="'+name+'"] input[type=checkbox]';
    var el = document.querySelector(sel);
    return el ? el.checked : true;
  }

  function getActive(phrase) {
    return cats
      .filter(function(c) {
        var score = phrase.scores[c.name] || 0;
        return isEnabled(c.name) && score >= getThreshold(c.name);
      })
      .map(function(c) { return c.name; });
  }

  function recompute() {
    phrases.forEach(function(p) {
      var el = document.querySelector('mark[data-idx="'+p.idx+'"]');
      if (!el) return;

      cats.forEach(function(c) { el.classList.remove(c.cssClass); });
      el.classList.remove('muted');
      el.removeAttribute('style');

      var active = getActive(p);
      var extras = el.querySelector('.extras');

      if (active.length === 0) {
        el.classList.add('muted');
        el.title = '';
        if (extras) extras.textContent = '';
      } else {
        el.style.background = catMap[active[0]].color;
        active.forEach(function(name) { el.classList.add(catMap[name].cssClass); });
        el.title = active.join(', ');
        if (extras) {
          extras.textContent =
            active.length > 1 ? '+' + active.slice(1).join(', ') : '';
        }
      }
    });

    var stats = {};
    cats.forEach(function(c) { stats[c.name] = {count: 0, scoreSum: 0}; });
    phrases.forEach(function(p) {
      var active = getActive(p);
      active.forEach(function(name) {
        stats[name].count++;
        stats[name].scoreSum += (p.scores[name] || 0);
      });
    });

    cats.forEach(function(c) {
      var countEl = document.querySelector('.count-cell[data-name="'+c.name+'"]');
      var avgEl   = document.querySelector('.avg-cell[data-name="'+c.name+'"]');
      if (countEl) countEl.textContent = stats[c.name].count;
      if (avgEl) {
        var avg = stats[c.name].count > 0
          ? stats[c.name].scoreSum / stats[c.name].count : 0;
        avgEl.textContent = avg.toFixed(2);
      }
      var listEl = document.querySelector('.phrase-list[data-name="'+c.name+'"]');
      if (listEl) {
        var pr = listEl.closest('.phrases-row');
        if (pr && !pr.classList.contains('hidden')) fillPhraseList(c.name, listEl);
      }
    });

    var tbody = document.getElementById('summary-tbody');
    if (!tbody) return;
    var catRows = Array.prototype.slice.call(tbody.querySelectorAll('tr.cat-row'));
    catRows.sort(function(a, b) {
      var na = a.dataset.name, nb = b.dataset.name;
      var diff = stats[nb].count - stats[na].count;
      return diff !== 0 ? diff : na.localeCompare(nb);
    });
    catRows.forEach(function(row) {
      var pr = tbody.querySelector('.phrases-row[data-name="'+row.dataset.name+'"]');
      tbody.appendChild(row);
      if (pr) tbody.appendChild(pr);
    });
  }

  function fillPhraseList(name, listEl) {
    var active = phrases
      .filter(function(p) { return getActive(p).indexOf(name) >= 0; })
      .sort(function(a, b) { return a.idx - b.idx; });

    if (active.length === 0) {
      listEl.innerHTML = '<li class="empty">No phrases for current threshold.</li>';
      return;
    }
    listEl.innerHTML = active.map(function(p) {
      var score = (p.scores[name] || 0).toFixed(2);
      return '<li><span class="score">'+score+'</span> \u201c' +
        escHtml(p.text)+'\u201d</li>';
    }).join('');
  }

  document.querySelectorAll('.filter-card input[type=checkbox]').forEach(function(cb) {
    cb.addEventListener('change', recompute);
  });

  document.querySelectorAll('input[type=range][data-name]').forEach(function(sl) {
    sl.addEventListener('input', function(e) {
      var display = e.target.nextElementSibling;
      if (display) display.textContent = parseFloat(e.target.value).toFixed(2);
      recompute();
    });
  });

  document.querySelectorAll('.cat-row').forEach(function(row) {
    row.addEventListener('click', function() {
      var name = row.dataset.name;
      var pr = document.querySelector('.phrases-row[data-name="'+name+'"]');
      var caret = row.querySelector('.caret');
      if (!pr) return;
      var hidden = pr.classList.toggle('hidden');
      if (caret) caret.textContent = hidden ? '\u25b8' : '\u25be';
      if (!hidden) {
        var listEl = pr.querySelector('.phrase-list');
        if (listEl) fillPhraseList(name, listEl);
      }
    });
  });

  recompute();
})();
"""


def render_to_html(
    transcription: TranscriptionData,
    out_path: Path,
    categories: Optional[CategoriesConfig] = None,
) -> None:
    """Write a standalone HTML report of the classified transcription.

    Args:
        transcription: The classified transcription data.
        out_path: Destination file path.
        categories: Optional categories configuration. When provided, enables
            per-category threshold sliders and long descriptions in the UI.
            When omitted, thresholds are derived from the pre-computed labels.
    """
    cat_defs = _build_cat_defs(transcription, categories)

    label_css = "\n".join(
        f"mark.{d['cssClass']} {{ background: {d['color']}; }}" for d in cat_defs
    )

    filters_html = _build_filters_html(cat_defs)
    transcript_html = _build_transcript_html(transcription)
    summary_html = _build_summary_html(transcription, cat_defs)

    phrases_json = json.dumps(_phrases_payload(transcription), ensure_ascii=False)
    cats_json = json.dumps(cat_defs, ensure_ascii=False)
    js = _JS_TEMPLATE.replace("/*__PHRASES_JSON__*/", phrases_json).replace(
        "/*__CATS_JSON__*/", cats_json
    )

    source = escape(transcription.source or "transcription")
    html = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>iptag — {source}</title>
<style>{_BASE_CSS}{label_css}</style>
</head>
<body>
<h1>{source}</h1>
<div class="filters">{filters_html}</div>
<div class="transcript">{transcript_html}</div>
{summary_html}
<script>{js}</script>
</body>
</html>
"""
    out_path.write_text(html, encoding="utf-8")


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _build_cat_defs(
    transcription: TranscriptionData,
    categories: Optional[CategoriesConfig],
) -> list[dict]:
    """Build a list of category definition dicts for use in HTML + JS."""
    if categories is not None:
        return [
            {
                "name": cat.name,
                "label": cat.name,
                "description": cat.description or cat.label,
                "color": html_color(cat.name),
                "cssClass": css_class(cat.name),
                "threshold": categories.threshold,
            }
            for cat in categories.categories
        ]

    # Derive from scores keys and existing labels (no config provided)
    results = transcription.metadata.get("classifications", [])
    all_names: list[str] = []
    for r in results:
        for name in r.scores:
            if name not in all_names:
                all_names.append(name)

    defs = []
    for name in all_names:
        active_scores = [
            r.scores[name] for r in results if name in r.labels and name in r.scores
        ]
        threshold = min(active_scores) if active_scores else 1.0
        defs.append(
            {
                "name": name,
                "label": name,
                "description": None,
                "color": html_color(name),
                "cssClass": css_class(name),
                "threshold": round(threshold, 4),
            }
        )
    return defs


def _phrases_payload(transcription: TranscriptionData) -> list[dict]:
    """Return per-phrase data for the embedded JS array."""
    results = transcription.metadata.get("classifications", [])
    return [{"idx": r.index, "text": r.text, "scores": r.scores} for r in results]


def _build_filters_html(cat_defs: list[dict]) -> str:
    parts = []
    for d in cat_defs:
        thresh = f"{d['threshold']:.2f}"
        desc_html = (
            f'<div class="cat-desc">{escape(d["description"])}</div>'
            if d["description"]
            else ""
        )
        parts.append(
            f'<div class="filter-card" data-name="{escape(d["name"])}">'
            f"<label>"
            f'<input type="checkbox" checked>'
            f'<span class="swatch" style="background:{d["color"]}"></span>'
            f"{escape(d['label'])}"
            f"</label>"
            f"{desc_html}"
            f'<div class="threshold-row">'
            f'<input type="range" min="0" max="1" step="0.01" '
            f'value="{thresh}" data-name="{escape(d["name"])}">'
            f'<span class="thresh-val">{thresh}</span>'
            f"</div>"
            f"</div>"
        )
    return "".join(parts)


def _build_transcript_html(transcription: TranscriptionData) -> str:
    results = transcription.metadata.get("classifications", [])
    parts: list[str] = []
    for i, r in enumerate(results):
        if i > 0:
            parts.append(" ")
        parts.append(
            f'<mark data-idx="{r.index}">'
            f"{escape(r.text)}"
            f'<span class="extras"></span>'
            f"</mark>"
        )
    return "".join(parts)


def _build_summary_html(transcription: TranscriptionData, cat_defs: list[dict]) -> str:
    if not cat_defs:
        return ""
    results = transcription.metadata.get("classifications", [])

    # Compute initial counts using r.labels (pre-computed threshold)
    stats: dict[str, dict] = {
        d["name"]: {"count": 0, "score_sum": 0.0} for d in cat_defs
    }
    for r in results:
        for label in r.labels:
            if label in stats:
                stats[label]["count"] += 1
                stats[label]["score_sum"] += r.scores.get(label, 0.0)

    rows: list[str] = []
    for d in sorted(cat_defs, key=lambda d: (-stats[d["name"]]["count"], d["name"])):
        name = d["name"]
        color = d["color"]
        count = stats[name]["count"]
        avg = stats[name]["score_sum"] / count if count else 0.0
        desc_html = (
            f'<div class="cat-desc">{escape(d["description"])}</div>'
            if d["description"]
            else ""
        )
        rows.append(
            f'<tr class="cat-row" data-name="{escape(name)}">'
            f'<td class="cat-name-cell">'
            f"<span class='swatch' style='background:{color}'></span>"
            f"{escape(name)}"
            f"{desc_html}"
            f"</td>"
            f'<td class="count-cell" data-name="{escape(name)}">{count}</td>'
            f'<td class="avg-cell" data-name="{escape(name)}">{avg:.2f}</td>'
            f'<td class="caret">&#9656;</td>'
            f"</tr>"
            f'<tr class="phrases-row hidden" data-name="{escape(name)}">'
            f'<td colspan="4">'
            f'<ul class="phrase-list" data-name="{escape(name)}"></ul>'
            f"</td>"
            f"</tr>"
        )

    return (
        "<table>"
        "<thead><tr>"
        "<th>category</th><th>count</th><th>avg score</th><th></th>"
        "</tr></thead>"
        f'<tbody id="summary-tbody">{"".join(rows)}</tbody>'
        "</table>"
    )
