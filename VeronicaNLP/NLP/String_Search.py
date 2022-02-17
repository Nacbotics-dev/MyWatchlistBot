#-*-coding:utf8;-*-
import operator
from collections import OrderedDict
from .text_formatter import Text_formatter
from VeronicaNLP.mathslib.linear_algebra import*

class String_Search(object):
    def __init__(self,data_source=None):
        self.boolean = False
        self.commonWords = ["to","at"]
        self.text_formatter = Text_formatter()
        self.dictx,self.lists = dict(),data_source
        
    def cosine_search(self,text1,text2,prints=False):
        space = []
        text1,text2 = self.text_formatter.cleanText(text1.lower()),self.text_formatter.cleanText(text2.lower())      
        text1 = self.text_formatter.replace_punc(text1)
        text2 = self.text_formatter.replace_punc(text2)
        space.append(text1.split())
        space.append(text2.split())
        common_words = sorted(list({ common_word for common_words in space for common_word in common_words }))
    
        def string_vector(string_list):
            "given a list of string_list, produce a vector whose i-th element is 1 if common_words[i] is in the list, 0 otherwise "
            return [1 if interest in string_list else 0 for interest in common_words]
    
        string_matrix = map(string_vector,space)
        string_similarities = [[cosine_similarity(common_word_i, common_word_j)for common_word_j in string_matrix]for common_word_i in string_matrix]
        try:cosine_similarity_index = (round(sum(string_similarities[0]),2)-1)*100
        except:cosine_similarity_index = 0
        if cosine_similarity_index >=1:
            self.dictx[text2] = cosine_similarity_index
        else:
            pass
        if prints:
            print("%s ---> %s"%(text1,text2),cosine_similarity_index)
        else:pass
        return(cosine_similarity_index)

    def match_string(self,x,y,prints=False):
        " returns the match of x to y as a percentage using euclidean distance "        
        x,y = self.text_formatter.cleanText(x.lower()),self.text_formatter.cleanText(y.lower())
        x = self.text_formatter.replace_punc(x)
        y = self.text_formatter.replace_punc(y)
        
        a = set(x.split())
        b = set(y.split())
        c = float(len(a&b))
        d = float(len(a|b))
        try:similarity_ratio = round(((c/d)*100/1),2)
        except:similarity_ratio = 0
        if similarity_ratio >= 1:self.dictx[y] = similarity_ratio
        else:pass
        if prints:
            print("%s ---> %s"%(x,y),similarity_ratio)
        else:pass
        return(similarity_ratio)
    
    def get_edit_distance(self,word1, word2):
        """ levenshetein distance algorithm in python """
        word2 = word2.lower()
        word1 = word1.lower()
        matrix = [[0 for x in range(len(word2) + 1)] for x in range(len(word1) + 1)]
        for x in range(len(word1) + 1):
            matrix[x][0] = x
        for y in range(len(word2) + 1):
            matrix[0][y] = y
        for x in range(1, len(word1) + 1):
            for y in range(1, len(word2) + 1):
                if word1[x - 1] == word2[y - 1]:
                    matrix[x][y] = min(matrix[x - 1][y] + 1,matrix[x - 1][y - 1],matrix[x][y - 1] + 1)
                else:
                    matrix[x][y] = min(matrix[x - 1][y] + 1,matrix[x - 1][y - 1] + 1,matrix[x][y - 1] + 1)        
        levenshtein_distance = (matrix[len(word1)][len(word2)])    
        return (levenshtein_distance)   

    def find_match(self,text,func,data_source,prints=False):
        text = " ".join([i for i in text.split() if i not in self.commonWords])
        for id,string in enumerate(data_source):
            func(text,string,prints)
        dictz = list(OrderedDict(sorted(self.dictx.items(), key=lambda t: t[1], reverse=True)))
        try:
            test = dictz[0]
            for id,string in enumerate(data_source):
                if func(test,string,prints) >=100:
                    self.dictx = dict()
                    return((id,string))
                else:pass
        except IndexError as e:
            self.dictx = dict()
            return None
        self.dictx = dict()

    def find_match_list_tuple(self,args,func,prints=False):
        arg = " ".join([i for i in args.split() if i not in self.commonWords])
        for id,string in enumerate(self.lists):
            func(arg,string[0])
        dictz = list(OrderedDict(sorted(self.dictx.items(), key=lambda t: t[1], reverse=True)))
        try:
            test = dictz[0]
            for id,string in enumerate(self.lists):
                if func(test,string[0],prints) >=100:
                    self.dictx = dict()
                    #################
                    #print(id)
                    ################
                    return(id,string)
                else:pass
        except IndexError as e:
            #print(str(e))
            self.dictx = dict()
            return None
        self.dictx = dict()
    
    def search(self,keyword,func,threshold=50,data_source=None,prints=None):
        result = list()
        for _,text in enumerate(data_source):
            if func(text,keyword,prints) >= threshold:
                result.append((text,_))
            else:pass
        return result     
    
    def match_greater_than(self,y,x,func,threshold=50,prints=False,flag="any"):
        """ match for x greater than y """
        if flag == "any":
            if any([i for i in range(len(x)) if func(y,x[i],prints) >= threshold]):return True
            else:return False
        if flag == "all":
            if all([i for i in range(len(x)) if func(y,x[i],prints) >= threshold]):return True
            else:return False
    
    def match_less_than(self,y,x,func,threshold=50,prints=False,flag="any"):
        print(""" match for x less than y""")
        if flag == "any":
            if any([i for i in range(len(x)) if func(y,x[i],prints) <= threshold]):return True
            else:return False
        if flag == "all":
            if all([i for i in range(len(x)) if func(y,x[i],prints) <= threshold]):return True
            else:return False
        
