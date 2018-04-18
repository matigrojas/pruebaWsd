# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from BeautifulSoup import BeautifulSoup


def generar_consulta_excite(consultas):
    urls = []
    for consulta in consultas:
        driver = webdriver.PhantomJS()
        driver.set_script_timeout(10)
        driver.maximize_window()
        consulta = consulta.replace(" ","+")
        driver.get("http://msxml.excite.com/info.xcite/search/web?fcoid=417&fcop=topnav&fpid=27&q="+str(consulta))
        try:
                element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "resultsMain")))
        finally:
            ids = driver.find_element_by_id('resultsMain')
            soup = BeautifulSoup(ids.get_attribute('innerHTML'))
            for url in soup.findAll('a',{"class":"resultTitle"}):
                una_url = str(url['href'])
                una_url = una_url.split("%26du%3d")
                aux = una_url[1].split("%26hash");
                url =  aux[0].replace("%253a",":").replace("%252f","/")
                if 'https' not in url:
                    url = "http://" + str(url)
                urls.append(url)
            driver.quit()
    return urls
