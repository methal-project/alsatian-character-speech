import os

folder_path = "D:/university/研一下期/analyse_emotion/pieces_more_info/tei2/"
li_files = os.listdir(folder_path)

for file in li_files:
    if ("xml" in file):
        os.rename(folder_path + file, folder_path + file[:-13] + ".xml")
    print(file[:-13] + ".xml")