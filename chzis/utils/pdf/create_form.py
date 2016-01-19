# -- coding: utf-8 --

import time
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.graphics.widgets import signsandsymbols
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

styles = getSampleStyleSheet()
pdfmetrics.registerFont(TTFont('Arial_Bold.', 'Arial_Bold.ttf'))
pdfmetrics.registerFont(TTFont('Verdana_Bold', 'Verdana_Bold.ttf'))

page_size = (3.50 * inch, 5.0 * inch)
doc = SimpleDocTemplate("form_letter.pdf",pagesize=page_size,
                        rightMargin=1,
                        leftMargin=1,
                        topMargin=1,
                        bottomMargin=1)


participants = ParagraphStyle(name="base",
                             fontName="Arial_Bold.",
                             alignment=TA_CENTER,
                             fontSize=13,
                             )

page_content = []
header = Paragraph("<strong>ZADANIE PODCZAS ZEBRANIA CHCRZESCIJAŃSKIEGO ŻYCIA I SŁUŻBY</strong>", participants)
# d = Drawing(10, 230)
# crossbox = signsandsymbols.Crossbox()
# crossbox.size = 10
# crossbox.crosswidth = 1
# d.add(crossbox)
# tickbox = signsandsymbols.Tickbox()
# tickbox.tickColor = colors.white
# d.add(tickbox)
# print letter
page_content.append(header)

#page_content.append(d)




doc.build(page_content)
