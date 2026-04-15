"""Render a classified transcription to a standalone HTML file."""

from html import escape
from pathlib import Path

from iptag.presentation.colors import css_class, html_color
from iptag.presentation.segments import (
    all_labels,
    build_segments,
    category_counts,
)
from iptag.transcriptions.models import TranscriptionData

_BASE_CSS = """
body { font-family: -apple-system, system-ui, sans-serif; max-width: 900px;
       margin: 2rem auto; padding: 0 1rem; line-height: 1.6; color: #222; }
h1 { font-size: 1.2rem; color: #555; font-weight: normal; }
.filters { margin: 1rem 0; padding: 0.75rem; background: #f5f5f5;
           border-radius: 6px; display: flex; flex-wrap: wrap; gap: 0.75rem; }
.filters label { cursor: pointer; user-select: none; }
.transcript { padding: 1rem; border: 1px solid #e0e0e0; border-radius: 6px;
              white-space: pre-wrap; }
mark { padding: 0.05rem 0.15rem; border-radius: 3px;
       border-bottom: 2px solid rgba(0,0,0,0.2); }
mark.muted { background: transparent !important; border-bottom-color: transparent;
             color: #999; }
mark .extras { font-size: 0.75em; color: #555; font-style: italic;
               margin-left: 0.25rem; }
table { border-collapse: collapse; margin-top: 1rem; }
th, td { padding: 0.25rem 0.75rem; text-align: left;
         border-bottom: 1px solid #eee; }
th { font-weight: 600; }
.swatch { display: inline-block; width: 0.9rem; height: 0.9rem;
          border-radius: 2px; margin-right: 0.4rem; vertical-align: middle; }
"""

_FILTER_JS = """
document.querySelectorAll('.filters input').forEach(cb => {
  cb.addEventListener('change', () => {
    const cls = cb.dataset.cls;
    document.querySelectorAll('mark.' + cls).forEach(el => {
      el.classList.toggle('muted', !cb.checked);
    });
  });
});
"""


def render_to_html(transcription: TranscriptionData, out_path: Path) -> None:
    """Write a standalone HTML report of the classified transcription."""
    labels = all_labels(transcription)

    label_css = "\n".join(
        f"mark.{css_class(lbl)} {{ background: {html_color(lbl)}; }}" for lbl in labels
    )

    filters_html = "".join(
        f'<label><input type="checkbox" data-cls="{css_class(lbl)}" checked>'
        f'<span class="swatch" style="background:{html_color(lbl)}"></span>'
        f"{escape(lbl)}</label>"
        for lbl in labels
    )

    transcript_html = _build_transcript_html(transcription)
    summary_html = _build_summary_html(transcription)

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
<script>{_FILTER_JS}</script>
</body>
</html>
"""
    out_path.write_text(html, encoding="utf-8")


def _build_transcript_html(transcription: TranscriptionData) -> str:
    parts: list[str] = []
    for seg in build_segments(transcription):
        if not seg.labels:
            parts.append(escape(seg.text))
            continue
        classes = " ".join(css_class(lbl) for lbl in seg.labels)
        extras = ""
        if len(seg.labels) > 1:
            joined = ", ".join(seg.labels[1:])
            extras = f'<span class="extras">+{escape(joined)}</span>'
        parts.append(
            f'<mark class="{classes}" title="{escape(", ".join(seg.labels))}">'
            f"{escape(seg.text)}{extras}</mark>"
        )
    return "".join(parts)


def _build_summary_html(transcription: TranscriptionData) -> str:
    counts = category_counts(transcription)
    if not counts:
        return ""
    rows = "\n".join(
        f"<tr><td><span class='swatch' style='background:{html_color(lbl)}'></span>"
        f"{escape(lbl)}</td><td>{stats['count']}</td>"
        f"<td>{stats['avg_score']:.2f}</td></tr>"
        for lbl, stats in sorted(
            counts.items(), key=lambda kv: (-kv[1]["count"], kv[0])
        )
    )
    return (
        "<table><thead><tr><th>category</th><th>count</th><th>avg score</th></tr>"
        f"</thead><tbody>{rows}</tbody></table>"
    )
