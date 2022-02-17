#-*-coding:utf8;-*-
import re

class Text_formatter(object):
    
    def filter_text2(self,text,filtery):
        texts = text.split()
        text = enumerate(texts)
        for i,j in text:
            if  filtery in j:
                return  " ".join(texts[0:i+1])
        else:
            return " ".join(texts)
    
    def gen_sentence(self,data_source,stoper ="."):
        document = []
        for id,sentence in enumerate(data_source):
            if stoper in sentence:document.append(filter_text2(sentence,stoper))
        return(document)

    def cleanText(self,input):
        input = re.sub('\n+', " ", input).lower()
        input = re.sub('\[[0-9]*\]', "", input)
        input = re.sub(' +', " ", input)
        input = re.sub("u\.s\.", "us", input)
        input = re.sub("\W+", " ", input)
        return input
    
    def replace_punc(self,text,rep=" "):
        text = text.lower()
        text = text.replace("?",rep)
        text = text.replace("_",rep)
        text = text.replace("-",rep)
        text = text.replace("gist",rep)
        text = text.replace("com",rep)
        text = text.replace("mp3",rep)
        text = text.replace("."," ")
        text = text.replace("com","")
        text = text.replace("_"," ")
        text = text.replace("-"," ")
        text = text.replace("tooxclusive","")
        text = text.replace("naijmp3","")
        text = text.replace("naij","")
        text = text.replace("9jaflaver","")
        text = text.replace("mp4",rep)
        text = text.replace(".",rep)
        text = text.replace(" ft "," featuring ")
        text = text.replace(" Ft "," featuring ")
        return(text)
    
    def filter_text(self,text,filtery="to",tuples=True):
        text = [i for i in self.replace_punc(text).split() if i!="ng"]
        for i,j in enumerate(text):
            if filtery in j:
                if tuples:return((" ".join(text[0:i])," ".join(text[i+1:])))
                else:return(" ".join(text[0:i]))
        else:
            return(" ".join(text))
        
