from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import sys,os
import glob

def main():
    #make_text_files()
    idf()

def make_text_files():
    # make text files from csv files
    piece_dir = ["tei", "tei-lustig", "tei2"]
    path = "../pieces_more_info/treated_files/"
    for i in piece_dir:
        full_path = path + i + "/"
        file_list = os.listdir(full_path)
        for file in file_list:
            df = pd.read_csv(full_path + file, index_col=False, encoding="utf-8")["text"]
            df.to_csv("text_brut/" + file[:-8] + ".txt",header=False, index=False, encoding="utf-8")
    return 0

def idf():
    path = "text_brut/"
    file_names = os.listdir(path)
    file_list = glob.glob(f"{path}/*.txt") # parcourir tous les fichiers .txt
    
    idf_vectorizer = TfidfVectorizer(input="filename", encoding="utf-8") 
    idf_vector = idf_vectorizer.fit_transform(file_list)
    idf_df = pd.DataFrame(idf_vector.toarray(), index = file_names, columns = idf_vectorizer.get_feature_names_out())
    #slice_df = idf_df[["herr", "uff", "madame", "kumme"]]
    idf_df.to_csv("idf_info.csv", encoding="utf-8")



if __name__ == "__main__":
    main()
