#!/usr/bin/env python3
"""Generate an SVG diagram from the At a Glance ASCII art in README.md."""

import re
import sys


COLORS = {
    "CUSTOMIZATION": {"bg": "#7c3aed", "icon": "📄"},
    "AGENTIC": {"bg": "#2563eb", "icon": "⚡"},
    "PLATFORM": {"bg": "#059669", "icon": "🧠"},
    "COMMUNITY": {"bg": "#d97706", "icon": "🌐"},
}


def parse_sections(readme_path):
    with open(readme_path) as f:
        content = f.read()

    match = re.search(r'## At a Glance\s*```(.*?)```', content, re.DOTALL)
    if not match:
        print("ERROR: Could not find At a Glance section", file=sys.stderr)
        sys.exit(1)

    block = match.group(1).strip()
    sections = []
    current = None

    for line in block.split('\n'):
        # Check indentation before stripping — continuation lines are indented
        inner = line.strip().strip('│')
        leading_spaces = len(inner) - len(inner.lstrip())
        stripped = inner.strip()

        if not stripped or stripped.startswith('┌') or stripped.startswith('└') or stripped.startswith('├') or set(stripped) <= {'─', '┤', '├'}:
            continue

        header_match = re.match(r'[📄⚡🧠🌐]\s+(\w+)\s*—\s*(.+)', stripped)
        if header_match:
            category = header_match.group(1).upper()
            subtitle = header_match.group(2).strip()
            current = {"category": category, "subtitle": subtitle, "items": []}
            sections.append(current)
            continue

        if current is not None:
            item_match = re.match(r'(.+?)\s{2,}(.+)', stripped)
            if item_match:
                name = item_match.group(1).strip()
                desc = item_match.group(2).strip()
                # If indented more than normal, it's a continuation of the previous item
                if leading_spaces > 2 and current["items"]:
                    last = current["items"][-1]
                    last["name"] += " " + name
                    last["desc"] += " " + desc
                else:
                    current["items"].append({"name": name, "desc": desc})

    return sections


def escape_xml(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def generate_svg(sections):
    width = 720
    pad = 20
    inner_w = width - 2 * pad
    header_h = 40
    item_h = 26
    section_gap = 12
    item_pad_top = 10
    item_pad_bottom = 8

    # Calculate total height
    total_h = pad
    for sec in sections:
        total_h += header_h + item_pad_top + len(sec["items"]) * item_h + item_pad_bottom + section_gap
    total_h += pad - section_gap

    lines = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {total_h}" width="{width}" height="{total_h}">')
    lines.append('''  <defs>
    <style>
      .sec-title { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; font-weight: 700; font-size: 13px; fill: #ffffff; }
      .sec-sub { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; font-weight: 400; font-size: 11.5px; fill: rgba(255,255,255,0.75); }
      .i-name { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; font-weight: 600; font-size: 12.5px; fill: #e2e8f0; }
      .i-desc { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; font-weight: 400; font-size: 12px; fill: #94a3b8; }
    </style>
  </defs>''')

    # Background
    lines.append(f'  <rect width="{width}" height="{total_h}" rx="12" fill="#0f172a"/>')

    y = pad
    for sec in sections:
        cat = sec["category"]
        info = COLORS.get(cat, {"bg": "#6b7280", "icon": "📦"})
        bg = info["bg"]
        icon = info["icon"]

        items_count = len(sec["items"])
        sec_h = header_h + item_pad_top + items_count * item_h + item_pad_bottom

        # Section container
        lines.append(f'  <rect x="{pad}" y="{y}" width="{inner_w}" height="{sec_h}" rx="8" fill="{bg}" opacity="0.08"/>')
        lines.append(f'  <rect x="{pad}" y="{y}" width="{inner_w}" height="{sec_h}" rx="8" fill="none" stroke="{bg}" stroke-opacity="0.25" stroke-width="1"/>')

        # Header background
        lines.append(f'  <rect x="{pad}" y="{y}" width="{inner_w}" height="{header_h}" rx="8" fill="{bg}" opacity="0.2"/>')
        # Fix bottom corners of header (overlap with a rect)
        lines.append(f'  <rect x="{pad}" y="{y + header_h - 8}" width="{inner_w}" height="8" fill="{bg}" opacity="0.2"/>')

        # Header text
        title_x = pad + 16
        lines.append(f'  <text x="{title_x}" y="{y + 26}" class="sec-title">{icon}  {cat}</text>')
        sub_x = title_x + len(cat) * 9 + 30
        lines.append(f'  <text x="{sub_x}" y="{y + 26}" class="sec-sub">— {escape_xml(sec["subtitle"])}</text>')

        # Items
        iy = y + header_h + item_pad_top
        for item in sec["items"]:
            lines.append(f'  <text x="{pad + 20}" y="{iy + 16}" class="i-name">{escape_xml(item["name"])}</text>')
            lines.append(f'  <text x="260" y="{iy + 16}" class="i-desc">{escape_xml(item["desc"])}</text>')
            iy += item_h

        y += sec_h + section_gap

    lines.append('</svg>')
    return '\n'.join(lines)


def main():
    readme_path = sys.argv[1] if len(sys.argv) > 1 else 'README.md'
    output_path = sys.argv[2] if len(sys.argv) > 2 else 'docs/at-a-glance.svg'

    sections = parse_sections(readme_path)
    svg = generate_svg(sections)

    with open(output_path, 'w') as f:
        f.write(svg)
    print(f"Generated {output_path} with {len(sections)} sections, {sum(len(s['items']) for s in sections)} items")


if __name__ == '__main__':
    main()
