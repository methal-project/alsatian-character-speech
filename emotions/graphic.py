import seaborn as sb
import pandas as pd
import matplotlib.pyplot as plt
import sys
from scipy.stats import percentileofscore
from argparse import ArgumentParser

emotion_list = [
    "anger"
    , "disgust", "fear", "joy", "sadness", "surprise", "trust", "anticipation"
]

vad_list = ["valence", "arousal", "dominance"]


parser = ArgumentParser()
parser.add_argument("--mode", help = 'single or group')
parser.add_argument("--pieces", help= 'name of pieces, seperate by ","')
parser.add_argument("--emotions", help= 'name of emotions, seperate by ","')
parser.add_argument("--filters", help= 'name of filters, seperate by ","')
parser.add_argument("--savepath", help= 'a path to save graphics')
parser.add_argument("--dramatype", help= 'a type of drama')

# ------------------------------------------- make plots -----------------------------------------------

def plot_only_one_piece(file_paths, emotion_list, filters, savepath):
    subplot_flag = False
    if len(file_paths) > 1:
        fig, axes = plt.subplots(1,len(file_paths))
        subplot_flag = True # pour verifier si on a besoins de subplot
    figure_num = 0
    for file_path in file_paths:
        df = pd.read_csv(file_path, index_col = False)
        if (filters != None and len(filters) > 1): # faire filtres
            my_hue = df[filters].apply(tuple, axis=1)
        emotion_label = emotion_list[0]

        if (filters and len(emotion_list)>1): # S'il y a emotions et filtres:
            if (len(filters) == 1): # s'il y a qu'une filtre
                df = df.groupby([filters[0]]).mean()
                if (subplot_flag):
                    graph = sb.scatterplot(ax = axes[figure_num], y = emotion_list[1] + "_roll_mean", x = emotion_list[0]+"_roll_mean", data=df, hue = filters[0], label = file_path[:-17])
                else:
                    graph = sb.scatterplot(y = emotion_list[1] + "_roll_mean", x = emotion_list[0]+"_roll_mean", data=df, hue = filters[0], label = file_path[:-17])
            else:
                if (subplot_flag):
                    graph = sb.scatterplot(ax = axes[figure_num], y = emotion_list[1] + "_roll_mean", x = emotion_list[0]+"_roll_mean", data=df, hue = my_hue, label = file_path[:-17])
                else:
                    graph = sb.scatterplot(y = emotion_list[1] + "_roll_mean", x = emotion_list[0]+"_roll_mean", data=df, hue = my_hue, label = file_path[:-17])                   
            graph.set_ylim(0,8)
            graph.set_xlim(0,8)
            graph.set_xlabel(emotion_list[0])
            graph.set_ylabel(emotion_list[1])
            #plt.show()
        elif (len(emotion_list)>1): # Si y'a que deux emotions:
            for i in range(len(emotion_list)):
                if (subplot_flag):
                    graph = sb.lineplot(ax = axes[figure_num], y = emotion_list[i] + "_roll_mean", x="progress", data=df, label = file_path[:-17] + "-" + emotion_list[i], err_style = None)
                else:
                    graph = sb.lineplot(y = emotion_list[i] + "_roll_mean", x="progress", data=df, label = file_path[:-17] + "-" + emotion_list[i], err_style = None)
        else: # s'il n'y a pas de filtres, et qu'une emotion, alors lineplot:
            if(subplot_flag):
                graph = sb.lineplot(ax = axes[figure_num], y = emotion_list[0] + "_roll_mean", x="progress", data=df, label = file_path[:-17], err_style = None)
            else:
                graph = sb.lineplot(y = emotion_list[0] + "_roll_mean", x="progress", data=df, label = file_path[:-17], err_style = None)
            #graph.set_ylim(0,1)
            graph.set_xlabel("progress of drama")
            graph.set_ylabel("emotion level")
        figure_num += 1
    if (savepath != None):
        plt.savefig(savepath)
    plt.show()


def more_pieces(pieces, emotions, dramatype, savepath):
    query = ""
    df = pd.read_csv("all_pieces_info.csv")

    if (pieces == "all"): 
        # pairplot for all pieces
        df = df.iloc[:,6:15]
        graph = sb.pairplot(df, kind="reg", diag_kind="kde")
        graph.set(xlim=(0,0.45), ylim = (0,0.45)) # configurer les limites d'axes
        if (savepath != None):
            savepath = savepath + "/pairplot.png"
            plt.savefig(savepath)
        plt.show()
    elif (emotions != None and pieces == None and dramatype == None):
        # compare two emotions of all pieces
        emotions = emotions.split(",")
        graph = sb.scatterplot(data = df, x = emotions[0], y = emotions[1], hue="drama_type")
        graph.set_ylim(0,0.5)
        graph.set_xlim(0,0.5)
        if (savepath != None):
            savepath = savepath + "/" + emotions[0] + "_" + emotions[1] + ".png"
            plt.savefig(savepath)
        plt.show()
    elif (emotions != None and pieces != None and dramatype == None):
        # compare two emotions of selected pieces
        list_pieces = pieces.split(",")
        df = df[df["shortName"].isin(list_pieces)]
        emotions = emotions.split(",")
        graph = sb.scatterplot(data = df, x = emotions[0], y = emotions[1], hue="shortName")
        graph.set_ylim(0,0.5)
        graph.set_xlim(0,0.5)
        if (savepath != None):
            pieces = pieces.replace(",", "_")
            savepath = savepath + "/" + pieces + "_" + emotions[0] + "_" + emotions[1] + ".png"
            plt.savefig(savepath)
        plt.show()
    elif(emotions != None and pieces == None and dramatype != None):
        # compare two emotions with selected drama type
        query = "drama_type == '" + dramatype + "'"
        emotions = emotions.split(",")
        df = df.query(query)
        if (len(emotions) == 1): # barplot pour une seule emotion
            graph = sb.barplot(data = df, x = "shortName", y = emotions[0], hue="drama_type")
            graph.set_ylim(0,1)
            if (savepath != None):
                savepath = savepath + "/" + dramatype + "_" + emotions[0] + ".png"
                plt.savefig(savepath)
            plt.show()
        elif (len(emotions) == 2): # scatterplot pour 2 emotions
            graph = sb.scatterplot(data = df, x = emotions[0], y = emotions[1], hue="drama_type")
            graph.set_ylim(0,1)
            graph.set_xlim(0,1)
            if (savepath != None):
                savepath = savepath + "/" + dramatype + "_" + emotions[0] + "_" + emotions[1] + ".png"
                plt.savefig(savepath)
            plt.show()
    elif (pieces != None and emotions == None and dramatype == None):
        query = "shortName == '" + pieces + "'"
        df = df.query(query)
        graph = sb.barplot(data = df)
        graph.set_ylim(0,1)
        graph.set_title(pieces)
        pieces = pieces.replace(",","_")
        if (savepath != None):
                savepath = savepath + "/" + pieces + ".png"
                plt.savefig(savepath)
        plt.show()
    else:
        print("Input error\n")
        sys.exit(1)

def single_piece(pieces, emotions, filters, savepath):
    filepath = []
    pieces_sep = []
    if (pieces == None):
        print("input error, no pieces\n")
        sys.exit(1)
    if (emotions == None):
        print("input error, no emotions\n")
        sys.exit(1)
    
    # In order not to have "," in filename:
    if ("," in emotions):
        emotions_name = emotions.replace(",","_")
    else:
        emotions_name = emotions
    if (filters != None and "," in filters):
        filters_name = filters.replace(",","_")
    elif(filters != None):
        filters_name = filters
    pieces_name = pieces.replace(",","_")

    if (savepath != None and filters != None):
        savepath = savepath + "/" + pieces_name + "_" + emotions_name + "_" + filters_name + ".png"
    elif (savepath != None and filters == None):
        pieces_name = pieces.replace(",","_")
        savepath = savepath + "/" + pieces_name + "_" + emotions_name + "_" + ".png"
    
    # convertir les string into list
    if ("," in pieces):
        # Si c'est pieces separ par ",", alors:
        pieces_sep = pieces.split(",")
        # sinon, folder contient le nom du repetoire
    emotion_list = emotions.split(",")    

    if(filters != None): # si on verifie emotions + filters (nom des colonnes des fichiers csv)
        filters = filters.split(",")
        # print(emotion_list, filters)
    if (filters == None and emotions == None):
        print("Input error\n")
        sys.exit(0)
    if (pieces_sep != []): # Si les pieces sont separe par ","
        for piece_name in pieces_sep:
            filepath.append(piece_name + "/" + "rolling_mean.csv")
    else:
        filepath.append(pieces + "/" + "rolling_mean.csv")
    plot_only_one_piece(filepath, emotion_list, filters, savepath)


def most_positive(pos, savepath):
    df = pd.read_csv("all_pieces_info.csv")
    if (pos):
        index = df['polarity'].idxmax()
    else:
        index = df['polarity'].idxmin()

    print('Document:', df.loc[index]['shortName'])
    polarity = 'positive' if df.loc[index]['polarity'] > 0 else 'negative'
    print('Polarity:', polarity)
    emotions = {}
    for label in emotion_list:
        emotions[label] = percentileofscore(df[label], df.loc[index][label])
    
    # Sort by values (highest value first)
    emotions = pd.Series(emotions)#.sort_values()
    emotions.plot(kind='barh', xlim=(0, 100), title=df.loc[index]['shortName'])
    if (savepath != None):
        print ("figure saved in " + savepath)
        if (pos):
            savepath += "/most_positive.png"
        else:
            savepath += "/most_negative.png"
        plt.savefig(savepath)
    plt.show()

def main(mode, pieces, emotions, filters, savepath, dramatype):

    if (mode == "most_positive"):
        most_positive(True, savepath)
    elif(mode == "most_negative"):
        most_positive(False, savepath)
    elif(mode == "single"):
        single_piece(pieces, emotions, filters, savepath)
    elif(mode == "group"):
        more_pieces(pieces, emotions, dramatype, savepath)

if __name__ == "__main__":

    args = parser.parse_args()
    mode = args.mode
    pieces = args.pieces
    emotions = args.emotions
    filters = args.filters
    savepath = args.savepath
    dramatype = args.dramatype

    main(mode, pieces, emotions, filters, savepath, dramatype)
