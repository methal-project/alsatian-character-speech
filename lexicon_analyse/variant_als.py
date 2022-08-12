import pandas as pd
import sys,os
import alsatian_tokeniser
# nom de la lexique
filename = "source_files/ELAL_all.tsv"

df = pd.read_csv(filename, sep="\t")
df = df.iloc[:,[0,1]]
list_als = df.to_dict("split")["data"] # contient tous les mots als et les variantes

dict_replace = {}
for word in list_als:
    variantes = word[1].split(";")
    forme_ori = variantes[0] # une forme originale
    if ("_C" not in forme_ori): # on ignore les variantes a corriger avec _C
        for vari in variantes:
            if vari not in dict_replace:
                dict_replace[vari] = forme_ori

list_rolling_means = os.listdir("../emo_analyse")
for roll_mean in list_rolling_means:
    if os.path.isdir("../emo_analyse/" + roll_mean):
        df = pd.read_csv("../emo_analyse/" + roll_mean + "/rolling_mean.csv")
        print(df.head())
        group_progress = df.groupby("progress")
        for group_name,data in group_progress:
            print(group_name)
        df_progress = group_progress.get_group(2)["text"].values[:]
        print (df_progress)
        break


'''
list_text_brut = os.listdir("../text_brut") # noms des textes-bruts
ret = alsatian_tokeniser.RegExpTokeniser()

for text in list_text_brut:

    with open("../text_brut/" + text, "r", encoding="utf-8") as fd:
        als_tokens = []
        ori_text = fd.read()
        tokens = ret.tokenise(ori_text)
        tokens = tokens.get_tokens()

        with open ("../text_brut_replaced/" + text[:-4] + "_words_replaced.txt", "w", encoding="utf-8") as out1:
            for i in range(len(tokens)):
                token = tokens[i].get_contents()
                if (token in dict_replace.keys()):
                    ori_text = ori_text.replace(token, dict_replace[token])
                    out1.write(token + " => " + dict_replace[token] + "\n")
        with open ("../text_brut_replaced/" + text, "w", encoding="utf-8") as out2:
            out2.write(ori_text)

with open("variante_raplace.csv", "w", encoding="utf-8") as fd:
    fd.write("variante,forme\n")
    for k in dict_replace.keys():
        fd.write(k + "," + dict_replace[k] + "\n")
'''
