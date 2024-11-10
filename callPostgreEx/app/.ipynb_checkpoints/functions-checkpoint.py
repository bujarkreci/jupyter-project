import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import base64
from typing import Tuple
import glob
import xlsxwriter
import io

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
    
def buffer_image(image: Image, format: str = 'PNG'):
    # Store image in buffer, so we don't have to write it to disk.
    buffer = io.BytesIO()
    image.save(buffer, format=format)
    return buffer, image

def resize(path: str, size: Tuple[int, int], format='PNG'):
    image = Image.open(path)
    image = image.resize(size)
    return buffer_image(image, format)

def rotate(image: Image, rotation: int = 90, format='JPEG'):
    image = image.rotate(rotation, Image.NEAREST, expand=1)
    return buffer_image(image, format)

def create_header(worksheet: xlsxwriter.workbook.Worksheet):
    bold = workbook.add_format({'bold': True})
    worksheet.write('A1', 'Image Name', bold)
    worksheet.write('B1', "Resized Image", bold)
    worksheet.write('C1', "Rotated Image", bold)
    worksheet.write('D1', "Metadata", bold)
    return worksheet

def append_xls(fpath, l, df, sheet_name,flagpath):
    image_width = 204.0
    image_height = 120.0
    
    cell_width = 150.0
    cell_height = 75.0

    x_scale = cell_width/image_width
    y_scale = cell_height/image_height    
       
    workbook = xlsxwriter.Workbook(fpath)
    worksheet = workbook.add_worksheet(sheet_name)
    numpimg = np.array(df["FlagPath"])
    title_format = workbook.add_format({'align': 'center', 'bold': True, 'font_size':25})
    text_format = workbook.add_format({'align': 'left', 'bold': True})
    text_formatdate = workbook.add_format({'align': 'left', 'bold': True, 'num_format':'yyyy-mm-dd'})
    header_format = workbook.add_format({'align': 'left', 'fg_color': 'gray', 'bold': True})
    image_buffer, image = resize(flagpath, (image_width, image_height), format='PNG')
    data = {'x_scale': x_scale, 'y_scale': y_scale, 'object_position': 1}
    worksheet.insert_image(0, 0, flagpath, {'image_data': image_buffer, **data})
    #worksheet.insert_image(0, 0, flagpath, {'image_data': image_buffer})
    worksheet.set_column(0, 0, 25)
    worksheet.set_row(0, 60)
    worksheet.write_row(0, 1, [sheet_name], title_format)
    worksheet.set_column(1, 1, 40)
    
    #worksheet.write_row(1, 0, ["Confederation"], header_format)
    #worksheet.write_row(1, 1, l["Confederation"], header_format)
    for i, colu in enumerate(l.columns, start=1):
        worksheet.write_row(i, 0, [colu], header_format)
        worksheet.write_row(i, 1, l[colu], text_format)
    
    start_row = 0
    worksheet.set_column(9, 10)
    df = df.loc[:,df.columns != "FlagPath"]
    worksheet.set_column(2, 2, 8)
    worksheet.set_column(3, 3, 25)  
    worksheet.set_column(4, 4, 15)
    worksheet.set_column(5, 6, 6)
    worksheet.set_column(7, 8, 25)
    worksheet.write_row(start_row, 2, df.columns, header_format)   
    
    
    #start_row = 0
    for i, column in enumerate(df.columns, start=2):
        if i == 4:
            worksheet.write_column(start_row+1, i, df[column], text_formatdate)
        else:
            worksheet.write_column(start_row+1, i, df[column], text_format)    
    
    
    worksheet.write_row(start_row, 9, ["Flag"], header_format)
    for ima in numpimg:
        image_buffer, image = resize(ima, (82, 48), format='PNG')
        data = {'x_scale': x_scale, 'y_scale': y_scale, 'object_position': 1}
        worksheet.insert_image(start_row+1, 9, ima, {'image_data': image_buffer, **data}) 
        worksheet.set_row(start_row+1, 25)
        start_row +=1
    
    workbook.close()
    
def image_formatter(im):
    return f'<img src="data:image/png;base64,{image_base64(im)}">'
    
def getAllCountriesFlags(url, countriesdictmap, replacingstrs, show='all'):
    
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
        tab1['Country'] = tab1['Country'].str.lower()        
        tab1['CountryClean'] = tab1['Country'].str.replace('\W', '', regex=True)
        tab1['CountryClean'] = tab1['CountryClean'].replace(replacingstrs, regex=True)
        
        #tab1['countryid'] = tab1['CountryLower'].map(natTeams.set_index('NationalTeamNameLower')['NationalTeamId'])
        tab1['countryid'] = tab1['CountryClean'].map(countriesdictmap)
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
    
def getAllFIFACodes(url, countriesdictmap, classname, starttab, endtab, replacingstrs):
    
    try:
    
        data = []        
        page = requests.get(url)
        soup = BeautifulSoup(page.text, parser='lxml', features="lxml")
        table = soup.find_all( "table", {"class":classname} )

        for tabi in table[starttab:endtab]: 
            table_body = tabi.find('tbody')

            rows = table_body.find_all('tr')
            for row in rows:
                cols = row.find_all('td') 
                cols = [ele.text.strip() for ele in cols]
                datas1 = [ele for ele in cols]
                data.append(datas1)

        tab1 = pd.DataFrame(data)
        tab1.columns = tab1.iloc[0]
        tab1 = tab1[1:]  
        cols = ["teamName","countryCode","dat2"]
        tab1.columns = cols
        columnstoshow = ["teamName","countryCode"]
        tab1 = tab1.loc[:,columnstoshow]        
        tab1 = tab1.dropna()  
        tab1["teamNameClean"] = tab1["teamName"].str.lower()
        tab1["teamNameClean"] = tab1["teamNameClean"].str.strip()        
        tab1["teamNameClean"] = tab1["teamNameClean"].replace(replacingstrs, regex=True)
        tab1["teamNameCleanAll"] = tab1["teamNameClean"].str.replace('\W', '', regex=True)
        tab1["countryCode"] = tab1["countryCode"].str.partition('[')[0]
        tab1['countryid'] = tab1['teamNameCleanAll'].map(countriesdictmap)
        tab1['countryid'] = tab1['countryid'].fillna(0)
        tab1['countryid'] = tab1['countryid'].astype(int)
        tab1 = tab1.set_index('countryid') 
        
        return tab1
    except:
        return print("Error occured with the dataset.")
    
def append_xlsFull(fpath, wccountries, countrymapping, allteams):    
    try:
        cols = ["Position","Player name","Date of birth","Caps","Goals","Current club","Country","FlagPath"]
        image_width = 204.0
        image_height = 120.0

        cell_width = 150.0
        cell_height = 75.0

        x_scale = cell_width/image_width
        y_scale = cell_height/image_height         
        data = {'x_scale': x_scale, 'y_scale': y_scale, 'object_position': 1}            
        #workbook = xlsxwriter.Workbook(fpath)

        team = []
        numdata = len(wccountries)
        for i in range(numdata):                
            ti = Teams(i+1,wccountries.index[i],wccountries.iloc[i]["link"], 
                      wccountries.iloc[i]["countryid"],wccountries.iloc[i]["FlagPath"])
            team.append(ti)
            
        with pd.ExcelWriter(fpath, engine='xlsxwriter') as writer:  
            workbook = writer.book
            title_format = workbook.add_format({'align': 'center', 'bold': True, 'font_size':25})
            text_format = workbook.add_format({'align': 'left', 'bold': True})
            text_formatdate = workbook.add_format({'align': 'left', 'bold': True, 'num_format':'yyyy-mm-dd'})
            header_format = workbook.add_format({'align': 'left', 'fg_color': 'gray', 'bold': True})
            for i in range(numdata):
                t = team[i]
                worksheet = workbook.add_worksheet(t.teamname)
                writer.sheets[t.teamname] = worksheet
                
                #team.append(t)
                dct = dict(t)
                CompleteShow=t.getCompleteTeamDetails(countrymapping, allteams,'local')
                CompleteShow = CompleteShow[cols]
                sep = dct['team head']
                sep = pd.DataFrame(sep)
                sep['Team name'] = t.teamname
                sep = sep.loc[:, sep.columns != 'teamid']
                

                
                #writer.sheets[t.teamname] = worksheet
                numpimg = np.array(CompleteShow["FlagPath"])
                image_buffer, image = resize(t.flagpath, (image_width, image_height), format='PNG')
                worksheet.insert_image(0, 0, t.flagpath, {'image_data': image_buffer, **data})
                worksheet.set_column(0, 0, 25)
                worksheet.set_row(0, 60)
                worksheet.write_row(0, 1, [t.teamname], title_format)
                worksheet.set_column(1, 1, 40)

                for j, colu in enumerate(sep.columns, start=1):
                    worksheet.write_row(j, 0, [colu], header_format)
                    worksheet.write_row(j, 1, sep[colu], text_format)

                start_row = 0
                worksheet.set_column(9, 10)
                CompleteShow = CompleteShow.loc[:,CompleteShow.columns != "FlagPath"]
                worksheet.set_column(2, 2, 8)
                worksheet.set_column(3, 3, 25)  
                worksheet.set_column(4, 4, 15)
                worksheet.set_column(5, 6, 6)
                worksheet.set_column(7, 8, 25)
                worksheet.write_row(start_row, 2, CompleteShow.columns, header_format)

                for i, column in enumerate(CompleteShow.columns, start=2):
                    if i == 4:
                        worksheet.write_column(start_row+1, i, CompleteShow[column], text_formatdate)
                    else:
                        worksheet.write_column(start_row+1, i, CompleteShow[column], text_format)

                worksheet.write_row(start_row, 9, ["Flag"], header_format)
                for ima in numpimg:
                    image_buffer, image = resize(ima, (82, 48), format='PNG')            
                    worksheet.insert_image(start_row+1, 9, ima, {'image_data': image_buffer, **data}) 
                    worksheet.set_row(start_row+1, 25)
                    start_row +=1

            workbook.close()
                    
    except Exception as inst: 
        return print(inst)
    
class Teams:    
    
    def __init__(self, teamid, teamname, link, countryid, flagpath):
        self.teamid = teamid
        self.teamname = teamname
        self.link = link
        self.countryid = countryid
        self.flagpath = flagpath
        
    def __str__(self):
        return dict(self)

    def __repr__(self):
        return str(self.__str__())
    
    def __iter__(self):
        yield from {
            "team id": self.countryid,
            "team name": self.teamname,
            "team flag": self.flagpath,
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
            res["teamid"] = self.countryid
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
            #table = soup.find( "table", {"class":"plainrowheaders"} )
            table = soup.find( "table", {"class":"sortable wikitable plainrowheaders"} )            
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
            tab1["teamid"] = self.countryid  
            tab1["countryLower"] = tab1['Country'].str.replace('\W', '', regex=True)
            tab1['countryLower'] = tab1['countryLower'].str.lower()
            #tab1['countryLower'] = tab1['countryLower'].apply(lambda x: "unitedstatesofamerica" if x == "unitedstates" else x)
            #tab1[tab1['countryLower'].str.contains("unitedstates")]            
            tab1['countryid'] = tab1['countryLower'].map(dictionarymap)            
            tab1['countryid'].astype('int')
            tab1['countryid'] = tab1['countryid'].fillna(0)

            return tab1
        except Exception as inst:
            return print(inst)
        
    def getCompleteTeamDetails(self, dictionarymap, joinflags, show='all'):
        try:
            getteamset = self.getTeamsDetailsSoup(dictionarymap)
            getteamset = getteamset.set_index("countryid")
            Showall = getteamset.merge(joinflags, on='countryid', how='left')
            #Showall = Showall.set_index("Number")           
            
            
            if show == 'web':
                cols = ["Position","Player name","Date of birth","Caps","Goals","Current club","Country","FlagPathWeb","Filename","image"]
            elif show == 'local':
                cols = ["Position","Player name","Date of birth","Caps","Goals","Current club","Country","FlagPath","Filename","image"]
            else:    
                cols = ["Position","Player name","Date of birth","Caps","Goals",
                        "Current club","Country","FlagPath","Filename","FlagPathWeb","image"]
            
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
            tab1["teamid"] = self.countryid

            return tab1
        except Exception as inst:
            return print(inst)
    
    