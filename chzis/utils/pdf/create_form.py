# -- coding: utf-8 --

import time
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Frame, BaseDocTemplate, PageTemplate, FrameBreak, PageBreak, NextPageTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.graphics.shapes import Drawing, String, Line
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.graphics.widgets import signsandsymbols
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.graphics import shapes
from reportlab import isPy3


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


class ShowBoundaryValue:
    def __init__(self,color=(0,0,0),width=0.1):
        self.color = color
        self.width = width

    if isPy3:
        def __bool__(self):
            return self.color is not None and self.width>=0
    else:
        def __nonzero__(self):
            return self.color is not None and self.width>=0


class MyFrame(Frame):

    def drawBoundary(self,canv):
            "draw the frame boundary as a rectangle (primarily for debugging)."
            from reportlab.lib.colors import Color, CMYKColor, toColor
            sb = self.showBoundary
            ss = type(sb) in (type(''),type(()),type([])) or isinstance(sb,Color)
            w = -1
            if ss:
                c = toColor(sb,self)
                ss = c is not self
            elif isinstance(sb,ShowBoundaryValue) and sb:
                c = toColor(sb.color,self)
                w = sb.width
                ss = c is not self
            if ss:
                canv.saveState()
                canv.setStrokeColor(c)
                if w>=0:
                    canv.setLineWidth(w)
            canv.rect(
                    self._x1 - 20,
                    self._y1,
                    self._x2 - self._x1 + 40,
                    self._y2 - self._y1
                    )
            if ss: canv.restoreState()

styles = getSampleStyleSheet()
pdfmetrics.registerFont(TTFont('Arial_Bold', 'Arial_Bold.ttf'))
pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial_Italic', 'Arial_Italic.ttf'))
pdfmetrics.registerFont(TTFont('Verdana_Bold', 'Verdana_Bold.ttf'))
pdfmetrics.registerFont(TTFont('Courier_New', 'Courier_New.ttf'))


def create_meeting_task_card(data=None, school_class=None):
    # page_size = (88.5 * mm, 140 * mm)
    # doc = SimpleDocTemplate("form_letter.pdf", pagesize=page_size,
    #                         rightMargin=0,
    #                         leftMargin=0,
    #                         topMargin=0,
    #                         bottomMargin=0)

    dynamic_content = {"name": "",
                       "slave": "",
                       "date": "",
                       "lesson": "",
                       "task_type": "",
                       "class": 1
                       }

    if data is not None:
        dynamic_content.update(data)

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
                                        wordWrap="LTR",
                                        allowOrphans = 0,
                                        allowWidows= 0,
                                        splitLongWords = 1
                                        )

    lesson_style = ParagraphStyle(name="base",
                                        fontName="Arial_Bold",
                                        alignment=TA_LEFT,
                                        fontSize=11.8,
                                        rightIndent=0,
                                        leftIndent=5,
                                        leading=13,
                                        wordWrap="LTR",
                                        allowOrphans = 0,
                                        allowWidows= 0,
                                        splitLongWords = 1
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
    user_name = Paragraph(u"Imię i nazwisko:<font name='Courier_New' size='12'>  {name}</font>".format(name=dynamic_content.get("name")), introduction_style)
    page_content.append(user_name)
    slave_user = Paragraph(
        "<para>Pomocnik(-ca):<font name='Courier_New' size='12'>  {slave}</font></para>".format(slave=dynamic_content.get("slave")),
        introduction_style)
    page_content.append(slave_user)
    date = Paragraph("Data:<font name='Courier_New' size='12'>  {date}</font>".format(date=dynamic_content.get('date')), introduction_style)
    page_content.append(date)
    lesson = Paragraph(u"Cecha przemawiania:<font name='Courier_New' size='12'>  {lesson}</font>".format(lesson=dynamic_content.get('lesson')), lesson_style)
    page_content.append(lesson)
    page_content.append(Spacer(0, 5 * mm))

    d = Drawing(10, 15)
    d.add(String(5, 1, "Zadanie", fontName="Arial_Bold", fontSize=9))
    page_content.append(d)

    d = Drawing(20, 13)
    d.add(MyCrossBox(left_col_margin, selected=True if dynamic_content.get('task_type') == "Bible Reading" else False))
    d.add(String(15 + left_col_margin, 1, "Czytanie Biblii", fontName="Arial", fontSize=9))
    d.add(String(136, 14, "Zadanie przedstawisz", fontName="Arial_Bold", fontSize=9))
    d.add(String(136, 1, "w sali:", fontName="Arial_Bold", fontSize=9))
    page_content.append(d)

    d = Drawing(20, 13)
    d.add(MyCrossBox(left_col_margin, selected=True if dynamic_content.get('task_type') == "Initial Call" else False))
    d.add(String(15 + left_col_margin, 1, "Pierwsza rozmowa", fontName="Arial", fontSize=9))

    d.add(MyCrossBox(right_col_margin - 2, selected=True if dynamic_content.get('class') == 1 else False))
    d.add(String(15 + right_col_margin, 1, "głównej", fontName="Arial", fontSize=9))

    page_content.append(d)
    d = Drawing(20, 13)
    d.add(MyCrossBox(left_col_margin, selected=True if dynamic_content.get('task_type') == "Return Visit" else False))
    d.add(String(15 + left_col_margin, 1, "Odwiedziny ponowne", fontName="Arial", fontSize=9))

    d.add(MyCrossBox(right_col_margin - 2, selected=True if dynamic_content.get('class') == 2 else False))
    d.add(String(15 + right_col_margin, 1, "drugiej", fontName="Arial", fontSize=9))

    page_content.append(d)
    d = Drawing(20, 13)
    d.add(MyCrossBox(left_col_margin, selected=True if dynamic_content.get('task_type') == "Bible Study" else False))
    d.add(String(15 + left_col_margin, 1, "Studium biblijne", fontName="Arial", fontSize=9))

    d.add(MyCrossBox(right_col_margin - 2, selected=True if dynamic_content.get('class') == 3 else False))
    d.add(String(15 + right_col_margin, 1, "trzeciej", fontName="Arial", fontSize=9))

    page_content.append(d)
    d = Drawing(20, 13)
    d.add(MyCrossBox(left_col_margin, selected=True if dynamic_content.get('task_type') == "Other" else False))
    d.add(String(15 + left_col_margin, 1, "Inne: ................................", fontName="Arial", fontSize=9))
    page_content.append(d)

    page_content.append(Spacer(0, 9.5 * mm))

    footer = Paragraph(
        "<para><font name='Arial_Bold'>Wskazówki:</font> Potrzebne informacje dotyczące twojego wystąpie-<br/>nia znajdziesz w miesięczniku <font name='Arial_Italic'>Chrzescijańskie życie i słuzba - pro<br/>gram zebrań.</font>" \
        " Pracuj nad wskazaną wyżej cechą przemawiania. Została ona opisana w podręczniku Szkoła teokratyczna. <font name='Arial_Bold'>Wez go ze sobą " \
        " na zebranie chrzescijańskiego życia i służby.</font></para>", footer_style)
    page_content.append(footer)

    page_content.append(Spacer(0, 7.0 * mm))
    annonation = Paragraph("S-89-P 10/15", annonation_style)
    page_content.append(annonation)

    return page_content


def build_pdf(data):
    A4_width, A4_height = A4[0], A4[1]
    doc = SimpleDocTemplate("form_letter.pdf", pagesize=A4,
                            rightMargin=0,
                            leftMargin=0,
                            topMargin=0,
                            bottomMargin=0)
    pdf_content = []
    frames = []
    w_counter = 0
    h_counter = 1
    width_position = 0
    same_line = True
    frame_w = 88.5 * mm
    frame_h = 140 * mm
    height_position = h_counter * frame_h
    frame_counter = 1
    for d in data:
        if A4_width - w_counter * frame_w > frame_w:
            if w_counter % 2 == 0:
                add = 0
            else:
                add = 40
            width_position = w_counter * frame_w + add
            same_line = True
        else:
            same_line = False
            w_counter = 0
            width_position = 0

        if not same_line:
            if A4_height - h_counter * frame_h >= frame_h:
                h_counter -= 1
                height_position = h_counter * frame_h
                same_line = True
        w_counter += 1

        frame_content = create_meeting_task_card(d)
        left_padding = (A4_width - 2 * 88.5 * mm - 40) / 2
        bottom_padding = (A4_height - 2 * 140 * mm) / 2
        frames.append(MyFrame(left_padding + width_position, bottom_padding + height_position, 88.5 * mm, 140 * mm, showBoundary=1))
        pdf_content.extend(frame_content)
        if len(frames) < len(data):
            pdf_content.append(FrameBreak())

        if frame_counter % 4 == 0 and len(data) - frame_counter * 4 > 0:
            w_counter = 0
            h_counter = 1
            same_line = True
            width_position = 0
            height_position = h_counter * frame_h
            pdf_content.append(NextPageTemplate("main_template"))
            pdf_content.append(PageBreak())

        frame_counter += 1

    template = PageTemplate(id = 'main_template', frames=frames)
    doc.addPageTemplates(template)
    doc.build(pdf_content)

if __name__ == '__main__':
    build_pdf(data=None)