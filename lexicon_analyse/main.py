import outils as ot
import alsatian_tokeniser as at


f_in = "source_files/fr_hmr.txt"         # fichier d'entrée
f_out = "out_files/spacy_elal_fr.txt"           # fichier de sortie
f_elal = "source_files/ELAL_all.tsv"                    # fichier lexicon d'émotions elal
f_feel = "source_files/FEEL.csv"                        # fichier lexicon d'émotions elal
f_vad = "source_files/French-fr-NRC-VAD-Lexicon.tsv"    # fichier lexicon d'émotions elal

f_token_fr = "token_fr.txt"             # fichier text apres tokenisation
mots_fr = "out_files/mots_fr.csv"       # fichier csv qui contient les mots cles trouve et leurs coeffs

emotion_list = [
    "valence", "arousal", "dominance", "anger"
    , "disgust", "fear", "joy", "sadness", "surprise", "trust", "anticipation"
]

block_flag = ot.block_flag


# Make text

def make_text(dic_all_words):
    count = 0
    size = 5
    block = ""
    keyword = {}
    emotion = {}

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


# make csv file mots


def make_csv_fr(dic_all_words):
    with open(f_token_fr, "r", encoding="utf-8") as fin_token:
        with open(mots_fr, "w", encoding="utf-8") as mots_fr_out:
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
                    ot.make_csv_french_words(id_block,keyword, mots_fr_out, emotion_list, header_flag)
                    header_flag = False
                    block = ""
                    id_block += 1


# ---------------------- main operations --------------------

'''
ot.make_tokenfile_fr(f_in, f_token_fr, size)

# creer les dictionnaires pour obtenir les mots cles

dic_elal = ot.make_dic_fr(f_elal)
dic_feel = ot.dic_csv_feel(f_feel)
dic_vad = ot.dic_csv_vad(f_vad)

dic_list = ot.merge_dic_fr(dic_elal, dic_feel, dic_vad)
dic_all_words = dic_list[1]
dic_triple_merged = dic_list[0]
'''

'''
ret = at.RegExpTokeniser()
token = ret.tokenise("S'isch m'r ganz e Kriz, alle-n-Äujeblick muess d'r Herr Dr. Freundlich kumme-n-üs d'r Stadt, um bim Vater um mini Hand anzehalte, in d'r guete Meinung d'r Vater weiss alles.")
print(token.get_contents())




# Quand le fichier csv de mots est fait, on calcule les moyennes:
df = pd.read_csv(mots_fr, sep=",")
df = df.groupby("Id_block")[["valence", "arousal", "dominance", "anger", "disgust", "fear", "joy", 
"sadness", "surprise", "trust", "anticipation"]].mean()
df.to_csv("out_files/moyen_emotions_fr.csv")
'''
    
dic = ot.make_dic_fr(f_elal)
make_text(dic)




