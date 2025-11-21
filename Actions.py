# TODO
class ModAction:
    trigger = -1

    def __init__(self, TargetCore, item, text):
        self.Core = TargetCore
        self.targettype = item
        self.text = text

    def trigger_check(self):
        if self.trigger > 0:
            self.do_action(self)
            return 1
        else:
            return -1

    def do_action(self, me):
        return

    def check_object(self, item):
        if item.__class__ == self.targettype.__class__:
            return True
        return False

    def set_trigger(self, item):
        self.trigger = item


# TODO
class ActionContainer:
    action = False

    def trigger_check(self):
        if self.action.triggercheck() > 0:
            self.action = False

    def has_action(self):
        if not self.action:
            return False
        return True

    def set_trigger(self, trigger):
        if self.action.checkObject(trigger):
            self.action.setTrigger(trigger)
            self.action.doaction()
            self.action = False
            return True
        return False
