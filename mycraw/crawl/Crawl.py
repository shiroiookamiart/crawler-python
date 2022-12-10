import json, requests, logging
from types import NoneType
from typing import Dict
from bs4 import BeautifulSoup
from urllib.parse import urljoin

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO
)

class Crawl:
    def __init__(self, urls) -> None:
        self.myurl = urls

    def downloadUrl(self, url): #funcion para descargar todo el html de la pagina web
        return requests.get(url, timeout=30).text

    def htmlParser(self, url, html) -> None: #parseador del html y ordenador de informacion en el json
        soup = BeautifulSoup(html, "html.parser")
        response: Dict = {}
        for link in soup.find_all('meta'):
            if link.get("property") == "og:site_name":
                response["namesite"] = link.get("content") 
            elif link.get("property") == "og:url":
                response["urlsite"] = link.get("content") 
            elif link.get("property") == "og:title":
                response["title"] = link.get("content") 
            elif link.get("property") == "og:description":
                response["descriptions"] = link.get("content")
            elif link.get("property") == "og:image":
                response["img"] = link.get("content")

        for text in soup.find_all(id='top'):
            string = text.find("div").text
            response["texto"] = string

        response["urlsites"] = []
        response["urlsitesexternal"] = []

        for links in soup.find_all("a"):
            urls = links.get("href")
            if urls and urls.startswith('/'): 
                valid = False
                urlmod = urljoin(url, urls)
                for ur in response["urlsites"]:
                    if ur == urlmod:
                        valid = True
                if valid == False:
                    response["urlsites"].append(urlmod)
            else:
                if type(urls) != NoneType and type(urls) != None:
                    if("javascript:void(0);" in urls) == False:
                        if url in urls:
                            valid = False
                            for ur in response["urlsites"]:
                                if ur == urls:
                                    valid = True
                            if valid == False:
                                response["urlsites"].append(urls)        
                        elif urls != url and urls != "#" and urls != "":
                            valid = False
                            for u in response["urlsitesexternal"]:
                                if u == urls:
                                    valid = True
                            if valid == False:
                                response["urlsitesexternal"].append(urls)      

        self.saveInfoJson(response)

    def saveInfoJson(self, info) -> None: #funcion para guadar y generar el archivo json
        with open("./result.json", "w") as outfile:
            string_json = json.dumps(info)
            json.dump(string_json, outfile)
            logging.info(f'Crawling terminado.')
            outfile.close()
            rs = input("¿Deseas ver el resultado en pantalla?(S=si / N=no)\n")
            if rs == "S":
                logging.info(f'Espere PorFavor...')
                self.readJsonFile()

    def readJsonFile(self) -> None: #funcion para leer el archivo
        try:
            with open("./result.json") as jsonfile:
                data = json.load(jsonfile)
                jsonfile.close()
                data = json.loads(data)
                print(json.dumps(data, sort_keys=True, indent=4))
        except Exception as inst:
            logging.warning(f'Archivo json, no existe. Proceselo primero. {inst}\n')

    def crawl(self, url) -> None: #craw validacion 
        html = self.downloadUrl(url)
        if html != "":
            self.htmlParser(url, html)

    def run(self): #inicializador de la app
        if len(self.myurl) > 0:
            url = self.myurl[0]
            if url != "":
                logging.info(f'Crawling: {url}')
                try:
                    self.crawl(url)
                except Exception:
                    logging.exception(f'Crawling error: Fallo el crawl, verifique url: {url}')
        else:
            logging.info(f'Crawling error: No hay parametro en url')       
    pass