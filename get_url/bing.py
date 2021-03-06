# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import os
import sys; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import requests
import json
import bs4 as bs



def generar_consulta_bing(q):    
    reload(sys)
    sys.setdefaultencoding('utf8')

    bing = []
    
    subscription_key = 'b705cc14560b4e52b59cf1f565287894'
    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"

    headers = {"Ocp-Apim-Subscription-Key" : subscription_key}

    for consulta in q:
        params  = {"q": consulta, "textDecorations":True, "textFormat":"HTML"}
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()
        data_response = json.dumps(search_results)
        data_decoded = json.loads(data_response)
        for x in range(0,10):
            bing.append(data_decoded["webPages"]["value"][x]["url"])

    return bing