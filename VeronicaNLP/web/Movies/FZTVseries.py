#-*-coding:utf8;-*-
import re
from .TV import TVSHOWS
from bs4 import BeautifulSoup


class FZTV(TVSHOWS):
    def __init__(self):
        super(FZTV, self).__init__()
        self.Movie_Set = self.movies.create()
        self.stopwords = ["download","stream","of","the"]        
        self.recent_updates = "https://fztvseries.mobi/fupdates.php"
        self.search = "https://fztvseries.mobi/search.php?search=%s&beginsearch=Search&vsearch=&by=series"
        
    def crawl_link(self,url,pattern=""):
        pages = dict()
        html = self.open_url(url)
        BS = BeautifulSoup(html, "html.parser")
        for link in BS.findAll("a",href=re.compile("(.*?)")):
            if "href" in link.attrs:
                try:
                    file_link = "https://fztvseries.mobi/"+link.attrs['href']
                    file_name = re.findall(pattern,str(link))[0]
                    pages[file_name.lower()] = file_link
                except Exception as e:pass
        return(pages)

    def crawl_episodes_link(self,url,pattern=""):
        pages = dict()
        html = self.open_url(url)
        BS = BeautifulSoup(html, "html.parser")
        for link in BS.findAll("a",href=re.compile("(.*?)")):
            if "href" in link.attrs:
                try:
                    file_link = "https://fztvseries.mobi/"+link.attrs['href']+"&ftype=2"
                    file_name = re.findall(pattern,str(link))[0]
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

    def notify(self):
        result = []
        my_movies = list(set([i["movie_name"] for i in self.Movie_Set]))
        movies = list(set([i["storage_name"] for i in self.Movie_Set]))
        data = self.check_updates()
        for i in my_movies:
            for j in data:
                if i in j:result.append(j)      #here we get the new episodes of the series we are following
                else:pass
        others = list(set([i.split("-")[0] for i in data if i.split("-")[0].strip(" ") not in my_movies]))
        if type(data) is str:return(data)
        d = [i.lower().strip(" ") for i in movies]
        result = list(set([i for i in result if i.lower().strip(" ") not in d]))
        text = "MOVIE UPDATE FROM FZTVSERIES\nHERE ARE UPDATES FROM MOVIES YOU ARE CURRENTLY WATCHING::\n\n"+",\n".join(result)
        text2 = "MOVIE UPDATE FROM FZTVSERIES\nNO EPISODE OF MOVIES YOU ARE FOLLOWING ARE OUT.\nBUT HERE ARE UPDATES FROM MOVIES THAT MIGHT INTEREST YOU::\n\n"+",\n".join(others)
        if others == []:return("No current movies from FZTVSERIES\n\n")
        elif " ".join(result) == "":return(text2)
        else:return(text)

    def check_movie(self,text):
        text = text.split()
        updates = self.check_updates()
        stopwords = list(set("is a new episode of out new episode of don come out is the episode of out check wether new episode don come out check if a new episode of  is out".split()))
        new_fztv = [i.lower() for i in updates]
        if type(updates) == str:return(updates)
        movies = list(set([i["storage_name"].lower().strip(" ") for i in self.Movie_Set]))
        Fztvmovies = [i for i in new_fztv if i not in movies]
        text = " ".join([i for i in text if i not in stopwords])
        try:text = self.match.find_match(text,self.match.match_string,Fztvmovies)[1]
        except:return("No not yet")
        if text != "":return("Yeah %s is out"%text)

    
    def return_missed_episodes(self,cmd):
        ##################################################################################################
        text = "+".join(cmd["filename"].split())
        url = self.search%text
        try:data = self.crawl_link(url,pattern=r'<b>(.*?)</b>')
        except:return("no internet connection check your conection and try again")
        ##################################################################################################
        L1 = self.get_true_name(cmd["filename"],data) #gets the name the file was used to save the file on fzseries   
        try:L2 = self.crawl_link(data[L1],pattern=r'<span itemprop="name">(.*?)</span></a>') #gets the seasons of the tvseries
        except:return("no such tvseries as %s"%cmd["filename"])
        try:
            L3 = self.crawl_episodes_link(L2[cmd["season"]],pattern=r'id="(.*?)" style=')#gets the season and its contents to download the file from
            L3_list = L3.keys() #returns a result of the form"xena warrior princess - s04e22 - dj vu all over again"
        except KeyError:
            return("%s is not upto %s"%(cmd["filename"],cmd["season"]))
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
        ##################################################################################################
        text = "+".join(cmd["filename"].split())
        url = self.search%text
        try:data = self.crawl_link(url,pattern=r'<b>(.*?)</b>')
        except:return("no internet connection check your conection and try again")
        ##################################################################################################
        L1 = self.get_true_name(cmd["filename"],data) #gets the name the file was used to save the file on fzseries   
        try:L2 = self.crawl_link(data[L1],pattern=r'<span itemprop="name">(.*?)</span></a>') #gets the seasons of the tvseries
        except:return("no such tvseries as %s"%cmd["filename"])
        try:
            L3 = self.crawl_episodes_link(L2[cmd["season"]],pattern=r'id="(.*?)" style=')#gets the season and its contents to download the file from
            L3_list = L3.keys() #returns a result of the form"xena warrior princess - s04e22 - dj vu all over again"
        except KeyError:
            return("%s is not upto %s"%(cmd["filename"],cmd["season"]))
        struct_filename = str(cmd["format"])
        try:
            episode = self.match.find_match(struct_filename,self.match.match_string,L3_list)[1] #matches the season and episode to download the file
            L4 = self.crawl_link(L3[episode],pattern=r'>(.*?)</a>') #gets the link to the file to download
        except:return("%s %s is not upto %s"%(cmd["filename"],cmd["season"],cmd["episode"]))
        L4_list = L4.keys()
        file = self.match.find_match(episode,self.match.match_string,L4_list)[1] #matches the season and episode to download the file
        link = self.crawl_link(L4[file],pattern=r'>(.*?)</a>') #gets the link to the file to download
        link = link['download link 1'].replace("https://fztvseries.mobi/","")
        filename = self.clean(link.split("/rlink/")[1])
        return("FILENAME %s\nLINK :%s"%(filename,link))
