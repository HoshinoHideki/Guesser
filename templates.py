import random, re


class Card:
    def __init__(self, template, english_line, armenian_line):
        self.template = template
        self.english_line = english_line
        self.armenian_line = armenian_line


class Template:
    def __init__(self, structure, english_template, armenian_template):
        self.structure = structure
        self.english_template = english_template
        self.armenian_template = armenian_template


class Word:
    def __init__(self, english, armenian):
        self.english = english
        self.armenian = armenian


pairs = {"I": "Ես",
         "You": "դու",
         "He": "նա",
         "She": "նա",
         "am": "եմ",
         "are": "ես",
         "is": "է",
         "man": "մարդ",
         "woman": "կին",
         "girl": "աղջիկ",
         "boy": "տղա", }


def make_sentence():
    pronoun = ["I", "You", "He", "She"]
    be = ["am", "are", "is"]
    noun = ["man", "woman", "girl", "boy"]

    pronoun = str(random.choice(pronoun))

    match pronoun:
        case "I":
            be = "am"
        case "You":
            be = "are"
        case "He" | "She":
            be = "is"

    noun = str(random.choice(noun))
    line_english = "{pronoun} {be} a {noun}."
    pronoun = pairs[pronoun]
    be = pairs[be]
    noun = pairs[noun]
    line_armenian = f"{pronoun} {noun} {be}:"

    print("English Line: " + line_english)
    print("Armenian Line:" + line_armenian)

class Phrase:
    def __init__(self):
        self.english = "Eat {noun food}"
        self.turkish = "{noun food} ye."

    def return_tag(self, phrase):
        tag = re.findall("(?:{)(.*)(?:})", phrase)
        return tag

p = Phrase()
tag = p.return_tag(p.english)

for string in tag:
    print(string.split())