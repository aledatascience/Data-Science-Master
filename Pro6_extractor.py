import pandas as pd
from matplotlib import pyplot as plt
import sqlalchemy as sa
from IPython.display import display, HTML

# Define the query file name and path
query = "query.txt"
## enter the Abbrevation of the database for example "SYD" and the name of the server
database_name = "SYD"
server_name = "GVAPROTDBLI05P"

def read_Prot6query(query_fname, db_name):
    engine = sa.create_engine("mssql+pyodbc://GVAPROTDBLI05P.gva.icrc.priv/"+ db_name +"_Reporting?driver=SQL+Server?ApplicationIntent=READONLY")
    with open(query_fname, 'r') as myfile:
        sql_query = myfile.read().replace('\n', '')
    sql_query = ' '.join(sql_query.split())
    
    con = engine.connect()
    df_prot6out = pd.read_sql(sql_query, con, index_col=None, coerce_float=True, params=None, parse_dates=None, columns=None, chunksize=None)
    print 'Query returned a dataset with shape ' + str(df_prot6out.shape)
    con.close()
    return df_prot6out

def PrintOutDatasetMissingPercentage(df_in, cmap_in='RdYlGn_r'):

    df_ratios = pd.DataFrame(df_in.isnull().mean().round(4) * 100)
    df_ratios = df_ratios.rename(columns = {df_ratios.columns[0]:"Missing values (%)"})
    df_ratios = df_ratios.style.background_gradient(cmap=cmap_in)
    display(df_ratios)




prot6Data = qb.read_Prot6query(query, database_name)
# Save the results as excel and csv files
prot6Data.to_excel("prot6Data.xlsx")
prot6Data.to_csv("prot6Data.csv")
