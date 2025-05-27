import pandas as pd
import os 

def clean_text_cols(df: pd.DataFrame, cols: list):
    df = df.copy()
    for col in cols:
       
        df[col] = df[col].str.lower()
        df[col] = df[col].str.replace('_', ' ')
        df[col] = df[col].str.replace('-', ' ')
       
    return df

def save_df(df: pd.DataFrame):
    if not os.path.exists('files/output'):
        os.mkdir('files/output')
    df.to_csv('files/output/solicitudes_de_credito.csv',index=True,sep=';')

def pregunta_01():
    
    df = pd.read_csv('files/input/solicitudes_de_credito.csv', sep=';', index_col=0)
    df.drop_duplicates(keep='first', inplace=True)
    df.dropna(inplace=True)
    df = clean_text_cols(df, ['sexo','tipo_de_emprendimiento','idea_negocio','barrio','línea_credito'])
    
    df.monto_del_credito = df.monto_del_credito.map(lambda x: float(x.replace('$','').replace(',','').replace(".00", "").strip() if isinstance(x,str) else x))
    
    
    df["year"] = df["fecha_de_beneficio"].map(
        lambda x: (
            int(x.split("/")[0])
            if len(x.split("/")[0]) > 2
            else int(x.split("/")[-1])
        )
    )
    df["month"] = df["fecha_de_beneficio"].map(lambda x: int(x.split("/")[1]))
    df["day"] = df["fecha_de_beneficio"].map(
        lambda x: (
            int(x.split("/")[-1])
            if len(x.split("/")[0]) > 2
            else int(x.split("/")[0])
        )
    )
    df["fecha_de_beneficio"] = pd.to_datetime(df[["year", "month", "day"]])

    df = df.drop(columns=["year", "month", "day"])

    df.drop_duplicates(keep='first', inplace=True)
    
    save_df(df)
    return df


pregunta_01()