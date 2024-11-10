import json
#from json import JSONEncoder as jen
from app import cfi
from app.models import Datas
import psycopg2 as pg
import pandas as pd

def create_pandas_table(sql_query, database):
    table = pd.read_sql_query(sql_query, database)
    return table

def selectProds(ago):
    try: 
        con = cfi 
        crs = con.cursor()         
        crs.callproc('customers_orders', (ago,))
        #sp = "{CALL dbo.procPosts }"        
        #crs.execute(sp) 
        rows = crs.fetchall() 
        #mydata = {}
        returndata = []          
        j = 0
        for r in rows: 
            fname = str(r[0])
            lname = str(r[1])
            address = str(r[2])
            city = str(r[3])
            state = str(r[4])
            country = str(r[5])
            title = str(r[6])
            price = str(r[7])
            qnt = str(r[8])
            tot = str(r[9])
            s = Datas(fname, lname, address, city, state, country, title, price, qnt, tot)
            #mydata[j] = s            
            returndata.append(s)
            j += 1        
        #con.close()       
        #print(returndata)
        stri=json.loads(str(returndata))         
        stri1 = pd.json_normalize(stri) 
        stri1.to_csv('raw_data.csv', index=False)
        #stri=dict(returndata)
        return stri1

    except pg.Error as ex: 
        print('Error in table') 
        print(ex)
    """
    finally:
        # closing database connection.
        if con:            
            con.close()
            print("PostgreSQL connection is closed")
    """
def insertProds(nam):
    con = None
    try: 
        con = cfi         
        crs = con.cursor() 
        #crs.callproc('get_docs_ex', [])
        crs.execute("CALL MyInsertSample(%s);", (nam,))        
        #crs.execute(sp) 
        con.commit()                

        print('Inserted new value...')

    except pg.Error as ex: 
        print('Error in table') 
        print(ex)
    """
    finally:
        # closing database connection.
        if con:            
            con.close()
            print("PostgreSQL connection is closed")
    """