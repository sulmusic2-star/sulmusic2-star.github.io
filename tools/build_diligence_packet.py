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
M = 0.46 * inch
INK = colors.HexColor('#07111c')
MUTED = colors.HexColor('#526170')
LINE = colors.HexColor('#c4d3db')
TEAL = colors.HexColor('#159e9a')
GOLD = colors.HexColor('#b5671a')
PAPER = colors.HexColor('#f6f2ea')
PANEL = colors.HexColor('#eef7f9')
DARK = colors.HexColor('#0b263c')
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


def pill(c, x, y, label, url):
    w = stringWidth(label, 'Helvetica-Bold', 8) + 18
    c.setStrokeColor(LINE)
    c.setFillColor(WHITE)
    c.roundRect(x, y - 14, w, 22, 11, fill=1, stroke=1)
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 8)
    c.drawString(x + 9, y - 7, label)
    c.linkURL(url, (x, y - 14, x + w, y + 8), relative=0)
    return x + w + 8


def metric(c, x, y, w, big, small):
    c.setFillColor(PANEL)
    c.setStrokeColor(LINE)
    c.roundRect(x, y - 50, w, 50, 13, fill=1, stroke=1)
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 20)
    c.drawString(x + 12, y - 22, big)
    c.setFillColor(MUTED)
    c.setFont('Helvetica-Bold', 8)
    c.drawString(x + 12, y - 38, small)


def project(c, x, y, w, h, kicker, title, body, proof, url):
    c.setFillColor(WHITE)
    c.setStrokeColor(LINE)
    c.roundRect(x, y - h, w, h, 18, fill=1, stroke=1)
    c.setFillColor(GOLD)
    c.setFont('Helvetica-Bold', 7)
    c.drawString(x + 14, y - 22, kicker.upper())
    c.setFillColor(TEAL)
    c.setFont('Helvetica-Bold', 7.5)
    c.drawRightString(x + w - 14, y - 22, proof)
    yy = wrapped(c, x + 14, y - 48, title, 18, INK, 'Helvetica-Bold', 20, w - 28)
    yy -= 4
    wrapped(c, x + 14, yy, body, 8.6, MUTED, 'Helvetica', 10.5, w - 28)
    c.linkURL(url, (x, y - h, x + w, y), relative=0)


def cap(c, x, y, w, title, body):
    c.setFillColor(WHITE)
    c.setStrokeColor(LINE)
    c.roundRect(x, y - 72, w, 72, 12, fill=1, stroke=1)
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 10)
    c.drawString(x + 10, y - 20, title)
    wrapped(c, x + 10, y - 36, body, 7.8, MUTED, 'Helvetica', 9.5, w - 20)


def draw_qr(c, url, x, y, size):
    widget = qr.QrCodeWidget(url)
    bounds = widget.getBounds()
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    drawing = Drawing(size, size, transform=[size / width, 0, 0, size / height, 0, 0])
    drawing.add(widget)
    renderPDF.draw(drawing, c, x, y)
    c.linkURL(url, (x, y, x + size, y + size), relative=0)


def header(c, label='PUBLIC DILIGENCE PACKET'):
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(colors.HexColor('#e7f4f7'))
    c.rect(0, H - 1.55 * inch, W, 1.55 * inch, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.setFont('Helvetica-Bold', 8)
    c.drawString(M, H - M - 2, label)


def footer(c, page):
    c.setFillColor(MUTED)
    c.setFont('Helvetica', 7.5)
    c.drawString(M, 0.34 * inch, 'Public proof packet - links route to live demos, GitHub examples, coverage summaries, decision records, and sample artifacts.')
    c.setFillColor(TEAL)
    c.setFont('Helvetica-Bold', 7.5)
    c.drawRightString(W - M, 0.34 * inch, f'sulmusic2-star.github.io / {page}')
    c.linkURL(links['portfolio'], (W - M - 130, 0.27 * inch, W - M, 0.47 * inch), relative=0)


def draw_page_one(c):
    header(c)
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 30)
    c.drawString(M, H - M - 34, 'Tim Sullivan')
    c.setFont('Helvetica-Bold', 13)
    c.drawString(M, H - M - 56, 'Product systems, workflow automation, and evidence-backed artifacts')
    wrapped(c, M, H - M - 76, 'A two-page route for evaluating public work: what changed, what was built, and where implementation proof lives.', 9.2, MUTED, 'Helvetica', 11, 420)

    bx, by, bw, bh = W - M - 2.6 * inch, H - M - 4, 2.6 * inch, 1.08 * inch
    c.setFillColor(DARK)
    c.roundRect(bx, by - bh, bw, bh, 18, fill=1, stroke=0)
    c.setFillColor(colors.HexColor('#6fffe8'))
    c.setFont('Helvetica-Bold', 7)
    c.drawString(bx + 14, by - 20, 'FAST REVIEW ROUTE')
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 13)
    c.drawString(bx + 14, by - 44, 'outcomes -> model -> lab')
    c.setFillColor(colors.HexColor('#b7c7d0'))
    c.setFont('Helvetica', 8)
    c.drawString(bx + 14, by - 63, 'Clickable links embedded')

    y = H - 2.02 * inch
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 14)
    c.drawString(M, y, 'What to inspect first')
    x = M
    for label, url in [('Portfolio', links['portfolio']), ('Outcome board', links['outcomes']), ('Operating model', links['operating']), ('Systems lab', links['lab']), ('GitHub', links['github'])]:
        x = pill(c, x, y - 25, label, url)

    y -= 66
    mw = (W - 2 * M - 36) / 4
    for i, (big, small) in enumerate([('43', 'passing public tests'), ('25', 'SquadBrain tests'), ('18', 'Lasting Ground tests'), ('CI', 'repeatable checks')]):
        metric(c, M + i * (mw + 12), y, mw, big, small)

    y -= 78
    pw = (W - 2 * M - 18) / 2
    ph = 1.72 * inch
    project(c, M, y, pw, ph, 'Mobile product system', 'SquadBrain: competitive practice system', 'Replayable practice with adaptive priority, matchmaking, achievements, and validated results.', '98.3% line coverage - TypeScript - ADRs', links['squad'])
    project(c, M + pw + 18, y, pw, ph, 'Evidence system', 'Lasting Ground: source-bounded packet system', 'Source lanes, support-depth states, validation gates, cautious language, and a sample packet.', '93.29% line coverage - Python - PDF', links['lasting'])

    y -= ph + 42
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


def draw_ledger_cell(c, x, y, w, h, title, body, url=None):
    c.setFillColor(WHITE)
    c.setStrokeColor(LINE)
    c.roundRect(x, y - h, w, h, 14, fill=1, stroke=1)
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 10)
    c.drawString(x + 12, y - 20, title)
    wrapped(c, x + 12, y - 38, body, 7.8, MUTED, 'Helvetica', 9.5, w - 24)
    if url:
        c.linkURL(url, (x, y - h, x + w, y), relative=0)


def draw_page_two(c):
    header(c, 'INSPECTION LEDGER')
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 25)
    c.drawString(M, H - M - 36, 'Proof routes, review timing, and public artifacts')
    wrapped(c, M, H - M - 60, 'Use this page to choose the right depth of review. Every route points to public artifacts that can be opened directly.', 9.2, MUTED, 'Helvetica', 11, 520)

    qr_size = 0.8 * inch
    draw_qr(c, links['diligence'], W - M - qr_size, H - M - 0.95 * inch, qr_size)
    c.setFillColor(MUTED)
    c.setFont('Helvetica-Bold', 7)
    c.drawRightString(W - M, H - M - 1.05 * inch, 'scan for live packet')

    y = H - 1.9 * inch
    cols = [M, M + 2.55 * inch, M + 5.1 * inch, M + 7.65 * inch]
    widths = [2.32 * inch, 2.32 * inch, 2.32 * inch, 2.32 * inch]
    h = 0.82 * inch
    items = [
        ('1 minute', 'Open the outcome board and check the two project evidence trails.', links['outcomes']),
        ('5 minutes', 'Run the systems lab, then open one code example from each project.', links['lab']),
        ('15 minutes', 'Read the operating model, decision records, and coverage summaries.', links['operating']),
        ('Full review', 'Start at the evaluator console and follow the role-specific path.', links['review']),
    ]
    for x, w, (t, b, u) in zip(cols, widths, items):
        draw_ledger_cell(c, x, y, w, h, t, b, u)

    y -= h + 0.38 * inch
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 14)
    c.drawString(M, y, 'Public evidence map')
    y -= 18
    left_w = (W - 2 * M - 18) / 2
    row_h = 0.56 * inch
    rows = [
        ('Live surface', 'SquadBrain demo', links['squad_demo'], 'Lasting Ground demo', links['lasting_demo']),
        ('Executable logic', 'TypeScript examples', links['squad_examples'], 'Python examples', links['lasting_examples']),
        ('Quality proof', '25 tests / 98.3% line coverage', links['squad_coverage'], '18 tests / 93.29% line coverage', links['lasting_coverage']),
        ('System boundary', 'Result validation / adaptive practice', links['squad'], 'Evidence scoring / support depth', links['lasting']),
    ]
    # Headers
    c.setFillColor(DARK)
    c.roundRect(M, y - 30, left_w, 30, 12, fill=1, stroke=0)
    c.roundRect(M + left_w + 18, y - 30, left_w, 30, 12, fill=1, stroke=0)
    c.setFillColor(colors.HexColor('#6fffe8'))
    c.setFont('Helvetica-Bold', 8)
    c.drawString(M + 14, y - 19, 'SQUADBRAIN')
    c.drawString(M + left_w + 32, y - 19, 'LASTING GROUND')
    y -= 42
    for label, s_text, s_url, l_text, l_url in rows:
        draw_ledger_cell(c, M, y, left_w, row_h, label, s_text, s_url)
        draw_ledger_cell(c, M + left_w + 18, y, left_w, row_h, label, l_text, l_url)
        y -= row_h + 8

    # Guardrail strip
    gy = 1.15 * inch
    c.setFillColor(PANEL)
    c.setStrokeColor(LINE)
    c.roundRect(M, gy, W - 2 * M, 0.58 * inch, 14, fill=1, stroke=1)
    c.setFillColor(GOLD)
    c.setFont('Helvetica-Bold', 7)
    c.drawString(M + 14, gy + 25, 'EVALUATION RULE')
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 10)
    c.drawString(M + 14, gy + 11, 'Only treat a claim as strong when it links to a working demo, public example, test/coverage artifact, decision record, or sample output.')
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
