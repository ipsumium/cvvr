""" 
Implementare api anaf - https://static.anaf.ro/static/10/Anaf/Informatii_R/doc_WS_V4.txt

Exemplu input

listacui=[37943096, 15381132, 1594483, 15560715, 22, 1345563, 14444712,550152,37960402]  # lista coduri cui
data=['2018-02-14','2018-02-14','2018-02-14','2018-02-14','2015-02-14','2017-02-14','2016-02-14','2016-02-14','2018-02-14'] #data la care se doresc informatiile despre firma
vcui=[True,True,True,True,False,True,True,True,True] #din cauza ca api-ul nu functioneaza cu prea multe coduri cui gresite trebuie limitat requestul 
#la cui-urile valabile din listacui, vcui True inseamna cui valabil, la final se va returna ERR pentru cui invalid din listacui

ls,js = verificare_tva(listacui, data,vcui)

Exemplu output

ls = ['VIAFORM X S.R.L.', 'AMG CERT SRL', 'REGIO IMPEX SRL', 'OPTOTEL COM SRL', 'ERR', 'ADDECO SRL', 'ELIT S.R.L.', 'COVALACT SA', 'RENDERLIFE S.R.L.']
js = [False, True, True, True, 'ERR', True, True, True, False]
"""
import json

import requests

url = 'https://webservicesp.anaf.ro/PlatitorTvaRest/api/v4/ws/tva'
headers = {"Content-Type": "application/json"}


def verificare_tva(listacui, data, vcui):
    data_api = [{'cui': val, 'data': data[index]} for index, val in enumerate(listacui) if vcui[index]]
    r = requests.post(url, json=data_api, headers=headers)
    print("ANAF-Status Cerere TVA", r.status_code, r.reason)
    lista_raspuns = json.loads(r.content)['found']
    nume_anaf = [i['denumire'] for i in lista_raspuns]
    status_tva = [i['scpTVA'] for i in lista_raspuns]
    nn_anaf = []
    tva_anaf = []
    ic = 0
    for index, val in enumerate(vcui):
        if val:
            nn_anaf.append(nume_anaf[ic])
            tva_anaf.append(status_tva[ic])
            ic += 1
        else:
            nn_anaf.append('ERR')
            tva_anaf.append('ERR')
    return nn_anaf, tva_anaf


# r.__dict__ afiseaza caracteristici obiect

def main():
    listacui = [37943096, 15381132, 1594483, 15560715, 22, 1345563, 14444712, 550152, 37960402]
    data = ['2018-02-14', '2018-02-14', '2018-02-14', '2018-02-14', '2015-02-14', '2017-02-14', '2016-02-14',
            '2016-02-14', '2018-02-14']
    vcui = [True, True, True, True, False, True, True, True, True]
    ls, js = verificare_tva(listacui, data, vcui)
    print(ls, '\n', js)


if __name__ == "__main__":
    main()
    input("Press Enter to exit!")    
