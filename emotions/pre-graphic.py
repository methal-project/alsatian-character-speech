#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File      :   pre-graphic.py
@Create on :   2022/08
@Author    :   Qinyue Liu
@Version   :   1.0
@Contact   :   qinyue.liu@etu.univ-grenoble-alpes.fr
@Desc      :   None
'''

# Requirements: os, csv, pandas

import pandas as pd
import os
import csv

emotion_list = [
    "anger"
    , "disgust", "fear", "joy", "sadness", "surprise", "trust", "anticipation"
]

vad_list = ["valence", "arousal", "dominance"]

def add_rolling_mean():
    """Function to add a file which contains rolling-means of all emotions for each theater piece

    Returns:
        None, but create csv files called rolling_mean.csv for each theater piece

    """
    li_files = os.listdir("results2") # directory name
    df_final = pd.DataFrame()
    for name in li_files:
        if os.path.isdir(name) and name != "__pycache__":
            folder_path = name + "/"
            csv_files = os.listdir("results2/"+folder_path)
            if ("all_emo.csv" in csv_files):
                id = csv_files.index("all_emo.csv")
                csv_files.pop(id)
            for i in range(len(csv_files)): # get csv files in each theater piece directory
                if (".csv" in csv_files[i] and "rolling_mean" not in csv_files[i]):
                    # initialize df_final
                    if (i == 0):
                        df_final = pd.read_csv(folder_path + csv_files[0]) # final csv file
                        if (df_final.shape[0] <= 5):
                            col_name = csv_files[i][:-4] # emotion name
                            df_final[col_name + "_roll_mean"] = df_final["avgLexVal"]
                        else:
                            roll_mean = df_final["avgLexVal"].rolling(5).mean()
                            col_name = csv_files[i][:-4] # emotion name
                            df_final[col_name + "_roll_mean"] = roll_mean
                    # ----------------------------------------------------
                    else:
                        if (df_final.shape[0] <= 5):
                            df = pd.read_csv(folder_path + csv_files[i]) # intermediate dataframe
                            col_name = csv_files[i][:-4] # emotion name
                            df_final[col_name + "_roll_mean"] = df_final["avgLexVal"]
                        else:
                            df = pd.read_csv(folder_path + csv_files[i]) # intermediate dataframe
                            roll_mean = df["avgLexVal"].rolling(5).mean()
                            col_name = csv_files[i][:-4] # emotion name
                            df_final[col_name + "_roll_mean"] = roll_mean # add a new column for rolling mean
            if ("Unnamed: 0" in df_final.columns):
                df_final.drop("Unnamed: 0", axis=1, inplace=True)
            if ("avgLexVal" in df_final.columns):
                df_final.drop("avgLexVal", axis = 1, inplace=True)
            df_final.to_csv("results2/"+folder_path + "rolling_mean.csv", index=False)


def get_percentage():
    """Function to calculate portion of each emotion in each piece

    Returns:
        An array which contains all the rolling-means
    """
    all_moyen = []
    li_files = os.listdir("results2")
    for name in li_files:
        if (os.path.isdir("results2/"+name) and "pycache" not in name):
            df = pd.read_csv("results2/"+name+"/rolling_mean.csv")
            drama_type = pd.read_csv("results2/"+name+"/joy.csv")["drama_type"].values[0]
            sum = 0
            portion = []
            piece_moyen = [] # information for each piece
            piece_moyen.append(name)
            piece_moyen.append(drama_type)
            for emo in emotion_list:
                sum += df[emo+"_roll_mean"].sum()
                portion.append(df[emo+"_roll_mean"].sum())
            for vad in vad_list:
                if (vad == "valence"):
                    polarity = 0
                    mean = df["valence_roll_mean"].mean()
                    for val in df["valence_roll_mean"]:
                        if val >= mean:
                            polarity += 1
                        else:
                            polarity -= 1
                    piece_moyen.append(polarity)
                piece_moyen.append(df[vad+"_roll_mean"].mean())

            for p in portion:
                emo_portion = p/sum
                piece_moyen.append(emo_portion)
            all_moyen.append(piece_moyen)
    return all_moyen

def write_csv(all_moyen):
    """Function to create a file which includes all the rolling-means of all pieces
    Args:
        param1: An array which contains all the rolling-means
    Returns:
        None

    """
    header = ["shortName", "drama_type", "polarity", "valence", "arousal", "dominance", "anger"
    , "disgust", "fear", "joy", "sadness", "surprise", "trust", "anticipation"
    ]
    with open("all_pieces_info2.csv", "w", encoding="utf-8") as out:
        writer = csv.writer(out)
        writer.writerow(header)
        writer.writerows(all_moyen)

def group_info():
    all_moyen = get_percentage()
    write_csv(all_moyen)

if __name__ == "__main__":
    add_rolling_mean()
    group_info()