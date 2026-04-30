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


def page_one(c):
    shell(c, 'PUBLIC DILIGENCE PACKET', 1)
    dark_panel(c, M, H - 4.55 * inch, 3.58 * inch, 3.74 * inch, 26)
    c.setFillColor(CYAN)
    c.setFont('Helvetica-Bold', 8)
    c.drawString(M + 22, H - 1.12 * inch, 'TIM SULLIVAN')
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 31)
    text(c, M + 22, H - 1.55 * inch, 'Product systems proof packet.', 30, WHITE, 'Helvetica-Bold', 32, 230)
    c.setFillColor(colors.HexColor('#c7d4db'))
    text(c, M + 22, H - 2.72 * inch, 'A compact review packet for public work across mobile product systems, evidence-backed workflows, validation logic, and generated artifacts.', 8.8, colors.HexColor('#c7d4db'), 'Helvetica', 11, 230)
    c.setFillColor(CYAN)
    c.setFont('Helvetica-Bold', 8)
    c.drawString(M + 22, H - 4.12 * inch, 'SCAN LIVE PACKET')
    c.setFillColor(WHITE)
    c.roundRect(M + 142, H - 4.33 * inch, 62, 62, 10, fill=1, stroke=0)
    draw_qr(c, links['diligence'], M + 151, H - 4.24 * inch, 44)

    x0 = M + 3.90 * inch
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 29)
    c.drawString(x0, H - 1.18 * inch, 'Review route')
    c.setFont('Helvetica-Bold', 29)
    c.drawString(x0, H - 1.56 * inch, 'for public proof.')
    text(c, x0, H - 1.86 * inch, 'The packet is built for a fast evaluator: first understand the system, then open working evidence.', 9.8, MUTED, 'Helvetica', 12, 430)
    py = H - 2.32 * inch
    for label, url in [('Portfolio', links['portfolio']), ('Outcome board', links['outcomes']), ('Systems lab', links['lab']), ('GitHub', links['github'])]:
        x0 = pill(c, x0, py, label, url)

    y = H - 3.30 * inch
    mw = (W - M - (M + 3.90 * inch) - 30) / 4
    start = M + 3.90 * inch
    for i, data in enumerate([
        ('Public tests', '43', 'Across showcase repos', TEAL),
        ('SquadBrain', '25', 'TypeScript tests', BLUE),
        ('Lasting Ground', '18', 'Python tests', GOLD),
        ('Delivery', 'CI', 'Repeatable checks', GREEN),
    ]):
        metric(c, start + i * (mw + 10), y, mw, *data)

    y -= 1.10 * inch
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 14)
    c.drawString(start, y + 66, 'Evidence stack')
    stages = [('01', 'Outcome', 'What changed and why it matters.'), ('02', 'Model', 'Rules, states, validation, and boundaries.'), ('03', 'Lab', 'Runnable browser proof and examples.'), ('04', 'Code', 'Coverage, ADRs, and public repos.')]
    sw = (W - M - start - 30) / 4
    for i, (n, title, body) in enumerate(stages):
        sx = start + i * (sw + 10)
        round_rect(c, sx, y - 4, sw, 70, PANEL, LINE, 16)
        c.setFillColor(TEAL if i % 2 == 0 else BLUE)
        c.roundRect(sx + 10, y + 42, 24, 16, 8, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 7)
        c.drawCentredString(sx + 22, y + 47, n)
        c.setFillColor(INK)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(sx + 10, y + 29, title)
        text(c, sx + 10, y + 15, body, 6.6, MUTED, 'Helvetica', 8.0, sw - 20)
    c.linkURL(links['outcomes'], (start, y - 4, start + sw, y + 66), relative=0)
    c.linkURL(links['operating'], (start + sw + 10, y - 4, start + 2 * sw + 10, y + 66), relative=0)
    c.linkURL(links['lab'], (start + 2 * (sw + 10), y - 4, start + 3 * sw + 20, y + 66), relative=0)
    c.linkURL(links['github'], (start + 3 * (sw + 10), y - 4, start + 4 * sw + 30, y + 66), relative=0)

    lane_y = 1.25 * inch
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 13)
    c.drawString(start, lane_y + 84, 'Public artifact lanes')
    lane_w = (W - M - start - 30) / 4
    lanes = [
        ('Demo', 'Working surfaces that can be opened immediately.', links['portfolio'], TEAL),
        ('Examples', 'Executable logic in public repos.', links['squad_examples'], BLUE),
        ('Coverage', 'Test and coverage summaries.', links['squad_coverage'], GOLD),
        ('Packet', 'Generated outputs and proof routes.', links['diligence'], GREEN),
    ]
    for i, (title, body, url, accent) in enumerate(lanes):
        lx = start + i * (lane_w + 10)
        round_rect(c, lx, lane_y, lane_w, 74, PANEL, LINE, 16)
        c.setFillColor(accent)
        c.roundRect(lx + 10, lane_y + 52, 24, 8, 4, fill=1, stroke=0)
        c.setFillColor(INK)
        c.setFont('Helvetica-Bold', 9.6)
        c.drawString(lx + 10, lane_y + 36, title)
        text(c, lx + 10, lane_y + 22, body, 6.7, MUTED, 'Helvetica', 8, lane_w - 20)
        c.linkURL(url, (lx, lane_y, lx + lane_w, lane_y + 74), relative=0)


def project_block(c, x, y, w, h, name, label, claim, proof, flow, accent, urls):
    round_rect(c, x, y, w, h, PANEL, LINE, 22)
    c.setFillColor(accent)
    c.roundRect(x + 16, y + h - 34, 48, 20, 10, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 7)
    c.drawCentredString(x + 40, y + h - 27, label.upper())
    c.setFillColor(TEAL)
    c.setFont('Helvetica-Bold', 7.4)
    c.drawRightString(x + w - 16, y + h - 25, proof)
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 17)
    text(c, x + 16, y + h - 58, name, 17, INK, 'Helvetica-Bold', 19, w - 32)
    text(c, x + 16, y + h - 104, claim, 7.8, MUTED, 'Helvetica', 9.4, w - 32)
    small_flow(c, x + 48, y + 34, w - 96, flow, accent)
    btn_y = y + 12
    bx = x + 16
    for lab, url in urls:
        bx = pill(c, bx, btn_y, lab, url)


def page_two(c):
    shell(c, 'PROJECT EVIDENCE LEDGER', 2)
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 28)
    c.drawString(M, H - 1.08 * inch, 'Two builds. One proof standard.')
    text(c, M, H - 1.38 * inch, 'Each project is presented as a system: the visible product, the underlying rules, the validation boundary, and the artifact trail a reviewer can inspect.', 9.4, MUTED, 'Helvetica', 11.5, 660)
    col_w = (W - 2 * M - 18) / 2
    top_y = H - 4.36 * inch
    project_block(c, M, top_y, col_w, 2.45 * inch, 'SquadBrain competitive practice system', 'Mobile', 'Adaptive practice, matchmaking, validated results.', '25 tests - 98.3% coverage - ADRs', ['surface', 'rules', 'proof'], BLUE, [('Demo', links['squad_demo']), ('Code', links['squad_examples']), ('Coverage', links['squad_coverage'])])
    project_block(c, M + col_w + 18, top_y, col_w, 2.62 * inch, 'Lasting Ground source-bounded packet system', 'Evidence', 'Source lanes, evidence scoring, cautious language, packet output.', '18 tests - 93.29% coverage - PDF', ['sources', 'review', 'packet'], GOLD, [('Demo', links['lasting_demo']), ('Code', links['lasting_examples']), ('Coverage', links['lasting_coverage'])])

    y = 1.08 * inch
    dark_panel(c, M, y, W - 2 * M, 1.12 * inch, 22)
    c.setFillColor(CYAN)
    c.setFont('Helvetica-Bold', 8)
    c.drawString(M + 18, y + 58, 'QUALITY RULE')
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 12)
    text(c, M + 18, y + 38, 'A claim is strong only when it routes to working product evidence, executable examples, tests, coverage, decision records, or generated outputs.', 12, WHITE, 'Helvetica-Bold', 14, W - 2 * M - 36)
    text(c, M + 18, y + 15, 'This packet uses only public artifacts and avoids inflated outcomes that cannot be verified from the public trail.', 7.8, colors.HexColor('#c7d4db'), 'Helvetica', 9, W - 2 * M - 36)


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
    c.setFont('Helvetica-Bold', 28)
    c.drawString(M, H - 1.08 * inch, 'Choose depth. Open receipts. Decide fast.')
    text(c, M, H - 1.38 * inch, 'The strongest public portfolio surface makes the reviewer path obvious: skim, run, inspect, then verify the implementation trail.', 9.4, MUTED, 'Helvetica', 11.5, 560)

    route_y = H - 2.78 * inch
    route_w = (W - 2 * M - 36) / 4
    routes = [
        ('1 minute', 'Outcome board', 'Check the two evidence trails.', links['outcomes'], TEAL),
        ('5 minutes', 'Systems lab', 'Run the browser proof surface.', links['lab'], BLUE),
        ('15 minutes', 'Model + ADRs', 'Inspect operating model and decisions.', links['operating'], GOLD),
        ('Full review', 'Evaluator console', 'Follow the role-specific route.', links['review'], GREEN),
    ]
    for i, (time, title, body, url, accent) in enumerate(routes):
        x = M + i * (route_w + 12)
        round_rect(c, x, route_y - 2, route_w, 92, DARK if i == 3 else PANEL, colors.Color(1, 1, 1, .20) if i == 3 else LINE, 18)
        c.setFillColor(CYAN if i == 3 else accent)
        c.setFont('Helvetica-Bold', 7)
        c.drawString(x + 13, route_y + 62, time.upper())
        c.setFillColor(WHITE if i == 3 else INK)
        c.setFont('Helvetica-Bold', 12)
        c.drawString(x + 13, route_y + 39, title)
        text(c, x + 13, route_y + 22, body, 7.2, colors.HexColor('#c7d4db') if i == 3 else MUTED, 'Helvetica', 8.6, route_w - 26)
        c.linkURL(url, (x, route_y - 2, x + route_w, route_y + 90), relative=0)

    y = H - 4.80 * inch
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 14)
    c.drawString(M, y + 60, 'Capability map')
    cw = (W - 2 * M - 36 - 1.68 * inch) / 4
    x = M
    for title, body, accent in [
        ('Product UX', 'Mobile surfaces, demos, task states, and readable outputs.', BLUE),
        ('Systems logic', 'Rules, scoring, validation gates, and state transitions.', TEAL),
        ('Evidence work', 'Source lanes, cautious language, support depth, and proof routes.', GOLD),
        ('Delivery', 'Tests, coverage, CI, docs, ADRs, sample artifacts.', GREEN),
    ]:
        matrix_cell(c, x, y - 44, cw, 100, title, body, accent)
        x += cw + 12
    c.setFillColor(WHITE)
    c.roundRect(x, y - 30, 1.18 * inch, 1.18 * inch, 13, fill=1, stroke=0)
    draw_qr(c, links['diligence'], x + 14, y - 16, 56)
    c.setFillColor(MUTED)
    c.setFont('Helvetica-Bold', 6.5)
    c.drawCentredString(x + 0.59 * inch, y - 37, 'LIVE PACKET')

    dark_panel(c, M, 0.92 * inch, W - 2 * M, 0.96 * inch, 20)
    c.setFillColor(CYAN)
    c.setFont('Helvetica-Bold', 8)
    c.drawString(M + 18, 1.55 * inch, 'BOTTOM LINE')
    c.setFillColor(WHITE)
    text(c, M + 18, 1.32 * inch, 'The public surface is built to show product judgment, operating logic, evidence discipline, and delivery maturity without making a reviewer guess.', 11.5, WHITE, 'Helvetica-Bold', 13.5, W - 2 * M - 36)


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
