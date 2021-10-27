# -*- coding: utf-8 -*-

import requests, numpy, datetime, time, threading
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
#lista de barrios a scrappear
sublinks=["pisos-sant_pere_santa_caterina_la_ribera","pisos-ciutat_vella_la_barceloneta","pisos-eixample_sant_antoni",
                "pisos-can_baro","pisos-vallcarca_els_penitents","pisos-el_baix_guinardo","pisos-el_carmel","pisos-el_guinardo",
                "pisos-horta_guinardo_horta","pisos-la_clota","pisos-la_font_en_fargues","pisos-la_teixonera","pisos-la_vall_hebron",
                "pisos-montbau","pisos-sant_genis_dels_agudells","pisos-la_maternitat_sant_ramon","pisos-les_corts_barrio",
                "pisos-pedralbes","pisos-nou_barris_canyelles","pisos-nou_barris_ciutat_meridiana","pisos-el_turo_de_la_peira_can_peguera",
                "pisos-la_guineueta","pisos-la_prosperitat","pisos-la_trinitat_nova","pisos-nou_barris_porta","pisos-nou_barris_roquetes",
                "pisos-torre_baro","pisos-vallbona","pisos-verdun","pisos-vilapicina_la_torre_llobeta","pisos-baro_de_viver",
                "pisos-la_vila_de_gracia","pisos-gracia_la_salut","pisos-el_coll","pisos-el_camp_en_grassot_gracia_nova","pisos-el_bon_pastor",
                "pisos-el_congres_els_indians","pisos-sant_andreu_la_sagrera","pisos-la_trinitat_vella","pisos-sant_andreu_navas","pisos-sant_andreu_barrio",
                "pisos-diagonal_mar_el_front_maritim_del_poblenou","pisos-el_besos_el_maresme","pisos-el_camp_de_arpa_del_clot","pisos-el_clot",
                "pisos-el_parc_la_llacuna_del_poblenou","pisos-sant_marti_el_poblenou","pisos-sant_marti_la_verneda_la_pau",
                "pisos-la_vila_olimpica_del_poblenou","pisos-provencals_del_poblenou","pisos-sant_marti_de_provencals",
                "pisos-el_poble_sec","pisos-sants_montjuic_hostafrancs","pisos-sants_montjuic_la_bordeta","pisos-la_font_de_la_guatlla",
                "pisos-la_marina_del_port_parc_de_montjuic", "pisos-la_marina_del_prat_vermell_zona_franca_port","pisos-sants_montjuic_sants",
                "pisos-sants_badal","pisos-el_putxet_el_farro","pisos-les_tres_torres","pisos-sant_gervasi_galvany","pisos-sant_gervasi_la_bonanova",
                "pisos-sarria_sant_gervasi_sarria","pisos-vallvidrera_el_tibidabo_les_planes", "pisos-la_sagrada_familia","pisos-la_nova_esquerra_de_eixample",
                "pisos-antiga_esquerra_de_eixample","pisos-el_fort_pienc","pisos-el_raval","pisos-el_barri_gotic","pisos-la_dreta_de_eixample"]

#sublinks=["pisos-barcelona","pisos-madrid"]
code=0
contracts=["venta","alquiler"]
results=pd.DataFrame(columns=["codigo","contrato","link","barrio","titulo","precio","habitaciones","banyos","metros"])
#%%
for contract in contracts:
    for sublink in sublinks:
        run=True
        once=True
        p=1
        while(run):
            if (once):
                page=""
                once=False
            else:
                p=p+1
                page=f"{p}/"
            link =f"https://www.pisos.com/{contract}/{sublink}/{page}"
            page = requests.get(link)
            
            soup = BeautifulSoup(page.content, 'html.parser')
            #detecta si el numero de pagina a la que vamos a entrar no tiene resultados de nuestro barrio
            try:
                if (soup.find("div",class_="u-hide u-show--s1024").get_text()=="Si quieres obtener resultados, modifica tu búsqueda."):break;
            except:
                pass
            print(f"Extrayendo información de la página {link}")
            #buscamos todos los anuncios de la pag
            listParents=soup.find_all("div",class_="ad-preview__info")
            for parent in listParents:
                #Por cada anuncio sacamos el nombre del piso y el barrio
                neighborhood=parent.findChildren("p",class_="p-sm")[0].get_text()
                title=parent.findChildren("a",class_="ad-preview__title")[0].get_text()
                #Sacamos el precio, el try except es porque a veces no hay precio y al castear el int da error
                try:
                    price=int(parent.findChildren("span",class_="ad-preview__price")[0].get_text().strip("\n €").replace(".",""))
                except:
                    price=None
                #sacamos la info
                infos=parent.findChildren("p",class_="ad-preview__char p-sm")
                #Iniciamos valores a null porque si no existe uno lo queremos vacio en la bd
                room=None
                bath=None
                meters=None
                #En finción de los posibles sufijos de la info la clasifica, esta en un try except porque a veces
                #info es una sola palabra y al hacer split() no devuelve los dos valores que espera y peta
                for info in infos:
                    try:
                        data,sufix =info.get_text().split()
                        if (sufix=="baño"):
                            bath=int(data)
                        elif (sufix=="baños"):
                            bath=int(data)
                        elif(sufix=="m²"):
                            meters=int(data)
                        elif(sufix=="habs."):
                            room=int(data)
                        elif(sufix=="hab."):
                            room=int(data)
                    except:
                        next
                results.loc[len(results)]=[code,contract,link,neighborhood,title,price,room,bath,meters]
                #Asignamos un codigo único a cada casa porque el nombre del anuncio a veces se repite, no es unívoco
                code=code+1
        #hacermos un guardado por cada barrio por si acaso hay algun problema tener algunos datos
    results.to_csv(f"barcelona_house_pricing{datetime.date.today().strftime('%d_%m_%y')}.csv", index=False)