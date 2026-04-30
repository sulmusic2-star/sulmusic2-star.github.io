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
TEAL = colors.HexColor('#14b8a6')
CYAN = colors.HexColor('#6fffe8')
BLUE = colors.HexColor('#1f6feb')
GOLD = colors.HexColor('#c36b1e')
PAPER = colors.HexColor('#eef6f7')
PANEL = colors.HexColor('#f8fcfd')
DARK = colors.HexColor('#07111c')
DARK2 = colors.HexColor('#0b263c')
DARK3 = colors.HexColor('#0f4b4a')
WHITE = colors.white

links = {
    'portfolio': 'https://sulmusic2-star.github.io/',
    'diligence': 'https://sulmusic2-star.github.io/diligence/',
    'outcomes': 'https://sulmusic2-star.github.io/outcomes/',
    'operating': 'https://sulmusic2-star.github.io/operating-model/',
    'review': 'https://sulmusic2-star.github.io/review/',
    'lab': 'https://sulmusic2-star.github.io/lab/',
    'squad_demo': 'https://sulmusic2-star.github.io/squadbrain-showcase/',
    'lasting_demo': 'https://sulmusic2-star.github.io/lasting-ground-showcase/',
    'squad': 'https://github.com/sulmusic2-star/squadbrain-showcase',
    'lasting': 'https://github.com/sulmusic2-star/lasting-ground-showcase',
    'squad_examples': 'https://github.com/sulmusic2-star/squadbrain-showcase/tree/main/examples',
    'lasting_examples': 'https://github.com/sulmusic2-star/lasting-ground-showcase/tree/main/examples',
    'squad_coverage': 'https://github.com/sulmusic2-star/squadbrain-showcase/blob/main/docs/coverage-summary.md',
    'lasting_coverage': 'https://github.com/sulmusic2-star/lasting-ground-showcase/blob/main/docs/coverage-summary.md',
    'github': 'https://github.com/sulmusic2-star',
}


def wrapped(c, x, y, value, size=10, color=INK, font='Helvetica', leading=12, max_width=300):
    c.setFillColor(color)
    c.setFont(font, size)
    words = value.split()
    line = ''
    for word in words:
        test = (line + ' ' + word).strip()
        if stringWidth(test, font, size) <= max_width:
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


def page_shell(c, label):
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(colors.HexColor('#dff3f6'))
    c.rect(0, H - 1.5 * inch, W, 1.5 * inch, fill=1, stroke=0)
    c.setFillColor(colors.HexColor('#f8fcfd'))
    c.rect(0, H - 1.5 * inch, 2.9 * inch, 1.5 * inch, fill=1, stroke=0)
    c.setFillColor(colors.Color(0.04, 0.07, 0.11, .05))
    c.rect(0, H - 1.52 * inch, W, 0.02 * inch, fill=1, stroke=0)
    c.setStrokeColor(colors.HexColor('#d6e5ea'))
    for i in range(12):
        x = i * 0.75 * inch
        c.line(x, 0, x, H)
    for i in range(7):
        y = i * 0.75 * inch
        c.line(0, y, W, y)
    c.setFillColor(GOLD)
    c.setFont('Helvetica-Bold', 8)
    c.drawString(M, H - M - 2, label)


def footer(c, page):
    c.setFillColor(MUTED)
    c.setFont('Helvetica', 7.5)
    c.drawString(M, 0.20 * inch, 'Public proof packet - every claim routes to a demo, example, coverage artifact, decision record, or sample output.')
    c.setFillColor(TEAL)
    c.setFont('Helvetica-Bold', 7.5)
    c.drawRightString(W - M, 0.20 * inch, f'sulmusic2-star.github.io / {page}')
    c.linkURL(links['portfolio'], (W - M - 130, 0.12 * inch, W - M, 0.32 * inch), relative=0)


def pill(c, x, y, label, url, dark=False):
    w = stringWidth(label, 'Helvetica-Bold', 8) + 18
    c.setStrokeColor(colors.Color(1, 1, 1, .26) if dark else LINE)
    c.setFillColor(colors.Color(1, 1, 1, .10) if dark else WHITE)
    c.roundRect(x, y - 14, w, 22, 11, fill=1, stroke=1)
    c.setFillColor(CYAN if dark else INK)
    c.setFont('Helvetica-Bold', 8)
    c.drawString(x + 9, y - 7, label)
    c.linkURL(url, (x, y - 14, x + w, y + 8), relative=0)
    return x + w + 8


def metric(c, x, y, w, big, small, accent=TEAL):
    c.setFillColor(PANEL)
    c.setStrokeColor(LINE)
    c.roundRect(x, y - 54, w, 54, 14, fill=1, stroke=1)
    c.setFillColor(accent)
    c.rect(x + 11, y - 47, 3, 40, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 20)
    c.drawString(x + 22, y - 23, big)
    c.setFillColor(MUTED)
    c.setFont('Helvetica-Bold', 8)
    c.drawString(x + 22, y - 40, small)


def flow_ribbon(c, x, y, w, labels):
    c.setFillColor(DARK)
    c.roundRect(x, y - 44, w, 44, 18, fill=1, stroke=0)
    step_w = w / len(labels)
    for i, lab in enumerate(labels):
        sx = x + i * step_w
        c.setFillColor(CYAN if i % 2 == 0 else colors.HexColor('#a7f3d0'))
        c.setFont('Helvetica-Bold', 7)
        c.drawString(sx + 16, y - 26, lab.upper())
        if i < len(labels) - 1:
            c.setStrokeColor(colors.Color(1, 1, 1, .22))
            c.line(sx + step_w - 8, y - 35, sx + step_w - 8, y - 9)
            c.setFillColor(colors.Color(1, 1, 1, .55))
            c.setFont('Helvetica-Bold', 12)
            c.drawString(sx + step_w - 3, y - 28, '->')


def project_card(c, x, y, w, h, kicker, title, body, proof, url, accent):
    c.setFillColor(WHITE)
    c.setStrokeColor(LINE)
    c.roundRect(x, y - h, w, h, 20, fill=1, stroke=1)
    c.setFillColor(colors.HexColor('#eef8fa'))
    c.roundRect(x + 9, y - h + 9, w - 18, h - 18, 14, fill=1, stroke=0)
    c.setFillColor(colors.HexColor('#f9fdfe'))
    c.roundRect(x + 14, y - h + 55, w - 28, h - 72, 12, fill=1, stroke=0)
    c.setFillColor(accent)
    c.roundRect(x + 14, y - 34, 34, 18, 9, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 7)
    c.drawCentredString(x + 31, y - 27, kicker[:4].upper())
    c.setFillColor(TEAL)
    c.setFont('Helvetica-Bold', 7.2)
    c.drawRightString(x + w - 18, y - 22, proof)
    yy = wrapped(c, x + 18, y - 55, title, 14.8, INK, 'Helvetica-Bold', 16.5, w - 36)
    yy -= 2
    wrapped(c, x + 18, yy, body, 7.7, MUTED, 'Helvetica', 9.2, w - 36)
    c.setStrokeColor(accent)
    c.setLineWidth(1.2)
    c.line(x + 18, y - h + 24, x + w - 18, y - h + 24)
    c.setFillColor(accent)
    c.setFont('Helvetica-Bold', 6.5)
    c.drawString(x + 18, y - h + 12, 'INPUT -> RULES -> PROOF')
    c.linkURL(url, (x, y - h, x + w, y), relative=0)


def cap(c, x, y, w, title, body):
    h = 62
    c.setFillColor(WHITE)
    c.setStrokeColor(LINE)
    c.roundRect(x, y - h, w, h, 12, fill=1, stroke=1)
    c.setFillColor(TEAL)
    c.roundRect(x + 10, y - 19, 18, 8, 4, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 10)
    c.drawString(x + 10, y - 31, title)
    wrapped(c, x + 10, y - 46, body, 6.8, MUTED, 'Helvetica', 8.0, w - 20)


def draw_qr(c, url, x, y, size):
    widget = qr.QrCodeWidget(url)
    b = widget.getBounds()
    drawing = Drawing(size, size, transform=[size / (b[2] - b[0]), 0, 0, size / (b[3] - b[1]), 0, 0])
    drawing.add(widget)
    renderPDF.draw(drawing, c, x, y)
    c.linkURL(url, (x, y, x + size, y + size), relative=0)


def draw_page_one(c):
    page_shell(c, 'PUBLIC DILIGENCE PACKET')
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 30)
    c.drawString(M, H - M - 35, 'Tim Sullivan')
    c.setFont('Helvetica-Bold', 13)
    c.drawString(M, H - M - 57, 'Product systems, workflow automation, and evidence-backed artifacts')
    wrapped(c, M, H - M - 78, 'A two-page route for evaluating public work: what changed, what was built, and where implementation proof lives.', 9.2, MUTED, 'Helvetica', 11, 430)

    bx, by, bw, bh = W - M - 2.85 * inch, H - M - 5, 2.85 * inch, 1.12 * inch
    c.setFillColor(DARK)
    c.roundRect(bx, by - bh, bw, bh, 18, fill=1, stroke=0)
    c.setFillColor(CYAN)
    c.setFont('Helvetica-Bold', 7)
    c.drawString(bx + 14, by - 20, 'FAST REVIEW ROUTE')
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 13)
    c.drawString(bx + 14, by - 44, 'outcomes -> model -> lab')
    c.setFillColor(colors.HexColor('#b7c7d0'))
    c.setFont('Helvetica', 8)
    c.drawString(bx + 14, by - 63, 'Clickable links embedded')
    c.linkURL(links['diligence'], (bx, by - bh, bx + bw, by), relative=0)

    y = H - 2.02 * inch
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 14)
    c.drawString(M, y, 'What to inspect first')
    x = M
    for label, url in [('Portfolio', links['portfolio']), ('Outcome board', links['outcomes']), ('Operating model', links['operating']), ('Systems lab', links['lab']), ('GitHub', links['github'])]:
        x = pill(c, x, y - 25, label, url)

    y -= 65
    mw = (W - 2 * M - 36) / 4
    for i, (big, small, accent) in enumerate([('43', 'passing public tests', TEAL), ('25', 'SquadBrain tests', BLUE), ('18', 'Lasting Ground tests', GOLD), ('CI', 'repeatable checks', DARK3)]):
        metric(c, M + i * (mw + 12), y, mw, big, small, accent)

    y -= 70
    flow_ribbon(c, M, y, W - 2 * M, ['outcome evidence', 'operating model', 'systems lab', 'public code'])
    y -= 72
    pw = (W - 2 * M - 18) / 2
    ph = 1.64 * inch
    project_card(c, M, y, pw, ph, 'Mobile', 'SquadBrain: competitive practice system', 'Replayable practice with adaptive priority, matchmaking, achievements, and validated results.', '98.3% line coverage - TypeScript - ADRs', links['squad'], BLUE)
    project_card(c, M + pw + 18, y, pw, ph, 'Evidence', 'Lasting Ground: source-bounded packet system', 'Source lanes, support-depth states, validation gates, cautious language, and a sample packet.', '93.29% line coverage - Python - PDF', links['lasting'], GOLD)

    y -= ph + 24
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 14)
    c.drawString(M, y, 'Capability signals')
    y -= 20
    cw = (W - 2 * M - 36) / 4
    caps = [
        ('Product judgment', 'Turns workflows into clear surfaces, demos, states, and readable outputs.'),
        ('Systems thinking', 'Models rules, scoring, validation, review boundaries, and source states.'),
        ('Evidence discipline', 'Shows uncertainty, support depth, and proof links instead of vague claims.'),
        ('Delivery maturity', 'Ships tests, coverage, CI, docs, ADRs, and sample artifacts.'),
    ]
    for i, (t, b) in enumerate(caps):
        cap(c, M + i * (cw + 12), y, cw, t, b)
    footer(c, 'page 1')


def review_tile(c, x, y, w, h, title, body, url, dark=False):
    c.setFillColor(DARK if dark else WHITE)
    c.setStrokeColor(colors.Color(1, 1, 1, .18) if dark else LINE)
    c.roundRect(x, y - h, w, h, 14, fill=1, stroke=1)
    c.setFillColor(CYAN if dark else INK)
    c.setFont('Helvetica-Bold', 10)
    c.drawString(x + 12, y - 20, title)
    wrapped(c, x + 12, y - 38, body, 7.8, colors.HexColor('#c7d4db') if dark else MUTED, 'Helvetica', 9.5, w - 24)
    c.linkURL(url, (x, y - h, x + w, y), relative=0)


def evidence_cell(c, x, y, w, h, label, value, url, accent):
    c.setFillColor(WHITE)
    c.setStrokeColor(LINE)
    c.roundRect(x, y - h, w, h, 12, fill=1, stroke=1)
    c.setFillColor(accent)
    c.rect(x + 10, y - h + 9, 3, h - 18, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 9.4)
    c.drawString(x + 20, y - 19, label)
    c.setFillColor(MUTED)
    c.setFont('Helvetica', 8)
    c.drawString(x + 20, y - 35, value)
    c.linkURL(url, (x, y - h, x + w, y), relative=0)


def draw_page_two(c):
    page_shell(c, 'INSPECTION LEDGER')
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 25)
    c.drawString(M, H - M - 36, 'Proof routes, review timing, and public artifacts')
    wrapped(c, M, H - M - 60, 'Use this page to choose the right depth of review. Every route points to public artifacts that can be opened directly.', 9.2, MUTED, 'Helvetica', 11, 540)

    qr_size = 0.74 * inch
    qx = W - M - qr_size
    qy = H - M - 0.92 * inch
    c.setFillColor(WHITE)
    c.roundRect(qx - 8, qy - 8, qr_size + 16, qr_size + 16, 10, fill=1, stroke=0)
    draw_qr(c, links['diligence'], qx, qy, qr_size)
    c.setFillColor(MUTED)
    c.setFont('Helvetica-Bold', 7)
    c.drawRightString(W - M, H - M - 1.03 * inch, 'scan for live packet')

    y = H - 1.92 * inch
    tile_w = (W - 2 * M - 36) / 4
    tiles = [
        ('1 minute', 'Open the outcome board and check the two project evidence trails.', links['outcomes'], False),
        ('5 minutes', 'Run the systems lab, then open one code example from each project.', links['lab'], False),
        ('15 minutes', 'Read the operating model, decision records, and coverage summaries.', links['operating'], False),
        ('Full review', 'Start at the evaluator console and follow the role-specific path.', links['review'], True),
    ]
    for i, (t, b, u, dark) in enumerate(tiles):
        review_tile(c, M + i * (tile_w + 12), y, tile_w, 0.78 * inch, t, b, u, dark)

    y -= 0.78 * inch + 30
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 14)
    c.drawString(M, y, 'Public evidence map')
    y -= 18
    col_w = (W - 2 * M - 18) / 2
    c.setFillColor(DARK)
    c.roundRect(M, y - 30, col_w, 30, 12, fill=1, stroke=0)
    c.roundRect(M + col_w + 18, y - 30, col_w, 30, 12, fill=1, stroke=0)
    c.setFillColor(CYAN)
    c.setFont('Helvetica-Bold', 8)
    c.drawString(M + 14, y - 19, 'SQUADBRAIN')
    c.drawString(M + col_w + 32, y - 19, 'LASTING GROUND')
    y -= 42
    rows = [
        ('Live surface', 'SquadBrain demo', links['squad_demo'], 'Lasting Ground demo', links['lasting_demo']),
        ('Executable logic', 'TypeScript examples', links['squad_examples'], 'Python examples', links['lasting_examples']),
        ('Quality proof', '25 tests / 98.3% line coverage', links['squad_coverage'], '18 tests / 93.29% line coverage', links['lasting_coverage']),
        ('System boundary', 'Result validation / adaptive practice', links['squad'], 'Evidence scoring / support depth', links['lasting']),
    ]
    row_h = 0.50 * inch
    for idx, (label, s_text, s_url, l_text, l_url) in enumerate(rows):
        evidence_cell(c, M, y, col_w, row_h, label, s_text, s_url, BLUE)
        evidence_cell(c, M + col_w + 18, y, col_w, row_h, label, l_text, l_url, GOLD)
        y -= row_h + 8

    gy = 1.12 * inch
    c.setFillColor(DARK)
    c.roundRect(M, gy, W - 2 * M, 0.62 * inch, 16, fill=1, stroke=0)
    c.setFillColor(CYAN)
    c.setFont('Helvetica-Bold', 7)
    c.drawString(M + 14, gy + 28, 'EVALUATION RULE')
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 10)
    c.drawString(M + 14, gy + 13, 'Treat a claim as strong only when it links to a working demo, public example, test/coverage artifact, decision record, or sample output.')
    footer(c, 'page 2')


def draw():
    c = canvas.Canvas(str(OUT), pagesize=(W, H))
    c.setTitle('Tim Sullivan - Public Diligence Packet')
    c.setAuthor('Tim Sullivan')
    c.setSubject('Product systems portfolio proof packet')
    draw_page_one(c)
    c.showPage()
    draw_page_two(c)
    c.showPage()
    c.save()


if __name__ == '__main__':
    draw()
    print(OUT)
