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
    """Function to do the visualization for single mode plot

    Args:
        param1: An array containing paths to files to be visualized.
        param2: An array containing names of emotions.
        param3: An array containing names of filters.
        param4: A String, path of directory to save figures.

    Returns:
        None

    """
    subplot_flag = False
    if len(file_paths) > 1:
        fig, axes = plt.subplots(1,len(file_paths))
        subplot_flag = True # to verify if we need to de sub-plot or not
    figure_num = 0
    for file_path in file_paths:
        df = pd.read_csv(file_path, index_col = False)
        if (filters != None and len(filters) > 1): # make filters
            my_hue = df[filters].apply(tuple, axis=1)

        if (filters and len(emotion_list)>1):
            if (len(filters) == 1):
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
        elif (len(emotion_list)>1):
            for i in range(len(emotion_list)):
                if (subplot_flag):
                    graph = sb.lineplot(ax = axes[figure_num], y = emotion_list[i] + "_roll_mean", x="progress", data=df, label = file_path[:-17] + "-" + emotion_list[i], err_style = None)
                else:
                    graph = sb.lineplot(y = emotion_list[i] + "_roll_mean", x="progress", data=df, label = file_path[:-17] + "-" + emotion_list[i], err_style = None)
        else: # If there's only one emotion and no filters, lineplot:
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
    """Function to do the visualization for group mode plot

    Args:
        param1: An array containing filenames.
        param2: An array containing names of emotions.
        param3: A String containing dramatype.
        param4: A String, path of directory to save figures.

    Returns:
        None

    """
    query = ""
    df = pd.read_csv("all_pieces_info.csv")

    if (pieces == "all"): 
        # pairplot for all pieces
        df = df.iloc[:,6:15]
        graph = sb.pairplot(df, kind="reg", diag_kind="kde")
        graph.set(xlim=(0,0.45), ylim = (0,0.45))
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
        if (len(emotions) == 1): # barplot for a single emotion
            graph = sb.barplot(data = df, x = "shortName", y = emotions[0], hue="drama_type")
            graph.set_ylim(0,1)
            if (savepath != None):
                savepath = savepath + "/" + dramatype + "_" + emotions[0] + ".png"
                plt.savefig(savepath)
            plt.show()
        elif (len(emotions) == 2): # scatterplot for 2 emotions
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
    """Function for treating arguments for the funtion plot_only_one_piece()

    Args:
        param1: A String containing filenames seperated by ",".
        param2: A String containing names of emotions seperated by ",".
        param3: A String containing names of filters seperated by ",".
        param4: A String, path of directory to save figures.

    Returns:
        None

    """
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
    
    # convert String into list
    if ("," in pieces):
        pieces_sep = pieces.split(",")

    emotion_list = emotions.split(",")    

    if(filters != None):
        filters = filters.split(",")
    if (filters == None and emotions == None):
        print("Input error\n")
        sys.exit(0)
    if (pieces_sep != []):
        for piece_name in pieces_sep:
            filepath.append(piece_name + "/" + "rolling_mean.csv")
    else:
        filepath.append(pieces + "/" + "rolling_mean.csv")
    plot_only_one_piece(filepath, emotion_list, filters, savepath)


def most_positive(pos, savepath):
    """Function to visualize the most positive or negative file

    Args:
        param1: A  boolean which define negative(False) or positive(True).
        param2: A String, path of directory to save figures.

    Returns:
        None

    """
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
    
    emotions = pd.Series(emotions)
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
