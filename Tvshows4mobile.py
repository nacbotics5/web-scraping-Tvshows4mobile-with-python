#-*-coding:utf8;-*-
import re
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
from replace_text_with_number import sub
from string_matcher import string_match



class Tvshows4mobile(object):
    def __init__(self):
        self.match = string_match()
        self.math = sub()
        self.stopwords = ["download","stream","of","the"]
        self.download_url = "http://d11.tvshows4mobile.com/"
        self.url = "http://tvshows4mobile.com/search/list_all_tv_series"
        self.user_agent = {'User-agent': 'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)'}
    
    def crawl_link(self,url):
        pages = dict()
        html = requests.get(url,headers = self.user_agent).content
        BS = BeautifulSoup(html, "html.parser")
        for link in BS.findAll("a",href=re.compile("(.*?)/index.html")):
            if "href" in link.attrs:
                try:
                    file_link = link.attrs['href']
                    file_name = re.findall(r'>(.*?)</a>',str(link))[0]
                    pages[file_name.lower()] = file_link
                except Exception as e:
                    print(str(e))
        return(pages)


    def download_link(self,url):
        pages = dict()
        html = requests.get(url,headers = self.user_agent).content
        BS = BeautifulSoup(html, "html.parser")
        for link in BS.findAll("a",href=re.compile("(.*?)/download/")):
            if "href" in link.attrs:
                try:
                    file_link = link.attrs['href']
                    file_name = re.findall(r'>(.*?)</a>',str(link))[0]
                    pages[file_name] = file_link
                except Exception as e:
                    return(str(e))
        return(pages)


    def download_movie(self,name,data):
        filenames = [i.lower() for i in data.keys()]
        return(self.match.find_match(name,self.match.match_string,filenames)[1])
      
      
    def open_url(self,url):
        html = requests.get(url,headers = self.user_agent).content
        return(html)

    def get_next_page(self,url):
        pages = set()
        html = requests.get(url,headers = self.user_agent).content
        BS = BeautifulSoup(html, "html.parser")
        for link in BS.findAll("a",href=re.compile('(.*?)/page(.*)html')):
            if "href" in link.attrs:
                try:
                    file_link = link.attrs['href']
                    if "sort" not in file_link:
                        pages.add(file_link)
                except Exception as e:
                    return(str(e))
        return(pages)


    def run_download(self,cmd):
        L3 = dict()
        cmd = self._extract(cmd)
        print(cmd)
        try:data = self.crawl_link(self.url)
        except:return("no internet connection")
        
        try:L1 = self.download_movie(cmd["filename"],data) #gets the link to a tvseries        
        except:return("sorry please specify the season and episode to download")
        
        L2 = self.crawl_link(data[L1]) #gets the contents/season of the tvseries
        links = self.get_next_page(L2[cmd["season"]])
        links.add(L2[cmd["season"]])
        for link in links:
            L3.update(self.crawl_link(link)) #gets the episodes in the season of a tvseries
        link = self.download_link(L3[cmd["episode"]]) #gets the link to the file to download
        url = self.generate_download_link(cmd,link)
        
        print("downloading %s"%url[1])
        with open(url[1], 'wb') as filem:
            data = html = requests.get(url[0],stream=True,headers = self.user_agent)
            chunks = int(data.headers['Content-length'])/1024
            print("file size :",chunks)
            try:
                for chunk in data.iter_content(chunk_size = chunks):
                    filem.write(chunk)
                return("Done downloading!")
            except:
                return("no internet connection")

    def _extract(self,cmd):
        dictz = dict()
        cmd = self.math.text_to_number(cmd).lower().split()
        lst1 = [i for i in cmd if i not in self.stopwords]
                
        a = self.match.find_match("episode",self.match.match_string,lst1)
        b = self.match.find_match("season",self.match.match_string,lst1)
        
        try:
            dictz["episode"] = a[1]+" "+lst1[a[0]+1]
            dictz["season"] = b[1]+" "+lst1[b[0]+1]
        except:return("sorry please specify the season and episode to download")        
                
        c = [i for i in " ".join(lst1).split() if i not in " ".join(dictz.values()).split()]
        
        dictz["filename"] = " ".join(c)
        return(dictz)
    
    def generate_download_link(self,user,dicts):
        stopwords = [".3gp","HD"]
        tags = user
        filex = [i for i in dicts.keys() if not any(j for j in stopwords if j in i)][0]
        url1 = "%20".join(filex.split())
        filez = "".join(filex.split("-")[0])
        url2 = "%20".join(filez.split())+"/"
        
        a = tags["season"].title().split()
        d =list()
        d.append(a[0])
        d.append(a[1])
        url3 = "%20".join(d)
        
        url = self.download_url+url2+url3+"/"+url1+"?opwvc=1"
        return(url,filex)
    
    def can_process(self,cmd):
        if "download" in cmd:
            return(True)
        else:
            return(False)
    
    
