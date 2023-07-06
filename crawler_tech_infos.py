import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import numpy as np


def read_technical_information(url):
    # HTTP-Anfrage senden und den HTML-Inhalt erhalten
    response = requests.get(url)
    html_content = response.content

    # BeautifulSoup verwenden, um den HTML-Inhalt zu analysieren
    soup = BeautifulSoup(html_content, "html.parser")

    # Alle TabContent finden
    tab_contents = soup.find_all("div", {"class": "TabContent"})

    if tab_contents:
        # Leeres DataFrame erstellen
        df = pd.DataFrame()

        # Durch die Tabellen iterieren
        for tab_content in tab_contents:
            # Datenzeilen extrahieren
            rows = tab_content.find_all("div", {"class": "row"})

            # Leeres DataFrame erstellen
            data = [] 

            # Durch die Datenzeilen iterieren und Werte extrahieren
            for row in rows:
                left_col = row.find("div", {"class": "col-left"}).text.strip()
                right_col = row.find("div", {"class": "col-right"}).text.strip()
                data.append([left_col, right_col])

            # DataFrame erstellen
            temp_df = pd.DataFrame(data, columns=['Property', "Value"]).set_index(['Property'])
            # Das aktuelle DataFrame an das Gesamt-DataFrame anhängen
            df = pd.concat([df, temp_df])
        
        # Doppelte Spalten entfernen
        df1 = df.drop_duplicates(keep='first')
        # Nur die erste Instanz der doppelten Spalte behalten
        df1 = df1[~df1.index.duplicated(keep='first')]     
        df1 = df1.set_index(df1.index).transpose()
        return df1
    else:
        print("Keine TabContents gefunden.")

        
        
        
        
def get_website_title(url):
    # HTTP-Anfrage senden und den HTML-Inhalt erhalten
    response = requests.get(url)
    html_content = response.content

    # BeautifulSoup verwenden, um den HTML-Inhalt zu analysieren
    soup = BeautifulSoup(html_content, "html.parser")

    # Den Titel der Website extrahieren
    title = soup.title.string    
    return title

def add_website_titles(df):
    # Neue Spalte "Turbine" zum DataFrame hinzufügen
    df["Turbine"] = ""
    # Alle Links im DataFrame durchgehen
    df_technical_infos= pd.read_excel('data/technical_information.xlsx')
    if not('check' in df_technical_infos.columns):
        df_technical_infos['check'] = np.nan
    counter = 0
    progress_bar = tqdm(total=len(df), desc="Progress")
    while (counter/(len(df)-1) < 1):
        counter = 0
        for index, row in df_technical_infos.iterrows():
            if np.isnan(df_technical_infos['check'][index]):
                try:
                    link = row["Links"]
                    
                    # Den Titel der Website abrufen
                    title = get_website_title(link)
                    
                    # Technischen Infos abrufen
                    tech_infos=read_technical_information(link)
                    for column in tech_infos:
                        df_technical_infos.at[index, column] = tech_infos[column]['Value']
                    df_technical_infos.at[index, 'check'] = 1
            
                    # Den Titel in die entsprechende Zeile des DataFrames einfügen
                    df_technical_infos.at[index, "Turbine"] = title
                    df_technical_infos.to_excel('data/technical_information.xlsx')
                    progress_bar.update(1)
                except Exception as e:
                    print(e)
            else:
                progress_bar.update(1)
                counter += 1
    return df_technical_infos

# Beispiel DataFrame
df = pd.read_csv("data/links_wind-turbine-models.csv")

# Titel der Websites abrufen und in das DataFrame einfügen
df = add_website_titles(df)

# Ergebnis anzeigen
print(df)
