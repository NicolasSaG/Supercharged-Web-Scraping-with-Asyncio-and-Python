from os.path import isfile, join
import os
import pandas as pd
import shutil


def get_files(year, final_txt):
    path = "recursos/datos/{}REDDA".format(
        year[2:])
    filenames = [f for f in os.listdir(path) if isfile(join(path, f))]

    print("Obteniendo archivos de {}".format(path))
    for filename in filenames:
        if filename.endswith(final_txt):
            shutil.copyfile("{}\\{}".format(path, filename),
                            "recursos/datos/pph/{}".format(filename))

    print("Archivos obtenidos".format(final_txt))


def obtener_vacios(df):
    no_vacios = df.dropna(how="all")
    return pd.merge(df, no_vacios, indicator=True, how='outer').query('_merge=="left_only"').drop('_merge', axis=1)


# obtener archivos solicitados de los años y guardarlos en una carpeta aparte
try:
    os.mkdir("recursos/datos/pph")
except:
    print("carpeta datos_solicidatos ya existe")

for year in range(2010, 2020):
    get_files(str(year), "PPH.xls")


dataframes = []
atipicos = []
for year in range(2010, 2020):
    path = "recursos/datos/pph/{}PPH.xls".format(year)
    df = pd.read_excel(path, index_col=None)
    df.index.name = "ID"

    vacios = obtener_vacios(df)
    vacios.insert(loc=1, column="AÑO", value=year)
    vacios.insert(loc=1, column="id_vacio", value=vacios.index)
    atipicos.append(vacios)

    # Se remueven filas vacias
    df.dropna(how="all", inplace=True)

    # Se unifican los tipos de dato de las fechas
    if df["FECHA"].dtype != "datetime64[ns]":
        df["FECHA"] = df["FECHA"].astype(str)
        df["FECHA"] = pd.to_datetime(df["FECHA"])

    # Se agregan las columnas para el semana, mes y año
    df.insert(loc=1, column="AÑO",
              value=df["FECHA"].dt.year, allow_duplicates=False)
    df.insert(loc=2, column="MES",
              value=df["FECHA"].dt.month, allow_duplicates=False)
    df.insert(loc=3, column="SEMANA",
              value=df["FECHA"].dt.isocalendar().week, allow_duplicates=False)

    dataframes.append(df)

# concatenar nulos
join_atipicos = pd.concat(atipicos).reset_index(drop=True)
path = 'recursos/datos/pph/{}'.format("atipicos.csv")
join_atipicos.to_csv(path, index=True)

# Se concatenan los dataframes
join_table = pd.concat(dataframes).reset_index(drop=True)

# Leemos estaciones.csv
path = "recursos/datos/{}".format("estaciones.csv")
stations = pd.read_csv(path, index_col=None)
df_stations = pd.DataFrame(stations)
locations = dict(
    zip(list(df_stations["Clave"]), list(df_stations["Estación"])))

# creacion de archivo bitacora para guardar eliminaciones de los otros archivos, inconsistencias, etc
bitacora_col = ['elemento', 'fecha', 'año',
                'mes', 'semana', 'localizacion', 'medicion']
dt_bt = pd.DataFrame(columns=bitacora_col)
dt_nulos = pd.DataFrame(columns=bitacora_col)
print('Escribiendo tabla de hechos...')
count = 0
count_nulos = 0
for index in range(0, len(join_table)):
    for col_title in join_table.columns.values[4:]:
        row_data = [
            "Precipitación pluvial",
            join_table.iloc[index]["FECHA"],
            join_table.iloc[index]["AÑO"],
            join_table.iloc[index]["MES"],
            join_table.iloc[index]["SEMANA"],
            locations[col_title],
            join_table.iloc[index][col_title]
        ]
        if(join_table.iloc[index][col_title] != -99.0):
            dt_bt.loc[count] = row_data
            count += 1
        else:
            dt_nulos.loc[count_nulos] = row_data
            count_nulos += 1
    dt_bt.index.name = "ID"
    dt_nulos.index.name = "ID"

# Escritura de tabla de hechos en archivo bitacora.csv
path = 'recursos/datos/pph/{}'.format("bitacora.csv")
dt_bt.to_csv(path, index=True)

path = 'recursos/datos/pph/{}'.format("nulos.csv")
dt_nulos.to_csv(path, index=True)

print('Completo')
