#-*-coding:utf8;-*-
import re
from .TV import TVSHOWS
from bs4 import BeautifulSoup


class Tvshows4mobile(TVSHOWS):
    def __init__(self):
        super(Tvshows4mobile, self).__init__()
        self.Movie_Set = self.movies.create()
        self.stopwords = ["download","stream","of","the"]   
        self.url = "https://tvshows4mobile.com/search/list_all_tv_series"
        self.recent_updates = "https://tvshows4mobile.com/search/recently_added"

    def crawl_link(self,url,pattern="(.*?)"):
        pages = dict()
        html = self.open_url(url)
        BS = BeautifulSoup(html, "html.parser")
        for link in BS.findAll("a",href=re.compile(pattern)):
            if "href" in link.attrs:
                try:
                    file_link = link.attrs['href']
                    file_name = re.findall(r'>(.*?)</a>',str(link))[0]
                    pages[file_name.lower()] = file_link
                except Exception as e:print(str(e))
        return(pages)

    def get_next_page(self,url):
        pages = set()
        try:html = self.open_url(url)
        except Exception as e:return("no internet connection check your conection and try again")
        BS = BeautifulSoup(html, "html.parser")
        for link in BS.findAll("a",href=re.compile('(.*?)/page(.*)html')):
            if "href" in link.attrs:
                try:
                    file_link = link.attrs['href']
                    if "sort" not in file_link:pages.add(file_link)
                except Exception as e:return(str(e))
        return(pages)
    
    def check_updates(self):
        """ returns a list of the latest movies in tvshows4mobile website """
        result = []
        try:html = self.open_url(self.recent_updates)
        except Exception as e:return("no internet connection check your conection and try again")
        BS = BeautifulSoup(html, "html.parser")
        movie_names = re.findall(r'<b>(.*?)]',str(BS))
        for movie in movie_names:
            movie_list = "".join(movie.split("[")[0])
            movie_list = re.sub("</b>","",movie_list)
            data =re.sub("-","",movie_list)
            result.append(data)
        return(result)
    
    def notify(self):
        result = []
        my_movies = list(set([i["movie_name"] for i in self.Movie_Set]))
        movies = list(set([i["storage_name"].lower().strip(" ") for i in self.Movie_Set]))
        data = self.check_updates()
        for i in my_movies:
            for j in data:
                if i.lower() in j.lower():result.append(self.seasons(j).lower())      #here we get the new episodes of the series we are following
                else:pass
        try:others = list(set([self.seasons(i.split("-")[0]) for i in data if self.seasons(i.split("-")[0]).lower() not in movies]))
        except:pass
        if type(data) is str:return(data)
        d = [i.lower().strip(" ") for i in movies]
        result = [i for i in result if i.lower().strip(" ") not in d]
        missed_movies = self.get_missed()
        text = "\nMOVIE UPDATE FROM TVSHOWS4MOBILE\nHERE ARE UPDATES FROM MOVIES YOU ARE CURRENTLY WATCHING ::\n\n"+",\n".join(result)
        text2 = "\nMOVIE UPDATE FROM TVSHOWS4MOBILE\nNO EPISODE OF MOVIES YOU ARE FOLLOWING ARE OUT.\n\nBUT HERE ARE UPDATES FROM MOVIES THAT MIGHT INTEREST YOU::\n"+",\n".join(others)
        text3 = "HERE AS SOME TVSERIES EPISODES YOU MIGHT HAVE MISSED ::\n\n"+",\n".join(missed_movies)
        
        if " ".join(result) == "":return(text3+text2)
        return(text3+text)

    def check_movie(self,text):
        text = text.split()
        stopwords = list(set("is a new episode of out new episode of don come out is the episode of out check wether new episode don come out check if a new episode of  is out".split()))
        try:new_tvshows = [self.seasons(i).lower() for i in self.check_updates()]
        except:return("no internet connection check your conection and try again")
        movies = list(set([i["storage_name"].lower().strip(" ") for i in self.Movie_Set]))
        tvshowsmovies = [i for i in new_tvshows if i not in movies]
        text = " ".join([i for i in text if i not in stopwords])
        try:text = self.match.find_match(text,self.match.match_string,tvshowsmovies)[1]
        except:return("No not yet")
        if text != None:return("Yeah %s is out"%text)

    def return_missed_episodes(self,cmd):
        L3 = dict()
        try:data = self.crawl_link(self.url,pattern="(.*?)/index.html")
        except:return("no internet connection check your conection and try again")
        
        try:L1 = self.get_true_name(cmd["filename"],data) #gets the link to a tvseries        
        except:return("sorry please specify the season and episode to download")
        try:L2 = self.crawl_link(data[L1],pattern="(.*?)/index.html") #gets the contents/seasons of the tvseries
        except:return("no such tvseries as %s"%cmd["filename"])
        try:
            links = self.get_next_page(L2[cmd["season"]])
            links.add(L2[cmd["season"]])
        except KeyError:
            return("%s is not upto %s"%(cmd["filename"],cmd["season"]))
        for link in links:
            L3.update(self.crawl_link(link,pattern="(.*?)/index.html")) #gets the episodes in the season of a tvseries
        L3_list = sorted(list(L3.keys()))
        return(L3_list)

    def get_missed(self):
        listx = list()
        data = self.movies.get_em_format()
        x = [self.extract_movie_data(i)[0] for i in data]
        for series in x:
            result = self.return_missed_episodes(series)
            if type(result) is str:pass
            else:
                missed_episodes = self.movies.find_missed_episodes(series["episode"],result)
                try:
                    for episodes in missed_episodes:
                        listx.append("%s %s %s"%(series["filename"],series["season"],episodes))
                except TypeError:pass 
        return(listx)
    
    def run_download(self,cmd):
        print(cmd)
        L3 = dict()
        try:data = self.crawl_link(self.url,pattern="(.*?)/index.html")
        except:return("no internet connection check your conection and try again")
        
        try:L1 = self.get_true_name(cmd["filename"],data) #gets the link to a tvseries        
        except:return("sorry please specify the season and episode to download")
        try:L2 = self.crawl_link(data[L1],pattern="(.*?)/index.html") #gets the contents/seasons of the tvseries
        except:return("no such tvseries as %s"%cmd["filename"])
        try:
            links = self.get_next_page(L2[cmd["season"]])
            links.add(L2[cmd["season"]])
        except KeyError:return("%s is not upto %s"%(cmd["filename"],cmd["season"]))
        for link in links:
            L3.update(self.crawl_link(link,pattern="(.*?)/index.html")) #gets the episodes in the season of a tvseries
        L3_list = L3.keys()
        try:
            epis = self.match.find_match(cmd["episode"][-2:],self.match.match_string,L3_list)[1]
        except:
            return("%s %s is not upto %s"%(cmd["filename"],cmd["season"],cmd["episode"]))
        link = self.crawl_link(L3[epis],pattern="(.*?)/download/") #gets the link to the file to download
        url = list(link.values())[0]
        name = list(link.keys())[0].split("(")[0]
        return("FILENAME %s\nLINK :%s"%(name,url))
        
