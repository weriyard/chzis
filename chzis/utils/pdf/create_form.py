# -- coding: utf-8 --

import time
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Frame, BaseDocTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.graphics.shapes import Drawing, String
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.graphics.widgets import signsandsymbols
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.graphics import shapes


class MyCrossBox(signsandsymbols.Crossbox):
    def __init__(self, x=0, y=0):
        signsandsymbols.Crossbox.__init__(self)
        self.x = x
        self.y = y

    def draw(self):
        # general widget bits
        s = float(self.size)  # abbreviate as we will use this a lot
        g = shapes.Group()

        # crossbox specific bits
        box = shapes.Rect(self.x + 1, self.y + 1, s - 2, s - 2,
                          fillColor=self.fillColor,
                          strokeColor=self.strokeColor,
                          strokeWidth=0.6)
        g.add(box)

        crossLine1 = shapes.Line(self.x + (s * 0.15), self.y + (s * 0.15), self.x + (s * 0.85), self.y + (s * 0.85),
                                 fillColor=self.crossColor,
                                 strokeColor=self.crossColor,
                                 strokeWidth=self.crosswidth)
        g.add(crossLine1)

        crossLine2 = shapes.Line(self.x + (s * 0.15), self.y + (s * 0.85), self.x + (s * 0.85), self.y + (s * 0.15),
                                 fillColor=self.crossColor,
                                 strokeColor=self.crossColor,
                                 strokeWidth=self.crosswidth)
        g.add(crossLine2)

        return g


styles = getSampleStyleSheet()
pdfmetrics.registerFont(TTFont('Arial_Bold', 'Arial_Bold.ttf'))
pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial_Italic', 'Arial_Italic.ttf'))
pdfmetrics.registerFont(TTFont('Verdana_Bold', 'Verdana_Bold.ttf'))

page_size = (88.5 * mm, 140 * mm)
doc = SimpleDocTemplate("form_letter.pdf", pagesize=page_size,
                        rightMargin=0,
                        leftMargin=0,
                        topMargin=0,
                        bottomMargin=0)

header_style = ParagraphStyle(name="base",
                              fontName="Arial_Bold",
                              alignment=TA_CENTER,
                              fontSize=12.1,
                              rightIndent=-4,
                              leftIndent=-4,
                              leading=14,
                              )

introduction_style = ParagraphStyle(name="base",
                                    fontName="Arial_Bold",
                                    alignment=TA_LEFT,
                                    fontSize=11.8,
                                    rightIndent=0,
                                    leftIndent=5,
                                    leading=26,
                                    )

footer_style = ParagraphStyle(name="base",
                              fontName="Arial",
                              alignment=TA_LEFT,
                              fontSize=8,
                              rightIndent=0,
                              leading=10,
                              leftIndent=5,
                              allowOrphans = 1,
                              splitLongWords = 1
                              )

annonation_style = ParagraphStyle(name="base",
                                  fontName="Arial",
                                  alignment=TA_LEFT,
                                  fontSize=7.5,
                                  rightIndent=0,
                                  leading=10,
                                  leftIndent=5,
                                  )

page_content = []

left_col_margin = 19
right_col_margin = 152

page_content.append(Spacer(0, 5 * mm))
header = Paragraph("<strong>ZADANIE PODCZAS ZEBRANIA CHRZESCIJAŃSKIEGO ŻYCIA I SŁUŻBY</strong>", header_style)
page_content.append(header)
page_content.append(Spacer(0, 8 * mm))
user_name = Paragraph("Imię i nazwisko:<font name='Arial' size='9'>........................................................</font>", introduction_style)
page_content.append(user_name)
slave_user = Paragraph(
    "<para>Pomocnik(-ca):<font name='Arial' size='9'>..........................................................</font></para>",
    introduction_style)
page_content.append(slave_user)
date = Paragraph("Data:<font name='Arial' size='9'>................................................................................</font>", introduction_style)
page_content.append(date)
property = Paragraph("Cecha przemawiania:.<font name='Arial' size='9'>...........................................</font>", introduction_style)
page_content.append(property)
page_content.append(Spacer(0, 5 * mm))

d = Drawing(10, 15)
d.add(String(5, 1, "Zadanie", fontName="Arial_Bold", fontSize=9))
page_content.append(d)

d = Drawing(20, 13)
crossbox = MyCrossBox(left_col_margin)
crossbox.size = 8
crossbox.crosswidth = 0.2
#crossbox.crossColor = colors.white
d.add(crossbox)
d.add(String(15 + left_col_margin, 1, "Czytanie Biblii", fontName="Arial", fontSize=9))
d.add(String(136, 14, "Zadanie przedstawisz", fontName="Arial_Bold", fontSize=9))
d.add(String(136, 1, "w sali:", fontName="Arial_Bold", fontSize=9))
page_content.append(d)

d = Drawing(20, 13)
crossbox = MyCrossBox(left_col_margin)
crossbox.size = 8
crossbox.crosswidth = 0.4
crossbox.crossColor = colors.white
d.add(crossbox)
d.add(String(15 + left_col_margin, 1, "Pierwsza rozmowa", fontName="Arial", fontSize=9))

crossbox1 = MyCrossBox(150)
crossbox1.size = 8
crossbox1.crosswidth = 0.4
crossbox1.crossColor = colors.white
d.add(crossbox1)
d.add(String(15 + right_col_margin, 1, "głównej", fontName="Arial", fontSize=9))

page_content.append(d)
d = Drawing(20, 13)
crossbox = MyCrossBox(left_col_margin)
crossbox.size = 8
crossbox.crosswidth = 0.4
crossbox.crossColor = colors.white
d.add(crossbox)
d.add(String(15 + left_col_margin, 1, "Odwiedziny ponowne", fontName="Arial", fontSize=9))

crossbox1 = MyCrossBox(150)
crossbox1.size = 8
crossbox1.crosswidth = 0.4
crossbox1.crossColor = colors.white
d.add(crossbox1)
d.add(String(15 + right_col_margin, 1, "drugiej", fontName="Arial", fontSize=9))

page_content.append(d)
d = Drawing(20, 13)
crossbox = MyCrossBox(left_col_margin)
crossbox.size = 8
crossbox.crosswidth = 0.4
crossbox.crossColor = colors.white
d.add(crossbox)
d.add(String(15 + left_col_margin, 1, "Studium biblijne", fontName="Arial", fontSize=9))

crossbox1 = MyCrossBox(150)
crossbox1.size = 8
crossbox1.crosswidth = 0.4
crossbox1.crossColor = colors.white
d.add(crossbox1)
d.add(String(15 + right_col_margin, 1, "trzeciej", fontName="Arial", fontSize=9))

page_content.append(d)
d = Drawing(20, 13)
crossbox = MyCrossBox(left_col_margin)
crossbox.size = 8
crossbox.crosswidth = 0.4
crossbox.crossColor = colors.white
d.add(crossbox)
d.add(String(15 + left_col_margin, 1, "Inne: ................................", fontName="Arial", fontSize=9))
page_content.append(d)

page_content.append(Spacer(0, 12.5 * mm))

footer = Paragraph(
    "<para><font name='Arial_Bold'>Wskazówki:</font> Potrzebne informacje dotyczące twojego wystąpie-<br/>nia znajdziesz w miesięczniku <font name='Arial_Italic'>Chrzescijańskie życie i słuzba - pro<br/>gram zebrań.</font>" \
    " Pracuj nad wskazaną wyżej cechą przemawiania. Została ona opisana w podręczniku Szkoła teokratyczna. <font name='Arial_Bold'>Wez go ze sobą " \
    " na zebranie chrzescijańskiego życia i służby.</font></para>", footer_style)
page_content.append(footer)

page_content.append(Spacer(0, 7.5 * mm))
annonation = Paragraph("S-89-P 10/15", annonation_style)
page_content.append(annonation)

doc.build(page_content)
