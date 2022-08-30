import pandas as pd
import os
import alsatian_tokeniser as alsatian_tokeniser
from sklearn.feature_extraction.text import TfidfVectorizer
# lexicon name
filename = "../source_files/ELAL_all.tsv"

df = pd.read_csv(filename, sep="\t")
df = df.iloc[:,[0,1]]
list_als = df.to_dict("split")["data"] # dictionary containing all the alsatian words

# make a dictionary of replacement
dict_replace = {}
for word in list_als:
    variantes = word[1].split(";")
    forme_ori = variantes[0] # the original form
    if ("_C" not in forme_ori): # we ignore variants with _C
        for vari in variantes:
            if vari not in dict_replace:
                dict_replace[vari] = forme_ori


# read csv files and replace variants
ret = alsatian_tokeniser.RegExpTokeniser()
path = "../pre_treatment/treated_files2/"
list_treated_files = os.listdir(path)

for file in list_treated_files:
    single_piece_tourne_parole = []
    df = pd.read_csv(path + file)
    text = ""
    for i in range(df.shape[0]):
        # for each phrase
        text = df["text"].values[i]
        rep_text = text
        tokens = ret.tokenise(text)
        tokens = tokens.get_tokens()
        for i in range(len(tokens)):
            # for each word
            tok = tokens[i].get_contents()
            if (tok in dict_replace.keys()):
                rep_text = rep_text.replace(tok, dict_replace[tok])
        single_piece_tourne_parole.append(rep_text)

    # to create csv corpus files
        df = df.replace(text, rep_text)
    df.to_csv("csv_replaced2/" + file, index = False)
    
    # calculate tf-idf for each theater piece:
    idf_vectorizer = TfidfVectorizer(input="content", encoding="utf-8")
    idf_vector = idf_vectorizer.fit(single_piece_tourne_parole)
    idf = idf_vector.idf_                           # array de idf de tous les mots
    words = idf_vectorizer.get_feature_names_out()  # tous les mots dans la piece
    idf_df = pd.DataFrame(idf, index = words, columns=["idf"])
    idf_df.to_csv("idf_info2/" + file[:-8] + ".csv", index_label="words")