import pandas as pd
import re

f_in = "al_hmr.txt"         # fichier d'entrée
f_out = "try_als.txt"           # fichier de sortie
f_csv = "ELAL_all.tsv"      # fichier lexicon d'émotions
emotion_list = [
    "valence", "arousal", "dominance", "anger", "anticipation"
    , "disgust", "fear", "joy", "sadness", "surprise", "trust"
]
regex = "[,|.| |?|!|\n]"
# liste d'émotions

'''
Quand il y a des cas avec ";", par exemple comme "claque;applaudir",
alors on ajoute des nouveux lignes pour chaque mots separe par ';'.

entrée: 
    csv: fichier csv (type chaîne de caractères)
sortie: 
    dic: un dictionnaire (type dict)
objectif: 
    sauvegarder dans un dictionnaire les données necessaires 
dans le fichier csv. le dictionnaire contient les mots français
et leurs coefficients d'émotions

'''
def make_dic_fr(csv):
    col_list = [
    "fr", "valence", "arousal", "dominance", "anger", "anticipation"
    , "disgust", "fear", "joy", "sadness", "surprise", "trust"
    ]
    source = pd.read_csv(csv, sep="\t", usecols=col_list)
    source = source.fillna(0)
    index = 0
    dic = {}
    for words in source["fr"]:
        if (str(words) != "0" and ";" in words): # cas avec ; dans la liste des mots
            try_list = words.split(";")
            copy = source.loc[index,"valence":"trust"].values.tolist()
            for key in try_list:
                if (key not in dic):
                    dic[key] = copy
        else: # cas normale (un seul mots dans la cellule)
            dic[words] = source.loc[index,"valence":"trust"].values.tolist()
        index += 1
    return dic
'''
entrée: 
    csv: fichier csv (type chaîne de caractères)
sortie: 
    dic: un dictionnaire (type dict)
objectif: 
    faire la même chose que make_fic_fr(), mais sans traiter
les celulles avec ";" 

'''
def make_dic_fr_simple(csv):
    col_list = [
    "fr", "valence", "arousal", "dominance", "anger", "anticipation"
    , "disgust", "fear", "joy", "sadness", "surprise", "trust"
    ]
    source = pd.read_csv(csv, sep="\t", usecols=col_list)
    source = source.fillna(0)
    index = 0
    dic = {}
    for key in source["fr"]:
        dic[key] = source.loc[index,"valence":"trust"].values.tolist()
        index += 1
    return dic

'''
entrée: 
    csv: fichier csv (type chaîne de caractères)
sortie: 
    dic: un dictionnaire (type dict)
objectif: 
    sauvegarder dans un dictionnaire les données necessaires 
dans le fichier csv. le dictionnaire contient les mots Alsaciens
et leurs coefficients d'émotions
'''
def make_dic_als(csv):
    col_list = [
    "als", "valence", "arousal", "dominance", "anger", "anticipation"
    , "disgust", "fear", "joy", "sadness", "surprise", "trust"
    ]
    source = pd.read_csv(csv, sep="\t", usecols=col_list)
    source = source.fillna(0)
    index = 0
    dic = {}
    for words in source["als"]:
        if (str(words) != "0" and ";" in words): # cas avec ; dans la liste des mots
            try_list = words.split(";")
            copy = source.loc[index,"valence":"trust"].values.tolist()
            for key in try_list:
                if (key not in dic):
                    dic[key] = copy
        else: # cas normale (un seul mots dans la cellule)
            dic[words] = source.loc[index,"valence":"trust"].values.tolist()
        index += 1
    return dic

'''
entrée: 
    dic: un dictionnaire (type dict)
    phrase: phrase où on cherché de mots-clés. (type chaîne de caractère)
sortie: 
    keywords: tous les mots-clés avec coefficients d'émotion (type dict)
objectif: 
    rechercher les mots-clés dans la phrase donnée selon le dictionnaire,
et sauvegarder les résultats dans un dictionnaire "keywords"
'''
def grab_keywords(dic, phrase):
    words = re.split(regex, phrase)
    keywords = {}
    for word in words:
        if (word not in keywords.keys() and word in dic.keys()):
            keywords[word] = dic[word]
    return keywords

'''
entrée:     
    keywords: tous les mots-clés avec coefficients d'émotion (type dict)
sortie: 
    emotion: un dictionnaire qui contient tous les coefficients
finales des emotions. (type dict)
objectif: 
    calculer la somme des coefficients de chaque emotion selon les mots-clés.
et trouver le coefficient le plus grand pour VAD et emotions de base.
'''

def emotion_calculate(keyword):
    emotion = {
        "valence":0,
        "arousal":0,
        "dominance":0,
        "anger":0,
        "anticipation":0,
        "disgust":0,
        "fear":0,
        "joy":0,
        "sadness":0,
        "surprise":0,
        "trust":0,
    }
    col = 0
    vad = ""
    emo = ""
    vad_max = 0
    emo_base_max = 0
    for key_e in emotion.keys():
        for key in keyword.keys():
            emotion[key_e] += keyword[key][col]
        # trouver le max dans vad
        if (col < 3):
            if (emotion[key_e] > vad_max):
                vad_max = emotion[key_e]
                vad = key_e
        else:
            if (emotion[key_e] > emo_base_max):
                emo_base_max = emotion[key_e]
                emo = key_e
        col += 1
    emotion.update({"vad_max":[vad, str(format(vad_max, ".3f"))], "emo_base_max":[emo, str(format(emo_base_max, ".3f"))]})
    return emotion

# ---------------------- main operations --------------------
count = 0
size = 5
block = ""
keyword = {}
keywords = {}
emotion = {}
dic = make_dic_als(f_csv)


try:
    with open(f_in, "r", encoding="utf-8") as fin:
        with open(f_out, "w", encoding="utf-8") as fout:
            fin_info = fin.readlines()
            file_len = len(fin_info)
            count_line = 0
            for line in fin_info:
                count_line += 1
                line = line.strip()
                if (count // size or count_line >= file_len):
                    if (count_line >= file_len):
                        block += line
                    keyword = grab_keywords(dic,block)
                    keywords.update(keyword) # variable pour sauvegarder tous les mots trouve
                    fout.write(block)
                    # resultats des mots-cles:
                    fout.write("\nMots-clés: \n\t")
                    for emo in emotion_list: # écrire chaque titre d'émotion
                        fout.write (emo + "\t")
                    fout.write("\n\n")
                    for key in keyword.keys(): # écrire chaque mots-clés et leurs coefficients
                        fout.write(key + "\t")
                        for score in keyword[key]:
                            fout.write(str(format(score, ".3f")) + "\t")
                        fout.write("\n")
                    # calculation des emotions:
                    fout.write("\nconclusions: \n")
                    emotion = emotion_calculate(keyword)
                    fout.write("vad: " + emotion["vad_max"][0] + ", " + emotion["vad_max"][1] +
                    "\nemotion base: " + emotion["emo_base_max"][0] + ", " + emotion["emo_base_max"][1] + "\n\n\n")

                    fout.write("----------------------------------------------------------------------------------------------------------------\n")
                    block = ""
                    count = 0
                else:
                    block += line + "\n"
                    count += 1
except OSError as err :
    print("Une erreur",err)
