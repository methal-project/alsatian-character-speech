import seaborn as sb
import pandas as pd
import matplotlib.pyplot as plt
import sys, os

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

def main():
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
    

if __name__ == "__main__":
    main()