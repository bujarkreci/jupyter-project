from decouple import config
import psycopg2 as pg
import pyodbc as pyo

secretKey = config("SECRET_KEY")
unamePostgre = config("PostgreUser")
passwPostgre = config("PostgrePass")
unameSQL = config("SQLUser")
passwSQL = config("SQLPass")

connPostgre = {
    'hostname' : '192.168.0.30',
    'database' : 'dellstore2',
    'username' : unamePostgre,
    'pwd' : passwPostgre,
    'port_id' : 5432
    }

connSQL = {
    'server' : '192.168.0.30', 
    'serverwithport' : '192.168.0.30,49172',
    'dbu' : 'FootballDetails', 
    'uname' : unameSQL, 
    'passw' : passwSQL,
    'port' : 49172
    }


class ConfigBase(object):
    
    SECRET_KEY = secretKey  

class ConfigPostgreSQL(ConfigBase):    
    conn = {
        "host" : connPostgre['hostname'],
        "dbname" : connPostgre['database'],
        "user" : connPostgre['username'],
        "password" : connPostgre['pwd'],
        "port" : connPostgre['port_id']
    }
    
class ConfigPostgreSQLAlchemy(ConfigBase):    
    par = 'postgresql://' + connPostgre['username'] + ':' + connPostgre['pwd'] + '@' + connPostgre['hostname'] + ':' + str(connPostgre['port_id']) + '/' + connPostgre['database']        
    
class ConfigSQLAlchemy(ConfigBase):
    par = "mssql+pyodbc://" + connSQL['uname'] + ":" + connSQL['passw'] + "@" + connSQL['server'] + ":" + str(connSQL['port']) + "/" + connSQL['dbu'] + "?driver=ODBC+Driver+17+for+SQL+Server"
    
#This ConfigSQLDirect is not working need further to investigate
class ConfigSQLDirect(ConfigBase):
    cnxn = ("Driver={SQL Server Native Client 11.0};"
            f"Server={connSQL['serverwithport']};"
            f"Database={connSQL['dbu']};"
            f"UID={connSQL['uname']};"
            f"PWD={connSQL['passw']};")

config = {    
    'PostgreSQL': ConfigPostgreSQL.conn,
    'PostgreSQLalchemy' : ConfigPostgreSQLAlchemy.par,
    'SQLAlchemy' : ConfigSQLAlchemy.par,
    'SQLDirect' : ConfigSQLDirect.cnxn
}