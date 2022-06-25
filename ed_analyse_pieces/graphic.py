import seaborn as sb
import pandas as pd
import matplotlib.pyplot as plt
import sys, os
import csv

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
                    # get first 10% largest values, and then their mean
                    num_rows = df.shape[0]
                    if (num_rows // 10 == 0):
                        num_largest_coeffs = 1
                    else:
                        num_largest_coeffs = num_rows // 10
                    df_largest = df.nlargest(num_largest_coeffs, "avgLexVal")
                    piece_moyen.append(df_largest["avgLexVal"].mean())
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

# ------------------------------------------- make plots -----------------------------------------------

def plot_only_one_piece(file_paths, emotion_list, filters):
    for i in range(len(file_paths)):
        df = pd.read_csv(file_paths[i], index_col = False)
        if (filters != []):
            my_hue = df[filters].apply(tuple, axis=1)
        emotion_label = emotion_list[i]

    #df = df.query("speaker == 'Ne Pierrot'")
        if (filters and emotion_list):
            graph = sb.lineplot(y="avgLexVal", x="progress", data=df, hue = my_hue, err_style = None)
            graph.set_ylim(0,1)
            '''if (x_ticks):
                graph.set_xticks(x_ticks)'''
            graph.set_xlabel("progress of drama")
            graph.set_ylabel(emotion_label)
            plt.show()
        else:
            graph = sb.lineplot(y="avgLexVal", x="progress", data=df, label = emotion_label, err_style = None)
    graph.set_ylim(0,1)
    graph.set_xlabel("progress of drama")
    '''if (x_ticks):
        graph.set_xticks(x_ticks)'''
    graph.set_ylabel("emotion level")
    plt.show()

def plot_mv_avg(filename, emotion_list, filters):
    df = pd.read_csv(filename, index_col=False)
    if (filters != []):
        my_hue = df[filters].apply(tuple, axis=1)
    for i in range(len(emotion_list)):
        emotion_label = emotion_list[i]
        if (filters and emotion_list):
            graph = sb.lineplot(y=emotion_label, x="progress", data=df, hue = my_hue, err_style = None)
            graph.set_ylim(-1,1)
            '''if (x_ticks):
                graph.set_xticks(x_ticks)'''
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
    if (arg_len == 4): # if we check emotions only
        folder = sys.argv[2]
        emotion_list = sys.argv[3].split(",") # it's a list
        
    elif(arg_len == 5): # if we check emotions + filters (col name of csv files)
        folder = sys.argv[2]
        emotion_list = sys.argv[3].split(",")
        filters = sys.argv[4].split(",")
        print(emotion_list, filters)
    else:
        print("Input error\n")
        sys.exit(0)
    if (mv_average == False):
        filepath = []
        for filename in emotion_list:
            filepath.append(folder + "/" + filename + ".csv")
        plot_only_one_piece(filepath, emotion_list, filters)
    else:
        filepath = folder + "/" + "all_emo.csv"
        plot_mv_avg(filepath, emotion_list, filters)

def more_pieces():
    query = ""
    df = pd.read_csv("all_pieces_info.csv")
    if (len(sys.argv) >= 4): # emotion or shortName seulement || emotion + drama_type
        handle = sys.argv[2]     
        if (handle == "--emotion"):
            emotion = sys.argv[3]
            emotion = emotion.split(",")
            print(emotion)
            if (len(sys.argv) == 4):
                if (len(emotion) == 1):
                    graph = sb.barplot(data = df, x = "shortName", y = emotion[0], hue="drama_type")
                    graph.set_ylim(0,1)
                    plt.show()
                elif (len(emotion) == 2):
                    graph = sb.scatterplot(data = df, x = emotion[0], y = emotion[1], hue="drama_type")
                    graph.set_ylim(0,1)
                    graph.set_xlim(0,1)
                    plt.show()
                else:
                    print("Can only compare two emotions\n")
                    sys.exit(1)
            else: # emotion + drama type
                drama_type = sys.argv[4]
                query = "drama_type == '" + drama_type + "'"
                df = df.query(query)
                if (len(emotion) == 1):
                    graph = sb.barplot(data = df, x = "shortName", y = emotion[0], hue="drama_type")
                    graph.set_ylim(0,1)
                    plt.show()
                elif (len(emotion) == 2):
                    graph = sb.scatterplot(data = df, x = emotion[0], y = emotion[1], hue="drama_type")
                    graph.set_ylim(0,1)
                    graph.set_xlim(0,1)
                    plt.show()
                else:
                    print("Can only compare two emotions\n")
                    sys.exit(1)
        elif(handle == "--shortName"):
            shortName = sys.argv[3]
            query = "shortName == '" + shortName + "'"
            df = df.query(query)
            graph = sb.barplot(data = df)
            graph.set_title(shortName)
            plt.show()
    elif (len(sys.argv) == 2): # sans argument, plot tous
        graph = sb.scatterplot(data = df)
        graph.set_ylabel("emotion_coeffs")
        graph.set_ylim(0,1)
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
    if (sys.argv[1] == "single"):
        single_piece(mv_average = False)
    elif(sys.argv[1] == "group"):
        more_pieces()
    elif(sys.argv[1] == "mv_average"):
        single_piece(mv_average = True)
    # df = df.query("shortName == 'am-letzte-maskebal' or shortName == 'arnold-der-pfingstmontag'")
    # group_info()
