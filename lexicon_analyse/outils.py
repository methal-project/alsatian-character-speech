import csv
import pandas as pd
import spacy as sp
import alsatian_tokeniser as at
import re

#nlp_fr = sp.load("fr_core_news_sm") # pour tokeniser textes en francais
block_flag = "fin_de_block"
column_order = {"anger":3, "disgust":4, "fear":5, "joy":6, "sadness":7, "surprise":8, "trust":9, "anticipation":10}
emotion_list = [
    "valence", "arousal", "dominance", "anger"
    , "disgust", "fear", "joy", "sadness", "surprise", "trust", "anticipation"
]
emotion_list_bi = ["valence", "arousal", "dominance", "anger"
    , "disgust", "fear", "joy", "sadness", "surprise"]
regex = "[,|.| |?|!|\n]"

# ------------------------------------ fonctions pour faire dictionnaire ------------------------------------


def make_dic_feel(csv_feel):
    '''
    Faire un dictionnaire de FEEL.

    Parameters:
        csv_feel (string): fichier csv

    Returns:
        dic (dict): un dictionnaire qui contient les mots français
        et leurs coefficients d'émotions (6 emotions de base)
    '''
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


def make_dic_vad(csv_vad):
    '''
    Faire un dictionnaire de NRC-VAD.

    Parameters:
        csv_vad (string): fichier csv

    Returns:
        dic (dict): un dictionnaire qui contient les mots français
        et leurs coefficients d'émotions (dimensions VAD)
    '''
    col_vad = ["French-fr","Valence", "Arousal", "Dominance"]

    # lire le fichier: 
    source_vad = pd.read_csv(csv_vad, sep="\t", usecols=col_vad)
    source_vad = source_vad.reindex(col_vad, axis="columns")
    ed_source = source_vad.rename(columns={"French-fr":"word"})
    ed_source.to_csv("../emotion_dynamics_essaie/NRC-VAD-fr-lexicon.csv", float_format="%.3f")
    
    index = 0
    dic = {}
    for key in source_vad["French-fr"]:
        dic[key] = source_vad.loc[index,"Valence":"Dominance"].values.tolist()
        index += 1
    return dic


def make_dic_elal(csv, binary):
    '''
    Faire un dictionnaire de ELAL fr.

    Parameters:
        csv (string): fichier csv
        binary (bool): verifier si binairiser les coefficients
    Returns:
        dic (dict): un dictionnaire qui contient les mots français
        et leurs coefficients d'émotions
    '''
    col_list = [
    "fr", "valence", "arousal", "dominance", "anger", "disgust", "fear", "joy", "sadness", "surprise", "trust", "anticipation"
    ]
    col_list_bi = [
    "fr", "valence", "arousal", "dominance", "anger", "disgust", "fear", "joy", "sadness", "surprise"]
    if (binary):
        source = pd.read_csv(csv, sep="\t", usecols=col_list_bi)
    else:
        source = pd.read_csv(csv, sep="\t", usecols=col_list)
    source = source.fillna(0)
    index = 0
    dic = {}
    for words in source["fr"]:
        if (str(words) != "0" and ";" in words): # cas avec ; dans la liste des mots
            try_list = words.split(";")
            if (binary):
                copy = source.reindex(col_list, axis="columns").loc[index,"valence":"surprise"].values.tolist()
                for i in range(3,len(copy)):
                    if copy[i] >= 0.5:
                        copy[i] = 1
                    else:
                        copy[i] = 0
            else:
                copy = source.reindex(col_list, axis="columns").loc[index,"valence":"anticipation"].values.tolist()
            for key in try_list:
                if (key not in dic):
                    dic[key] = copy
        else: # cas normale (un seul mots dans la cellule)
            if (binary):
                dic[words] = source.reindex(col_list, axis="columns").loc[index,"valence":"surprise"].values.tolist()
                for i in range(3,len(copy)):
                    if copy[i] >= 0.5:
                        copy[i] = 1
                    else:
                        copy[i] = 0
            else:
                dic[words] = source.reindex(col_list, axis="columns").loc[index,"valence":"anticipation"].values.tolist()
        index += 1
    return dic

def make_dic_als(csv, binary):
    '''
    Faire un dictionnaire de ELAL alsacien.

    Parameters:
        csv (string): fichier csv
        binary (bool): verifier si binairiser les coefficients
    Returns:
        dic (dict): un dictionnaire qui contient les mots alsacien
        et leurs coefficients d'émotions
    '''
    col_list = [
    "als", "valence", "arousal", "dominance", "anger"
    , "disgust", "fear", "joy", "sadness", "surprise", "trust", "anticipation"
    ]
    col_list_bi = [
    "als", "valence", "arousal", "dominance", "anger", "disgust", "fear", "joy", "sadness", "surprise"]
    if (binary):
        source = pd.read_csv(csv, sep="\t", usecols=col_list_bi)
    else:
        source = pd.read_csv(csv, sep="\t", usecols=col_list)
    source = source.fillna(0)
    index = 0
    dic = {}
    for words in source["als"]:
        if (str(words) != "0" and ";" in words): # cas avec ; dans la liste des mots
            try_list = words.split(";")
            if (binary):
                copy = source.reindex(col_list, axis="columns").loc[index,"valence":"surprise"].values.tolist()
                for i in range(3,len(copy)):
                    if copy[i] >= 0.5:
                        copy[i] = 1
                    else:
                        copy[i] = 0
            else:
                copy = source.reindex(col_list, axis="columns").loc[index,"valence":"anticipation"].values.tolist()
            for key in try_list:
                if (key not in dic):
                    dic[key] = copy
        else: # cas normale (un seul mots dans la cellule)
            if (binary):
                dic[words] = source.reindex(col_list, axis="columns").loc[index,"valence":"surprise"].values.tolist()
                for i in range(3,len(copy)):
                    if copy[i] >= 0.5:
                        copy[i] = 1
                    else:
                        copy[i] = 0
            else:
                dic[words] = source.reindex(col_list, axis="columns").loc[index,"valence":"anticipation"].values.tolist()
        index += 1
    return dic

def make_dic_nrc_intensif(lexicon_intensif, binary):
    '''
    Faire un dictionnaire de nrc fr.

    Parameters:
        lexicon_intensif (string): lexicon de nrc intensif
        binary (bool): verifier si binairiser les coeffs ou pas
        nrc_intensif_moyen (dict): les moyennes des coeffs des emotions

    Returns:
        dic (dict): un dictionnaire qui contient les mots français
        et leurs coefficients d'émotions
    '''    
    dic = {}
    if (binary):
        nrc_intensif_moyen = calculate_moyenne_nrc_intensif(lexicon_intensif)
    with open(lexicon_intensif, "r", encoding="utf-8") as lexicon:
        for line in lexicon:
            line = line.strip()
            list_line = line.split("\t")
            key = list_line[1]
            emotion = list_line[2]
            score = list_line[3]
            if (key != "French-fr"):
                score = float(score)
                if(binary): # S'il faut binariser le NRC:   
                    emotion_li = [0,0,0,0,0,0]
                    if (emotion == "trust" or emotion == "anticipation"):
                        continue
                    if (score >= nrc_intensif_moyen[emotion]):
                        score = 1
                    else:
                        score = 0
                if (key not in dic):
                    emotion_li = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
                    emo_index = column_order[emotion] - 3
                    emotion_li[emo_index] = score
                    dic[key] = emotion_li
                else:
                    emo_index = column_order[emotion] - 3
                    if (dic[key][emo_index] == 0):
                        dic[key][emo_index] = score
    return dic

def merge_vad(dic_vad, dic):
    '''
    Ajouter les coefficients de vad au dictionnaire.

    Parameters:
        dic_vad (dict): dictionnaire de vad
        dic (dict): dictionnaire des emotions (FEEL ou NRC)

    Returns:
        hybrid_dic (dict): un dictionnaire qui contient les mots français
        et leurs coefficients
    '''
    hybrid_dic = {}
    for emo_key in dic.keys():
        for vad_key in dic_vad.keys():
            if (emo_key == vad_key):
                hybrid_dic[emo_key] = dic_vad[vad_key] + dic[emo_key]
    return hybrid_dic


            
def NRC_intensif_to_FEEL(all_words_dic, nrc_intensif_file, nrc_intensif_moyen):
    with open(nrc_intensif_file, "r", encoding="utf-8") as fd_nrc:
        for line in fd_nrc:
            line = line.strip()
            list_line = line.split("\t")
            key = list_line[1]
            emotion = list_line[2]
            score = list_line[3]
            if (key != "French-fr"):
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

def grab_keywords(dic, words):
    '''
    rechercher les mots-clés dans la phrase donnée selon le dictionnaire,
        et sauvegarder les résultats dans un dictionnaire "keywords"

    Parameters:
        dic (dict): un dictionnaire du lexicon
        words (string): phrase où on cherche de mots-clés

    Returns:
        keywords (dict): tous les mots-clés avec coefficients d'émotion
    '''
    keywords = {}
    for word in words:
        if (word not in keywords.keys() and word in dic.keys()):
            keywords[word] = dic[word]
    return keywords


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

def make_csv_words(id_block, keyword, fout, emo_title_list, header_flag):
    '''
    faire un fichier csv de tous les mots-clés trouvés

    Parameters:
        id_block:   int     index du bloc
        keyword:    dict    mots-clés trouvés
        fout:       file_descripter fichier de sortie
        emo_title_list: list    titre de chaque colonne dans fichier csv
        header_flag: bool   utilisé pour vérifier si on doit écrire le titre de colonne ou pas

    Returns:
        None
    '''
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


def make_csv_moyen(mots_csv_in, moyen_csv_out,binary):
    '''
    faire un fichier csv qui affiche toutes les moyennes d'emotions de chaque bloc

    Parameters:
        mots_csv_in:    nom du fichier csv qui contient les mots-cles
        moyen_csv_out:  nom du fichier csv de la sortie

    Returns:
        None
    '''
    df = pd.read_csv(mots_csv_in, sep=",")
    if (binary):
        df = df.groupby("Id_block")[emotion_list_bi].mean()
    else:
        df = df.groupby("Id_block")[emotion_list].mean()
    df.to_csv(moyen_csv_out)


def make_csv_fr(dic_all_words,f_token_fr, out_file, binary):
    '''
    faire un fichier csv qui affiche toutes les moyennes d'emotions de chaque bloc

    Parameters:
        dic_all_words (dict): dictionnaire lexicon
        f_token_fr (string): nom du fichier de texte tokenisé
        out_file (string): fichier csv qui contient les mots-clés et coeffs
        binary (bool): vérifier s'il faut binairiser les coeffs

    Returns:
        None
    '''
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
                    if (binary):
                        make_csv_words(id_block,keyword, mots_fr_out, emotion_list_bi, header_flag)
                    else:
                        make_csv_words(id_block,keyword, mots_fr_out, emotion_list, header_flag)
                    header_flag = False
                    block = ""
                    id_block += 1

def make_csv_als(dic,size, f_in_als, out_file, binary):
    '''
    faire un fichier csv qui affiche toutes les moyennes d'emotions de chaque bloc

    Parameters:
        dic (dict): dictionnaire lexicon
        f_in_als (string): nom du fichier de texte Alsacien
        out_file (string): fichier csv qui contient les mots-clés et coeffs
        binary (bool): vérifier s'il faut binairiser les coeffs

    Returns:
        None
    '''
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
                    if (binary):
                        make_csv_words(id_block,keyword, fout, emotion_list_bi, header_flag)
                    else:
                        make_csv_words(id_block,keyword, fout, emotion_list, header_flag)
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

def merge_dic_fr(dic_elal, dic_feel, dic_vad):
    
    Merge les trois dictionnaires et obtenir 2 nouveaux dictionnaires
    qui contient les mots en commun et les mots totals

    Parameters:
        dic_elal (dict) : sortie de la fonction make_dic_elal
        dic_feel (dict) : sortie de la fonction make_dic_feel
        dic_vad  (dict) : sortie de la fonction make_dic_vad

    Returns:
        super_hybird_dic (dict): contient tous les mots en common de 3 dictionnaires
        all_words_dic (dict): contient tous les mots en common de feel et vad et aussi les mots dans elal
    
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
'''