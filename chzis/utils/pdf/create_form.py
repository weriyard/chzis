# -- coding: utf-8 --

import time
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Frame, BaseDocTemplate, PageTemplate, FrameBreak, PageBreak
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
    def __init__(self, x=0, y=0, size=8, oversize=0, selected=False):
        signsandsymbols.Crossbox.__init__(self)
        self.x = x
        self.y = y
        self.size = size
        self._oversize = oversize
        if selected:
            self.select()
        else:
            self.unselect()

    def select(self):
        self.crosswidth = 1
        self.crossColor = colors.black
        self._oversize = 2

    def unselect(self):
        self.crosswidth = 0
        self.crossColor = colors.white
        self._oversize = -1

    def draw(self):
        s = float(self.size)  # abbreviate as we will use this a lot
        g = shapes.Group()

        box = shapes.Rect(self.x + 1, self.y + 1, s - 2, s - 2,
                          fillColor=self.fillColor,
                          strokeColor=self.strokeColor,
                          strokeWidth=0.6)
        g.add(box)

        s += self._oversize

        crossLine1 = shapes.Line(self.x + (s * 0.15) - self._oversize , self.y + (s * 0.15) - self._oversize , self.x + (s * 0.85), self.y + (s * 0.85),
                                 fillColor=self.crossColor,
                                 strokeColor=self.crossColor,
                                 strokeWidth=self.crosswidth)
        g.add(crossLine1)

        crossLine2 = shapes.Line(self.x + (s * 0.15) - self._oversize , self.y + (s * 0.85) , self.x + (s * 0.85), self.y + (s * 0.15) - self._oversize,
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

def create_meeting_task_card(meeting_item=None, school_class=None):
    # page_size = (88.5 * mm, 140 * mm)
    # doc = SimpleDocTemplate("form_letter.pdf", pagesize=page_size,
    #                         rightMargin=0,
    #                         leftMargin=0,
    #                         topMargin=0,
    #                         bottomMargin=0)

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
    d.add(MyCrossBox(left_col_margin, selected=True if meeting_item == "Bible Reading" else False))
    d.add(String(15 + left_col_margin, 1, "Czytanie Biblii", fontName="Arial", fontSize=9))
    d.add(String(136, 14, "Zadanie przedstawisz", fontName="Arial_Bold", fontSize=9))
    d.add(String(136, 1, "w sali:", fontName="Arial_Bold", fontSize=9))
    page_content.append(d)

    d = Drawing(20, 13)
    d.add(MyCrossBox(left_col_margin, selected=True if meeting_item == "Initial Call" else False))
    d.add(String(15 + left_col_margin, 1, "Pierwsza rozmowa", fontName="Arial", fontSize=9))

    d.add(MyCrossBox(right_col_margin - 2, selected=True if school_class == 1 else False))
    d.add(String(15 + right_col_margin, 1, "głównej", fontName="Arial", fontSize=9))

    page_content.append(d)
    d = Drawing(20, 13)
    d.add(MyCrossBox(left_col_margin, selected=True if meeting_item == "Return Visit" else False))
    d.add(String(15 + left_col_margin, 1, "Odwiedziny ponowne", fontName="Arial", fontSize=9))

    d.add(MyCrossBox(right_col_margin - 2, selected=True if school_class == 2 else False))
    d.add(String(15 + right_col_margin, 1, "drugiej", fontName="Arial", fontSize=9))

    page_content.append(d)
    d = Drawing(20, 13)
    d.add(MyCrossBox(left_col_margin, selected=True if meeting_item == "Bible Study" else False))
    d.add(String(15 + left_col_margin, 1, "Studium biblijne", fontName="Arial", fontSize=9))

    d.add(MyCrossBox(right_col_margin - 2, selected=True if school_class == 3 else False))
    d.add(String(15 + right_col_margin, 1, "trzeciej", fontName="Arial", fontSize=9))

    page_content.append(d)
    d = Drawing(20, 13)
    d.add(MyCrossBox(left_col_margin, selected=True if meeting_item == "Other" else False))
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

    return page_content

def build_pdf():
    A4_width, A4_height = A4[0], A4[1]
    print A4
    doc = SimpleDocTemplate("form_letter.pdf", pagesize=A4,
                        rightMargin=0,
                        leftMargin=0,
                        topMargin=0,
                        bottomMargin=0)
    #page_size = (88.5 * mm, 140 * mm)
    pdf_content = []
    frames = []
    tasks = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    w_counter = 0
    h_counter = 1
    width_wstart = 0
    height_start = 0
    frame_w = 88.5 * mm
    frame_h = 140 * mm
    for task in tasks:
        print "------------------"

        print A4_width - w_counter * frame_w
        if A4_width - w_counter * frame_w >= frame_w:
            print 'licze szerokosc', w_counter * frame_w
            width_wstart = w_counter * frame_w
            w_counter += 1
        else:
            h_counter -= 1
            w_counter = 0
            width_wstart = 0
            height_start = 0

        print h_counter * frame_h
        if A4_height - h_counter * frame_h >= frame_h:
            print 'licze wysokosccc', h_counter, frame_h
            height_start = h_counter * frame_h


        frame_content = create_meeting_task_card()
        print "WYM->", width_wstart, height_start
        frames.append(Frame(width_wstart, height_start, 88.5 * mm, 140 * mm))
        pdf_content.extend(frame_content)
        pdf_content.append(FrameBreak())
    template = PageTemplate(frames=frames)
    doc.addPageTemplates(template)
    doc.build(pdf_content)

if __name__ == '__main__':
    build_pdf()