from itertools import cycle

def scalebar(xi,
             yi,
             height,
             lenght=None,
             element_lenght=None,
             element_number=None,
             font_size=None):
    """
    Draw a scalebar. Return a list of lines.
    """
    zero1 = cycle([1, 0])
    half_height = height/2.
    if font_size is None:
        font_size = half_height
    lines = []
    if element_number is None:
        element_number = int(lenght/element_lenght)
    xn = xi
    for i in range(element_number):
        lines.append(r"""<rect
           x="%s"
           y="%s"
           width="%s"
           height="%s"
           stroke="blue"
           stroke-width="0"
           fill="blue"/>""" % (xn,
                               yi + half_height*next(zero1),
                               element_lenght,
                               half_height,)+"\n")
        lines.append(r'<text x="%s" y="%s" fill="blue" font-size="%s" '
                     'text-anchor="middle" >'
                     '%s </text>' % (
                                     xn,
                                     yi - half_height/5.,
                                     font_size,
                                     element_lenght*i))
        xn += element_lenght
    lines.append(r'<text x="%s" y="%s" fill="blue" font-size="%s" '
                 'text-anchor="middle" >'
                 '%s </text>' % (
                                 xn,
                                 yi - half_height/5.,
                                 font_size,
                                 element_lenght*(i+1)))
    lines.append(r"""<text x="%s" y="%s" fill="blue" font-size="%s">
        mm </text>""" % (
            element_lenght*element_number + xi + element_lenght/10.,
            yi + half_height,
            font_size))
    return lines


def scalebar(xi,
             yi,
             height,
             lenght=None,
             element_lenght=None,
             element_number=None,
             font_size=None):
    """
    Draw a scalebar. The rectangle and the text
    """
    zero1 = cycle([1, 0])
    half_height = height/2.
    if font_size is None:
        font_size = half_height
    text = []
    square_elements = []
    if element_number is None:
        element_number = int(lenght/element_lenght)
    xn = xi
    for i in range(element_number):
        square_elements.append((xn,
                               yi + half_height*next(zero1),
                               element_lenght,
                               half_height))
        text.append((xn,
                    yi - half_height/5.,
                    font_size,
                    element_lenght*i))
        xn += element_lenght
    text.append((xn,
                yi - half_height/5.,
                font_size,
                element_lenght*(i+1)))
    text.append((
            element_lenght*element_number + xi + element_lenght/10.,
            yi + half_height,
            font_size,
            "mm"))
    return square_elements,text
