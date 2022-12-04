import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import base64

def extractDataset(docpath):
    try:
        # fill dataset
        table = pd.read_csv(docpath)        

        # connect to PostgreSQL server        
        tab2 = pd.DataFrame(table)
        tab2 = tab2.set_index('NationalTeam')       
        
        return tab2
    except:
        return print("Error occured with the dataset.")
    
def path_to_image_html(path): 
    source = '<img src="'+ path + '" width="50" >'
    return source


def get_thumbnail(path):
    i = Image.open(path)
    i.thumbnail((40, 40), Image.LANCZOS)
    return i

def image_base64(im):
    if isinstance(im, str):
        im = get_thumbnail(im)
    with BytesIO() as buffer:
        im.save(buffer, 'png')
        return base64.b64encode(buffer.getvalue()).decode()

def image_formatter(im):
    return f'<img src="data:image/png;base64,{image_base64(im)}">'
    
def getAllCountriesFlags(url, countriesdictmap, show='all'):
    
    try:
    
        data = []        
        page = requests.get(url)
        soup = BeautifulSoup(page.text, parser='lxml', features="lxml")
        table = soup.find_all( "table", {"class":"two-column td-image"} )

        for tabi in table: 
            table_body = tabi.find('tbody')

            rows = table_body.find_all('tr')
            for row in rows:
                cols = row.find_all('td') 

                t = row.find_all('img')
                cols1 = [ele.get('src') for ele in t] 
                cols = [ele.text.strip() for ele in cols]
                datas1 = [ele for ele in cols]
                datas2 = [ele for ele in cols1]
                res = [*datas1, *datas2]
                data.append(res) # Get rid of empty values   

        tab1 = pd.DataFrame(data)
        tab1.columns = tab1.iloc[0]
        tab1 = tab1[1:]
        tab1 = tab1.dropna()
        ColumnNames = {"A":"Country",None:"FlagPath"}            
        tab1 = tab1.rename(columns=ColumnNames)        
        tab1['FlagPathWeb'] = tab1['FlagPath'].apply(lambda x: "{}{}".format('https://www.countries-ofthe-world.com/', x))
        tab1['Country'] = tab1['Country'].str.replace('\W', '', regex=True)        
        tab1['CountryLower'] = tab1['Country'].str.lower()
        #tab1['countryid'] = tab1['CountryLower'].map(natTeams.set_index('NationalTeamNameLower')['NationalTeamId'])
        tab1['countryid'] = tab1['CountryLower'].map(countriesdictmap)
        tab1['countryid'] = tab1['countryid'].fillna(0)
        tab1['countryid'] = tab1['countryid'].astype(int)
        tab1 = tab1.set_index('countryid')
        
        if show == 'web':
            showcols = ["FlagPathWeb"]
            
        elif show == 'local':
            showcols = ["FlagPath"]
            
        else:
            showcols = ["Country","FlagPath","FlagPathWeb"]
        
        tab1 = tab1[showcols]

        return tab1
    except:
        return print("Error occured with the dataset.")

class Teams:    
    
    def __init__(self, teamid, teamname, link):
        self.teamid = teamid
        self.teamname = teamname
        self.link = link          
        
    def __str__(self):
        return dict(self)

    def __repr__(self):
        return str(self.__str__())
    
    def __iter__(self):
        yield from {
            "team id:": self.teamid,
            "team name": self.teamname,
            "team head": self.getTeamsHeadSoup()
        }.items()  

        
    def getTeamsHeadSoup(self):
        """ Get teams """

        try:
            data = []
            # fill dataset            
            page = requests.get(self.link)            
            soup = BeautifulSoup(page.text, parser='lxml', features="lxml")            
            table = soup.find("table", {"class":"infobox"} )
            table_body = table.find('tbody')
            rows = table_body.find_all('tr')            
            for row in rows:
                cols = row.find_all(['th','td'])    
                cols = [ele.text.strip() for ele in cols if ele]    
                data.append(cols[0:2]) # Get rid of empty values    
            tab1 = pd.DataFrame(data)
            cols = {0:"ind",1:"val"}
            columns = list(cols.values())
            tab1 = tab1.rename(columns=cols)
            tab1 = tab1.loc[:,columns]
            tab1 = tab1.dropna()
            datas = ["Head coach","FIFA code","Confederation","Captain"]
            dat = tab1.loc[(tab1["ind"].isin(datas))]  
            res = dat.set_index("ind").T
            res["teamid"] = self.teamid
            res = res.to_dict(orient="records")
            return res
        except:
            return print("Error occured with the link.")
    
    #dictionarymap parameter has to be in format {countryLowercase : id}
    def getTeamsDetailsSoup(self, dictionarymap):
        try:
            data = []   
            page = requests.get(self.link)
            soup = BeautifulSoup(page.text, parser='lxml', features="lxml")            
            table = soup.find( "table", {"class":"plainrowheaders"} )
            if table.empty:
                raise Exception("There is an empty dataset")
                
            table_body = table.find('tbody')
            
            rows = table_body.find_all('tr')
            for row in rows:
                cols = row.find_all(['td','th'])    
                states = row.find_all('img')
                cols = [ele.text.strip() for ele in cols if ele]  
                cols1 = [ele.get('alt') for ele in states] 
                datas1 = [ele for ele in cols]
                datas2 = [ele for ele in cols1]
                res = [*datas1, *datas2]
                data.append(res) # Get rid of empty values    
              
            ColumnNames = {"No.":"Number","Pos.":"Position","Player":"Player name","Date of birth (age)":"Date of birth",
                   "Club":"Current club",None:"Country"}
            tab1 = pd.DataFrame(data)                        
            tab1.columns = tab1.iloc[0]            
            tab1 = tab1[1:]
            tab1 = tab1.dropna()
            tab1 = tab1.rename(columns=ColumnNames)
            tab1["Position"] = tab1["Position"].str[1:]
            tab1["Date of birth"] = tab1["Date of birth"].str.replace('(', '', regex=True)
            tab1["Date of birth"] = tab1["Date of birth"].str.partition(')')[0]
            tab1["Date of birth"] = pd.to_datetime(tab1["Date of birth"])
            dtypescols = {"Number":"int","Caps":"int","Goals":"int"}
            tab1 = tab1.astype(dtypescols)
            tab1.index = np.arange(1, len(tab1) + 1)
            tab1.index.name = "playerid"
            tab1["teamid"] = self.teamid  
            tab1["countryLower"] = tab1['Country'].str.replace('\W', '', regex=True)
            tab1['countryLower'] = tab1['countryLower'].str.lower()
            tab1['countryid'] = tab1['countryLower'].map(dictionarymap)
            tab1['countryid'].astype('int')

            return tab1
        except Exception as inst:
            return print(inst)
        
    def getCompleteTeamDetails(self, dictionarymap, joinflags, show='all'):
        try:
            getteamset = self.getTeamsDetailsSoup(dictionarymap)
            getteamset = getteamset.set_index("countryid")
            Showall = getteamset.merge(joinflags, on='countryid', how='left')
            Showall = Showall.set_index("Number")           
            
            
            if show == 'web':
                cols = ["Position","Player name","Date of birth","Caps","Goals","Current club","Country","FlagPathWeb","image"]
            elif show == 'local':
                cols = ["Position","Player name","Date of birth","Caps","Goals","Current club","Country","FlagPath","image"]
            else:    
                cols = ["Position","Player name","Date of birth","Caps","Goals","Current club","Country","FlagPath","FlagPathWeb","image"]
            
            Showall = Showall[cols]

            return Showall
        except:
            return print("Error occured with this dataset.")
        
    def getTeamsHead(self):
        """ Get teams """

        try:
            # fill dataset
            table = pd.read_html(self.link)        

            # connect to PostgreSQL server
            cols = {0:"ind",1:"val"}
            columns = list(cols.values())
            tab = pd.DataFrame(table[0])
            tab = tab.rename(columns=cols)
            tab = tab.loc[:,columns]
            tab = tab.dropna()
            datas = ["Head coach","FIFA code","Confederation"]
            dat = tab.loc[(tab["ind"].isin(datas))]            
            res = dat.set_index("ind").T
            res["teamid"] = self.teamid
            
            res = res.to_dict(orient="records")
            return res
        except:
            return print("Error occured with the link.")


    def getTeamsDetails(self,mtch):
        try:
            html = requests.get(self.link).content        
            # fill dataset
            table1 = pd.read_html(html)
            tab1 = pd.DataFrame()
            for df in table1:    
                new_df=df.dropna(how='all').dropna(axis=1,how='any')            
                if mtch in str(df.iloc[:,:]):                    
                    tab1 = pd.DataFrame(new_df)
                else:
                    continue
            if tab1.empty:
                raise Exception("There is an empty dataset")
            ColumnNames = {"No.":"Number","Pos.":"Position","Player":"Player name","Date of birth (age)":"Date of birth",
                   "Club":"Current club"}
            #tab = pd.DataFrame(tab)
            tab1 = tab1.dropna()
            tab1 = tab1.rename(columns=ColumnNames)
            dtypescols = {"Number":"int","Caps":"int","Goals":"int"}
            tab1 = tab1.astype(dtypescols)
            tab1.index = np.arange(1, len(tab1) + 1)
            tab1.index.name = "playerid"
            tab1["teamid"] = self.teamid

            return tab1
        except Exception as inst:
            return print(inst)
    
    