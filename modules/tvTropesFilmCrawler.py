from bs4 import BeautifulSoup
import pandas as pd
import requests
from time import sleep

counter = 0

def __init__(self):
    from bs4 import BeautifulSoup
    import pandas as pd
    import requests
    counter = 0
    
def GetSubPageTropes(pageAddress):
    page = requests.get(pageAddress)
    soup = BeautifulSoup(page.content, 'html.parser')
    aTags = list()

    for ultag in soup.find_all('ul'):
        for litag in ultag.find_all('li'):
            for atag in litag.find_all('a'):
                if('/Main/' in atag['href'] and '/tvtropes.org/' in atag['href']):
                    if(atag['href'].split('/')[-1] == atag.text.replace(' ', '')):
                        aTags.append(atag)
    return aTags

def GetTropes(pageAddress):
    sleep(5)
    page = requests.get(pageAddress)
    soup = BeautifulSoup(page.content, 'html.parser')

    aTags = list()
    subPageLinks = list()
    subPages = False

    for ultag in soup.find_all('ul'):
        for litag in ultag.find_all('li'):
            for atag in litag.find_all('a'):
                if('/Main/' in atag['href'] and '/tvtropes.org/' in atag['href']):
                    if(atag['href'].split('/')[-1] == atag.text.replace(' ', '')):
                        aTags.append(atag)
                if('Trope' in atag['href'] and 'To' in atag['href']):
                    aTags = aTags + GetSubPageTropes(atag['href'])

    name = pageAddress.split('/')[-1]
    global counter
    counter += 1
    print(str(counter) +") " + name + ": " + str(len(aTags)) + " tropes")
    return aTags

def GetFilmList():
    filmsList = list()
    address = 'http://tvtropes.org/pmwiki/pmwiki.php/Main/'
    lists = ['ScienceFictionFilms', 'MysteryAndDetectiveFilms', 'MilitaryAndWarfareFilms', 'IndexOfFilmWesterns', 'HorrorFilms', 'FantasyFilms', 'AnimatedFilms']
    
    for category in lists:
        page = requests.get(address + category)
        soup = BeautifulSoup(page.content, 'html.parser')
        for ultag in soup.find_all('ul'):
            for litag in ultag.find_all('li'):
                for emtag in litag.find_all('em'):
                    for atag in emtag.find_all('a'):
                        if(atag['href'].split('/')[-1] == atag.text.replace(' ', '')):
                            filmsList.append(atag)
    return filmsList

def GenerateDataFrame():
    columns = ['name', 'tvTropesAddress', 'tropeCount', 'runTime']

    films_df = pd.DataFrame(columns=columns)
    filmNames = pd.Series()
    filmAddresses = pd.Series()
    tropeCounts = pd.Series()
    runTime = pd.Series()

    filmsList = GetFilmList()
    for film in filmsList:
        filmNames = filmNames.append(pd.Series(film.text))
        filmAddresses = filmAddresses.append(pd.Series(film['href']))
        tropeCounts = tropeCounts.append(pd.Series(0))
        runTime = runTime.append(pd.Series(0))

    films_df = pd.concat([filmNames, filmAddresses, tropeCounts, runTime], axis=1)
    films_df.columns = columns
    films_df = films_df.reset_index(drop=True)
    print(len(films_df))
    films_df = films_df.drop_duplicates()
    print(len(films_df))
    #return films_df
    films_df.to_csv('tropesData.csv',  encoding='utf-8')

def TestCrawl():
    df = pd.read_csv('tropesData.csv')
    testDf = df
    testDf['tropeCount'] = testDf['tvTropesAddress'].apply(lambda x: len(GetTropes(x)))
    # print(testDf)
    testDf.to_csv('tropesData.csv', encoding='utf-8')

def DisneyCrawl():
    df = pd.read_csv('disneyTropesData.csv')
    #testDf = df[:6]
    df['tropeCount'] = df['tvTropesAddress'].apply(lambda x: len(GetTropes(x)))
    # print(testDf)
    #for index, row in df.iterrows():
    #    if(row['tropeCount'] == 0):
    #        row['tropeCount'] = len(GetTropes(row['tvTropesAddress']))
        #if(index % 5 == 0):
            #df.to_csv('disneyTropesData.csv', encoding='utf-8')
    df.to_csv('tropesData.csv', encoding='utf-8')

def GenerateDisneyDataFrame():
    filmsList = list()
    address = 'http://tvtropes.org/pmwiki/pmwiki.php/Franchise/DisneyAnimatedCanon'
    
    page = requests.get(address)
    soup = BeautifulSoup(page.content, 'html.parser')
    divs = soup.find("div", {"id": "folder0"})
    for oltag in divs.find_all('ol'):
        for litag in oltag.find_all('li'):
            for emtag in litag.find_all('em'):
                for atag in emtag.find_all('a'):
                    filmsList.append(atag)

    print(filmsList)
    print(len(filmsList))

    columns = ['name', 'tvTropesAddress', 'tropeCount', 'runTime']

    films_df = pd.DataFrame(columns=columns)
    filmNames = pd.Series()
    filmAddresses = pd.Series()
    tropeCounts = pd.Series()
    runTime = pd.Series()

    #filmsList = GetFilmList()
    for film in filmsList:
        filmNames = filmNames.append(pd.Series(film.text))
        filmAddresses = filmAddresses.append(pd.Series(film['href']))
        tropeCounts = tropeCounts.append(pd.Series(0))
        runTime = runTime.append(pd.Series(0))

    films_df = pd.concat([filmNames, filmAddresses, tropeCounts, runTime], axis=1)
    films_df.columns = columns
    films_df = films_df.reset_index(drop=True)
    print(len(films_df))
    # films_df.drop_duplicates(keep=False)
    print(len(films_df))
    #return films_df
    films_df.to_csv('disneyTropesData.csv',  encoding='utf-8')
