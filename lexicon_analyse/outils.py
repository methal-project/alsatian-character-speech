import csv
import pandas as pd
import spacy as sp

nlp_fr = sp.load("fr_core_news_sm") # pour tokeniser textes en francais
block_flag = "fin_de_block"

# ------------------------------------ fonctions pour faire dictionnaire ------------------------------------

def dic_csv_feel(csv_feel):
    col_feel = ["word", "anger", "disgust", "fear", "joy", "sadness", "surprise"]

    # lire le fichier: 
    source_feel = pd.read_csv(csv_feel, sep=";", usecols=col_feel)
    source_feel = source_feel[col_feel]
    index = 0
    dic = {}
    
    for key in source_feel["word"]:
        dic[key] = source_feel.loc[index,"anger":"surprise"].values.tolist()
        index += 1
    return dic

def dic_csv_vad(csv_vad):
    col_vad = ["French-fr","Valence", "Arousal", "Dominance"]

    # lire le fichier: 
    source_vad = pd.read_csv(csv_vad, sep="\t", usecols=col_vad)
    index = 0
    dic = {}
    for key in source_vad["French-fr"]:
        dic[key] = source_vad.loc[index,"Valence":"Dominance"].values.tolist()
        index += 1
    return dic


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
    "fr", "valence", "arousal", "dominance", "anger", "disgust", "fear", "joy", "sadness", "surprise", "trust", "anticipation"
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
    sauvegarder dans un dictionnaire les données necessaires 
dans le fichier csv. le dictionnaire contient les mots Alsaciens
et leurs coefficients d'émotions
'''
def make_dic_als(csv):
    col_list = [
    "als", "valence", "arousal", "dominance", "anger"
    , "disgust", "fear", "joy", "sadness", "surprise", "trust", "anticipation"
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

def merge_dic_fr(dic_elal, dic_feel, dic_vad):
    hybrid_dic = {}
    found = False
    # merge d'abord vad avec fell
    for feel_key in dic_feel.keys():
        for vad_key in dic_vad.keys():
            if (feel_key == vad_key):
                hybrid_dic[feel_key] = dic_vad[vad_key] + dic_feel[feel_key]
    super_hybrid_dic = {}
    all_words_dic = {}
    for key in hybrid_dic.keys():
        for elal_key in dic_elal.keys():
            if (key == elal_key and found == False):
                super_hybrid_dic[key] = hybrid_dic[key] + dic_elal[elal_key][-2:]
                all_words_dic[key] = hybrid_dic[key] + dic_elal[elal_key][-2:]
                found = True
        if (found == False):
            all_words_dic[key] = hybrid_dic[key] + [0.0,0.0] # Si mots non trouve dans elal_key, alors coefs manquants = 0
        else:
            found = False
    return [super_hybrid_dic, all_words_dic]
            

# ----------------------------------------- fonctions pour la tokenization -------------------------------------------

def fr_token(phrase, fd, block_flag):
    doc = nlp_fr(phrase)
    for token in doc:
        fd.write(token.text + ";")
    fd.write("\n" + block_flag + "\n")

def fr_token_dict(phrase):
    doc = nlp_fr(phrase)
    words = []
    for token in doc:
        words.append(token.text)
    return words

def make_tokenfile_fr(f_in, f_out, size):
    block = ""
    with open(f_in, "r", encoding="utf-8") as fin:
        with open(f_out, "w", encoding="utf-8") as fout:
            fin_info = fin.readlines()
            file_len = len(fin_info)
            count_line = 0 # pour verifier si on est a la fin du fichier
            count = 0 # pour faire la block
            for line in fin_info:
                count_line += 1
                line = line.strip()
                if (count // size or count_line >= file_len):
                    if (count_line >= file_len):
                        block += line
                    fr_token(block, fout, block_flag)
                    count = 0
                    block = ""
                else:
                    block += line + "\n"
                    count += 1

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
def grab_keywords(dic, words):
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

# --------------------------------------- fonctions de la calculation des emotions --------------------------------------

def emotion_calculate(keyword):
    emotion = {
        "valence":0.0,
        "arousal":0.0,
        "dominance":0.0,
        "anger":0.0,
        "disgust":0.0,
        "fear":0.0,
        "joy":0.0,
        "sadness":0.0,
        "surprise":0.0,
        "trust":0.0,
        "anticipation":0.0,
    }
    col = 0
    vad = ""
    emo = ""
    vad_max = 0.0
    emo_base_max = 0.0
    for key_e in emotion.keys():
        for key in keyword.keys():
            emotion[key_e] += keyword[key][col]/len(keyword.keys())
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

# -------------------------------------------- fonctions qui gerent la sortie des analyses -------------------------

def make_csv_french_words(id_block, keyword, fout, emo_title_list, header_flag):
    dic_line = {}
    word_list = ["Id_block","Mots"] + emo_title_list
    writer = csv.DictWriter(fout, fieldnames = word_list)
    if (header_flag):
        writer.writeheader()
    for mot in keyword.keys():
        dic_line["Id_block"] = id_block
        dic_line["Mots"] = mot
        for i in range(len(emo_title_list)):
            dic_line[emo_title_list[i]] = keyword[mot][i]
        writer.writerows([dic_line])
    



def make_csv_emotion_moyen_block(id, dic_emotion, fout):
    dic_line = {}
    dic_line["index_block"] = id
    emo_list = ["index_block"]
    for emo in list(dic_emotion.keys())[:-2]:
        dic_line[emo] = format(dic_emotion[emo], ".3f")
        emo_list.append(emo)
    writer = csv.DictWriter(fout, fieldnames = emo_list)
    if (id == 1):
        writer.writeheader()
    if(dic_line):
        writer.writerows([dic_line])


# ------------------------------ Les fonctions puet-etre inutile -------------------------------

'''
entrée: 
    csv: fichier csv (type chaîne de caractères)
sortie: 
    dic: un dictionnaire (type dict)
objectif: 
    faire la même chose que make_fic_fr(), mais sans traiter
les celulles avec ";" 


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