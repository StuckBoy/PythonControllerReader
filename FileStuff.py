from os import listdir

from pygame import draw, font

font.init()
FONT = font.Font('SuperMystery.ttf', 11)
"""
The typeface and size used for font rendering throughout the file.
"""
default_color = (75, 200, 200)
"""
The default color used throughout the file to render text.
"""


class ColorBox:
    rect = False
    textitem = False
    text = ""

    def __init__(self):
        self.text = "#rrggbb"
        self.textitem = FONT.render(self.text, True, default_color)
        self.rect = self.textitem.get_rect()

    ##THIS IS ABSOLUTELY GENIUS RIGHT HERE
    ##I DON'T KNOW THE OFFICIAL NAME OF THIS PATTERN
    ##I'M CALLING IT THE DOUBLE DUMMY PATTERN

    def doclicked(self):
        return self

    def updatetext(self, new):
        self.text = new
        self.textitem = FONT.render(self.text, True, default_color)
        rect = self.textitem.get_rect()
        rect.x = self.rect.x
        rect.y = self.rect.y
        self.rect = rect


class FileBox:
    rect = False
    textitem = False
    text = ""

    def __init__(self, textitem, rect, text):
        self.rect = rect
        self.textitem = textitem
        self.text = text

    ##THIS IS ABSOLUTELY GENIUS RIGHT HERE
    ##I DON'T KNOW THE OFFICIAL NAME OF THIS PATTERN
    ##I'M CALLING IT THE DOUBLE DUMMY PATTERN
    def clickdummy(self, item):
        return

    def doclicked(self):
        dummy = self.clickdummy(self)
        return dummy

    def updatetext(self, new):
        self.text = new
        self.textitem = FONT.render(self.text, True, default_color)
        rect = self.textitem.get_rect()
        rect.x = self.rect.x
        rect.y = self.rect.y
        self.rect = rect


class FileWindow:
    xpos = 0
    ypos = 0
    height = 0
    width = 0
    state = False
    """
    The returned "secret sauce"
    """
    item_dict = {}

    mode = False

    def __init__(self):
        return

    def update(self):
        biggest = 0
        for item in self.item_dict:
            if item.rect.width > biggest:
                biggest = item.rect.width
        self.width = biggest + 4

    def update_self(self, directory=False, coords=(), mode=False):
        self.height = 0
        self.width = 0
        self.x, self.y = coords[0], coords[1]
        self.item_dict = {}
        self.mode = mode
        if directory:
            filelist = listdir(directory)
            buffer = 2
            for item in filelist:
                textbox = FONT.render(str(item), True, default_color)
                rect = textbox.get_rect()
                addheight = rect.height
                rect.x = self.x + 2
                rect.y = self.y - addheight - buffer

                box = FileBox(textbox, rect, str(item))
                buffer = buffer + addheight + 1
                width = rect.width
                if width > self.width:
                    self.width = width
                self.item_dict[box] = rect

            # TODO Related to saving, internals can probably be unified with the loop above for reduced complexity
            if self.mode == "save":
                textbox = FONT.render("NEW", True, default_color)
                rect = textbox.get_rect()
                addheight = rect.height
                rect.x = self.x + 2
                rect.y = self.y - addheight - buffer
                box = FileBox(textbox, rect, "NEW")
                buffer = buffer + addheight + 1
                width = rect.width
                if width > self.width:
                    self.width = width
                self.item_dict[box] = rect

            buffer = buffer + 2  # TODO What does adding 2 do here?
            self.height = buffer
            self.width = self.width + 4  # TODO What does adding 4 do here?
            self.state = True  # TODO What's the difference between a true and false state?

        return self.item_dict

    def draw(self, WINDOW):
        if self.state:
            draw.rect(WINDOW, (75, 75, 175), (self.x, self.y - self.height, self.width, self.height))
            for item in self.item_dict:
                WINDOW.blit(item.textitem, item.rect)

    def set_do_clicked(self, function, function2=False):
        for item in self.item_dict:
            if item.text != "NEW":
                item.do_clicked = function
            else:
                item.do_clicked = function2
