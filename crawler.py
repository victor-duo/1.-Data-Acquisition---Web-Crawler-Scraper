import requests
import json
from bs4 import BeautifulSoup

def crawler(seed):
    frontier=[seed]
    crawled=[]
    i=0
    infoGlob={}
    info=[]
    taille=[]
    while frontier:
        size=len(frontier)
        page=[frontier[i]].pop()
        i=i+1
        if(i==size and i!=1):
            break
        try:
            print('Crawled:'+page)
            source = requests.get(page, headers={'User-Agent':'Mediapartners-Google'}).text
            soupHTML=BeautifulSoup(source,"html5lib")
            soup=BeautifulSoup(source,"xml")
            links=soup.findAll("loc")
            author=soupHTML.findAll('span',itemprop="name")
            headline=soupHTML.findAll('h1')
            date=soupHTML.findAll('time',itemprop="datePublished")
            #print(len(author),len(headline),len(date))
            taille.append([len(author),len(headline),len(date)])
            infoArticle=[]
            if(len(author)!=0 and len(headline)!=0 and len(date)!=0):
                infoArticle.append(author[0].text)
                headlineText=headline[0].text
                headlineText=headlineText.replace('\n','')
                infoArticle.append(headlineText)
                dateText=date[0].text
                dateText=dateText.replace('\xa0',' ')
                dateText=dateText.replace('\n','')
                infoArticle.append(dateText)
            elif(len(author)==0 and len(headline)!=0 and len(date)!=0):
                headlineText=headline[0].text
                headlineText=headlineText.replace('\n','')
                infoArticle.append(headlineText)
                dateText=date[0].text
                dateText=dateText.replace('\xa0',' ')
                dateText=dateText.replace('\n','')
                infoArticle.append(dateText)
            info.append(infoArticle)
            if page not in crawled:
                for link in links:
                    linkText=link.text
                    if("jpg" not in linkText and "png" not in linkText and "live" not in linkText):
                        frontier.append(link.text)
                crawled.append(page)
        except Exception as e:
           print(e)
    print(len(frontier))
    infoGlob["article"]=info
    jSoninfoGlob=json.dumps(infoGlob, ensure_ascii=False)
    with open('C://Users//R510J//Desktop//Travail//Inge//Algorithme//Python//data.json', 'w') as f:
        json.dump(jSoninfoGlob, f, ensure_ascii=False)
    return crawled
crawler('https://www.theguardian.com/sitemaps/news.xml')

json_file=open('C://Users//R510J//Desktop//Travail//Inge//Algorithme//Python//data.json','r')
data = json.load(json_file) #load for loading from a file, loads for loading from a string
data1=json.loads(data)
#print(data1["article"])
json_file.close()
