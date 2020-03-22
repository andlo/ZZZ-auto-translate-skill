# <img src="https://raw.githack.com/FortAwesome/Font-Awesome/master/svgs/solid/language.svg" card_color="#22A7F0" width="50" height="50" style="vertical-align:bottom"/> Auto Translate


## About
This enables auto translation of skills. If a skill is missing a translation to the current language it will be auto
translated using google translate.

This includes files in vocab, dialog, regex and locale folders within the skill folder. 

Be aware that googel translation isnt perfect, and the translation needs manuel inspection. 

This will translate all skills at initialization and after that check eveytime a kill is loaded if it needs translation.

Each file that is beeing translated will have a line on top added and for every line a comment with the original text. Like this:
```
# This file is auto translated by auto-translate skill. 
# The temperature in {{friendly_name}} is {{temperature}} degrees.
Temperaturen i {{friendly_name}} er {{temperature}} grader.  
# It is {{temperature}} degrees in {{friendly_name}}.
det er {{temperature}} grader i {{friendly_name}}. 
```
If the translation is complete - as there werent any language folder for current language - there will be added a AUTO_TRANSLATED file into the lang folder.

## Examples
translate skills

## Credits
Andreas Lorensen (@andlo)

## Category
**Configuration**
Productivity

## Tags
#Translate
#Language

