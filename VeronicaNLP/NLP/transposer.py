#-*-coding:utf8;-*-
import re

class Transposer(object):
    """ text transposition class """
    def __init__(self):
        self.transpose = {"i":"you",
                        "are":"am",
                        "yours":"mine",
                        "mine":"yours",
                        "am":"are",            
                        "you":"i",
                        "i'm":"you're",
                        "you're":"i'm",
                        "was":" were",
                        "i'd": "you would",
                        "i've": "you have",
                        "i'll": "you will",
                        "my": "your",
                        "you've": "I have",
                        "you'll": "I will",
                        "i will":"you'll",
                        "I have":"you've",
                        "you would":"i'd",
                        "you have":"i've",
                        "you will":"i'll",
                        "your": "my",
                        "you": "me",
                        "me": "you"}

    def transpose_text(self,text):
        '''convert a number written as text to its real number equivalence'''
        text = text.lower()
        text = re.sub(r"you are","i'm", text)
        text = re.sub(r"i am", "you are", text)
        text = re.sub(r"your", "i'm", text)
        text = re.sub(r"i'm", "your", text)
        text = re.sub(r"i will","you'll", text)
        text = re.sub(r"i would","you would", text)
        text = re.sub(r"me", "i", text)        
        return text

    def transpose_sentence(self,fragment):
        """ transposes a sentence """
        dbms = self.transpose
        tokens = fragment.lower().split()
        for i, token in enumerate(tokens):
            if token in dbms:
                tokens[i] = dbms[token]
        return ' '.join(tokens)

    def transposer(self,user):
        """ transposes a filtered sentence """
        if "me" in self.transpose_sentence(user).split():
            return self.transpose_text(self.transpose_sentence(user))        
        else:
            return self.transpose_sentence(user)
