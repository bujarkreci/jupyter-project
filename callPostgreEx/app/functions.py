import pandas as pd
import numpy as np
import requests

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

class Teams:
    def __init__(self, teamid, teamname, link):
        self.teamid = teamid
        self.teamname = teamname
        self.link = link                

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