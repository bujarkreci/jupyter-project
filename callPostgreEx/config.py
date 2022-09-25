from decouple import config
import psycopg2 as pg

secretKey = config("SECRET_KEY")
unamePostgre = config("PostgreUser")
passwPostgre = config("PostgrePass")

connPostgre = {
    'hostname' : '192.168.0.30',
    'database' : 'dellstore2',
    'username' : unamePostgre,
    'pwd' : passwPostgre,
    'port_id' : 5432
    }


class ConfigBase(object):
    
    SECRET_KEY = secretKey  

class ConfigPostgreSQL(ConfigBase):    
    conn = pg.connect(
        host = connPostgre['hostname'],
        dbname = connPostgre['database'],
        user = connPostgre['username'],
        password = connPostgre['pwd'],
        port = connPostgre['port_id']
        )
    
class ConfigPostgreSQLAlchemy(ConfigBase):    
    par = 'postgresql://' + connPostgre['username'] + ':' + connPostgre['pwd'] + '@' + connPostgre['hostname'] + ':' + str(connPostgre['port_id']) + '/' + connPostgre['database']        

config = {    
    'PostgreSQL': ConfigPostgreSQL.conn,
    'PostgreSQLalchemy' : ConfigPostgreSQLAlchemy.par
}