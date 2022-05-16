import pandas as pd
import seaborn as sb
import matplotlib.pyplot as mp

df1_csv = "out_files/moyenne_fr_FEEL.csv"
df2_csv = "out_files/moyenne_als_ELAL.csv"

def correlation_df(df1_csv, df2_csv, compare_moyen, compare_cor):
    df1 = pd.read_csv(df1_csv)
    df2 = pd.read_csv(df2_csv)

    df_merge = df1.merge(df2, how="inner", on="Id_block", suffixes=('_als','_fr'))
    df_merge.to_csv(compare_moyen, float_format="%.3f")

    cor_series = df_merge.corr() 
    cor_series.to_csv(compare_cor, float_format="%.3f")

    cor_series = cor_series.round(2)
    sb.heatmap(cor_series, cmap="YlGnBu", annot=True)
    mp.show()
