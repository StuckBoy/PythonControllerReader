import sys
from os import listdir
from zipfile import ZipFile

import pygame
from pygame import image, transform

from ClickableOptionButton import ClickableOptionButton
from FileStuff import FileWindow, FileBox
from GenericController import GenericController
from joystickstuff import Button, TriggerAxis, Stick, Hat, Background

if getattr(sys, 'frozen', False):
    import pyi_splash

pygame.init()
joysticks = {}
for i in range(pygame.joystick.get_count()):
    joysticks[i] = pygame.joystick.Joystick(i)
font = pygame.font.Font('SuperMystery.ttf', 32)
background = pygame.image.load("assets/Background.png")
rect = background.get_rect()
x = int(rect.bottomright[0])
y = int(rect.bottomright[1])
pygame.display.set_caption('Controller Input Visualizer')
display = pygame.display.set_mode((x, y + 24))
clock = pygame.time.Clock()
filewindow = FileWindow()


class APMCounter():
    valuelist = []
    timepassed = 0
    actionperlastminute = 0
    averageapm = 0
    highest = 0
    ValueTarget = False

    def __init__(self, target):
        self.ValueTarget = target
        self.text = font.render('APLM: ' + str(self.actionperlastminute), True, (149, 75, 220))
        rect = self.text.get_rect()
        self.width = rect.width
        self.height = rect.height

    def update(self):
        num = self.ValueTarget.getcount()
        self.valuelist.append(num)
        self.timepassed = self.timepassed + 1
        if self.timepassed > 3600:
            self.valuelist.pop(0)
        length = len(self.valuelist)
        num1 = self.valuelist[length - 1]
        num2 = self.valuelist[0]
        value = num1 - num2
        self.actionperlastminute = value
        if self.actionperlastminute > self.highest:
            self.highest = self.actionperlastminute
        self.averageapm = int(self.valuelist[length - 1] / (self.timepassed / 3600))

    def draw(self, WINDOW):
        self.text = font.render('APLM: ' + str(self.actionperlastminute), True, (149, 75, 220))
        WINDOW.blit(self.text, (int(x / 2) - int(self.width / 2), y - self.height))

    def resetCounter(self):
        self.valuelist = []
        self.timepassed = 0


controller = False


def load(filename=""):
    if filename[-4:] == '.zip':
        return loadzip(filename)
    else:
        return loadfile(filename)


def loadzip(filename=""):
    Controller = False
    with ZipFile(filename, 'r') as zf:
        folder = filename[:-4].removeprefix('./layouts/')
        with zf.open(folder + '/layout.txt') as layout:
            print('peepus poopus')
            lines = layout.readlines()
            bookmarks = []
            length = len(lines)
            ## removes the newline character from the end of each line
            for i in range(length):
                lines[i] = lines[i].decode().removesuffix('\r\n')
                if lines[i][0] != '(':
                    bookmarks.append(i)
            buttondict = {}
            for i in range(bookmarks[0], bookmarks[1]):
                if lines[i][0] == '(':
                    lines[i] = lines[i].removeprefix('(')
                    lines[i] = lines[i].removesuffix(')')
                    values = lines[i].split(',')
                    buttonnum = int(values[0])
                    xpos = int(values[1])
                    ypos = int(values[2])
                    offimage = str(values[3]).removeprefix('.')
                    onimage = str(values[4]).removeprefix('.')
                    rotation = int(values[5])
                    name = ""
                    if 6 < len(values):
                        name = str(values[6])
                    addbutton = Button(buttonnum, xpos, ypos, False, name)
                    # addbutton.unpressed = offimage
                    offimagename = folder + offimage
                    onimagename = folder + onimage
                    with zf.open(offimagename) as f:
                        off = image.load(f)
                    # addbutton.pressed = onimage
                    with zf.open(onimagename) as f:
                        on = image.load(f)
                    off = transform.rotate(off, rotation)
                    on = transform.rotate(on, rotation)
                    addbutton.on = on
                    addbutton.off = off
                    addbutton.rotate = rotation
                    # addbutton.load()
                    buttondict[buttonnum] = addbutton

            axisdict = {}
            for i in range(bookmarks[1], bookmarks[2]):
                if lines[i][0] == '(':
                    lines[i] = lines[i].removeprefix('(')
                    lines[i] = lines[i].removesuffix(')')
                    values = lines[i].split(',')
                    axisnum = int(values[0])
                    xpos = int(values[1])
                    ypos = int(values[2])
                    triggerimage = str(values[3])
                    paddleimage = str(values[4])
                    flipbool = values[5]
                    mode = str(values[6])
                    rotate = int(values[7])
                    name = str(values[8])
                    pressed = str(values[9])
                    unpressed = str(values[10])
                    if name == "%r":
                        name = ""
                    if flipbool == 'True':
                        flipbool = True
                    else:
                        flipbool = False
                    addtrigger = TriggerAxis(xpos, ypos, axisnum, False, mode, rotate, name)

                    paddleimagename = folder + paddleimage.removeprefix('.')
                    triggerimagename = folder + triggerimage.removeprefix('.')
                    pressname = folder + pressed.removeprefix('.')
                    unpressname = folder + unpressed.removeprefix('.')

                    with zf.open(paddleimagename) as f:
                        paddle = image.load(f)
                    with zf.open(triggerimagename) as f:
                        bar = image.load(f)
                    with zf.open(pressname) as f:
                        press = image.load(f)
                    with zf.open(unpressname) as f:
                        unpress = image.load(f)
                    if flipbool == True:
                        paddle = transform.rotate(paddle, 90)
                        bar = transform.rotate(bar, 90)
                    addtrigger.paddle = paddle
                    addtrigger.paddleimage = paddleimagename
                    addtrigger.bar = bar
                    addtrigger.bar_image = triggerimagename
                    addtrigger.unpressedimage = unpress
                    addtrigger.unpressed = unpressname
                    addtrigger.pressed = pressname
                    addtrigger.pressedimage = press

                    # addtrigger.paddleimage = paddleimage
                    # addtrigger.barimage = triggerimage
                    addtrigger.horizontal = flipbool
                    # addtrigger.load()
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
                    xpos = int(values[3])
                    ypos = int(values[4])
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

                    offimagename = folder + offimage.removeprefix('.')
                    onimagename = folder + onimage.removeprefix('.')
                    with zf.open(offimagename) as f:
                        off = image.load(f)
                    # addbutton.pressed = onimage
                    with zf.open(onimagename) as f:
                        on = image.load(f)
                    off = transform.rotate(off, rotation)
                    on = transform.rotate(on, rotation)
                    addstick.stickunpressed = off
                    addstick.stickpressed = on

                    # addstick.pressed = onimage
                    # addstick.unpressed = offimage
                    # addstick.load()
                    sticklist.append(addstick)
            hatdict = {}
            for i in range(bookmarks[3], bookmarks[4]):
                if lines[i][0] == '(':
                    # (number,xposition,yposition,rotation,onimage,offimage,backgroundimage)
                    lines[i] = lines[i].removeprefix('(')
                    lines[i] = lines[i].removesuffix(')')
                    values = lines[i].split(',')
                    hatnum = int(values[0])
                    xpos = int(values[1])
                    ypos = int(values[2])
                    rotation = int(values[3])
                    onimage = str(values[4])
                    offimage = str(values[5])
                    backgroundimage = str(values[6])
                    name = ""
                    if 7 < len(values):
                        name = str(values[7])

                    addhat = Hat(hatnum, xpos, ypos, False, name)

                    offimagename = folder + offimage
                    onimagename = folder + onimage
                    backgroundimagename = folder + backgroundimagename.removeprefix(".")
                    with zf.open(offimagename) as f:
                        off = image.load(f)
                    # addbutton.pressed = onimage
                    with zf.open(onimagename) as f:
                        on = image.load(f)
                    with zf.open(backgroundimagename) as f:
                        bg = image.load(f)
                    off = transform.rotate(off, rotation)
                    on = transform.rotate(on, rotation)
                    bg = transform.rotate(bg, rotation)
                    addhat.pressed = on
                    addhat.unpressed = off
                    addhat.backgroundimage = bg
                    # addhat.unpressed = offimage
                    # addhat.pressed = onimage
                    # addhat.background = backgroundimage
                    # addhat.rotate = rotation
                    # addhat.load()
                    hatdict[hatnum] = addhat

            bgline = bookmarks[4] + 1
            bgline = lines[bgline]
            bgline = bgline.removeprefix('(')
            bgline = bgline.removesuffix(')')
            bgvalues = bgline.split(",")
            background = Background(bgvalues[0], bgvalues[1])
            background.rect.x = background.rect.x + x
            background.rect.y = background.rect.y + y

            if controller:
                Controller = GenericController(controller.gamepad)
            else:
                if (len(joysticks) > 0):
                    Controller = GenericController(joysticks[0])
                else:
                    Controller = GenericController(False)
            Controller.buttondict = buttondict
            Controller.axisdict = axisdict
            Controller.sticklist = sticklist
            Controller.hatdict = hatdict
            Controller.background = background
            Controller.resetListItems()
    return Controller


def loadfile(filename=""):
    if filename == "":
        filename = "./layouts/layout.txt"
    file = open(filename, 'r')

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
            xpos = int(values[1])
            ypos = int(values[2])
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
            xpos = int(values[1])
            ypos = int(values[2])
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
            xpos = int(values[3])
            ypos = int(values[4])
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
            addstick = Stick(xpos, ypos, vertaxis, horizontalaxis, buttonnumber, False, stickname, buttonname)
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
            xpos = int(values[1])
            ypos = int(values[2])
            rotation = int(values[3])
            onimage = str(values[4])
            offimage = str(values[5])
            backgroundimage = str(values[6])
            name = ""
            if 7 < len(values):
                name = str(values[7])

            addhat = Hat(hatnum, xpos, ypos, False, name)
            addhat.unpressed = offimage
            addhat.pressed = onimage
            addhat.background = backgroundimage
            addhat.rotate = rotation
            addhat.load()
            hatdict[hatnum] = addhat

    bgline = bookmarks[4] + 1
    bgline = lines[bgline]
    bgline = bgline.removeprefix('(')
    bgline = bgline.removesuffix(')')
    bgvalues = bgline.split(",")
    background = Background(bgvalues[0], bgvalues[1])

    if controller:
        Controller = GenericController(controller.gamepad)
    else:
        if len(joysticks) > 0:
            Controller = GenericController(joysticks[0])
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


def createlogfile():
    filelist = listdir('./logs')
    listlen = len(filelist)
    logname = 'log_' + str(listlen) + ".txt"
    file = open('./logs/' + logname, 'w')
    duration = controller.timecount
    actions = controller.actioncount
    minutes = int(duration / 3600)
    seconds = int((duration % 3600) / 60)
    leftover = duration % 60
    average = counter.averageapm
    highest = counter.highest
    file.write("Frames Logged(60 fps): " + str(duration) + '\n')
    file.write(
        "Actual time passed: " + str(minutes) + "m" + str(seconds) + "s" + " and " + str(leftover) + " frames" + '\n')
    file.write("Actions logged: " + str(actions) + '\n')
    file.write("Overall average per minute: " + str(average) + '\n')
    file.write("Highest minute: " + str(highest) + '\n')
    buttondict = controller.buttondict
    axisdict = controller.axisdict
    hatdict = controller.hatdict
    sticklist = controller.sticklist
    file.write("BTTONS *************\n")
    for item in buttondict:
        var = buttondict[item].actions
        if len(buttondict[item].name) > 0:
            name = buttondict[item].name
        else:
            name = buttondict[item].buttonnum
        # name = buttondict[item].name
        file.write("Button " + str(name) + ": " + str(var) + "\n")
    file.write("AXIS *************\n")
    for item in axisdict:
        var = axisdict[item].actions
        if len(axisdict[item].name) > 0:
            name = axisdict[item].name
        else:
            name = axisdict[item].axis
        # name = axisdict[item].name
        file.write("Axis " + str(name) + ": " + str(var) + "\n")
    file.write("HATS *************\n")
    for item in hatdict:
        var = hatdict[item].actions
        if len(hatdict[item].name) > 0:
            name = hatdict[item].name
        else:
            name = hatdict[item].hatnumber
        # name = hatdict[item].name
        file.write("Hat " + str(name) + ": " + str(var) + "\n")
    file.write("STICKS *************\n")
    for i in range(len(sticklist)):
        pressed = sticklist[i].pressactions
        moved = sticklist[i].moveactions
        total = pressed + moved
        if len(sticklist[i].stickname) > 0:
            name = sticklist[i].stickname
        else:
            name = i

        if len(sticklist[i].buttonname) > 0:
            buttname = sticklist[i].buttonname
        else:
            buttname = "pressed"
        # name = sticklist[i].name
        file.write("Stick " + str(name) + "- total = " + str(total) + " - " + buttname + " = " + str(
            pressed) + " - moved = " + str(moved) + "\n")

    file.close()
    reset()


controller = load("./layouts/layout.txt")
controller.resetListItems()
counter = APMCounter(controller)


def reset():
    counter.resetCounter()
    controller.resetCounter()
    return 0


def toggle_lines():
    controller.StickLines = not controller.StickLines


def load_clicked(self):
    """
    FIXME Documentation necessary. This method is the load bearing bit of the
     decorator pattern being employed. Summarize behavior here and enshrine for
     future reference.
    """
    dummy = load("./layouts/" + self.text)
    draw_list[0] = dummy
    counter.ValueTarget = dummy
    return dummy


def load_button_do_clicked():
    itemlist = filewindow.UpdateSelf("./layouts/", (position[0], position[1]))

    for item in itemlist:
        item.clickdummy = load_clicked

    return itemlist


# all_lowercase = ultra-temporary variables
resetimage = pygame.image.load('./assets/resetbutton.png')
resetrect = resetimage.get_rect()
# double_camel_case = Sum of it's previously stated parts
ResetButton = ClickableOptionButton(1, y, resetimage)
ResetButton.do_clicked = reset

loadimage = pygame.image.load('assets/loadbutton.png')
loadrect = loadimage.get_rect()
LoadButton = ClickableOptionButton(ResetButton.rect.x + loadrect.width + 1, ResetButton.rect.y, loadimage)
LoadButton.do_clicked = load_button_do_clicked

linetoggleimage = pygame.image.load('./assets/linesbutton.png')
line_rect = linetoggleimage.get_rect()
LineToggleButton = ClickableOptionButton(x - line_rect.width, y, linetoggleimage)
LineToggleButton.do_clicked = toggle_lines

log_button_image = pygame.image.load('./assets/logbutton.png')
log_rect = log_button_image.get_rect()
LogButton = ClickableOptionButton(LoadButton.rect.x + LoadButton.rect.width, y, log_button_image)
LogButton.do_clicked = createlogfile

collidables = [ResetButton, LineToggleButton, LoadButton, LogButton]
draw_list = [controller, counter, ResetButton, LoadButton, LineToggleButton, LogButton, filewindow]


def collision_check(mouse_pos, collision_box):
    mouse_x = mouse_pos[0]
    mouse_y = mouse_pos[1]

    if collision_box[0] <= mouse_x <= collision_box[0] + collision_box[2]:
        if collision_box[1] <= mouse_y <= collision_box[1] + collision_box[3]:
            return True
    return False


# controller = PlayStation5Controller(0)

done = False

if getattr(sys, 'frozen', False):
    pyi_splash.close()

while not done:

    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                touch = False
                check = False
                filewindow.state = False

                for i in range(len(collidables) - 1, -1, -1):
                    item = collidables[i]
                    touch = collision_check(position, item.rect)
                    if touch:
                        collided = item
                        if collided.__class__ == ClickableOptionButton:
                            check = collided.do_clicked()
                            if check.__class__ == dict:
                                for item in check:
                                    collidables.append(item)
                        elif collided.__class__ == FileBox:
                            check = collided.do_clicked()
                            print("high")
                            if check.__class__ == GenericController:
                                controller = check
                        break

                if check.__class__ != dict:
                    for item in filewindow.item_dict:
                        for thing in collidables:
                            if thing == item:
                                collidables.remove(item)
                    break

        # Was a device added?
        if event.type == pygame.JOYDEVICEADDED:
            # This event will be generated when the program starts for every
            # joystick, filling up the list without needing to create them manually.
            joy = pygame.joystick.Joystick(event.device_index)
            ID = joy.get_instance_id()
            joysticks[ID] = joy
            if controller:
                if controller.gamepad == False:
                    controller.gamepad = joysticks[ID]
                    controller.resetListItems()

        # Was a device removed?
        if event.type == pygame.JOYDEVICEREMOVED:
            # This event will be generated when the program starts for every
            # joystick, filling up the list without needing to create them manually.
            joy = event.instance_id
            # ID = ActiveStick.gamepad.get_instance_id()
            if controller:
                if controller.gamepad:
                    if controller.gamepad.get_instance_id() == joy:
                        controller.gamepad = False
                        words = "PRESS BUTTON"
                        text = font.render(words, True, (200, 74, 220))
            del joysticks[joy]
    if done:
        break

    controller.update()
    counter.update()
    display.blit(background, (0, 0))

    for item in draw_list:
        item.draw(display)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
