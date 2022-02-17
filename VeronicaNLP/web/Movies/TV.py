from .MyMovies import Mymovie
import requests,os,webbrowser,sys
from VeronicaNLP.NLP.String_Search import String_Search
from VeronicaNLP.NLP.Convert_text_to_number import Replace

class TVSHOWS(object):
	"""docstring for TVSHOWS"""
	def __init__(self):
		self.movies = Mymovie()
		self.substitute = Replace()
		self.match = String_Search()
		self.browser = requests.session()
		self.stopwords = ["download","stream","of","the"]
		self.user_agent = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'}
	
	def open_url(self,url):
		html = self.browser.get(url,headers = self.user_agent,allow_redirects=False).content
		return(html)

	def get_true_name(self,name,data):
		filenames = [i.lower() for i in data.keys()]
		try:return(self.match.find_match(name,self.match.match_string,filenames)[1])
		except:return(None)
	
	def resume_download(self,fileurl, resume_byte_pos):
		resume_header = {'Range': 'bytes=%d-' % resume_byte_pos}
		return requests.get(fileurl, headers=resume_header, stream=True,  verify=False, allow_redirects=True)

	
	def format_to_value(self,fragment,fztvseries=True):
		"""fwd determines wether it's fztvseries or tvshows
		0 for fzseries 1 for tvshows"""
		if fztvseries:
			dbms = {"00":"0","01":"1","02":"2","03":"3","04":"4","05":"5","06":"6","07":"7","08":"8","09":'9'} 
		else:
			dbms = {"0":"00","1":"01","2":"02","3":"03","4":"04","5":"05","6":"06","7":"07","8":"08","9":'09'}
		tokens = fragment.lower().split()
		for i, token in enumerate(tokens):
			if token in dbms:tokens[i] = dbms[token]
		return ' '.join(tokens)

	def clean(self,text):
		text = text.replace("_"," ").split("-")
		if len(text)>2:
			ext = text[-1][-4:]
			filename = "-".join(text[:-1]).rstrip(" ")+ext
			return(filename)
		else:
			ext = text[-1][-4:]
			form = text[-1].strip(" ").split(" ")[0]
			filename = "".join(text[:-1]).rstrip(" ")+" - "+form.strip(" ")+ext
			return(filename)
			

	def seasons(self,text):
		text = text.replace("Season","S").replace("Episode","E").split(" S ")
		texta = text[1].split(" ")
		form = text[0]+"- "+"S"+"".join(texta)
		return(form)

	def extract_movie_data(self,cmd,fztvseries = True):
		"""
		extracts the needed info to download a series movie.
		which includes :
			filename: the series to download
			episode: the series episode to download
			season: the series season to download
		accepts the paremeters:
			cmd:a text which may the info is to be extracted from
			fztvseries:specifies if the fumction is to extract info specific for the fztvseries site or not
						if true the yes
						else ignore
		"""
		
		alpha,dictz,episodes = list(),dict(),list()
		cmd = self.format_to_value(self.substitute.text_to_number(cmd+" "),fztvseries).lower().split()
		lst1 = [i for i in cmd if i not in self.stopwords]
		try:
			data = " ".join(lst1)
			rec1 = data.split("from")[1]
			rec2 = [i for i in rec1.split() if i not in ["episode","to","from","season"]]
			for i in range(int(rec2[0]),int(rec2[1])+1):episodes.append("episode %i"%i)
		except:pass
		a = self.match.find_match("episode",self.match.match_string,lst1)
		b = self.match.find_match("season",self.match.match_string,lst1)   
		try:dictz["episode"] = a[1]+" "+lst1[a[0]+1]
		except:return("please specify episode to download")
		try:dictz["season"] = b[1]+" "+lst1[b[0]+1]
		except:return("sorry please specify the season to download")                    
		c = [i for i in " ".join(lst1).split() if i not in " ".join(dictz.values()).split()]
		Efilename = " ".join(c).split("from")
		try:filename = Efilename[0]
		except:filename = " ".join(c)
		if filename == "":
			try:filename = Efilename[1]
			except:return("sorry please specify the movie to download")   
		else:pass
		dictz["filename"] = filename
		dictz["format"] = "s%se%s"%(self.substitute.format_number(dictz["season"].split()[1]),self.substitute.format_number(dictz["episode"].split()[1]))
		alpha.append(dictz)
		try:
			for i in episodes[1:]:
				dictz = dict()
				i = self.format_to_value(i,fztvseries)
				dictz["episode"] = i
				dictz["season"] = b[1]+" "+lst1[b[0]+1]
				dictz["filename"] = filename
				dictz["format"] = "s%se%s"%(self.substitute.format_number(dictz["season"].split()[1]),self.substitute.format_number(dictz["episode"].split()[1]))
				alpha.append(dictz)
		except:pass
		return(alpha)

