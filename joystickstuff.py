import os

from pygame import image, transform, draw, color

from constants import COLOR_WHITE

# Enables monitoring of inputs while unfocused (DO NOT REMOVE THIS. EVER.)
os.environ['SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS'] = '1'


class Background:
    """
    Defines the background drawn behind the controller and inputs within the
    window.
    """

    def __init__(self, bg_path="", bg_color=""):
        self.path = bg_path
        self.image = image.load(self.path)
        self.rect = self.image.get_rect()
        if bg_color == "":  # Default to white if there isn't a color declared
            bg_color = COLOR_WHITE
        self.color = bg_color

    def set_color(self, color_key):
        """
        Reassigns the color used to fill in the background.
        :param color_key: The color we wish to use. (TODO Is this in hex? RGB? Anything?)
        """
        self.color = color_key

    def draw(self, window):
        draw.rect(window, color.Color(self.color), self.rect)
        window.blit(self.image, self.rect)


"""
Here begins the definitions of the following objects (in order of appearance):
- Button
- TriggerAxis
- Stick
- Hat

Our goals are the following:
- Identify similarities between these 4 classes
- Construct a base class from which each can inherit behaviors that appear everywhere
- Extend that base class and implement missing functionality/abstract behaviors
- Remove 4/5 of the total classes defined within this file.
"""


class Button:
    """
    TODO
    """
    unpressed = "./buttons/unpressed.png"
    pressed = "./buttons/pressed.png"
    off = image.load(unpressed)
    on = image.load(pressed)
    rotate = 0
    actions = 0
    name = ""

    def __init__(self, buttonnum=-1, x=-1, y=-1, controller=False, name=""):
        self.assetdict = {}
        self.x = x
        self.y = y
        self.buttonnum = buttonnum
        self.state = 0
        self.image = self.off
        self.controller = controller
        self.name = name
        self.assetdict["pressed"] = self.pressed, self.on, self.set_pressed
        self.assetdict["unpressed"] = self.unpressed, self.off, self.set_unpressed

    def set_pressed(self, path=''):
        if path == '':
            path = self.pressed
        self.pressed = path
        self.load()

    def set_unpressed(self, path=''):
        if path == '':
            path = self.unpressed
        self.unpressed = path
        self.load()

    def update_self(self):
        if self.controller.gamepad:
            if len(self.controller.buttondict) > 0:
                if self.buttonnum in self.controller.buttondict:
                    safetylength = self.controller.gamepad.get_numbuttons()
                    if self.buttonnum < safetylength:
                        self.state = self.controller.gamepad.get_button(self.buttonnum)
            else:
                self.state = 0
        else:
            self.state = 0
        if self.state == 0:
            self.image = self.off
            return False
        else:
            if self.image != self.on:
                self.image = self.on
                self.actions = self.actions + 1
                return True
            return False

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def load(self):
        self.off = image.load(self.unpressed)
        self.on = image.load(self.pressed)
        self.on = transform.rotate(self.on, self.rotate)
        self.off = transform.rotate(self.off, self.rotate)
        self.assetdict["pressed"] = self.pressed, self.on, self.set_pressed
        self.assetdict["unpressed"] = self.unpressed, self.off, self.set_unpressed

    def rotate(self):
        """
        Rotates self by increments of 90 degrees. If the current rotation does
        not exceed 270 degrees (3/4 of a rotation), it rotates as expected. In
        the event that the rotation would complete a circle, the rotation is
        reverted back to 0 (i.e. starting position)
        :return:
        """
        if self.rotate < 270:  # Check if we're less than 3/4 of a rotation
            self.rotate = self.rotate + 90  # Continue rotation, there's room
        else:  # Otherwise short circuit back to default rotation
            self.rotate = 0
        self.load()  # Load the image, irrespective of preceding events


class TriggerAxis:
    """
    TODO
    """
    bar_image = "./Axis/triggerbar.png"
    paddleimage = "./Axis/paddlebar.png"
    pressed = "./Axis/buttons/pressed.png"
    unpressed = "./Axis/buttons/unpressed.png"
    pressedimage = image.load(pressed)
    unpressedimage = image.load(unpressed)
    button = unpressedimage
    bar = image.load(bar_image)
    paddle = image.load(paddleimage)
    horizontal = False
    rotate = 0
    actions = 0

    name = ""

    def __init__(self, x=-1, y=-1, axis=-1, controller=False, mode='axis', rotate=0, name=""):
        self.assetdict = {}
        self.x = x
        self.y = y
        self.ymod = -1
        self.axis = axis
        self.axisstate = 0
        self.controller = controller
        self.activestate = False
        self.mode = mode
        self.modedict = {'axis': self.draw_axis_mode, 'button': self.draw_button_mode}
        self.loaddict = {'axis': self.load_axis_mode, 'button': self.load_button_mode}
        self.draw = self.modedict[mode]
        self.load = self.loaddict[mode]
        self.rotate = rotate
        self.name = name
        self.assetdict["pressed"] = self.pressed, self.pressedimage, self.setpressed
        self.assetdict["unpressed"] = self.unpressed, self.unpressedimage, self.setunpressed
        self.assetdict["bar"] = self.bar_image, self.bar, self.setbar
        self.assetdict["paddle"] = self.paddleimage, self.paddle, self.set_paddle

    def setpressed(self, path=''):
        if path == '':
            path = self.pressed
        self.pressed = path
        self.load()

    def setunpressed(self, path=''):
        if path == '':
            path = self.unpressed
        self.unpressed = path
        self.load()

    def setbar(self, path=''):
        if path == '':
            path = self.bar_image
        self.bar_image = path
        self.load()

    def set_paddle(self, path=''):
        if path == '':
            path = self.paddleimage
        self.paddleimage = path
        self.load()

    def update_self(self):
        if self.controller.gamepad:
            if len(self.controller.axisdict) >= 0:
                if self.axis in self.controller.axisdict:
                    self.axisstate = self.controller.gamepad.get_axis(self.axis)
            else:
                self.axisstate = 0
        else:
            self.axisstate = 0
        self.ymod = abs(-1 - self.axisstate) / 2

        if not self.activestate:
            if self.ymod > .1:
                self.activestate = True
                self.actions = self.actions + 1
                return True
            return False

        if self.ymod < .1:
            self.activestate = False
        return False

    def draw(self, WINDOW):
        """
        Placeholder for potential pattern decoration. As such, this should
        remain defined within the class as to confer this affect to all
        instances.
        :param WINDOW:
        :return:
        """
        return False

    def draw_axis_mode(self, WINDOW):
        if self.horizontal:
            WINDOW.blit(self.bar, (self.x, self.y))
            WINDOW.blit(self.paddle, (self.x + (100 * self.ymod), self.y - 4))
        else:
            WINDOW.blit(self.bar, (self.x, self.y))
            WINDOW.blit(self.paddle, (self.x - 4, (self.y + (100 * self.ymod))))

    def draw_button_mode(self, window):
        if not self.activestate:
            if self.button != self.unpressedimage:
                self.button = self.unpressedimage
        else:
            if self.button != self.pressedimage:
                self.button = self.pressedimage

        window.blit(self.button, (self.x, self.y))

    def load(self):
        return

    def load_axis_mode(self):
        self.bar = image.load(self.bar_image)
        self.paddle = image.load(self.paddleimage)
        if self.horizontal:
            self.bar = transform.rotate(self.bar, 90)
            self.paddle = transform.rotate(self.paddle, 90)
        self.assetdict["bar"] = self.bar_image, self.bar, self.setbar
        self.assetdict["paddle"] = self.paddleimage, self.paddle, self.set_paddle

    def load_button_mode(self):
        self.unpressedimage = image.load(self.unpressed)
        self.pressedimage = image.load(self.pressed)
        self.pressedimage = transform.rotate(self.pressedimage, self.rotate)
        self.unpressedimage = transform.rotate(self.unpressedimage, self.rotate)
        self.assetdict["pressed"] = self.pressed, self.pressedimage, self.setpressed
        self.assetdict["unpressed"] = self.unpressed, self.unpressedimage, self.setunpressed

    def rotate(self):
        self.horizontal = not self.horizontal
        self.load()

    def mode_adjust(self):
        self.draw = self.modedict[self.mode]
        self.load = self.loaddict[self.mode]


class Stick:
    """
    TODO
    """
    pressed = "./sticks/stickpressed.png"
    unpressed = "./sticks/stickunpressed.png"
    stickunpressed = image.load(unpressed)
    stickpressed = image.load(pressed)
    rotate = 0
    moveactions = 0
    pressactions = 0
    stickname = ""
    buttonname = ""

    def __init__(self, x, y, vertaxis=-1, horaxis=-1, buttonnum=-1, controller=False, stickname="", buttonname=""):
        self.assetdict = {}
        self.x = x
        self.y = y
        self.vertaxis = vertaxis
        self.vertstate = 0
        self.vertmod = 0
        self.horaxis = horaxis
        self.horstate = 0
        self.hormod = 0
        self.buttonnum = buttonnum
        self.image = self.stickunpressed
        self.pressedstate = False
        self.controller = controller
        self.rect = self.image.get_rect()
        self.horactive = False
        self.vertactive = False
        self.stickname = stickname
        self.buttonname = buttonname
        self.assetdict["pressed"] = self.pressed, self.stickpressed, self.set_pressed
        self.assetdict["unpressed"] = self.unpressed, self.stickunpressed, self.set_unpressed

    def set_pressed(self, path=''):
        if path == '':
            path = self.pressed
        self.pressed = path
        self.load()

    def set_unpressed(self, path=''):
        if path == '':
            path = self.unpressed
        self.unpressed = path
        self.load()

    def update_self(self):
        if self.buttonnum >= 0:  # TODO What does 0 mean in this context?
            if self.controller.gamepad:
                if self.buttonnum < self.controller.gamepad.get_numbuttons():
                    self.pressedstate = self.controller.gamepad.get_button(self.buttonnum)
            else:
                self.pressedstate = 0  # TODO What does 0 mean in this context?
        action = False
        if self.pressedstate == 0:  # TODO What does 0 mean in this context?
            self.image = self.stickunpressed
            action = False
        else:
            if self.image != self.stickpressed:
                self.image = self.stickpressed
                self.pressactions = self.pressactions + 1
                action = True
            else:
                action = False
        if self.controller.gamepad:
            if self.vertaxis >= 0:  # TODO What does 0 mean in this context?
                if self.vertaxis < self.controller.gamepad.get_numaxes():
                    self.vertstate = self.controller.gamepad.get_axis(self.vertaxis)
                else:
                    self.vertstate = 0  # TODO What does 0 mean in this context?
                self.vertmod = (self.rect.height / 2) * self.vertstate
            if self.horaxis >= 0:  # TODO What does 0 mean in this context?
                if self.horaxis < self.controller.gamepad.get_numaxes():
                    self.horstate = self.controller.gamepad.get_axis(self.horaxis)
                else:
                    self.horstate = 0  # TODO What does 0 mean in this context?
            self.hormod = (self.rect.width / 2) * self.horstate

        if not self.horactive:
            if abs(self.hormod) > 2:  # TODO What does 2 mean in this context?
                self.horactive = True
                self.moveactions = self.moveactions + 1
                self.controller.actioncount = self.controller.actioncount + 1

        if abs(self.hormod) < 2:  # TODO What does 2 mean in this context?
            self.horactive = False

        if not self.vertactive:
            if abs(self.vertmod) > 2:  # TODO What does 2 mean in this context?
                self.vertactive = True
                self.moveactions = self.moveactions + 1
                self.controller.actioncount = self.controller.actioncount + 1

        if abs(self.vertmod) < 2:  # TODO What does 2 mean in this context?
            self.vertactive = False

        return action

    def draw(self, window):
        window.blit(self.image, (self.x + self.hormod, self.y + self.vertmod))

    def load(self):
        self.stickpressed = image.load(self.pressed)
        self.stickunpressed = image.load(self.unpressed)
        self.stickpressed = transform.rotate(self.stickpressed, self.rotate)
        self.stickunpressed = transform.rotate(self.stickunpressed, self.rotate)
        self.assetdict["pressed"] = self.pressed, self.stickpressed, self.set_pressed
        self.assetdict["unpressed"] = self.unpressed, self.stickunpressed, self.set_unpressed

    def rotate(self):
        if self.rotate < 270:  # If we have at least one more rotation left
            self.rotate = self.rotate + 90
        else:  # Reset orientation
            self.rotate = 0
        self.load()

    def change_horizontal_axis(self, newaxisnum):
        self.horaxis = newaxisnum

    def change_vertical_axis(self, newaxisnum):
        self.vertaxis = newaxisnum

    def change_button(self, newbuttonnum):
        self.buttonnum = newbuttonnum

    def drop_items(self):

        droplist = []
        axis = []

        if self.vertaxis >= 0:  # TODO What does 0 mean in this context?
            # TODO How can this instantiation be done more cleanly?
            axisadd = TriggerAxis(self.x, self.y - (self.stickunpressed.get_rect().bottomright[1]), self.vertaxis,
                                  self.controller)
            axisadd.rotate()
            axis.append(axisadd)

        if self.horaxis >= 0:  # TODO What does 0 mean in this context?
            # TODO How can this instantiation be done more cleanly?
            axisadd = TriggerAxis(self.x, self.y - (self.stickunpressed.get_rect().bottomright[1] * 2), self.horaxis,
                                  self.controller)
            axisadd.rotate()
            axis.append(axisadd)

        droplist.append(axis)
        if self.buttonnum >= 0:  # TODO What does 0 mean in this context?
            # TODO How can this instantiation be done more cleanly?
            buttonadd = Button(self.buttonnum, self.x, (self.y - self.stickunpressed.get_rect().bottomright[1] * 3),
                               self.controller)
            droplist.append(buttonadd)

        self.vertaxis = -1
        self.horaxis = -1
        self.buttonnum = -1

        return droplist


class Hat:
    """
    TODO
    """
    background = './hats/hatbackground.png'
    defaultpressed = './hats/pressed.png'
    defaultunpressed = './hats/unpressed.png'
    centerdefault = './hats/smileunpressed.png'
    rotate = 0
    rotatemod = 0
    actions = 0
    name = ""
    directions = {(0, 0): "center", (0, 1): "N", (0, -1): "S", (1, 0): "E", (1, -1): "SE", (1, 1): "NE", (-1, 0): "W",
                  (-1, 1): "NW", (-1, -1): "SW"}

    def __init__(self, hat_num=-1, x=-1, y=-1, controller=False, name="", mode="hat"):
        self.asset_dict = {}
        self.ModeDict = {}
        self.hat_number = hat_num
        # x and y will be the top left coordinate for the background
        self.x = x
        self.y = y
        self.state = (0, 0)
        self.controller = controller
        self.name = name
        self.mode = mode
        self.HatModeSetList = [
            self.setcenter, self.setbackground,
            self.setNPressed,
            self.setNEPressed,
            self.setNWPressed,
            self.setSPressed,
            self.setSWPressed,
            self.setSEPressed,
            self.setEPressed,
            self.setWPressed
        ]
        self.QuadModeSetList = [
            self.setNPressed, self.setNUnpressed,
            self.setSPressed, self.setSUnpressed,
            self.setEPressed, self.setEUnpressed,
            self.setWPressed, self.setWUnpressed
        ]
        self.OctoModeSetList = [
            self.setNPressed, self.setNUnpressed,
            self.setNEPressed, self.setNEUnpressed,
            self.setNWPressed, self.setNWUnpressed,
            self.setSPressed, self.setSUnpressed,
            self.setSWPressed, self.setSWUnpressed,
            self.setSEPressed, self.setSEUnpressed,
            self.setEPressed, self.setEUnpressed,
            self.setWPressed, self.setWUnpressed
        ]
        self.ModeDict['hat'] = self.HatModeSetList, self.updateHatImage, self.drawHatMode
        # self.ModeDict['quad'] = self.QuadModeSetList, self.updateQuadImage, self.drawQuadMode
        # self.ModeDict['octo'] = self.OctoModeSetList, self.updateOctoImage, self.drawOctoMode
        self.setlist = self.ModeDict[self.mode][0]
        self.updateImage = self.ModeDict[self.mode][1]
        self.draw = self.ModeDict[self.mode][2]
        self.setdefaults()

    def setdefaults(self):
        del self.asset_dict
        self.asset_dict = {}
        for item in self.setlist:
            item()
        self.load()

    def setcenter(self, PATHNAME=''):
        if PATHNAME == '':
            PATHNAME = self.centerdefault
        self.asset_dict["center"] = PATHNAME, image.load(PATHNAME), self.setcenter
        self.stateimage = self.asset_dict['center'][1]
        self.staterect = self.stateimage.get_rect()

    def setbackground(self, PATHNAME=''):
        if PATHNAME == '':
            PATHNAME = self.background
        self.asset_dict["background"] = PATHNAME, image.load(PATHNAME), self.setbackground
        self.backgroundrect = self.asset_dict['background'][1].get_rect()
        self.backgroundcenterx = self.backgroundrect[2] / 2
        self.centery = self.backgroundrect[3] / 2

    def setNPressed(self, PATHNAME=''):
        if PATHNAME == '':
            PATHNAME = self.defaultpressed
        self.asset_dict["Npressed"] = PATHNAME, image.load(PATHNAME), self.setNPressed

    def setNUnpressed(self, PATHNAME=''):
        if PATHNAME == '':
            PATHNAME = self.defaultunpressed
        self.asset_dict["Nunpressed"] = PATHNAME, image.load(PATHNAME), self.setNUnpressed

    def setSPressed(self, PATHNAME=''):
        if PATHNAME == '':
            PATHNAME = self.defaultpressed
        self.asset_dict["Spressed"] = PATHNAME, image.load(PATHNAME), self.setSPressed

    def setSUnpressed(self, PATHNAME=''):
        if PATHNAME == '':
            PATHNAME = self.defaultunpressed
        self.asset_dict["Sunpressed"] = PATHNAME, image.load(PATHNAME), self.setSUnpressed

    def setWPressed(self, PATHNAME=''):
        if PATHNAME == '':
            PATHNAME = self.defaultpressed
        self.asset_dict["Wpressed"] = PATHNAME, image.load(PATHNAME), self.setWPressed

    def setWUnpressed(self, PATHNAME=''):
        if PATHNAME == '':
            PATHNAME = self.defaultunpressed
        self.asset_dict["Wunpressed"] = PATHNAME, image.load(PATHNAME), self.setWUnpressed

    def setEPressed(self, PATHNAME=''):
        if PATHNAME == '':
            PATHNAME = self.defaultpressed
        self.asset_dict["Epressed"] = PATHNAME, image.load(PATHNAME), self.setEPressed

    def setEUnpressed(self, PATHNAME=''):
        if PATHNAME == '':
            PATHNAME = self.defaultunpressed
        self.asset_dict["Eunpressed"] = PATHNAME, image.load(PATHNAME), self.setEUnpressed

    def setNEPressed(self, PATHNAME=''):
        if PATHNAME == '':
            PATHNAME = self.defaultpressed
        self.asset_dict["NEpressed"] = PATHNAME, image.load(PATHNAME), self.setNEPressed

    def setNEUnpressed(self, PATHNAME=''):
        if PATHNAME == '':
            PATHNAME = self.defaultunpressed
        self.asset_dict["NEunpressed"] = PATHNAME, image.load(PATHNAME), self.setNEUnpressed

    def setNWPressed(self, PATHNAME=''):
        if PATHNAME == '':
            PATHNAME = self.defaultpressed
        self.asset_dict["NWpressed"] = PATHNAME, image.load(PATHNAME), self.setNWPressed

    def setNWUnpressed(self, PATHNAME=''):
        if PATHNAME == '':
            PATHNAME = self.defaultunpressed
        self.asset_dict["NWunpressed"] = PATHNAME, image.load(PATHNAME), self.setNWUnpressed

    def setSWPressed(self, PATHNAME=''):
        if PATHNAME == '':
            PATHNAME = self.defaultpressed
        self.asset_dict["SWpressed"] = PATHNAME, image.load(PATHNAME), self.setSWPressed

    def setSWUnpressed(self, PATHNAME=''):
        if PATHNAME == '':
            PATHNAME = self.defaultunpressed
        self.asset_dict["SWunpressed"] = PATHNAME, image.load(PATHNAME), self.setSWUnpressed

    def setSEPressed(self, PATHNAME=''):
        if PATHNAME == '':
            PATHNAME = self.defaultpressed
        self.asset_dict["SEpressed"] = PATHNAME, image.load(PATHNAME), self.setSEPressed

    def setSEUnpressed(self, PATHNAME=''):
        if PATHNAME == '':
            PATHNAME = self.defaultunpressed
        self.asset_dict["SEunpressed"] = PATHNAME, image.load(PATHNAME), self.setSEUnpressed

    def changeMode(self, mode):
        # self.ModeDict['hat'] = self.HatModeSetList, self.updateHatImage(), self.drawHatMode()
        # self.ModeDict['quad'] = self.QuadModeSetList, self.updateQuadImage(), self.drawQuadMode()
        # self.ModeDict['octo'] = self.OctoModeSetList, self.updateOctoImage(), self.drawOctoMode()
        self.mode = mode
        self.draw = self.ModeDict[self.mode][2]
        self.updateImage = self.ModeDict[self.mode][1]
        self.setlist = self.ModeDict[self.mode][0]
        self.setdefaults()
        self.load()
        return

    def UpdateSelf(self):
        action = False
        if self.hat_number >= 0:
            if self.controller:
                if self.controller.gamepad:
                    length = self.controller.gamepad.get_numhats()
                    if length > self.hat_number > -1:
                        if self.state != self.controller.gamepad.get_hat(self.hat_number) and self.state != (0, 0):
                            action = True
                            self.actions = self.actions + 1
                        self.state = self.controller.gamepad.get_hat(self.hat_number)
                    else:
                        self.state = (0, 0)
        else:
            self.state = (0, 0)

        self.updateImage()
        return action

    def updateImage(self):
        self.updateHatImage()
        return

    def updateHatImage(self):

        # self.imagex = (self.state[0] * self.staterect[2]) + self.backgroundrect[2]/2 - self.staterect[3]/2 + self.x+1
        # self.imagey = (-self.state[1] * self.staterect[3]) - self.staterect[3]/2 + self.backgroundrect[3]/2 + self.y
        self.rotatemod = 0
        xstate = self.state[0]
        ystate = self.state[1]
        staterectx = self.staterect[2]
        staterecty = self.staterect[3]
        backgroundrectx = self.backgroundrect[2]
        backgroundrecty = self.backgroundrect[3]
        if self.state == (0, 0):
            self.stateimage = self.asset_dict['center'][1]
        else:
            imgkey = str(self.directions[self.state]) + 'pressed'
            self.stateimage = self.asset_dict[imgkey][1]
            if xstate != 0:
                self.rotatemod = self.rotatemod - (90 * xstate)
            if ystate != 0:
                if self.rotatemod != 0:
                    self.rotatemod = self.rotatemod - (45 * ystate * -xstate)
                elif ystate == -1:
                    self.rotatemod = 180

        self.staterect = self.stateimage.get_rect()

        if xstate != 0 and ystate != 0:
            self.imagex = xstate * staterectx + backgroundrectx / 2 - staterectx / 2 + self.x + 1 - staterectx / 4
            self.imagey = (-ystate * staterecty) - staterecty / 2 + backgroundrecty / 2 + self.y - staterecty / 4
        else:
            self.imagex = (xstate * staterectx) + backgroundrectx / 2 - staterectx / 2 + self.x + 1
            self.imagey = (-ystate * staterecty) - staterecty / 2 + backgroundrecty / 2 + self.y
        self.stateimage = transform.rotate(self.stateimage, self.rotate + self.rotatemod)

    def updateQuadImage(self):
        # self.assetdict["SEunpressed"] = PATHNAME, image.load(PATHNAME), self.setSEUnpressed
        # self.assetdict = {
        #       Npressed, Nunpressed,
        #       Spressed, Sunpressed,
        #       Epressed, Eunpressed,

        #       Wpressed, Wunpressed
        #   }

        # self.assetdict["North"] (PATHNAME, image.load(PATHNAME, self.NorthPressed)

        xstate = self.state[0]
        ystate = self.state[1]

    # if xstate == -1:

    def draw(self, WINDOW):
        self.drawHatMode(WINDOW)
        return

    def drawHatMode(self, WINDOW):
        WINDOW.blit(self.asset_dict['background'][1], (self.x, self.y))
        WINDOW.blit(self.stateimage, (self.imagex, self.imagey))

    def drawQuadMode(self, WINDOW):
        WINDOW.blit()

    def load(self):
        for item in self.asset_dict:
            self.asset_dict[item] = self.asset_dict[item][0], image.load(self.asset_dict[item][0]), \
                self.asset_dict[item][2]
        self.updateImage()

    def ModeAdjust(self):
        self.setlist = self.ModeDict[self.mode][0]
        self.updateImage = self.ModeDict[self.mode][1]
        self.draw = self.ModeDict[self.mode][2]
