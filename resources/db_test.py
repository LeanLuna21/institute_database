import sqlite3
import pandas as pd

#step 1 - load datafile
df = pd.read_csv("resources/cursos.csv")
#step 2 - clean columns
df.columns = df.columns.str.strip()
#step 3 - create/connect sqlite db
connection = sqlite3.connect('resources/Alas_test.db')
#step 4
# to write the database
df.to_sql("cursos", connection, if_exists="replace") #fail(raise exc) replace(the existing) append(add)

# repeat for the other csv - adding the other tables from csv
df2 = pd.read_csv("resources/alumnos.csv")
df2.columns = df2.columns.str.strip()
df2.to_sql("alumnos",connection,if_exists="replace")

df3 = pd.read_csv("resources/profesores.csv")
df3.columns = df3.columns.str.strip()
df3.to_sql("profesores",connection,if_exists="replace")

df4 = pd.read_csv("resources/pagos.csv")
df4.columns = df4.columns.str.strip()
df4.to_sql("pagos",connection, if_exists="replace")
# step 5. Close conection
connection.close()
