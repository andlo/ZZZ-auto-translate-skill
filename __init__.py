"""
skill auto-translate
Copyright (C) 2020  Andreas Lorensen

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from mycroft import MycroftSkill, intent_file_handler
from os import makedirs, listdir, walk
from os.path import join, isdir, isfile
from mtranslate import translate


class AutoTranslate(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        self.skillsdir = self.config_core.get('skills', {}).get('msm', {}).get('directory')
        self.add_event('mycroft.skills.loaded',
                       self.handler_mycroft_skills_loaded)

    def handler_mycroft_skills_loaded(self, message):
        self.translate_skill(message.data.get('path'))

    @intent_file_handler('auto.translate.intent')
    def handle_auto_translate(self, message):
        self.speak_dialog('auto.translate')
        for skill in listdir(self.skillsdir):
            self.translate_skill(join(self.skillsdir, skill))

    def translate_skill(self, folder):
        ''' translate skill '''
        translate_folders = []
        lang_folders = []
        if isdir(join(folder, 'vocab')):
            lang_folders.append(join(folder, 'vocab/en-us'))
        if isdir(join(folder, 'dialog')):
            lang_folders.append(join(folder, 'dialog/en-us'))
        if isdir(join(folder, 'regex')):
            lang_folders.append(join(folder, 'regex/en-us'))
        if isdir(join(folder, 'locale')):
            lang_folders.append(join(folder, 'locale/en-us'))

        for folder in lang_folders:
            dest = folder.replace('en-us', self.lang)
            translate_folders.append(folder)
            if not isdir(dest):
                translate_folders.append(folder)
                if not isdir(dest):
                    makedirs(dest, exist_ok=True)
                    with open(join(dest, 'AUTO_TRANSLATED'), "w") as f:
                        f.write('Files in this folder is auto translated by auto-translate skill. ')
                        f.write('Please do a manuel inspection of the translation in every file ')

        for folder in translate_folders:
            for root, dirs, files in walk(folder, topdown=True):
                for file in files:
                    self.treanslate_file(root, file)

    def treanslate_file(self, root, file):
        ''' translate file '''
        dest = root.replace('en-us', self.lang)
        makedirs(dest, exist_ok=True)
        if not isfile(join(dest, file)):
            translated = []
            with open(join(root, file), "r") as f:
                lines = f.readlines()
                for line in lines:
                    if line[0] == '#':
                        translated.append(line.strip('\n') + " \n")
                    else: 
                        translated.append('# ' + line.strip('\n') + '\n')
                        translated.append(self.translate_line(line, '', '') + " \n")
            with open(join(dest, file), "w") as f:
                f.writelines('# This file is auto translated by auto-translate skill. \n')
                f.writelines(translated)
            self.log.info('New translation ' + join(dest, file))

    def translate_line(self, line, part, result):
        ''' translate real words in line - not regex tags and other stuff '''
        regex_chars = ['(', ')', '|', '?', '<', '>', '.', '*', ',', '!', '$', '\\', '.', ':', '[', ']','{','}']
        if line == '':
            translated_part = translate(part, self.lang, 'en-us')
            return result + translated_part
        if line[0] in regex_chars:
            translated_part = translate(part, self.lang, 'en-us')
            if (part.endswith(' ')) and (len(part) > 1) :
                translated_part = translated_part + ' '
            elif part.endswith(' '):
                translated_part = ' '
            result = result + translated_part
            
            if len(line) == 1:
                return result + line[0] 
            elif line[1] in regex_chars:
                return self.translate_line(line[1:], '', result + line[0])  
            elif line[0] == '<': 
                tag = line.split('>')[0]
                return self.translate_line(line[len(tag)+1:], '', result + line.split('>')[0] + '>') 
            elif line[0] == '{': 
                tag = line.split('}')[0]
                return self.translate_line(line[len(tag)+1:], '', result + line.split('}')[0] + '}') 
            elif line[0] == '[': 
                tag = line.split(']')[0]
                return self.translate_line(line[len(tag)+1:], '', result + line.split(']')[0] + ']') 
            elif line[0] == '?':       
                return self.translate_line(line[1:], '', result + line[0]) 
            elif line[0] == '\\':       
                return self.translate_line(line[2:], '', result + line[:2]) 
            else:
                return self.translate_line(line[1:], '', result + line[0])    
        else:
            return self.translate_line(line[1:], part + line[0], result)

        self.unsupported_languages = []
  
        lang = self.lang
        if lang not in self.unsupported_languages:
            if lang in self.lang_map:
                return True
            if lang[:2] in self.lang_map:
                return True
            for l in self.lang_map:
                if self.lang_map[l].lower() == lang.lower():
                    return True
        return False


def create_skill():
    return AutoTranslate()
