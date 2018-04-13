# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pattern.web import download
from BeautifulSoup import BeautifulSoup
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

def generar_consulta_intelligo(consultas):
    urls = []
    # Para arreglar problema de la variable twtrr
    user_agent = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) " +
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"
    )

    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = user_agent

    driver = webdriver.PhantomJS(desired_capabilities=dcap)
    driver.set_script_timeout(15)
    driver.set_window_size(1280, 1024)
    # driver.maximize_window()
    for consulta in consultas:
        driver.get("http://patentes.explora-intelligo.info/index.html?setLng=en")
        ids = driver.find_element_by_id('btnCloseHelp')
        ids.click()
        driver.find_element_by_id('tbQuery').send_keys(consulta)
        driver.find_element_by_id('btnQuery').click()
        try:
            element = WebDriverWait(driver, 30).until(
                                                      EC.presence_of_element_located((By.ID, "svg_graph"))
                                                      )
        finally:
            html = driver.find_element_by_id('docs')
            contenido = html.get_attribute('innerHTML')
            soup = BeautifulSoup(contenido)
            urls.append(get_url(soup))

    urls_intelligo = []
    for url_clave in urls:
        for url in url_clave:
            urls_intelligo.append(url)
    driver.quit()
    return urls_intelligo


def get_url(soup):
    urls = []
    contador = 0
    for a in soup.findAll('a'):
                html = download(a['href'], unicode=True)
                soupEspaceNet = BeautifulSoup(html)
                urlDescription = soupEspaceNet.findAll('a', {"class": "publicationLinkClass"})
                for url in urlDescription:
                    urlEspace = "http://worldwide.espacenet.com/" + str(url['href'])
                    urlEspace = urlEspace.replace("biblio","description")
                    urls.append(urlEspace)
                    contador = contador + 1
                    if (contador > 9 ) :
                        return urls
    return urls
