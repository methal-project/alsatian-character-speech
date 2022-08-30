from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import os
import glob

def main():
    make_text_files()
    idf()

def make_text_files():
    """Function to extract pure text files (words of characters) from csv files
    
    Returns:
        None, creates .txt files
    """
    # make text files from csv files
    file_list = os.listdir("csv_replaced2")
    for file in file_list:
        df = pd.read_csv("csv_replaced2/" + file, index_col=False, encoding="utf-8")["text"]
        df.to_csv("text_brut2/" + file[:-8] + ".txt",header=False, index=False, encoding="utf-8")

def idf():
    """Function to calculate idf by files

    Returns:
        None
    """
    path = "text_brut2/"
    file_names = os.listdir(path)
    file_list = glob.glob(f"{path}/*.txt") # get all the .txt files
    # Calculate tf-idf by files
    idf_vectorizer = TfidfVectorizer(input="filename", encoding="utf-8") 
    idf_vector = idf_vectorizer.fit_transform(file_list)
    idf_df = pd.DataFrame(idf_vector.toarray(), index = file_names, columns = idf_vectorizer.get_feature_names_out())
    idf_df.to_csv("idf_info2.csv", encoding="utf-8")


if __name__ == "__main__":
    main()
