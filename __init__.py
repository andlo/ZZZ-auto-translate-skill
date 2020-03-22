from mycroft import MycroftSkill, intent_file_handler


class AutoTranslate(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('translate.auto.intent')
    def handle_translate_auto(self, message):
        self.speak_dialog('translate.auto')


def create_skill():
    return AutoTranslate()

