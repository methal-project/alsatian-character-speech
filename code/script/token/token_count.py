from pathlib import Path
import pandas as pd

wd = Path('../../working_dir')
tokpath = wd / "tokens/"
metapath = wd / "metadata/metadata_avec_period.csv"
outpath = wd / "metadata/metadata_V2.csv"
punc = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~«»'

df_meta = pd.read_csv(metapath, index_col=0)
df_meta['Tokens'] = 1
df_meta['TokensNoPunctuation'] = 1

def all_txts(input_dir):
    return sorted(Path(input_dir).rglob('*tok'))

def is_punc(word):
    if word in punc:
        return False
    else:
        return True

def count_tok(p):
    with p.open('r') as f:
        data = f.readlines()
        df_meta.loc[p.stem[:-4], 'Tokens'] = len(data)
        data_sans_punc = []
        for line in data:
            if is_punc(line.strip('\n')):
                data_sans_punc.append(line)
        df_meta.loc[p.stem[:-4], 'TokensNoPunctuation'] = len(data_sans_punc)

def main():
    txts = all_txts(tokpath)
    for i in txts:
        count_tok(i)

    print("Total : ", len(txts))
    print(df_meta)
    df_meta.to_csv(outpath)


if __name__ == '__main__':
    main()