import os
import re
import sys
import csv
from VeronicaNLP.NLP.text_formatter import Text_formatter


class Mymovie(object):
    def __init__(self):
        self.texts = Text_formatter()
        try:self.path = [os.environ["USERPROFILE"]]
        except KeyError:self.path = [os.environ["HOME"]+"/"]
        self.escape = ["nltk_data","My Qpython","AppData"]
        

    def prepare_paths(self):
        for path in self.path:
            for  root,dirs,files in os.walk(path):
                dirs = [i for i in dirs if not i.startswith(".")]
                dirs = [i for i in dirs if i not in self.escape]
                dirs = [path+"/%s/"%i for i in dirs]
                return(dirs)


    def file_finder(self,pattern=[".mp4",".avi",".mkv",".3gp"]):
        result = []
        for path in self.prepare_paths():
            for root,dirs,files in os.walk(path):
                for name in files:                    
                    if any([i for i in pattern if i in name]) and os.path.getsize(root+"/"+name) > 5273:result.append((root+"\\",name))
                    else:pass
        return(result)

    def get_seasonal(self):
        data = [i[1] for i in self.file_finder()]
        filex = list()
        for line in data:
            matchObj = re.match( r'[a-zA-Z0-9].*[Ss][0-9].*[Ee][0-9].*',line, re.M|re.I)
            if  matchObj:filex.append(matchObj.group())
        return(filex)

    def get_last_episode(self):
        """ returns last episode i have of all the movies i'm following """
        lst = sorted([re.sub(r'[-_]',' ',i) for i in self.get_seasonal()])
        movie_name = set([re.split(r'[Ss][0-9].*[Ee][0-9].*',i)[0] for i in lst])
        data = dict()
        for i in movie_name:
            lzt = list()
            for j in lst:
                if i in j:lzt.append(j)
            data[i] = lzt
        return([data[movie][-1] for movie in movie_name])

    def get_em_format(self):
        filex = self.get_last_episode()
        tvshows = [re.split(r'[Ss][0-9].*[Ee][0-9].*',i)[0].rstrip(" ") for i in filex]
        episodes = [re.findall(r'[Ss][0-9].*[Ee][0-9].*',i)[0].split()[0] for i in filex]
        listx,listy = list(),list()
        for id,text in enumerate(tvshows):
            listx.append(text+" "+episodes[id].replace("S","season ").replace("E"," episode "))
        return(listx)

    def find_missed_episodes(self,txt,data):
        for id,text in enumerate(data):
            if txt in text:return(data[id+1:])

    def create(self):
        playlist = []
        music_list = self.file_finder()
        musicname = [i[1] for i in music_list]
        music = [i.split(" - ") for i in musicname]
        data = [i for i in music if len(i) > 1]
        for i in data:
            dicts = dict()
            filename = self.texts.replace_punc(i[1].split("(")[0])
            filename = filename.split(")")[0]
            dicts["movie_name"] = i[0]
            dicts["series_title"] = filename
            dicts["storage_name"] = "%s - %s"%(i[0],filename)
            playlist.append(dicts)
        return(playlist)
        


