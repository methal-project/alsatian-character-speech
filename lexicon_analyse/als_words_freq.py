import outils
import os

def grab_keywords(words_freq, dic, words):
    '''
    rechercher les mots-clés dans la phrase donnée selon le dictionnaire,
        et sauvegarder les résultats dans un dictionnaire "keywords"

    Parameters:
        words_freq (dict): un dictionnaire qui contient les frequences des mots
        dic (dict): un dictionnaire du lexicon
        words (string): phrase où on cherche de mots-clés

    Returns:
        keywords (dict): tous les mots-clés avec coefficients d'émotion
    '''
    for word in words:
        if (word not in words_freq.keys() and word in dic.keys()):
            words_freq[word] = 1
        elif (word in words_freq.keys()):
            words_freq[word] += 1
    return words_freq


if __name__ == "__main__":
    path = "pieces_more_info/treated_files/"
    list_dirs = os.listdir(path)
    dic_elal = outils.make_dic_als("lexicon_analyse/source_files/ELAL_all.tsv", False)
    words_freq = {}

    for dirname in list_dirs:
        if os.path.isdir(path+dirname):
            list_files = os.listdir(path + dirname + "/")
        for file in list_files:
            file_path = path + dirname + "/" + file
            df = outils.pd.read_csv(file_path)
            texts = df["text"]
            for txt in texts:
                ret = outils.at.RegExpTokeniser()
                phrase = (ret.tokenise(txt)).get_contents()
                tokens = outils.re.split(outils.regex, phrase)
                words_freq = grab_keywords(words_freq, dic_elal, tokens)

    new_df = outils.pd.DataFrame.from_dict(words_freq, orient = "index", columns = ["frequence"])
    new_df.to_csv("mots-als-freq.csv")
