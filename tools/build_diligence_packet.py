from pathlib import Path
from reportlab.graphics import renderPDF
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/tim-sullivan-diligence-packet.pdf'
W, H = landscape(letter)
M = 0.42 * inch
INK = colors.HexColor('#07111c')
MUTED = colors.HexColor('#526170')
LINE = colors.HexColor('#b6c9d3')
PAPER = colors.HexColor('#eef6f7')
PANEL = colors.HexColor('#fbfdf8')
DARK = colors.HexColor('#07111c')
DARK2 = colors.HexColor('#0b263c')
TEAL = colors.HexColor('#14b8a6')
CYAN = colors.HexColor('#6fffe8')
BLUE = colors.HexColor('#1f6feb')
GOLD = colors.HexColor('#c36b1e')
GREEN = colors.HexColor('#0f766e')
WHITE = colors.white

links = {
    'portfolio': 'https://sulmusic2-star.github.io/',
    'diligence': 'https://sulmusic2-star.github.io/diligence/',
    'outcomes': 'https://sulmusic2-star.github.io/outcomes/',
    'operating': 'https://sulmusic2-star.github.io/operating-model/',
    'review': 'https://sulmusic2-star.github.io/review/',
    'architecture': 'https://sulmusic2-star.github.io/architecture/',
    'lab': 'https://sulmusic2-star.github.io/lab/',
    'squad_demo': 'https://sulmusic2-star.github.io/squadbrain-showcase/',
    'lasting_demo': 'https://sulmusic2-star.github.io/lasting-ground-showcase/',
    'squad_case': 'https://sulmusic2-star.github.io/case-studies/squadbrain/',
    'lasting_case': 'https://sulmusic2-star.github.io/case-studies/lasting-ground/',
    'squad': 'https://github.com/sulmusic2-star/squadbrain-showcase',
    'lasting': 'https://github.com/sulmusic2-star/lasting-ground-showcase',
    'squad_examples': 'https://github.com/sulmusic2-star/squadbrain-showcase/tree/main/examples',
    'lasting_examples': 'https://github.com/sulmusic2-star/lasting-ground-showcase/tree/main/examples',
    'squad_coverage': 'https://github.com/sulmusic2-star/squadbrain-showcase/blob/main/docs/coverage-summary.md',
    'lasting_coverage': 'https://github.com/sulmusic2-star/lasting-ground-showcase/blob/main/docs/coverage-summary.md',
    'github': 'https://github.com/sulmusic2-star',
}


def text(c, x, y, value, size=10, color=INK, font='Helvetica', leading=12, width=300):
    c.setFillColor(color)
    c.setFont(font, size)
    words = value.split()
    line = ''
    for word in words:
        test = (line + ' ' + word).strip()
        if stringWidth(test, font, size) <= width:
            line = test
        else:
            if line:
                c.drawString(x, y, line)
                y -= leading
            line = word
    if line:
        c.drawString(x, y, line)
        y -= leading
    return y


def shell(c, label, page):
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(colors.HexColor('#dff3f6'))
    c.rect(0, H - 1.16 * inch, W, 1.16 * inch, fill=1, stroke=0)
    c.setStrokeColor(colors.HexColor('#d6e5ea'))
    for i in range(13):
        x = i * 0.72 * inch
        c.line(x, 0, x, H)
    for i in range(8):
        y = i * 0.72 * inch
        c.line(0, y, W, y)
    c.setFillColor(GOLD)
    c.setFont('Helvetica-Bold', 7.5)
    c.drawString(M, H - M + 2, label)
    c.setFillColor(MUTED)
    c.setFont('Helvetica', 7.2)
    c.drawString(M, 0.20 * inch, 'Public packet - portfolio, proof routes, demos, code examples, coverage, and generated artifacts.')
    c.setFillColor(TEAL)
    c.setFont('Helvetica-Bold', 7.2)
    c.drawRightString(W - M, 0.20 * inch, f'sulmusic2-star.github.io / page {page}')


def round_rect(c, x, y, w, h, fill, stroke=LINE, r=16, sw=1):
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.setLineWidth(sw)
    c.roundRect(x, y, w, h, r, fill=1, stroke=1)


def dark_panel(c, x, y, w, h, r=22):
    c.setFillColor(DARK)
    c.roundRect(x, y, w, h, r, fill=1, stroke=0)
    c.setFillColor(colors.Color(0.08, 0.72, 0.64, 0.16))
    c.circle(x + w - 40, y + h - 28, 90, fill=1, stroke=0)


def pill(c, x, y, label, url, fill=WHITE, color=INK):
    w = stringWidth(label, 'Helvetica-Bold', 7.4) + 18
    round_rect(c, x, y, w, 22, fill, LINE, 11)
    c.setFillColor(color)
    c.setFont('Helvetica-Bold', 7.4)
    c.drawString(x + 9, y + 7, label)
    c.linkURL(url, (x, y, x + w, y + 22), relative=0)
    return x + w + 7


def metric(c, x, y, w, label, value, caption, accent):
    round_rect(c, x, y, w, 70, PANEL, LINE, 16)
    c.setFillColor(accent)
    c.roundRect(x + 12, y + 12, 4, 46, 2, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 21)
    c.drawString(x + 24, y + 39, value)
    c.setFillColor(GOLD)
    c.setFont('Helvetica-Bold', 6.7)
    c.drawString(x + 24, y + 25, label.upper())
    c.setFillColor(MUTED)
    c.setFont('Helvetica', 7.2)
    c.drawString(x + 24, y + 13, caption)


def draw_qr(c, url, x, y, size):
    widget = qr.QrCodeWidget(url)
    b = widget.getBounds()
    drawing = Drawing(size, size, transform=[size / (b[2] - b[0]), 0, 0, size / (b[3] - b[1]), 0, 0])
    drawing.add(widget)
    renderPDF.draw(drawing, c, x, y)
    c.linkURL(url, (x, y, x + size, y + size), relative=0)


def small_flow(c, x, y, w, labels, accent):
    c.setStrokeColor(accent)
    c.setLineWidth(1.3)
    c.line(x, y + 18, x + w, y + 18)
    gap = w / (len(labels) - 1)
    for i, label in enumerate(labels):
        cx = x + i * gap
        c.setFillColor(DARK if i == 1 else WHITE)
        c.setStrokeColor(accent)
        c.roundRect(cx - 31, y + 5, 62, 26, 13, fill=1, stroke=1)
        c.setFillColor(CYAN if i == 1 else accent)
        c.setFont('Helvetica-Bold', 6.2)
        c.drawCentredString(cx, y + 15, label.upper())



def tiny_label(c, x, y, label, accent=GOLD, color=None):
    c.setFillColor(color or accent)
    c.setFont('Helvetica-Bold', 6.7)
    c.drawString(x, y, label.upper())


def proof_chip(c, x, y, label, value, accent):
    round_rect(c, x, y, 116, 42, PANEL, LINE, 12)
    c.setFillColor(accent)
    c.roundRect(x + 9, y + 25, 22, 7, 3.5, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 15)
    c.drawString(x + 9, y + 10, value)
    tiny_label(c, x + 42, y + 27, label, GOLD)


def artifact_tile(c, x, y, w, h, label, title, body, url, accent, dark=False):
    round_rect(c, x, y, w, h, DARK if dark else PANEL, colors.Color(1, 1, 1, .18) if dark else LINE, 15)
    tiny_label(c, x + 12, y + h - 20, label, CYAN if dark else GOLD)
    c.setFillColor(WHITE if dark else INK)
    c.setFont('Helvetica-Bold', 11)
    text(c, x + 12, y + h - 40, title, 11, WHITE if dark else INK, 'Helvetica-Bold', 12, w - 24)
    text(c, x + 12, y + h - 62, body, 6.9, colors.HexColor('#c7d4db') if dark else MUTED, 'Helvetica', 8.2, w - 24)
    c.setFillColor(accent)
    c.roundRect(x + 12, y + 8, 32, 6, 3, fill=1, stroke=0)
    c.linkURL(url, (x, y, x + w, y + h), relative=0)


def mini_console(c, x, y, w, h, title, subtitle, rows, accent=CYAN):
    dark_panel(c, x, y, w, h, 20)
    c.setFillColor(accent)
    c.circle(x + 17, y + h - 18, 3.2, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.circle(x + 28, y + h - 18, 3.2, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.circle(x + 39, y + h - 18, 3.2, fill=1, stroke=0)
    tiny_label(c, x + 52, y + h - 22, title, accent)
    c.setStrokeColor(colors.Color(1, 1, 1, .13))
    c.line(x + 14, y + h - 34, x + w - 14, y + h - 34)
    text(c, x + 16, y + h - 53, subtitle, 10.5, WHITE, 'Helvetica-Bold', 12, w - 32)
    row_y = y + h - 82
    for n, body in rows:
        c.setFillColor(colors.Color(1, 1, 1, .07))
        c.setStrokeColor(colors.Color(1, 1, 1, .12))
        c.roundRect(x + 16, row_y - 7, w - 32, 21, 10, fill=1, stroke=1)
        c.setFillColor(accent)
        c.setFont('Helvetica-Bold', 7.4)
        c.drawString(x + 28, row_y, n)
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 7.4)
        c.drawString(x + 58, row_y, body[:62])
        row_y -= 24


def page_one(c):
    shell(c, 'PUBLIC DILIGENCE PACKET', 1)
    dark_panel(c, M, H - 4.58 * inch, 3.45 * inch, 3.78 * inch, 26)
    tiny_label(c, M + 22, H - 1.12 * inch, 'TIM SULLIVAN', CYAN)
    text(c, M + 22, H - 1.54 * inch, 'Product systems proof packet.', 30, WHITE, 'Helvetica-Bold', 32, 230)
    text(c, M + 22, H - 2.82 * inch, 'Public review routes for mobile product logic, evidence workflows, validation gates, generated artifacts, and delivery proof.', 8.6, colors.HexColor('#c7d4db'), 'Helvetica', 10.8, 226)
    c.setFillColor(WHITE)
    c.roundRect(M + 22, H - 4.30 * inch, 62, 62, 10, fill=1, stroke=0)
    draw_qr(c, links['diligence'], M + 31, H - 4.21 * inch, 44)
    tiny_label(c, M + 98, H - 4.02 * inch, 'LIVE PACKET', CYAN)
    text(c, M + 98, H - 4.18 * inch, 'Scan or open the site to inspect the live proof route.', 7.1, colors.HexColor('#c7d4db'), 'Helvetica', 8.5, 118)

    x = M + 3.78 * inch
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 27)
    c.drawString(x, H - 1.08 * inch, 'Fast proof route')
    c.drawString(x, H - 1.43 * inch, 'for public review.')
    text(c, x, H - 1.72 * inch, 'Skim the route, run the lab, inspect the code, then verify the artifact trail.', 9.2, MUTED, 'Helvetica', 11, 410)
    bx = x
    for label, url in [('Portfolio', links['portfolio']), ('Outcomes', links['outcomes']), ('Lab', links['lab']), ('GitHub', links['github'])]:
        bx = pill(c, bx, H - 2.02 * inch, label, url)

    metric_y = H - 2.85 * inch
    proof_chip(c, x, metric_y, 'public tests', '43', TEAL)
    proof_chip(c, x + 112, metric_y, 'SquadBrain', '25', BLUE)
    proof_chip(c, x + 224, metric_y, 'Lasting Ground', '18', GOLD)
    proof_chip(c, x + 336, metric_y, 'delivery', 'CI', GREEN)

    console_y = H - 4.70 * inch
    mini_console(c, x, console_y, 3.92 * inch, 1.90 * inch, 'INTERACTIVE PROOF CONSOLE', 'Choose a build. Open proof.', [
        ('01', 'SquadBrain: adaptive practice -> validated results'),
        ('02', 'Lasting Ground: source lanes -> packet output'),
        ('03', 'Review route: packet -> lab -> examples'),
    ])
    c.linkURL(links['portfolio'], (x, console_y, x + 3.92 * inch, console_y + 1.54 * inch), relative=0)

    tile_y = 0.88 * inch
    tile_w = (W - 2 * M - 36) / 4
    tiles = [
        ('Demo', 'Open product surfaces', 'Live project pages and browser routes.', links['portfolio'], TEAL, False),
        ('Examples', 'Inspect code paths', 'Executable TypeScript and Python examples.', links['squad_examples'], BLUE, False),
        ('Coverage', 'Check tests', 'Coverage summaries and CI-backed checks.', links['squad_coverage'], GOLD, False),
        ('Packet', 'Review output', 'Generated packets and proof-route artifacts.', links['diligence'], GREEN, True),
    ]
    for i, t in enumerate(tiles):
        artifact_tile(c, M + i * (tile_w + 12), tile_y, tile_w, 84, *t)


def project_block(c, x, y, w, h, name, label, claim, proof, flow, accent, urls):
    round_rect(c, x, y, w, h, PANEL, LINE, 22)
    c.setFillColor(accent)
    c.roundRect(x + 16, y + h - 34, 52, 20, 10, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 7)
    c.drawCentredString(x + 42, y + h - 27, label.upper())
    tiny_label(c, x + w - 150, y + h - 26, proof, TEAL)
    title_bottom = text(c, x + 16, y + h - 60, name, 15.2, INK, 'Helvetica-Bold', 17, w - 32)
    text(c, x + 16, title_bottom - 3, claim, 7.4, MUTED, 'Helvetica', 9.0, w - 32)
    small_flow(c, x + 50, y + 28, w - 100, flow, accent)
    bx = x + 16
    for lab, url in urls:
        bx = pill(c, bx, y + 6, lab, url)


def ledger_row(c, x, y, cols, fills=None):
    widths = [1.50 * inch, 2.25 * inch, 2.25 * inch, 2.25 * inch, 1.65 * inch]
    xx = x
    for i, (value, bold) in enumerate(cols):
        fill = fills[i] if fills else PANEL
        c.setFillColor(fill)
        c.setStrokeColor(LINE)
        c.rect(xx, y, widths[i], 32, fill=1, stroke=1)
        c.setFillColor(WHITE if fill == DARK else INK if bold else MUTED)
        c.setFont('Helvetica-Bold' if bold else 'Helvetica', 7.3)
        text(c, xx + 7, y + 20, value, 7.3, WHITE if fill == DARK else INK if bold else MUTED, 'Helvetica-Bold' if bold else 'Helvetica', 8.2, widths[i] - 14)
        xx += widths[i]


def page_two(c):
    shell(c, 'PROJECT EVIDENCE LEDGER', 2)
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 27)
    c.drawString(M, H - 1.05 * inch, 'Two builds. One proof standard.')
    text(c, M, H - 1.34 * inch, 'Each project is shown as product surface, operating logic, validation boundary, and inspectable public artifact.', 9.2, MUTED, 'Helvetica', 11, 650)

    top_y = H - 3.96 * inch
    col_w = (W - 2 * M - 18) / 2
    project_block(c, M, top_y, col_w, 2.35 * inch, 'SquadBrain competitive practice system', 'Mobile', 'Adaptive practice, matchmaking, validated results.', '25 tests - 98.3%', ['surface', 'rules', 'proof'], BLUE, [('Demo', links['squad_demo']), ('Code', links['squad_examples']), ('Coverage', links['squad_coverage'])])
    project_block(c, M + col_w + 18, top_y, col_w, 2.35 * inch, 'Lasting Ground source-bounded packet system', 'Evidence', 'Source lanes, evidence scoring, cautious language, packet output.', '18 tests - 93.29%', ['sources', 'review', 'packet'], GOLD, [('Demo', links['lasting_demo']), ('Code', links['lasting_examples']), ('Coverage', links['lasting_coverage'])])

    y = H - 5.00 * inch
    tiny_label(c, M, y + 32, 'IMPLEMENTATION RECEIPTS', GOLD)
    ledger_row(c, M, y, [('Layer', True), ('SquadBrain', True), ('Lasting Ground', True), ('Public route', True), ('Proof type', True)], [DARK, DARK, DARK, DARK, DARK])
    rows = [
        [('Surface', True), ('Mobile game loop, quick match, progress states', False), ('Packet review page and sample PDF surface', False), ('Demos and case studies', False), ('UX / product', False)],
        [('Logic', True), ('Adaptive priority, matchmaking, ranking movement', False), ('Source lanes, evidence scoring, support depth', False), ('Examples folders', False), ('Executable code', False)],
        [('Guardrail', True), ('Recomputed results and risk flags', False), ('Cautious language and visible source gaps', False), ('Tests + coverage', False), ('Validation', False)],
        [('Artifact', True), ('ADRs, coverage summary, live demo', False), ('Sample PDF, coverage summary, evaluator guide', False), ('Packet + repo docs', False), ('Delivery proof', False)],
    ]
    yy = y - 32
    for row in rows:
        ledger_row(c, M, yy, row)
        yy -= 32

    dark_panel(c, M, 0.38 * inch, W - 2 * M, 0.54 * inch, 16)
    tiny_label(c, M + 18, 0.72 * inch, 'QUALITY RULE', CYAN)
    text(c, M + 18, 0.56 * inch, 'Claims route to working product evidence, executable examples, tests, coverage, decision records, or generated outputs.', 8.2, WHITE, 'Helvetica-Bold', 9.4, W - 2 * M - 36)


def matrix_cell(c, x, y, w, h, title, body, accent):
    round_rect(c, x, y, w, h, PANEL, LINE, 15)
    c.setFillColor(accent)
    c.roundRect(x + 12, y + h - 22, 26, 8, 4, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 10)
    c.drawString(x + 12, y + h - 43, title)
    text(c, x + 12, y + h - 58, body, 7.1, MUTED, 'Helvetica', 8.5, w - 24)


def page_three(c):
    shell(c, 'REVIEW PATHS AND CAPABILITY MAP', 3)
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 27)
    c.drawString(M, H - 1.05 * inch, 'Choose depth. Open receipts. Decide fast.')
    text(c, M, H - 1.34 * inch, 'A reviewer should know where to skim, what to run, and which artifacts prove the implementation trail.', 9.2, MUTED, 'Helvetica', 11, 620)

    route_y = H - 2.88 * inch
    route_w = (W - 2 * M - 36) / 4
    routes = [
        ('1 minute', 'Outcome board', 'Check evidence trails.', links['outcomes'], TEAL, False),
        ('5 minutes', 'Systems lab', 'Run browser proof.', links['lab'], BLUE, False),
        ('15 minutes', 'Model + ADRs', 'Inspect decisions.', links['operating'], GOLD, False),
        ('Full review', 'Evaluator console', 'Follow the role route.', links['review'], GREEN, True),
    ]
    for i, (time, title, body, url, accent, dark) in enumerate(routes):
        artifact_tile(c, M + i * (route_w + 12), route_y, route_w, 92, time, title, body, url, accent, dark)

    y = H - 4.46 * inch
    mini_console(c, M, y - 55, 3.35 * inch, 1.90 * inch, 'REVIEW PATH', 'What the public trail demonstrates', [
        ('01', 'Turns vague workflows into explicit states'),
        ('02', 'Pairs UI surfaces with rules and guardrails'),
        ('03', 'Packages proof as demos, code, PDFs, CI'),
    ])

    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 14)
    c.drawString(M + 3.62 * inch, y + 66, 'Capability map')
    cw = (W - (M + 3.62 * inch) - M - 24) / 2
    items = [
        ('Product UX', 'Mobile surfaces, demos, task states, readable outputs.', BLUE),
        ('Systems logic', 'Rules, scoring, validation gates, state transitions.', TEAL),
        ('Evidence work', 'Source lanes, cautious language, support depth.', GOLD),
        ('Delivery', 'Tests, coverage, CI, docs, ADRs, sample artifacts.', GREEN),
    ]
    for i, (title, body, accent) in enumerate(items):
        xx = M + 3.62 * inch + (i % 2) * (cw + 12)
        yy = y + 4 - (i // 2) * 86
        matrix_cell(c, xx, yy, cw, 74, title, body, accent)

    dark_panel(c, M, 0.82 * inch, W - 2 * M, 1.02 * inch, 20)
    tiny_label(c, M + 18, 1.49 * inch, 'BOTTOM LINE', CYAN)
    text(c, M + 18, 1.27 * inch, 'The public surface now behaves like a review system: route, run, inspect, verify.', 11.2, WHITE, 'Helvetica-Bold', 13, W - 2 * M - 140)
    text(c, M + 18, 1.04 * inch, 'It shows product judgment, operating logic, evidence discipline, and delivery maturity without making a reviewer guess.', 7.8, colors.HexColor('#c7d4db'), 'Helvetica', 9.2, W - 2 * M - 150)
    c.setFillColor(WHITE)
    c.roundRect(W - M - 84, 0.98 * inch, 62, 62, 10, fill=1, stroke=0)
    draw_qr(c, links['diligence'], W - M - 75, 1.07 * inch, 44)

def draw():
    c = canvas.Canvas(str(OUT), pagesize=(W, H))
    c.setTitle('Tim Sullivan - Public Diligence Packet')
    c.setAuthor('Tim Sullivan')
    c.setSubject('Product systems portfolio proof packet')
    page_one(c)
    c.showPage()
    page_two(c)
    c.showPage()
    page_three(c)
    c.showPage()
    c.save()


if __name__ == '__main__':
    draw()
    print(OUT)
