import seaborn as sb
import pandas as pd
import matplotlib.pyplot as plt
import sys, os
import csv

def plot_emotion(file_paths, emotion_list, filters):
    for i in range(len(file_paths)):
        df = pd.read_csv(file_paths[i], index_col = False)
        if (filters != []):
            my_hue = df[filters].apply(tuple, axis=1)
        emotion_label = emotion_list[i]
    #df = df.query("speaker == 'Ne Pierrot'")
        if (filters and emotion_list):
            graph = sb.lineplot(y="avgLexVal", x="Unnamed: 0", data=df, hue = my_hue)
            graph.set_ylim(0,1)
            graph.set_xlabel("progress of drama")
            graph.set_ylabel(emotion_label)
            plt.show()
        else:
            graph = sb.lineplot(y="avgLexVal", x="Unnamed: 0", data=df, label = emotion_label)
    graph.set_ylim(0,1)
    graph.set_xlabel("progress of drama")
    graph.set_ylabel("emotion level")
    plt.show()

def get_moyennes():
    all_moyen = []
    piece_moyen = []
    li_files = os.listdir(".")
    for name in li_files:
        if os.path.isdir(name): # Si c'est un repertoire de piece de theatre
            drama_type = False
            piece_moyen.append(name)
            folder_path = name + "/"
            csv_files = os.listdir(folder_path)
            for csv_file in csv_files: # csv files dans chaque repertoire de piece
                if (".csv" in csv_file):
                    df = pd.read_csv(folder_path + csv_file)
                    if (drama_type == False):
                        piece_moyen.append(df["drama_type"].values[0])
                        drama_type = True
                    piece_moyen.append(df["avgLexVal"].mean())
            all_moyen.append(piece_moyen)
            piece_moyen = []
    return all_moyen

def write_csv(all_moyen):
    header = ["shortName", "drama_type", "anger", "anticipation", "arousal", 
    "disgust", "dominance", "fear", "joy", "sadness", "surprise", "trust", "valence"
    ]
    with open("all_pieces_info.csv", "w", encoding="utf-8") as out:
        writer = csv.writer(out)
        writer.writerow(header)
        writer.writerows(all_moyen)
    
def group_info():
    all_moyen = get_moyennes()
    write_csv(all_moyen)
    

def single_piece():
    arg_len = len(sys.argv)
    filters = []
    if (arg_len == 3): # si y'a deux args
        folder = sys.argv[1]
        emotion_list = sys.argv[2].split(",") # it's a list
        
    elif(arg_len == 4):
        folder = sys.argv[1]
        emotion_list = sys.argv[2].split(",")
        filters = sys.argv[3].split(",")
        print(emotion_list, filters)
    else:
        print("Input error\n")
        sys.exit(0)
    
    filepath = []
    for filename in emotion_list:
        filepath.append(folder + "/" + filename + ".csv")
    plot_emotion(filepath, emotion_list, filters)

def more_pieces():
    query = ""
    df = pd.read_csv("all_pieces_info.csv")
    if (len(sys.argv) >= 3): # emotion or shortName seulement || emotion + drama_type
        handle = sys.argv[1]     
        if (handle == "--emotion"):
            emotion = sys.argv[2]
            if (len(sys.argv) == 3):
                graph = sb.barplot(data = df, x = "shortName", y = emotion, hue="drama_type")
                graph.set_ylim(0,1)
                plt.show()
            else:
                drama_type = sys.argv[3]
                query = "drama_type == '" + drama_type + "'"
                df = df.query(query)
                graph = sb.barplot(data = df, x = "shortName", y = emotion, hue="drama_type")
                graph.set_ylim(0,1)
                plt.show()
        elif(handle == "--shortName"):
            shortName = sys.argv[2]
            query = "shortName == '" + shortName + "'"
            df = df.query(query)
            graph = sb.barplot(data = df)
            graph.set_title(shortName)
            plt.show()
    elif (len(sys.argv) == 1): # sans argument, plot tous
        graph = sb.barplot(data = df)
        graph.set_ylim(0,1)
        plt.show()
    elif(len(sys.argv) == 2): # tous les theatres dans une meme categorie
        drama_type = sys.argv[1]
        query = "drama_type == '" + drama_type + "'"
        df = df.query(query)
        graph = sb.barplot(data = df)
        graph.set_ylim(0,1)
        graph.set_title(drama_type)
        plt.show()


if __name__ == "__main__":
    #single_piece()
    #df = df.query("shortName == 'am-letzte-maskebal' or shortName == 'arnold-der-pfingstmontag'")
    more_pieces()