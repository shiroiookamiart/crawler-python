#paquete de script crawl desarrollado por david beltran ingeniero e ilustrador comic
#web de test http://dluxstudios.co/ - http://localhost.co/webscrapy/ - https://theporndude.com

import os
from crawl.Crawl import Crawl

if __name__ == "__main__":
    urls = ["https://theporndude.com/"]  #pagina a setear, debe estar dentro de los []
    rs = input("¿Deseas procesar la pagina {}?(S=si / N=no)\n".format(urls[0]))
    if rs == "S":
        Crawl(urls).run()
    else:    
        rs2 = input("¿Deseas ver el resultado del archivo en pantalla? (S=si / N=no) \n")
        if rs2 == "S":
            Crawl(urls).readJsonFile()