from dataclasses import replace
import pandas as pd
import os
import alsatian_tokeniser
from sklearn.feature_extraction.text import TfidfVectorizer
# nom de la lexique
filename = "source_files/ELAL_all.tsv"

df = pd.read_csv(filename, sep="\t")
df = df.iloc[:,[0,1]]
list_als = df.to_dict("split")["data"] # contient tous les mots als et les variantes

# -------------------------------------------- faire un dictionnaire de remplacement ----------
dict_replace = {}
for word in list_als:
    variantes = word[1].split(";")
    forme_ori = variantes[0] # une forme originale
    if ("_C" not in forme_ori): # on ignore les variantes a corriger avec _C
        for vari in variantes:
            if vari not in dict_replace:
                dict_replace[vari] = forme_ori

list_tei = os.listdir("../pieces_more_info/treated_files/tei/")
list_tei_lustig = os.listdir("../pieces_more_info/treated_files/tei-lustig/")
list_tei2 = os.listdir("../pieces_more_info/treated_files/tei2/")
#list_treated_files = list_tei + list_tei_lustig + list_tei2

#all_tourne_parole = [] # liste qui contient toutes les paroles

# -------------------------------------- lire fichiers csv et remplacer les variantes ------------------

path = "../pieces_more_info/treated_files/"
ret = alsatian_tokeniser.RegExpTokeniser()
folders = ["tei", "tei-lustig", "tei2"]


for folder in folders:
    if folder == "tei":
        list_treated_files = list_tei
    elif folder == "tei-lustig":
        list_treated_files = list_tei_lustig
    else:
        list_treated_files = list_tei2

    for file in list_treated_files:

        single_piece_tourne_parole = []
        df = pd.read_csv(path + folder + "/" + file)
        text = ""
        for i in range(df.shape[0]): # df.shape[0] == nombre de lignes
            # for each phrase
            #replaced = False
            text = df["text"].values[i]
            rep_text = text
            tokens = ret.tokenise(text)
            tokens = tokens.get_tokens()
            for i in range(len(tokens)):
                # for each word
                tok = tokens[i].get_contents()
                if (tok in dict_replace.keys()):
                    #replaced = True
                    rep_text = rep_text.replace(tok, dict_replace[tok])
                    #print (tok + " => " + dict_replace[tok] + "\n")
            '''if (replaced == True):
                print(text + " => " + rep_text)
                replaced = False'''
            single_piece_tourne_parole.append(rep_text)

            df = df.replace(text, rep_text)

        df.to_csv("../csv_replaced/" + file, index = False)

# ----------------------------------------- mtn calculate idfs ---------------------------------------- 
        
        #df_replaced = pd.read_csv("../csv_replaced/" + file)
        '''group_progress = df_replaced.groupby("progress")

        for group_name,data in group_progress:
            df_progress = group_progress.get_group(group_name)["text"].values[:]
            single_piece_tourne_parole.append(df_progress[0])'''
            #all_tourne_parole.append(df_progress[0])
        # calculate tf-idf pour une seule piece:

        idf_vectorizer = TfidfVectorizer(input="content", encoding="utf-8")
        idf_vector = idf_vectorizer.fit_transform(single_piece_tourne_parole)
        idf_df = pd.DataFrame(idf_vector.toarray(), columns = idf_vectorizer.get_feature_names_out())
        idf_df.to_csv("../idf_info/" + file[:-8] + ".csv",index=False)




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
