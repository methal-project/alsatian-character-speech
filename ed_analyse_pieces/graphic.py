from numpy import NaN
import seaborn as sb
import pandas as pd
import matplotlib.pyplot as plt
import sys, os
import csv

emotion_list = [
    "anger"
    , "disgust", "fear", "joy", "sadness", "surprise", "trust", "anticipation"
]

vad_list = ["valence", "arousal", "dominance"]

def get_moyennes():
    all_moyen = []
    li_files = os.listdir(".")
    for name in li_files:
        if (os.path.isdir(name) and "drizehne" not in name): # Si c'est un repertoire de piece de theatre
            df = pd.read_csv(name+"/rolling_mean.csv")
            drama_type = pd.read_csv(name+"/joy.csv")["drama_type"].values[0]
            sum = 0
            sum_vad = 0
            portion = []
            portion_vad = []
            piece_moyen = [] # les infos pour chaque pièce
            piece_moyen.append(name)
            piece_moyen.append(drama_type)
            for emo in emotion_list:
                sum += df[emo+"_roll_mean"].sum()
                portion.append(df[emo+"_roll_mean"].sum())
            for vad in vad_list:
                sum_vad += df[vad+"_roll_mean"].sum()
                portion_vad.append(df[vad+"_roll_mean"].sum())

            for v in portion_vad:
                v_portion = v/sum_vad
                piece_moyen.append(v_portion)
            for p in portion:
                emo_portion = p/sum
                piece_moyen.append(emo_portion)
            if (piece_moyen[3] == NaN):
                print(name)
            all_moyen.append(piece_moyen)
    return all_moyen


def add_rolling_mean():
    li_files = os.listdir(".") # nom des repetoires
    df_final = pd.DataFrame()
    for name in li_files:
        if os.path.isdir(name): # Si c'est un repertoire de piece de theatre
            folder_path = name + "/"
            csv_files = os.listdir(folder_path)
         
            for i in range(1,len(csv_files)): # csv files dans chaque repertoire de piece
                if (".csv" in csv_files[i] and "rolling_mean" not in csv_files[i]):
                    # initialiser df_final -------------------------------
                    if (i == 1):
                        df_final = pd.read_csv(folder_path + csv_files[1])
                        roll_mean = df_final["avgLexVal"].rolling(5).mean()
                        col_name = csv_files[i][:-4] # nom du sentiment
                        df_final[col_name + "_roll_mean"] = roll_mean
                    # ----------------------------------------------------
                    else:
                        df = pd.read_csv(folder_path + csv_files[i])
                        roll_mean = df["avgLexVal"].rolling(5).mean()
                        col_name = csv_files[i][:-4] # nom du sentiment
                        df_final[col_name + "_roll_mean"] = roll_mean # ajouter un nouvel col pour noter rolling mean
            if ("Unnamed: 0" in df_final.columns):
                df_final.drop("Unnamed: 0", axis=1, inplace=True)
            df_final.to_csv(folder_path + "rolling_mean.csv", index=False)

def write_csv(all_moyen):
    header = ["shortName", "drama_type", "valence", "arousal", "dominance", "anger"
    , "disgust", "fear", "joy", "sadness", "surprise", "trust", "anticipation"
    ]
    with open("all_pieces_info.csv", "w", encoding="utf-8") as out:
        writer = csv.writer(out)
        writer.writerow(header)
        writer.writerows(all_moyen)
    
def group_info():
    all_moyen = get_moyennes()
    write_csv(all_moyen)

# ------------------------------------------- make plots -----------------------------------------------

def plot_only_one_piece(file_path, emotion_list, filters):
    
    df = pd.read_csv(file_path, index_col = False)
    if (filters != []): # faire filtres
        my_hue = df[filters].apply(tuple, axis=1)
    emotion_label = emotion_list[0]

    if (filters and len(emotion_list)>1): # S'il y a emotions et filtres:
        graph = sb.scatterplot(y = emotion_list[1] + "_roll_mean", x = emotion_list[0]+"_roll_mean", data=df, hue = my_hue)
        graph.set_ylim(0,1)
        graph.set_xlim(0,1)
        graph.set_xlabel(emotion_list[0])
        graph.set_ylabel(emotion_list[1])
        plt.show()
    elif (len(emotion_list)>1): # Si y'a que deux emotions:
        for i in range(len(emotion_list)):
            graph = sb.lineplot(y = emotion_list[i] + "_roll_mean", x="progress", data=df, label = emotion_label, err_style = None)
    else: # s'il n'y a pas de filtres:
        graph = sb.lineplot(y = emotion_list[0] + "_roll_mean", x="progress", data=df, label = emotion_label, err_style = None)
    graph.set_ylim(0,1)

    graph.set_xlabel("progress of drama")
    graph.set_ylabel("emotion level")
    plt.show()

def plot_mv_avg(filename, emotion_list, filters):
    # filename est le fichier csv fait par R
    df = pd.read_csv(filename, index_col=False)
    if (filters != []):
        my_hue = df[filters].apply(tuple, axis=1)
    for i in range(len(emotion_list)):
        emotion_label = emotion_list[i] # nom d'emotion
        if (filters and emotion_list):
            graph = sb.lineplot(y=emotion_label, x="progress", data=df, hue = my_hue, err_style = None)
            graph.set_ylim(-1,1)
            graph.set_xlabel("progress of drama")
            graph.set_ylabel(emotion_label)
            plt.show()
        else:
            graph = sb.lineplot(y=emotion_label, x="progress", data=df, label = emotion_label, err_style = None)
    graph.set_ylim(-1,1)
    graph.set_xlabel("progress of drama")
    graph.set_ylabel("emotion level")
    plt.show()

def single_piece(mv_average):
    arg_len = len(sys.argv)
    filters = []
    if (arg_len == 4): # si on verifie emotions seulement
        folder = sys.argv[2]
        emotion_list = sys.argv[3].split(",") # it's a list
        
    elif(arg_len == 5): # si on verifie emotions + filters (nom des colonnes des fichiers csv)
        folder = sys.argv[2]
        emotion_list = sys.argv[3].split(",")
        filters = sys.argv[4].split(",")
        # print(emotion_list, filters)
    else:
        print("Input error\n")
        sys.exit(0)
    if (mv_average == False): # pour verifier s'il faut utiliser moving average
        filepath = folder + "/" + "rolling_mean.csv"
        plot_only_one_piece(filepath, emotion_list, filters)
    else:
        filepath = folder + "/" + "all_emo.csv" # nom du fichier fait par R
        plot_mv_avg(filepath, emotion_list, filters)

def more_pieces():
    query = ""
    df = pd.read_csv("all_pieces_info.csv")
    if (len(sys.argv) >= 4): # emotion ou shortName seulement || emotion + drama_type
        handle = sys.argv[2]     
        if (handle == "--emotion"):
            emotion = sys.argv[3]
            emotion = emotion.split(",")
            # print(emotion)
            if (len(sys.argv) == 4): # plot une seule emotion avec differents types de dramas (barplot)
                if (len(emotion) == 1):
                    graph = sb.barplot(data = df, x = "shortName", y = emotion[0], hue="drama_type")
                    graph.set_ylim(0,1)
                    plt.show()
                elif (len(emotion) == 2): # plot deux emotions avec differents types de dramas (scatterplot)
                    graph = sb.scatterplot(data = df, x = emotion[0], y = emotion[1], hue="drama_type")
                    graph.set_ylim(0,0.5)
                    graph.set_xlim(0,0.5)
                    plt.show()
                else:
                    print("Can only compare two emotions\n")
                    sys.exit(1)
            else: # plot emotion + drama type
                drama_type = sys.argv[4]
                query = "drama_type == '" + drama_type + "'"
                df = df.query(query)
                if (len(emotion) == 1): # barplot pour une seule emotion
                    graph = sb.barplot(data = df, x = "shortName", y = emotion[0], hue="drama_type")
                    graph.set_ylim(0,1)
                    plt.show()
                elif (len(emotion) == 2): # scatterplot pour 2 emotions
                    graph = sb.scatterplot(data = df, x = emotion[0], y = emotion[1], hue="drama_type")
                    graph.set_ylim(0,1)
                    graph.set_xlim(0,1)
                    plt.show()
                else:
                    print("Can only compare two emotions\n")
                    sys.exit(1)
        elif(handle == "--shortName"): # plot tous les emotions d'une seule piece
            shortName = sys.argv[3]
            query = "shortName == '" + shortName + "'"
            df = df.query(query)
            graph = sb.barplot(data = df)
            graph.set_title(shortName)
            plt.show()
    elif (len(sys.argv) == 2): # sans argument, plot tous
        graph = sb.pairplot(df, kind="reg", diag_kind="kde")
        plt.show()
    elif(len(sys.argv) == 3): # tous les theatres dans une meme categorie
        drama_type = sys.argv[2]
        query = "drama_type == '" + drama_type + "'"
        df = df.query(query)
        graph = sb.scatterplot(data = df)
        graph.set_ylim(0,1)
        graph.set_ylabel("emotion_coeffs")
        graph.set_title(drama_type)
        plt.show()
    else:
        print("Input error\n")
        sys.exit(1)


if __name__ == "__main__":
    add_rolling_mean()
    #group_info()

    if (sys.argv[1] == "single"):
        single_piece(mv_average = False)
    elif(sys.argv[1] == "group"):
        more_pieces()
    elif(sys.argv[1] == "mv_average"): # pour moving avg
        single_piece(mv_average = True)
    
