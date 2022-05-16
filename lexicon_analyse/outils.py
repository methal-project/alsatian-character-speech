import csv
import pandas as pd
import spacy as sp
import alsatian_tokeniser as at
import re

nlp_fr = sp.load("fr_core_news_sm") # pour tokeniser textes en francais
block_flag = "fin_de_block"
column_order = {"anger":3, "disgust":4, "fear":5, "joy":6, "sadness":7, "surprise":8, "trust":9, "anticipation":10}
emotion_list = [
    "valence", "arousal", "dominance", "anger"
    , "disgust", "fear", "joy", "sadness", "surprise", "trust", "anticipation"
]
regex = "[,|.| |?|!|\n]"

# ------------------------------------ fonctions pour faire dictionnaire ------------------------------------

'''
entrée: 
    csv_feel: fichier csv (type chaîne de caractères)
sortie: 
    dic: un dictionnaire (type dict)
objectif: 
    sauvegarder dans un dictionnaire les données necessaires 
dans le fichier csv (NRC).  le dictionnaire contient les mots français
et leurs coefficients d'émotions (6 emotions de base)

'''

def make_dic_feel(csv_feel):
    col_feel = ["word", "anger", "disgust", "fear", "joy", "sadness", "surprise"]

    # lire le fichier: 
    source_feel = pd.read_csv(csv_feel, sep=";", usecols=col_feel)
    source_feel = source_feel[col_feel]
    index = 0
    dic = {}
    
    for key in source_feel["word"]:
        dic[key] = source_feel.reindex(col_feel, axis="columns").loc[index,"anger":"surprise"].values.tolist()
        index += 1
    return dic

'''
entrée: 
    csv_vad: fichier csv (type chaîne de caractères)
sortie: 
    dic: un dictionnaire (type dict)
objectif: 
    sauvegarder dans un dictionnaire les données necessaires 
dans le fichier csv (NRC). le dictionnaire contient les mots français
et leurs coefficients d'émotions (dimensions VAD)

'''
def make_dic_vad(csv_vad):
    col_vad = ["French-fr","Valence", "Arousal", "Dominance"]

    # lire le fichier: 
    source_vad = pd.read_csv(csv_vad, sep="\t", usecols=col_vad)
    index = 0
    dic = {}
    for key in source_vad["French-fr"]:
        dic[key] = source_vad.reindex(col_vad, axis="columns").loc[index,"Valence":"Dominance"].values.tolist()
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
def make_dic_elal(csv):
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
            copy = source.reindex(col_list, axis="columns").loc[index,"valence":"anticipation"].values.tolist()
            for key in try_list:
                if (key not in dic):
                    dic[key] = copy
        else: # cas normale (un seul mots dans la cellule)
            dic[words] = source.reindex(col_list, axis="columns").loc[index,"valence":"anticipation"].values.tolist()
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
            copy = source.reindex(col_list, axis="columns").loc[index,"valence":"anticipation"].values.tolist()
            for key in try_list:
                if (key not in dic):
                    dic[key] = copy
        else: # cas normale (un seul mots dans la cellule)
            dic[words] = source.reindex(col_list, axis="columns").loc[index,"valence":"anticipation"].values.tolist()
        index += 1
    return dic


'''
entrée: 
    dic_elal: dict (sortie de la fonction make_dic_elal)
    dic_feel: dict (sortie de la fonction make_dic_feel)
    dic_vad:  dict (sortie de la fonction make_dic_vad)
sortie: 
    super_hybird_dic: dict qui contient tous les mots en common de 3 dictionnaires
    all_words_dic: dict qui contient tous les mots en common de feel et vad et aussi les mots dans elal
objectif: 
    merge les trois dictionnaires et obtenir 2 nouveaux dictionnaires
    qui contient les mots en commun et les mots totals

'''
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
            
def NRC_intensif_to_FEEL(all_words_dic, nrc_intensif_file, nrc_intensif_moyen):
    with open(nrc_intensif_file, "r", encoding="utf-8") as fd_nrc:
        for line in fd_nrc:
            line = line.strip()
            list_line = line.split("\t")
            key = list_line[1]
            emotion = list_line[2]
            score = list_line[3]
            if (key in all_words_dic):
                if (float(score) >= nrc_intensif_moyen[emotion]):
                    all_words_dic[key][column_order[emotion]] = 1


        return all_words_dic



# ----------------------------------------- fonctions pour la tokenization -------------------------------------------

'''
faire la tokenisation d'une phrase et écrire les tokens dans un fichier.
les tokens sont séparé par ";"
'''
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

def calculate_moyenne_nrc_intensif(nrc_intensif_file):
    df = pd.read_csv(nrc_intensif_file, sep="\t", usecols=["French-fr", "emotion", "emotion-intensity-score"])
    moyen = df.groupby("emotion")["emotion-intensity-score"].mean()
    moyen = moyen.to_dict()
    return moyen

# -------------------------------------------- fonctions qui gerent la sortie des analyses -------------------------
'''
entrée: 
    id_block:   int     index du bloc
    keyword:    dict    mots-clés trouvés
    fout:       file_descripter fichier de sortie
    emo_title_list: list    titre de chaque colonne dans fichier csv
    header_flag: bool   utilisé pour vérifier si on doit écrire le titre de colonne ou pas
sortie: 
objectif: 
    faire un fichier csv de tous les mots-clés trouvés
'''
def make_csv_words(id_block, keyword, fout, emo_title_list, header_flag):
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

'''
entrée: 
    mots_csv_in:    nom du fichier csv qui contient les mots-cles
    moyen_csv_out:  nom du fichier csv de la sortie
sortie: 
objectif: 
    faire un fichier csv qui affiche toutes les moyennes d'emotions de chaque bloc
'''
def make_csv_moyen(mots_csv_in, moyen_csv_out):
    df = pd.read_csv(mots_csv_in, sep=",")
    df = df.groupby("Id_block")[["valence", "arousal", "dominance", "anger", "disgust", "fear", "joy", 
    "sadness", "surprise", "trust", "anticipation"]].mean()
    df.to_csv(moyen_csv_out)


def make_csv_fr(dic_all_words,f_token_fr, out_file):
    with open(f_token_fr, "r", encoding="utf-8") as fin_token:
        with open(out_file, "w", encoding="utf-8") as mots_fr_out:
            words = []
            block = ""
            header_flag = True
            id_block = 0
            for line in fin_token:
                line = line.strip()
                if (block_flag not in line):
                    block += line 
                else:
                    words = block.split(";")
                    keyword = grab_keywords(dic_all_words, words)
                    make_csv_words(id_block,keyword, mots_fr_out, emotion_list, header_flag)
                    header_flag = False
                    block = ""
                    id_block += 1

def make_csv_als(dic,size, f_in_als, out_file):
    keyword = {}
    block = ""
    with open(f_in_als, "r", encoding="utf-8") as fin:
        with open(out_file, "w", encoding="utf-8") as fout:
            fin_info = fin.readlines()
            file_len = len(fin_info)
            count_line = 0 # pour verifier si on est a la fin du fichier
            count = 0 # pour faire la block
            id_block = 0
            header_flag = True
            for line in fin_info:
                line = line.strip()
                if (count // size or count_line >= file_len):
                    if (count_line >= file_len):
                        block += line
                    ret = at.RegExpTokeniser()
                    phrase = (ret.tokenise(block)).get_contents()
                    tokens = re.split(regex, phrase)
                    keyword = grab_keywords(dic, tokens)
                    make_csv_words(id_block, keyword, fout, emotion_list, header_flag)
                    header_flag = False
                    count = 0
                    block = ""
                    id_block += 1
                else:
                    block += line + "\n"
                    count += 1
                count_line += 1

# ------------------------------ fonctions qui faire fichiers de textes ------------------------

def make_text(f_in, f_out, dic_all_words):
    count = 0
    size = 5
    block = ""
    keyword = {}
    emotion = {}
    df_text_block = []

    try:
        with open(f_in, "r", encoding="utf-8") as fin:
            with open(f_out, "w", encoding="utf-8") as fout:                 
                fin_info = fin.readlines()
                file_len = len(fin_info)
                count_line = 0
                count_id = 0
                for line in fin_info:
                    count_line += 1
                    line = line.strip()
                    if (count // size or count_line >= file_len):
                        if (count_line >= file_len):
                            block += line
                        words = fr_token_dict(block)
                        keyword = grab_keywords(dic_all_words,words)
                        fout.write("Index block: " + str(count_id) + "\n")
                        count_id += 1
                        fout.write(block)
                        df_text_block.append(block)
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

                        fout.write("Moyenne: \n")
                        for emo in emotion.keys():
                            fout.write(emo + ": " + str(emotion[emo]) + "\t")

                        fout.write("\nvad: " + emotion["vad_max"][0] + ", " + emotion["vad_max"][1] +
                        "\nemotion base: " + emotion["emo_base_max"][0] + ", " + emotion["emo_base_max"][1] + "\n\n\n")

                        fout.write("----------------------------------------------------------------------------------------------------------------\n")
                        block = ""
                        count = 0
                    else:
                        block += line + "\n"
                        count += 1
    except OSError as err :
        print("Une erreur",err)
    return df_text_block


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
'''