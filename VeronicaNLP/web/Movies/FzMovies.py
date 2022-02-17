#-*-coding:utf8;-*-
import requests,re
from .TV import TVSHOWS
from bs4 import BeautifulSoup
from veronica.NLP.string_matcher import string_match
from veronica.NLP.text_formatter import Text_formatter


class FzMovies(TVSHOWS):
    def __init__(self):
        self.match = string_match()
        self.fromat = Text_formatter()
        self.stopwords = ["download","stream"]        
        self.recent_updates = "https://www.fzmovies.net/movieslist.php?catID=2&by=date"
        self.search = "https://www.fzmovies.net/csearch.php?searchname=%s"
        
    def crawl_link(self,url,pattern=""):
        pages = dict()
        html = self.open_url(url)
        BS = BeautifulSoup(html, "html.parser")
        for link in BS.findAll("a",href=re.compile("(.*?)")):
            if "href" in link.attrs:
                try:
                    file_link = "https://www.fzmovies.net/"+link.attrs['href']
                    file_name = re.findall(pattern,str(link))[0]
                    pages[file_name.lower()] = file_link
                except Exception as e:pass
        return(pages)

    def crawl_download_link(self,url,pattern=""):
        pages = dict()
        try:html = self.open_url(url)
        except:html = open(url,encoding="utf-8").read()
        BS = BeautifulSoup(html, "html.parser")
        for link in BS.findAll("a",href=re.compile("(.*?)")):
            if "href" in link.attrs:
                try:
                    file_link = "https://www.fzmovies.net/"+link.attrs['href']
                    file_name = self.fromat.replace_punc(re.findall(pattern,str(link))[0]," ")
                    pages[file_name.lower()] = file_link
                except Exception as e:pass
        return(pages)

    
    def check_updates(self):
        """ returns a list of the latest movies in tvshows4mobile website """
        result = []
        try:html = self.open_url(self.recent_updates)
        except Exception as e:return("no internet connection check your conection and try again")
        BS = BeautifulSoup(html, "html.parser")
        movie_names = re.findall(r'<td>(.*?)</b>',str(BS))
        for movie in movie_names:
            datum = {}
            update = movie.split("</td><td><a")
            url = update[1].split("><b>")[0]
            url = re.sub("href=","https://fztvseries.mobi/",url)
            movie_episode = update[0]
            movie_name = movie.split("<b>")[-1]
            datum["series name"] = movie_name
            datum["the episode"] = movie_episode
            datum["url"] = url
            result.append(movie_episode)
        return(result)

    def run_download(self,cmd):
        ##################################################################################################
        text = "+".join(cmd["filename"].split())
        url = self.search%text
        try:data = self.crawl_link(url,pattern=r'<b>(.*?)</b>')
        except:return("poor internet connection please check your internet connection")
        #print(data)
        ##################################################################################################
        L1 = self.get_true_name(cmd["filename"],data) #gets the name the file  that was used to save the file on Fzmovies
        try:L2 = self.crawl_download_link(data[L1],pattern=r'>(.*?)<') #gets the the movie page
        except:return("no such tvseries as %s"%cmd["filename"])
        try:
            real_name = self.match.find_match(cmd["filename"],self.match.match_string,L2.keys())[1]
            L4 = self.crawl_link(L2[real_name],pattern=r'>(.*?)</a>') #gets the link to the file to download
        except:return("%s is not upto %s"%(cmd["filename"],cmd["episode"]))
        link = self.crawl_link(L4["click here to download this movie on your device"],pattern=r'>(.*?)</a>') #gets the link to the file to download
        links = self.crawl_link(link['download link 1'],pattern=r'<a(.*?)</a>')
        data = list(links.items())[0]
        link = data[1].replace("https://www.fzmovies.net/","")
        filename = re.findall('href="(.*?)">',data[0])[0].split("/res/")[1]
        filename = filename.split("_")
        ext = filename[-1][-1:]
        filename = " ".join(filename[:-1])+filename[-1][-4:]
        return("FILENAME %s\nLINK :%s"%(filename,link))

    def _extract(self,cmd):
        alpha = dict()
        alpha["filename"] = " ".join([i for i in cmd.split(" ") if i not in self.stopwords])
        return(alpha)

