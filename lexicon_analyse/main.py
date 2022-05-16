
import outils as ot
import statistiques as stat



f_in_fr = "source_files/fr_hmr.txt"
f_in_als = "source_files/al_hmr.txt"         # fichier d'entrée
f_elal = "source_files/ELAL_all.tsv"                    # fichier lexicon d'émotions elal
f_feel = "source_files/FEEL.csv"                        # fichier lexicon d'émotions elal
f_vad = "source_files/French-fr-NRC-VAD-Lexicon.tsv"    # fichier lexicon d'émotions elal
nrc_intensif_file = "source_files/French-fr-NRC-Emotion-Intensity-Lexicon-v1.txt"


f_token_fr = "token_fr.txt"             # fichier text apres tokenisation

f_out_fr = "out_files/spacy_elal_fr.txt"           # fichier de sortie
mots_fr_feel = "out_files/mots_fr_FEEL.csv"       # fichier csv qui contient les mots cles trouve et leurs coeffs
mots_fr_feel_intensif = "out_files/mots_fr_FEEL_nrc_intensif.csv"
mots_fr_elal = "out_files/mots_fr_ELAL.csv"
mots_als = "out_files/mots_als_ELAL.csv"
moyen_fr = "out_files/moyenne_fr_FEEL.csv"
moyen_fr_intensif = "out_files/moyenne_fr_FEEL_intensif.csv"
moyen_als = "out_files/moyenne_als_ELAL.csv"
compare_cor_FEEL = "out_files/compare_cor_fr_als.csv"
compare_moyen_FEEL = "out_files/compare_moyen_fr_als.csv"
compare_cor_FEEL_intensif = "out_files/compare_cor_fr_als_intensif.csv"
compare_moyen_FEEL_intensif = "out_files/compare_moyen_fr_als_intensif.csv"

emotion_list = [
    "valence", "arousal", "dominance", "anger"
    , "disgust", "fear", "joy", "sadness", "surprise", "trust", "anticipation"
]

block_flag = ot.block_flag


# make csv file mots





# ---------------------- main operations --------------------

'''
# obtenir le fichier de tokenization des mots francais

#ot.make_tokenfile_fr(f_in, f_token_fr, size)

# creer les dictionnaires pour obtenir les mots cles

dic_elal = ot.make_dic_elal(f_elal)
dic_feel = ot.make_dic_feel(f_feel)
dic_vad = ot.make_dic_vad(f_vad)

dic_list = ot.merge_dic_fr(dic_elal, dic_feel, dic_vad)
dic_all_words = dic_list[1] # dictionnaire utilise pour mots francais
dic_triple_merged = dic_list[0]
dic = ot.make_dic_als(f_elal) # dic utilise pour mots alsaciens
print(dic_all_words["furieux"])
moyen_nrc_intensif = ot.calculate_moyenne_nrc_intensif(nrc_intensif_file)
dic_all_words = ot.NRC_intensif_to_FEEL(dic_all_words, nrc_intensif_file, moyen_nrc_intensif)
print(dic_all_words["furieux"])

# faire les fichiers csv qui contient les mots-cles
ot.make_csv_als(dic, 5, f_in_als, mots_als)
ot.make_csv_fr(dic_all_words, f_token_fr,mots_fr_feel_intensif)

# faire les fichiers csv qui contient les moyennes des emotions par block
ot.make_csv_moyen(mots_fr_feel_intensif, moyen_fr_intensif)
ot.make_csv_moyen(mots_als,moyen_als)
# --------------------- correlation des fichiers ----------------------------------------
stat.correlation_df(moyen_als, moyen_fr_intensif, compare_moyen_FEEL_intensif, compare_cor_FEEL_intensif)

# --------------------- comparer lexicon elal et nrc --------------------------------


df_elal_fr = ot.pd.read_csv(mots_fr_elal, usecols=['Id_block', 'Mots'])
df_feel_fr = ot.pd.read_csv(mots_fr_feel, usecols= ['Id_block', 'Mots'])
df_elal_als = ot.pd.read_csv(mots_als, usecols=['Id_block', 'Mots'])

same_words_df = df_elal_fr.merge(df_feel_fr, how = "inner", on=["Id_block","Mots"])
diff_words_df = ot.pd.concat([same_words_df, df_feel_fr]).drop_duplicates(keep=False)

# obtenir les textes et les sauvegarder dans dataframe
text_block = ot.make_text(f_in_fr,"nothing.txt",{},)
text_block_fr_df = ot.pd.DataFrame({"Id_block_text_fr":range(len(text_block)), "Text_fr":text_block})
text_block = ot.make_text(f_in_als,"nothing.txt",{},)
text_block_als_df = ot.pd.DataFrame({"Id_block_text_als":range(len(text_block)), "Text_als":text_block})

# renommer les colonnes pour mieux construre le fichier csv
same_words_df = same_words_df.rename(columns={"Mots":"Mots_en_commun", "Id_block":"Id_block_Mots_en_commun"})
diff_words_df = diff_words_df.rename(columns={"Mots":"Mots_dans_nrc_pas_dans_elal", "Id_block":"Id_block_Mots_differents"})
df_elal_als = df_elal_als.rename(columns={"Mots":"Mots_en_alsacien", "Id_block":"Id_block_Mots_als"})

pk_df = ot.pd.concat([same_words_df, diff_words_df, df_elal_als, text_block_fr_df, text_block_als_df], axis=1)

pk_df.to_csv("out_files/compare_mots_cles_elal_nrc.csv")
#print(text_block_df.head(10))

'''
stat.correlation_df(moyen_als, moyen_fr_intensif, compare_moyen_FEEL_intensif, compare_cor_FEEL_intensif)
