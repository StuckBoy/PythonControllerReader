import sys
from os import listdir

import pygame

from Actions import ModAction, ActionContainer
from ClickableOptionButton import ClickableOptionButton
from FileStuff import FileBox, FileWindow, ColorBox
from GenericController import LoadGenericController, GenericController
from joystickstuff import Button, Stick, TriggerAxis, Hat, Background

if getattr(sys, 'frozen', False):
    import pyi_splash

pygame.init()

font = pygame.font.Font('SuperMystery.ttf', 24)

pygame.display.set_caption('Build Your Controller Layout')
workrectimage = pygame.image.load('./assets/background.png')
workrect = workrectimage.get_rect()
width = workrect.width
height = workrect.height
x = 150
y = 350

displaywidth = 600
displayheight = 725
# Resize width if necessary
if x + width > displaywidth:
    displaywidth = x + width + 20
# Resize height if necessary
if y + height + 115 > displayheight:
    displayheight = y + height + 115

display = pygame.display.set_mode((displaywidth, displayheight))
rect = pygame.rect.Rect(0, 0, displaywidth, displayheight)

clock = pygame.time.Clock()

done = False
words = "PRESS BUTTON"
name = ""
text = font.render(words, True, (200, 74, 220))

drawlist = []
joysticks = {}
for i in range(pygame.joystick.get_count()):
    joysticks[i] = pygame.joystick.Joystick(i)

ActiveStick = False
currentAction = ActionContainer()

collidables = []

filewindow = FileWindow()

"""
Unsure what this does, need more insight to quantify this naming convention
"""


class HoldingCell():
    # TODO
    def __init__(self):
        self.holding = False
        self.dragging = False
        self.buttonlist = []
        self.changelist = []

    # TODO
    def holdItem(self, item):
        self.holding = item
        if item:
            self.dragging = True

    # TODO
    def stopdrag(self):
        self.dragging = False

    # TODO
    def Drag(self, position):
        self.holding.x = position[0] - 5
        self.holding.rect.x = position[0] - 5
        self.holding.y = position[1] - 5
        self.holding.rect.y = position[1] - 5

    # TODO
    def update(self):
        # For each entry in button list
        for item in self.buttonlist:
            # For each thing that can collide
            for thing in collidables:
                # If we found a match
                if item == thing:
                    # Remove it from the collidables
                    collidables.remove(item)
        self.buttonlist = []
        # If the thing being held is a Button
        if self.holding.__class__ == Button:
            self.changelist = []
            directory = './buttons/'
            filelist = listdir(directory)
            for file in filelist:
                self.changelist.append(directory + file)
            self.buttonlist = ButtonModList
            buffer = 0
            for item in ButtonModList:
                buffer = buffer + item.rect.height + 2
                item.rect.x = x
                item.rect.y = y - buffer
        # If the thing being held is a Stick
        if self.holding.__class__ == Stick:
            self.changelist = []
            directory = './sticks/'
            filelist = listdir(directory)
            for file in filelist:
                self.changelist.append(directory + file)
            self.buttonlist = StickModList
            buffer = 0
            for item in StickModList:
                buffer = buffer + item.rect.height + 2
                item.rect.x = x
                item.rect.y = y - buffer
        # If the thing being held is a TriggerAxis
        if self.holding.__class__ == TriggerAxis:
            self.changelist = []
            directory = './Axis/'
            filelist = listdir(directory)
            for file in filelist:
                self.changelist.append(directory + file)
            self.buttonlist = AxisModList
            buffer = 0
            for item in AxisModList:
                buffer = buffer + item.rect.height + 2
                item.rect.x = x
                item.rect.y = y - buffer
        # If the thing being held is a Hat
        if self.holding.__class__ == Hat:
            self.changelist = []
            directory = './hats/'
            filelist = listdir(directory)
            for file in filelist:
                self.changelist.append(directory + file)
            self.buttonlist = HatModList
            buffer = 0
            for item in HatModList:
                buffer = buffer + item.rect.height + 2
                item.rect.x = x
                item.rect.y = y - buffer
        # If the thing being held is a Background
        if self.holding.__class__ == Background:
            self.changelist = []
            directory = './backgrounds/'
            filelist = listdir(directory)
            for file in filelist:
                self.changelist.append(directory + file)
            self.buttonlist = BGModList
            buffer = 0
            for item in BGModList:
                buffer = buffer + item.rect.height + 2
                item.rect.x = x
                item.rect.y = y - buffer
        templist = []
        for item in collidables:
            templist.append(item)
        collidables.clear()
        for item in self.buttonlist:
            collidables.append(item)
        for item in templist:
            collidables.append(item)

    def draw(self, WINDOW):
        for item in self.buttonlist:
            item.draw(WINDOW)


widgetCell = HoldingCell()


# TODO
def save(filename=""):
    if filename == "":
        filename = "./layouts/layout.txt"

    if filename[len(filename) - 4:] != ".txt":
        filename = filename + ".txt"

    file = open(filename, 'w')
    if ActiveStick:
        buttondict = ActiveStick.buttondict
        length = len(buttondict)
        print("Number of Independent buttons: " + str(length) + '\n')
        file.write("Number of Independent buttons: " + str(length) + '\n')
        # For each button defined
        for button in buttondict:
            # (buttonnum, x, y, offimage, onimage, rotation)
            number = str(buttondict[button].buttonnum)
            xposition = str(buttondict[button].x - x)
            yposition = str(buttondict[button].y - y)
            onimage = str(buttondict[button].pressed)
            offimage = str(buttondict[button].unpressed)
            rotation = str(buttondict[button].rotate)
            name = str(buttondict[button].name)
            buttontext = "({},{},{},{},{},{},{})\n".format(number, xposition, yposition, offimage, onimage, rotation,
                                                           name)
            print(buttontext)
            file.write(buttontext)
        axisdict = ActiveStick.axisdict
        length = len(axisdict)
        print("Number of Independent Axis: " + str(length) + '\n')
        file.write("Number of Independent Axis: " + str(length) + '\n')
        # For each axis defined
        for axis in axisdict:
            # (axisnumber, xpos, ypos, barimage, paddleimage, flippedbool)
            number = str(axisdict[axis].axis)
            xpos = str(axisdict[axis].x - x)
            ypos = str(axisdict[axis].y - y)
            barim = str(axisdict[axis].bar_image)
            paddleim = str(axisdict[axis].paddleimage)
            flip = str(axisdict[axis].horizontal)
            mode = str(axisdict[axis].mode)
            rotate = str(axisdict[axis].rotate)
            name = str(axisdict[axis].name)
            pressim = str(axisdict[axis].pressed)
            unpressedim = str(axisdict[axis].unpressed)
            axistext = "({},{},{},{},{},{},{},{},{},{},{})\n".format(number, xpos, ypos, barim, paddleim, flip, mode,
                                                                     rotate, name, pressim, unpressedim)
            print(axistext)
            file.write(axistext)
        sticklist = ActiveStick.sticklist
        length = len(sticklist)
        print("Number of Sticks: " + str(length) + '\n')
        file.write("Number of Sticks: " + str(length) + '\n')
        # For each stick
        for stick in sticklist:
            # (vertaxis,horizontalaxis,buttonnumber, xpos, ypos, pressed, unpressed)
            vertaxis = str(stick.vertaxis)
            horizontal = str(stick.horaxis)
            button = str(stick.buttonnum)
            xpos = str(stick.x - x)
            ypos = str(stick.y - y)
            pressed = str(stick.pressed)
            unpressed = str(stick.unpressed)
            stickname = str(stick.stickname)
            buttonname = str(stick.buttonname)
            sticktext = "({},{},{},{},{},{},{},{},{})\n".format(vertaxis, horizontal, button, xpos, ypos, pressed,
                                                                unpressed, stickname, buttonname)
            print(sticktext)
            file.write(sticktext)
        hatdict = ActiveStick.hatdict
        length = len(hatdict)
        print("Number of Hats: " + str(length) + '\n')
        file.write("Number of Hats: " + str(length) + '\n')
        # For each hat
        for hat in hatdict:
            # (number,xposition,yposition,rotation,onimage,offimage,backgroundimage)
            number = str(hatdict[hat].hat_number)
            xposition = str(hatdict[hat].x - x)
            yposition = str(hatdict[hat].y - y)
            onimage = str(hatdict[hat].defaultpressed)
            offimage = str(hatdict[hat].defaultunpressed)
            backgroundimage = str(hatdict[hat].background)
            rotation = str(hatdict[hat].rotate)
            name = str(hatdict[hat].name)
            hattext = '({},{},{},{},{},{},{},{})\n'.format(number, xposition, yposition, rotation, onimage, offimage,
                                                           backgroundimage, name)
            print(hattext)
            file.write(hattext)
        print("Background Info:")
        file.write("Background Info:\n")
        bgpath = ActiveStick.background.path
        bgcolor = ActiveStick.background.color
        backgroundtext = '({},{})\n'.format(bgpath, bgcolor)
        print(backgroundtext)
        file.write(backgroundtext)

    else:
        print("nothing to save")
        ##buttons
        # triggers
        # sticks
    file.close()


# TODO
def load(filename=""):
    # Edge case
    if filename[-4:] == ".zip":
        return loadzip(filename)
    else:  # Otherwise process
        return loadfile(filename)


# TODO Zips aren't supported
def loadzip(filename=""):
    return False


# TODO
def loadfile(filename=""):
    # Default to layout.txt, we have nothing to work on
    if filename == "":
        filename = "layout.txt"
    file = open(filename, 'r')
    # TODO What behavior does this exhibit?
    #  is it "defaulting" the outer scope's collidables, as intended?
    collidables = [SaveButton, LoadButton, ReloadButton]

    ## generates a list object that holds each line as a string
    # Current load order is buttons first, then axis, then sticks
    lines = file.readlines()
    bookmarks = []
    length = len(lines)
    ## removes the newline character from the end of each line
    for i in range(length):
        lines[i] = lines[i].removesuffix('\n')
        if lines[i][0] != '(':
            bookmarks.append(i)

    buttondict = {}
    for i in range(bookmarks[0], bookmarks[1]):
        if lines[i][0] == '(':
            lines[i] = lines[i].removeprefix('(')
            lines[i] = lines[i].removesuffix(')')
            values = lines[i].split(',')
            buttonnum = int(values[0])
            xpos = int(values[1]) + x
            ypos = int(values[2]) + y
            offimage = str(values[3])
            onimage = str(values[4])
            rotation = int(values[5])
            name = ""
            if 6 < len(values):
                name = str(values[6])
            addbutton = Button(buttonnum, xpos, ypos, False, name)
            addbutton.unpressed = offimage
            addbutton.pressed = onimage
            addbutton.rotate = rotation
            addbutton.load()
            buttondict[buttonnum] = addbutton

    axisdict = {}
    for i in range(bookmarks[1], bookmarks[2]):
        if lines[i][0] == '(':
            lines[i] = lines[i].removeprefix('(')
            lines[i] = lines[i].removesuffix(')')
            values = lines[i].split(',')
            axisnum = int(values[0])
            xpos = int(values[1]) + x
            ypos = int(values[2]) + y
            triggerimage = str(values[3])
            paddleimage = str(values[4])
            flipbool = values[5]
            mode = str(values[6])
            rotate = int(values[7])
            name = str(values[8])
            pressname = str(values[9])
            unpressedname = str(values[10])
            if 8 < len(values):
                name = str(values[8])
            if flipbool == 'True':
                flipbool = True
            else:
                flipbool = False
            addtrigger = TriggerAxis(xpos, ypos, axisnum, False, mode, rotate, name)
            addtrigger.paddleimage = paddleimage
            addtrigger.bar_image = triggerimage
            addtrigger.pressed = pressname
            addtrigger.unpressed = unpressedname
            addtrigger.horizontal = flipbool
            addtrigger.load()
            axisdict[axisnum] = addtrigger

    sticklist = []
    for i in range(bookmarks[2], bookmarks[3]):
        if lines[i][0] == '(':
            lines[i] = lines[i].removeprefix('(')
            lines[i] = lines[i].removesuffix(')')
            ##Stick extraction data format
            # (vertaxis,horizontalaxis,buttonnum, xpos, ypos, pressed, unpressed)
            values = lines[i].split(',')
            vertaxis = int(values[0])
            horizontalaxis = int(values[1])
            xpos = int(values[3]) + x
            ypos = int(values[4]) + y
            buttonnumber = int(values[2])
            onimage = values[5]
            offimage = values[6]
            stickname = ""
            buttonname = ""
            if 7 < len(values):
                stickname = values[7]
            if 8 < len(values):
                buttonname = values[8]
            # stick creation data format
            # (xpos,ypos,vertaxis, horizontalaxis, buttonnumber)
            addstick = Stick(xpos, ypos, vertaxis, horizontalaxis, buttonnumber, stickname, buttonname)
            addstick.pressed = onimage
            addstick.unpressed = offimage
            addstick.load()
            sticklist.append(addstick)
    hatdict = {}
    for i in range(bookmarks[3], bookmarks[4]):
        if lines[i][0] == '(':
            # (number,xposition,yposition,rotation,onimage,offimage,backgroundimage)
            lines[i] = lines[i].removeprefix('(')
            lines[i] = lines[i].removesuffix(')')
            values = lines[i].split(',')
            hatnum = int(values[0])
            xpos = int(values[1]) + x
            ypos = int(values[2]) + y
            rotation = int(values[3])
            onimage = str(values[4])
            offimage = str(values[5])
            backgroundimage = str(values[6])
            name = ""
            if 7 < len(values):
                name = str(values[7])

            addhat = Hat(hatnum, xpos, ypos, False, name)
            addhat.defaultunpressed = offimage
            addhat.defaultpressed = onimage
            addhat.background = backgroundimage
            addhat.rotate = rotation
            addhat.setdefaults()
            addhat.load()
            hatdict[hatnum] = addhat

    bgline = bookmarks[4] + 1
    bgline = lines[bgline]
    bgline = bgline.removeprefix('(')
    bgline = bgline.removesuffix(')')
    bgvalues = bgline.split(",")
    background = Background(bgvalues[0], bgvalues[1])
    background.rect.x = background.rect.x + x
    background.rect.y = background.rect.y + y

    # Is an "active stick" present?
    # Maintains controller/stick uniqueness
    if ActiveStick:
        Controller = GenericController(ActiveStick.gamepad)
    else:
        Controller = GenericController(False)

    Controller.buttondict = buttondict
    Controller.axisdict = axisdict
    Controller.sticklist = sticklist
    Controller.hatdict = hatdict
    Controller.background = background
    file.close()
    Controller.resetListItems()
    if Controller:
        return Controller
    return False


# TODO
def loadclicked(self):
    dummy = load("./layouts/" + self.text)
    return dummy


# TODO
def LoadButtonDoClicked():
    itemlist = filewindow.update_self("./layouts/", (position[0], position[1]))

    for item in itemlist:
        item.clickdummy = loadclicked

    return itemlist


# TODO
def saveclicked(self):
    save("./layouts/" + self.text)


# TODO
def NewFileBoxClicked(self):
    return self


# TODO
def SaveButtonDoClicked():
    itemlist = filewindow.update_self("./layouts/", (position[0], position[1]), "save")

    for item in itemlist:
        if item.text != "NEW":
            item.clickdummy = saveclicked
        else:
            item.clickdummy = NewFileBoxClicked

    return itemlist


# TODO
def makeStick():
    emptystick = Stick(MakeStickButton.rect.x + 145, MakeStickButton.rect.y)
    print(emptystick)
    if emptystick.controller == False:
        if ActiveStick:
            emptystick.controller = ActiveStick
    return emptystick


# TODO
def reloadController():
    if ActiveStick:
        if ActiveStick.gamepad:
            stick = LoadGenericController(ActiveStick.gamepad)
        else:
            stick = LoadGenericController()
    else:
        stick = LoadGenericController()
    return stick


"""
Seeing as python likes to merge its "headers and implementations", the fact that
this section of declarations begins here is tipping me off. It could mean that
there is opportunity to break out this related-yet-significantly different
section into its own class.
"""

saveimage = pygame.image.load('assets/savebutton.png')
loadimage = pygame.image.load('assets/loadbutton.png')
makestickimage = pygame.image.load('assets/makestickbutton.png')
reloadimage = pygame.image.load('assets/reloadbutton.png')

SaveButton = ClickableOptionButton((x + width) / 2 - (saveimage.get_rect().bottomright[0]) / 2, y + height + 20,
                                   saveimage)
LoadButton = ClickableOptionButton(SaveButton.rect.x + 145, SaveButton.rect.y, loadimage)
ReloadButton = ClickableOptionButton(0, 0, reloadimage)

MakeStickButton = ClickableOptionButton(SaveButton.rect.x + (LoadButton.rect.x - SaveButton.rect.x) / 2,
                                        SaveButton.rect.y + 50, makestickimage)
SaveButton.do_clicked = SaveButtonDoClicked
LoadButton.do_clicked = LoadButtonDoClicked
MakeStickButton.do_clicked = makeStick
ReloadButton.do_clicked = reloadController

collidables.append(SaveButton)
collidables.append(LoadButton)
collidables.append(ReloadButton)
collidables.append(MakeStickButton)
secondarybuttonmenulist = []


# TODO
def changeButtonImage():
    morph = widgetCell.holding
    if morph.__class__ == Button or morph.__class__ == Stick or morph.__class__ == Hat:
        unpressed = morph.unpressed
        num = widgetCell.changelist.index(unpressed)
        if num + 1 < len(widgetCell.changelist):
            num = num + 1
        else:
            num = 0
        unpressed = widgetCell.changelist[num]
        prunedex = unpressed.index("unpressed")
        pressed = unpressed[:prunedex] + unpressed[prunedex + 2:]
        morph.unpressed = unpressed
        morph.pressed = pressed
        morph.load()

    stickcollidables()


# TODO
def ChangeAssetImageButtonDoClicked(self):
    num = self.changelist.index(self.path)
    if num + 1 < len(self.changelist):
        num = num + 1
    else:
        num = 0

    newpath = self.changelist[num]
    self.setter(newpath)
    self.path = newpath
    ChangeButtonDoClicked()


# TODO
def ChangeButtonDoClicked():
    morph = widgetCell.holding
    # grab image asset dict:
    # image asset list should include:
    # image asset path name
    # image asset surface
    # function for changing the path name
    assets = morph.assetdict
    ybuffer = y
    xpos = changebutton.rect[0] + 140
    buttonfont = pygame.font.Font('SuperMystery.ttf', 12)
    for item in secondarybuttonmenulist:
        for thing in collidables:
            if item == thing:
                collidables.remove(item)
    secondarybuttonmenulist.clear()

    for asset in assets:
        imgpath = str(assets[asset][0])
        parse = imgpath.split('/')
        folderpath = parse[0]
        for i in range(1, len(parse) - 1, 1):
            folderpath = folderpath + "/" + parse[i]
        dirlist = listdir(folderpath)
        for i in range(0, len(dirlist), 1):
            dirlist[i] = folderpath + '/' + dirlist[i]

        widgetCell.changelist = dirlist

        imgsurface = assets[asset][1]
        changefunction = assets[asset][2]

        ##MAKE BUTTON FOR CHANGING ASSET

        text = buttonfont.render(str(asset), True, (75, 75, 30), (175, 175, 80))
        textrect = text.get_rect()
        imgrect = imgsurface.get_rect()
        imgheight = imgrect.height
        imgwidth = imgrect.width
        textheight = textrect.height
        textwidth = textrect.width

        ybuffer = ybuffer - imgheight - 5
        addrect = pygame.rect.Rect(xpos, ybuffer, imgwidth, imgheight)
        imgbutton = FileBox(imgsurface, addrect, imgpath)
        imgbutton.changelist = dirlist
        imgbutton.path = imgpath
        imgbutton.setter = changefunction
        imgbutton.parent = morph

        ybuffer = ybuffer - 2 - textheight
        addrect = pygame.rect.Rect(xpos, ybuffer, textwidth, textheight)
        button = FileBox(text, addrect, imgpath)
        button.changelist = dirlist
        button.path = imgpath
        button.setter = changefunction
        button.parent = morph

        button.clickdummy = ChangeAssetImageButtonDoClicked
        imgbutton.clickdummy = ChangeAssetImageButtonDoClicked

        secondarybuttonmenulist.append(button)
        secondarybuttonmenulist.append(imgbutton)
    for item in secondarybuttonmenulist:
        collidables.append(item)
    stickcollidables()
    return False


# TODO
def rotateButtonImage():
    morph = widgetCell.holding
    morph.Rotate()
    stickcollidables()


ChangeImage = pygame.image.load('assets/changebutton.png')
changebutton = ClickableOptionButton(x + 20, y - ChangeImage.get_rect().height, ChangeImage)
changebutton.do_clicked = ChangeButtonDoClicked
RotateImage = pygame.image.load('assets/rotatebutton.png')
rotatebutton = ClickableOptionButton(x + 40 + 135, y - 50, RotateImage)
rotatebutton.do_clicked = rotateButtonImage
ButtonModList = [changebutton, rotatebutton]

horizontalaxis = pygame.image.load('assets/horizontalaxisbutton.png')

changehorizontalbutton = ClickableOptionButton(changebutton.rect.x, changebutton.rect.y - 50, horizontalaxis)


# TODO
def addButtontoController(Core, buttonnum):
    buttonadd = Button(buttonnum, Core.x, Core.y - (Core.stickunpressed.get_rect().bottomright[1] * 2), ActiveStick)
    buttonadd.rotate()
    ActiveStick.buttondict[buttonnum] = buttonadd


# TODO
def addAxistoController(Core, Axisnum):
    axisadd = TriggerAxis(Core.x, Core.y - (Core.stickunpressed.get_rect().bottomright[1] * 2), Axisnum, ActiveStick)
    axisadd.rotate()
    ActiveStick.axisdict[Axisnum] = axisadd


# TODO
def changehorizontalaxis(self):
    numswap = self.trigger.axis
    if self.Core.horaxis >= 0:
        temp = self.Core.horaxis
        self.Core.horaxis = numswap
        addAxistoController(self.Core, temp)
    else:
        self.Core.horaxis = numswap
    if ActiveStick:
        tempdict = []
        for key in ActiveStick.axisdict:
            tempdict.append(key)
        for item in tempdict:
            if ActiveStick.axisdict[item] == self.trigger:
                del ActiveStick.axisdict[item]
        del tempdict
    stickcollidables()


# TODO
def changehorizontalclicked():
    action = ModAction(widgetCell.holding, TriggerAxis(), "CLICK DESIRED HORIZONTAL AXIS")
    ModAction.do_action = changehorizontalaxis
    return action


changehorizontalbutton.do_clicked = changehorizontalclicked

vertaxis = pygame.image.load('assets/vertaxisbutton.png')

changevertbutton = ClickableOptionButton(rotatebutton.rect.x, changehorizontalbutton.rect.y, vertaxis)


# TODO
def changevertaxis(self):
    numswap = self.trigger.axis
    if self.Core.vertaxis >= 0:
        temp = self.Core.vertaxis
        self.Core.vertaxis = numswap
        addAxistoController(self.Core, temp)
    else:
        self.Core.vertaxis = numswap
    if ActiveStick:
        tempdict = []
        for key in ActiveStick.axisdict:
            tempdict.append(key)
        for item in tempdict:
            if ActiveStick.axisdict[item] == self.trigger:
                del ActiveStick.axisdict[item]
        del tempdict
    stickcollidables()


# TODO
def changevertclicked():
    action = ModAction(widgetCell.holding, TriggerAxis(), "CLICK DESIRED VERTICAL AXIS")
    ModAction.do_action = changevertaxis
    return action


changevertbutton.do_clicked = changevertclicked

changeButtonImage = pygame.image.load('assets/addbutton.png')
changeStickButton = ClickableOptionButton(changevertbutton.rect.x - 12, changehorizontalbutton.rect.y - 50,
                                          changeButtonImage)


# TODO
def changestickbutton(self):
    numswap = self.trigger.buttonnum
    if self.Core.buttonnum >= 0:
        temp = self.Core.buttonnum
        self.Core.buttonnum = numswap
        addButtontoController(self.Core, temp)
    else:
        self.Core.buttonnum = numswap
    if ActiveStick:
        tempdict = []
        for key in ActiveStick.buttondict:
            tempdict.append(key)
        for item in tempdict:
            if ActiveStick.buttondict[item] == self.trigger:
                del ActiveStick.buttondict[item]
    stickcollidables()


# TODO
def changebuttonclicked():
    action = ModAction(widgetCell.holding, Button(), "CLICK DESIRED BUTTON")
    ModAction.do_action = changestickbutton
    return action


changeStickButton.do_clicked = changebuttonclicked

DropSettingsImage = pygame.image.load('assets/dropsettings.png')
detachAllButton = ClickableOptionButton(changeStickButton.rect.x - DropSettingsImage.get_rect().bottomright[0] - 10,
                                        changeStickButton.rect.y, DropSettingsImage)


# TODO
def detachAllclicked():
    if widgetCell.holding:
        items_to_add = widgetCell.holding.dropItems()
    else:
        items_to_add = []
    for item in items_to_add:
        if item.__class__ == list:
            for thing in item:
                ActiveStick.axisdict[thing.axis] = thing
        else:
            ActiveStick.buttondict[item.buttonnum] = item

    stickcollidables()


detachAllButton.do_clicked = detachAllclicked

StickModList = [changebutton, rotatebutton, changehorizontalbutton, changevertbutton, changeStickButton,
                detachAllButton]

changeModeImage = pygame.image.load('assets/modebutton.png')
changeModeButton = ClickableOptionButton(rotatebutton.rect.x - 146, rotatebutton.rect.y, changeModeImage)


# TODO
def changeMode():
    morph = widgetCell.holding
    if morph.__class__ == TriggerAxis:
        if morph.mode == 'axis':
            morph.mode = 'button'
        elif morph.mode == 'button':
            morph.mode = 'axis'
        morph.ModeAdjust()
        morph.load()

    stickcollidables()


changeModeButton.do_clicked = changeMode

AxisModList = [changebutton, changeModeButton, rotatebutton]

HatModList = [changebutton]

BGModList = []

ChangeColorImage = pygame.image.load('assets/changecolorbutton.png')
changecolorbutton = ClickableOptionButton(x + 20, y - ChangeColorImage.get_rect().height, ChangeColorImage)


# TODO
def change_color_clicked():
    colorbox = ColorBox()
    colorbox.rect.x = changecolorbutton.rect.x + 5 + changecolorbutton.rect.width
    colorbox.rect.y = changecolorbutton.rect.y
    secondarybuttonmenulist.append(colorbox)
    for item in secondarybuttonmenulist:
        collidables.append(item)


changecolorbutton.do_clicked = change_color_clicked

BGModList.append(changecolorbutton)


# TODO
def CollisionCheck(mousepos, collisionbox):
    mousex = mousepos[0]
    mousey = mousepos[1]

    # Interesting
    if collisionbox[0] <= mousex <= collisionbox[0] + collisionbox[2]:
        if collisionbox[1] <= mousey <= collisionbox[1] + collisionbox[3]:
            return True
    return False


# TODO
def stickcollidables():
    collidables.append(ActiveStick.background)
    for item in ActiveStick.buttondict:
        rectangle = ActiveStick.buttondict[item].off.get_rect()
        ActiveStick.buttondict[item].rect = rectangle
        ActiveStick.buttondict[item].rect.x = ActiveStick.buttondict[item].x
        ActiveStick.buttondict[item].rect.y = ActiveStick.buttondict[item].y
        if ActiveStick.buttondict[item] not in collidables:
            collidables.append(ActiveStick.buttondict[item])
    for item in ActiveStick.axisdict:
        if ActiveStick.axisdict[item].mode == 'axis':
            rectangle1 = ActiveStick.axisdict[item].bar.get_rect()
            ActiveStick.axisdict[item].rect = rectangle1
            ActiveStick.axisdict[item].rect.x = ActiveStick.axisdict[item].x
            ActiveStick.axisdict[item].rect.y = ActiveStick.axisdict[item].y
            if ActiveStick.axisdict[item] not in collidables:
                collidables.append(ActiveStick.axisdict[item])
        elif ActiveStick.axisdict[item].mode == 'button':
            rectangle = ActiveStick.axisdict[item].unpressedimage.get_rect()
            ActiveStick.axisdict[item].rect = rectangle
            ActiveStick.axisdict[item].rect.x = ActiveStick.axisdict[item].x
            ActiveStick.axisdict[item].rect.y = ActiveStick.axisdict[item].y
            if ActiveStick.axisdict[item] not in collidables:
                collidables.append(ActiveStick.axisdict[item])

    for item in ActiveStick.sticklist:
        rectangle2 = item.stickunpressed.get_rect()
        item.rect = rectangle2
        item.rect.x = item.x
        item.rect.y = item.y
        if item not in collidables:
            collidables.append(item)

    for item in ActiveStick.hatdict:
        rectangle3 = ActiveStick.hatdict[item].asset_dict['background'][1].get_rect()
        ActiveStick.hatdict[item].rect = rectangle3
        ActiveStick.hatdict[item].rect.x = ActiveStick.hatdict[item].x
        ActiveStick.hatdict[item].rect.y = ActiveStick.hatdict[item].y
        if ActiveStick.hatdict[item] not in collidables:
            collidables.append(ActiveStick.hatdict[item])


def clear_text():
    # TODO Does calling this work if it's only ever called from main?
    words = ""
    text = font.render(words, True, (200, 74, 220))


# TODO
if getattr(sys, 'frozen', False):
    pyi_splash.close()

# TODO
while not done:
    for event in pygame.event.get():
        # TODO
        if event.type == pygame.QUIT:
            done = True
        # TODO
        if event.type == pygame.JOYBUTTONDOWN:
            print("Button Pressed")
            if ActiveStick == False:
                ActiveStick = LoadGenericController(joysticks[event.instance_id])
                background = Background('./backgrounds/background.png')
                background.rect.x = x
                background.rect.y = y
                ActiveStick.background = background
                name = ActiveStick.gamepad.get_name()
                stickcollidables()
                clear_text()
            elif ActiveStick.gamepad == False:
                newname = joysticks[event.instance_id].get_name()
                if name == newname:
                    ActiveStick.gamepad = joysticks[event.instance_id]
                    ActiveStick.resetListItems()
                    stickcollidables()
                    name = ActiveStick.gamepad.get_name()
                    clear_text()
                else:
                    ActiveStick = LoadGenericController(joysticks[event.instance_id])
                    background = Background('./backgrounds/background.png')
                    background.rect.x = x
                    background.rect.y = y
                    ActiveStick.background = background
                    name = ActiveStick.gamepad.get_name()
                    stickcollidables()
                    clear_text()

        # TODO
        if event.type == pygame.JOYDEVICEADDED:
            # This event will be generated when the program starts for every
            # joystick, filling up the list without needing to create them manually.
            joy = pygame.joystick.Joystick(event.device_index)
            ID = joy.get_instance_id()
            joysticks[ID] = joy

        # TODO
        if event.type == pygame.JOYDEVICEREMOVED:
            # This event will be generated when the program starts for every
            # joystick, filling up the list without needing to create them manually.
            deviceremovedID = event.instance_id
            # ID = ActiveStick.gamepad.get_instance_id()
            if ActiveStick:
                if ActiveStick.gamepad:
                    IDofgamepad = ActiveStick.gamepad.get_instance_id()
                    if IDofgamepad == deviceremovedID:
                        ActiveStick.gamepad = False
                        words = "PRESS BUTTON"
                        text = font.render(words, True, (200, 74, 220))
            del joysticks[deviceremovedID]

        # TODO
        if event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            touch = False
            filewindow.state = False
            check = False
            for i in range(len(collidables) - 1, -1, -1):
                item = collidables[i]
                touch = CollisionCheck(position, item.rect)
                if touch:
                    collided = item
                    if item not in secondarybuttonmenulist:
                        for item in secondarybuttonmenulist:
                            for thing in collidables:
                                if item == thing:
                                    collidables.remove(thing)
                        secondarybuttonmenulist.clear()
                    if collided.__class__ == ClickableOptionButton:
                        check = collided.do_clicked()
                        if check.__class__ == GenericController or check.__class__ == LoadGenericController:
                            ActiveStick = check
                            if check.gamepad:
                                name = check.gamepad.get_name()
                                clear_text()
                            else:
                                name = 'UNKNOWN'
                            stickcollidables()
                        if check.__class__ == Stick:
                            if ActiveStick:
                                widgetCell.holdItem(check)
                                widgetCell.stopdrag()
                                widgetCell.update()

                                ActiveStick.sticklist.append(check)
                                stickcollidables()
                        if check.__class__ == ModAction:
                            currentAction.action = check

                        if check.__class__ == dict:
                            for item in check:
                                collidables.append(item)
                    elif collided.__class__ == FileBox:
                        check = collided.do_clicked()
                        if check.__class__ == GenericController or check.__class__ == LoadGenericController:
                            ActiveStick = check
                            if check.gamepad:
                                name = check.gamepad.get_name()
                                clear_text()
                            else:
                                name = 'UNKNOWN'
                            stickcollidables()
                        if check.__class__ == FileBox:
                            filewindow.state = True
                            widgetCell.holding = check
                            check.updatetext("")
                    elif collided.__class__ == ColorBox:
                        widgetCell.holding = collided
                        collided.updatetext("")

                    elif currentAction.has_action():
                        currentAction.set_trigger(collided)
                    elif widgetCell.holding == False or widgetCell.holding != collided:
                        widgetCell.holdItem(collided)
                        widgetCell.stopdrag()
                        widgetCell.update()
                    elif widgetCell.holding == collided:
                        widgetCell.dragging = True
                    break

            if not touch:
                widgetCell.holdItem(False)
                widgetCell.update()
                for item in secondarybuttonmenulist:
                    for thing in collidables:
                        if item == thing:
                            collidables.remove(thing)
                secondarybuttonmenulist.clear()
            if check.__class__ != dict:
                for item in filewindow.item_dict:
                    for thing in collidables:
                        if thing == item:
                            collidables.remove(item)
                break

        # TODO
        if event.type == pygame.MOUSEBUTTONUP:
            widgetCell.stopdrag()

        # TODO
        if event.type == pygame.KEYDOWN:
            if widgetCell.holding.__class__ == FileBox:
                if event.unicode == '\x08':
                    widgetCell.holding.updatetext(widgetCell.holding.text[:-1])
                elif event.unicode == '\r':
                    save('./layouts/' + widgetCell.holding.text)
                    filewindow.state = False
                    widgetCell.holding = False
                else:
                    widgetCell.holding.updatetext(widgetCell.holding.text + str(event.unicode))

            if widgetCell.holding.__class__ == ColorBox:
                if event.unicode == '\x08':
                    widgetCell.holding.updatetext(widgetCell.holding.text[:-1])
                elif event.unicode == '\r':
                    ActiveStick.background.set_color(widgetCell.holding.text)
                    widgetCell.holding = False
                else:
                    widgetCell.holding.updatetext(widgetCell.holding.text + str(event.unicode))

    if done:
        break

    if widgetCell.dragging:
        position = pygame.mouse.get_pos()
        widgetCell.Drag(position)

    pygame.draw.rect(display, (255, 255, 255), rect)
    display.blit(text, (20, 20))
    pygame.draw.rect(display, (0, 0, 0), (x - 1, y - 1, width + 2, height + 2))
    display.blit(workrectimage, (x, y))
    SaveButton.draw(display)
    LoadButton.draw(display)

    MakeStickButton.draw(display)
    ReloadButton.draw(display)
    if widgetCell.holding:
        widgetCell.draw(display)
    for item in secondarybuttonmenulist:
        display.blit(item.textitem, item.rect)

    if ActiveStick:
        font = pygame.font.Font('SuperMystery.ttf', 24)
        active = font.render(str(name).upper(), True, (40, 200, 60))
        display.blit(active, (20, 60))
        ActiveStick.update()
        ActiveStick.draw(display)

    if filewindow.state:
        filewindow.update()
    filewindow.draw(display)

    if currentAction.has_action():
        actiontext = currentAction.action.text
        font = pygame.font.Font('SuperMystery.ttf', 24)
        active = font.render(actiontext, True, (20, 20, 230))
        display.blit(active, (175, 120))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
