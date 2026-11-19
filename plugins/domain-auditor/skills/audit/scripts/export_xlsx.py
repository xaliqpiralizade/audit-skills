#!/usr/bin/env python3
"""Audit hesabatındakı tapıntıları Excel (.xlsx) faylına ixrac edir.

Yalnız standart Python kitabxanasından istifadə edir (Python 3.8+).

İstifadə:
    python3 export_xlsx.py audit-hesabati-hr-2026-11-19.md [cixis.xlsx]

Hesabat references/hesabat-shablonu.md formatında olmalıdır:
    ### HR-001 · Başlıq
    - **Bölmə:** ...
    - **Risk dərəcəsi:** Kritik
    ...
"""

import re
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

COLUMNS = [
    ("Nömrə", 10),
    ("Başlıq", 40),
    ("Bölmə", 24),
    ("Risk dərəcəsi", 14),
    ("Təsvir", 60),
    ("Sübut", 45),
    ("Niyə problemdir", 60),
    ("Tövsiyə", 60),
]
FIELD_KEYS = ["Bölmə", "Risk dərəcəsi", "Təsvir", "Sübut", "Niyə problemdir", "Tövsiyə"]
RISK_ORDER = ["Kritik", "Yüksək", "Orta", "Aşağı"]

HEADING_RE = re.compile(r"^###\s+([A-ZƏÖÜÇŞĞİ]+-\d+)\s*[·:\-–—]\s*(.+?)\s*$")
FIELD_RE = re.compile(r"^\s*[-*]\s+\*\*(.+?):\*\*\s*(.*)$")


def clean(text):
    """Markdown işarələrini sadələşdirir: `kod`, **qalın**, [mətn](link) -> mətn (link)."""
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", text)
    text = text.replace("**", "").replace("`", "")
    return text.strip()


def parse_findings(md):
    findings = []
    current = None
    field = None
    for line in md.splitlines():
        heading = HEADING_RE.match(line)
        if heading:
            current = {"Nömrə": heading.group(1), "Başlıq": clean(heading.group(2))}
            findings.append(current)
            field = None
            continue
        if current is None:
            continue
        if line.startswith("#"):  # növbəti bölmə başladı
            current = None
            field = None
            continue
        m = FIELD_RE.match(line)
        if m and m.group(1).strip() in FIELD_KEYS:
            field = m.group(1).strip()
            current[field] = clean(m.group(2))
        elif field and line.strip():
            current[field] = (current[field] + "\n" + clean(line)).strip()
    return findings


def col_letter(idx):
    letters = ""
    idx += 1
    while idx:
        idx, rem = divmod(idx - 1, 26)
        letters = chr(65 + rem) + letters
    return letters


def cell(ref, value, style=0):
    value = escape(str(value)).replace("\n", "&#10;")
    s = ' s="%d"' % style if style else ""
    return '<c r="%s" t="inlineStr"%s><is><t xml:space="preserve">%s</t></is></c>' % (ref, s, value)


def num_cell(ref, value, style=0):
    s = ' s="%d"' % style if style else ""
    return '<c r="%s"%s><v>%d</v></c>' % (ref, s, value)


def sheet_xml(rows, widths, freeze=True, autofilter=None):
    cols = "".join(
        '<col min="%d" max="%d" width="%d" customWidth="1"/>' % (i + 1, i + 1, w)
        for i, w in enumerate(widths)
    )
    pane = (
        '<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" '
        'activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>'
        if freeze
        else ""
    )
    body = "".join('<row r="%d">%s</row>' % (i + 1, "".join(r)) for i, r in enumerate(rows))
    af = '<autoFilter ref="%s"/>' % autofilter if autofilter else ""
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        "%s<cols>%s</cols><sheetData>%s</sheetData>%s</worksheet>" % (pane, cols, body, af)
    )


STYLES = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
    '<fonts count="2"><font><sz val="11"/><name val="Calibri"/></font>'
    '<font><b/><sz val="11"/><name val="Calibri"/></font></fonts>'
    '<fills count="3"><fill><patternFill patternType="none"/></fill>'
    '<fill><patternFill patternType="gray125"/></fill>'
    '<fill><patternFill patternType="solid"><fgColor rgb="FFD9E1F2"/></patternFill></fill></fills>'
    '<borders count="1"><border/></borders>'
    '<cellStyleXfs count="1"><xf/></cellStyleXfs>'
    '<cellXfs count="3"><xf/>'
    '<xf fontId="1" fillId="2" applyFont="1" applyFill="1"><alignment vertical="top" wrapText="1"/></xf>'
    '<xf applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>'
    "</cellXfs></styleSheet>"
)


def build_xlsx(findings, out_path, source_name):
    header = [cell(col_letter(i) + "1", name, 1) for i, (name, _) in enumerate(COLUMNS)]
    rows = [header]
    for r, f in enumerate(findings, start=2):
        rows.append(
            [cell(col_letter(i) + str(r), f.get(name, ""), 2) for i, (name, _) in enumerate(COLUMNS)]
        )
    last = col_letter(len(COLUMNS) - 1) + str(max(len(rows), 1))
    sheet1 = sheet_xml(rows, [w for _, w in COLUMNS], autofilter="A1:" + last)

    counts = {k: 0 for k in RISK_ORDER}
    other = 0
    for f in findings:
        risk = f.get("Risk dərəcəsi", "").strip()
        if risk in counts:
            counts[risk] += 1
        else:
            other += 1
    summary = [[cell("A1", "Risk dərəcəsi", 1), cell("B1", "Say", 1)]]
    for i, k in enumerate(RISK_ORDER, start=2):
        summary.append([cell("A%d" % i, k), num_cell("B%d" % i, counts[k])])
    n = len(RISK_ORDER) + 2
    if other:
        summary.append([cell("A%d" % n, "Dərəcəsi tanınmayan"), num_cell("B%d" % n, other)])
        n += 1
    summary.append([cell("A%d" % n, "Cəmi", 1), num_cell("B%d" % n, len(findings), 1)])
    summary.append([])  # boş sətir (sətir nömrələri ardıcıl qalmalıdır)
    summary.append([cell("A%d" % (n + 2), "Mənbə: " + source_name)])
    summary.append(
        [cell("A%d" % (n + 3), "Bu, daxili yoxlamadır, rəsmi audit rəyi deyil.")]
    )
    sheet2 = sheet_xml(summary, [28, 10], freeze=False)

    files = {
        "[Content_Types].xml": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
            '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
            '<Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
            '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
            "</Types>"
        ),
        "_rels/.rels": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
            "</Relationships>"
        ),
        "xl/workbook.xml": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            '<sheets><sheet name="Tapıntılar" sheetId="1" r:id="rId1"/>'
            '<sheet name="İcmal" sheetId="2" r:id="rId2"/></sheets>'
            '<definedNames><definedName name="_xlnm._FilterDatabase" localSheetId="0" hidden="1">'
            "'Tapıntılar'!$A$1:$%s$%d</definedName></definedNames>"
            "</workbook>" % (col_letter(len(COLUMNS) - 1), max(len(rows), 1))
        ),
        "xl/_rels/workbook.xml.rels": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/>'
            '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
            "</Relationships>"
        ),
        "xl/worksheets/sheet1.xml": sheet1,
        "xl/worksheets/sheet2.xml": sheet2,
        "xl/styles.xml": STYLES,
    }
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, content in files.items():
            zf.writestr(name, content.encode("utf-8"))


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 1
    src = Path(argv[1])
    if not src.is_file():
        print("Fayl tapılmadı: %s" % src, file=sys.stderr)
        return 1
    out = Path(argv[2]) if len(argv) > 2 else src.with_suffix(".xlsx")
    findings = parse_findings(src.read_text(encoding="utf-8"))
    if not findings:
        print(
            "Xəbərdarlıq: tapıntı tapılmadı. Başlıqlar '### HR-001 · Başlıq' formatındadırmı?",
            file=sys.stderr,
        )
    build_xlsx(findings, out, src.name)
    print("%d tapıntı ixrac edildi: %s" % (len(findings), out))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
