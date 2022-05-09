import pandas as pd

df1_csv = "out_files/moyenne_fr_FEEL.csv"
df2_csv = "out_files/moyenne_als_ELAL.csv"

def correlation_df(df1_csv, df2_csv):
    df1 = pd.read_csv(df1_csv)
    df2 = pd.read_csv(df2_csv)

    cor_series = df1.corrwith(df2, axis=0 , method="spearman")
    return cor_series
