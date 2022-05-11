import re
import outils as ot
import statistiques as stat
import alsatian_tokeniser as at

f_in_fr = "source_files/fr_hmr.txt"
f_in_als = "source_files/al_hmr.txt"         # fichier d'entrée
f_elal = "source_files/ELAL_all.tsv"                    # fichier lexicon d'émotions elal
f_feel = "source_files/FEEL.csv"                        # fichier lexicon d'émotions elal
f_vad = "source_files/French-fr-NRC-VAD-Lexicon.tsv"    # fichier lexicon d'émotions elal

f_token_fr = "token_fr.txt"             # fichier text apres tokenisation

f_out_fr = "out_files/spacy_elal_fr.txt"           # fichier de sortie
mots_fr_feel = "out_files/mots_fr_FEEL.csv"       # fichier csv qui contient les mots cles trouve et leurs coeffs
mots_fr_elal = "out_files/mots_fr_ELAL.csv"
mots_als = "out_files/mots_als_ELAL.csv"
moyen_fr = "out_files/moyenne_fr_FEEL.csv"
moyen_als = "out_files/moyenne_als_ELAL.csv"
pk = "out_files/pk.csv"

emotion_list = [
    "valence", "arousal", "dominance", "anger"
    , "disgust", "fear", "joy", "sadness", "surprise", "trust", "anticipation"
]
regex = "[,|.| |?|!|\n]"
block_flag = ot.block_flag


# Make text

def make_text(f_out, f_in, dic_all_words):
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
                        words = ot.fr_token_dict(block)
                        keyword = ot.grab_keywords(dic_all_words,words)
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
                        emotion = ot.emotion_calculate(keyword)

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


# make csv file mots


def make_csv_fr(dic_all_words):
    with open(f_token_fr, "r", encoding="utf-8") as fin_token:
        with open(mots_fr_elal, "w", encoding="utf-8") as mots_fr_out:
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
                    keyword = ot.grab_keywords(dic_all_words, words)
                    ot.make_csv_words(id_block,keyword, mots_fr_out, emotion_list, header_flag)
                    header_flag = False
                    block = ""
                    id_block += 1


def make_csv_als(dic,size):
    keyword = {}
    block = ""
    with open(f_in_als, "r", encoding="utf-8") as fin:
        with open(mots_als, "w", encoding="utf-8") as fout:
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
                    if(header_flag):
                        print(tokens)
                    keyword = ot.grab_keywords(dic, tokens)
                    ot.make_csv_words(id_block, keyword, fout, emotion_list, header_flag)
                    header_flag = False
                    count = 0
                    block = ""
                    id_block += 1
                else:
                    block += line + "\n"
                    count += 1
                count_line += 1

# ---------------------- main operations --------------------

'''
# obtenir le fichier de tokenization des mots francais

ot.make_tokenfile_fr(f_in, f_token_fr, size)

# creer les dictionnaires pour obtenir les mots cles

dic_elal = ot.make_dic_elal(f_elal)
dic_feel = ot.make_dic_feel(f_feel)
dic_vad = ot.make_dic_vad(f_vad)

dic_list = ot.merge_dic_fr(dic_elal, dic_feel, dic_vad)
dic_all_words = dic_list[1] # dictionnaire utilise pour mots francais
dic_triple_merged = dic_list[0]
dic = ot.make_dic_als(f_elal) # dic utilise pour mots alsaciens

# faire les fichiers csv qui contient les mots-cles
make_csv_als(dic,size=5)
make_csv_fr(dic_all_words)
make_csv_fr(dic_elal)

# faire les fichiers csv qui contient les moyennes des emotions par block
ot.make_csv_moyen(mots_fr, moyen_fr)
ot.make_csv_moyen(mots_als, moyen_als)


# --------------------- correlation des fichiers ----------------------------------------
cor_als_fr = stat.correlation_df(moyen_als, moyen_fr).to_dict()
with open(pk, "w", encoding="utf-8") as pk_out:
    writer = ot.csv.DictWriter(pk_out, fieldnames = ["Id_block"] + emotion_list)

    title = ot.csv.writer(pk_out)
    title.writerow(["Correlation d'emotions fr_FEEL als_ELAL"])
    writer.writeheader()
    writer.writerows([cor_als_fr])
'''

# --------------------- comparer lexicon elal et nrc --------------------------------

'''
df_elal_fr = ot.pd.read_csv(mots_fr_elal, usecols=['Id_block', 'Mots'])
df_feel_fr = ot.pd.read_csv(mots_fr_feel, usecols= ['Id_block', 'Mots'])
df_elal_als = ot.pd.read_csv(mots_als, usecols=['Id_block', 'Mots'])

same_words_df = df_elal_fr.merge(df_feel_fr, how = "inner", on=["Id_block","Mots"])
diff_words_df = ot.pd.concat([same_words_df, df_feel_fr]).drop_duplicates(keep=False)

# obtenir les textes et les sauvegarder dans dataframe
text_block = make_text(f_in_fr,{})
text_block_fr_df = ot.pd.DataFrame({"Id_block_text_fr":range(len(text_block)), "Text_fr":text_block})
text_block = make_text(f_in_als,{})
text_block_als_df = ot.pd.DataFrame({"Id_block_text_als":range(len(text_block)), "Text_als":text_block})

# renommer les colonnes pour mieux construre le fichier csv
same_words_df = same_words_df.rename(columns={"Mots":"Mots_en_commun", "Id_block":"Id_block_Mots_en_commun"})
diff_words_df = diff_words_df.rename(columns={"Mots":"Mots_dans_nrc_pas_dans_elal", "Id_block":"Id_block_Mots_differents"})
df_elal_als = df_elal_als.rename(columns={"Mots":"Mots_en_alsacien", "Id_block":"Id_block_Mots_als"})

pk_df = ot.pd.concat([same_words_df, diff_words_df, df_elal_als, text_block_fr_df, text_block_als_df], axis=1)

pk_df.to_csv("out_files/compare_mots_elal_nrc.csv")
#print(text_block_df.head(10))
# '''