
import os #, csv, json, sys, string
import pandas as pd
import numpy as np
#import spacy as sp
#from collections import defaultdict, Counter

#import gzip

from tqdm import tqdm

#import pickle as pkl
from argparse import ArgumentParser
import logging
import alsatian_tokeniser as als_t

tqdm.pandas()
#nlp_fr = sp.load("fr_core_news_sm")

parser = ArgumentParser()
parser.add_argument('--dataPath', help='path to CSV data file with texts')
parser.add_argument('--lexPath', help='path to lexicon. CSV with columns "word" plus emotion columns')
parser.add_argument('--lexNames', nargs="*", type=str, help='Names of the lexicons/column names in the lexicon CSV')
parser.add_argument('--savePath', help='path to save folder')
parser.add_argument("--mode", help="calculate mode, type tf_idf_files, tf_idf_phrases or no_idf")

def read_lexicon(path, LEXNAMES):
    df = pd.read_csv(path)
    df = df[~df['word'].isna()]
    df = df[['word']+LEXNAMES]
    df['word'] = [x.lower() for x in df['word']]
    return df
    # df = df[~df['val'].isna()]

def prep_dim_lexicon(df, dim):
    ldf = df[['word']+[dim]]
    ldf = ldf[~ldf[dim].isna()]
    ldf.drop_duplicates(subset=['word'], keep='first', inplace=True)
    ldf[dim] = [float(x) for x in ldf[dim]]
    ldf.rename({dim: 'val'}, axis='columns', inplace=True)
    ldf.set_index('word', inplace=True)
    return ldf

def get_alpha(token):
    return token.isalpha()


def get_vals(twt, lexdf, idf_df, analyse_mode):
    ret = als_t.RegExpTokeniser()
    tokens = (ret.tokenise(twt.lower())).get_tokens()
    tt = []
    for tok in tokens:
        tt.append(tok.get_contents())
    #tt = twt.lower().split(" ") # maybe use spacy to tokenize here
    at = [w for w in tt if w != ""] # compter num de tokens
    pw = [] # contient tous les mots parcourus
    tf = {} # numbre de terms dans la tourne de parole
    for x in tt:
        if (x in lexdf.index):
            pw.append(x)
            if (x not in tf.keys()):
                tf[x] = 1
            else:
                tf[x] = tf[x] + 1
    pv = []
    if (analyse_mode == "tf_idf_phrases"):
        for w in pw:
            if w in idf_df.index:
                pv.append(lexdf.loc[w]['val'] * idf_df.loc[w,"idf"] * tf[w])
            else:
                pv.append(0)
    elif (analyse_mode == "tf_idf_files"):
        pv = [lexdf.loc[w]['val']*idf_df[w]*10 for w in pw if w in idf_df] # contient coeffs de chaque mots
    else:    
        pv = [lexdf.loc[w]['val'] for w in pw]


    numTokens = len(at)
    numLexTokens = len(pw)
    
    avgLexVal = np.mean(pv)  # nan for 0 tokens

    return [numTokens, numLexTokens, avgLexVal]


def process_df(df, lexdf, idf_df, analyse_mode):
    logging.info("Number of rows: " + str(len(df)))

    
    resrows = [get_vals(x, lexdf, idf_df, analyse_mode) for x in df['text']] # tokenisation
    resrows = [x + y for x,y in zip(df.values.tolist(), resrows)]

    resdf = pd.DataFrame(resrows, columns=df.columns.tolist() + ['numTokens', 'numLexTokens', 'avgLexVal'])
    resdf = resdf[resdf['numLexTokens']>=1]
    
    resdf['lexRatio'] = resdf['numLexTokens']/resdf['numTokens']
    return resdf

def main(dataPath, LEXICON, LEXNAMES, savePath, analyse_mode):

    os.makedirs(savePath, exist_ok=True)

    logfile = os.path.join(savePath, 'log.txt')

    logging.basicConfig(filename=logfile, format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
    
    df = pd.read_csv(dataPath)

    # idf de ce fichier
    if (analyse_mode == "tf_idf_phrases"):
        idf_df = pd.read_csv("../intermediate/idf_info/" + savePath + ".csv", index_col=0, encoding="utf-8")
    elif ( analyse_mode == "tf_idf_files"):
        idf_df = pd.read_csv("../intermediate/idf_info.csv", index_col=0, encoding="utf-8")
        idf_df = idf_df.loc[savePath + ".txt"][:]
    else:
        idf_df = None

    #idf_coeff = idf_df.loc[savePath+".txt"][:]
    #print(idf_coeff.loc['uff'])

    for LEXNAME in LEXNAMES:

        lexdf = prep_dim_lexicon(LEXICON, LEXNAME)
        logging.info(LEXNAME + " lexicon length: " + str(len(lexdf)))
        resdf = process_df(df, lexdf, idf_df, analyse_mode)
    
        resdf.to_csv(os.path.join(savePath, LEXNAME+'.csv'), index=False)

if __name__=='__main__':
    args = parser.parse_args()

    dataPath = args.dataPath
    lexPath = args.lexPath

    LEXNAMES = args.lexNames
    LEXICON = read_lexicon(lexPath, LEXNAMES)

    savePath = args.savePath
    analyse_mode = args.mode

    main(dataPath, LEXICON, LEXNAMES, savePath, analyse_mode)