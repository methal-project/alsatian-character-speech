from multiprocessing.pool import Pool
from pathlib import Path
import pandas as pd
from metaphone_als import dm



# DIR_IN = Path('../../working_dir/tokens/all')
DIR_IN = Path('../../working_dir/tokens/bas-rhin')
DIR_OUT = Path('../../working_dir/metaphone/bas-rhin')
DIR_OUT.mkdir(exist_ok=True,parents=True)

# filename = 'clemens-gift.txt.tok'
# p = Path(filename)
punc = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~«»'


def all_txts(input_dir):
    return sorted(Path(input_dir).rglob('*tok'))

def is_punc(word):
    if word in punc:
        return False
    else:
        return True


def txt2csv(p):
    with p.open('r') as f:
        data = f.readlines()
        # metaphone
        key1 = []
        key2 = []
        data_sans_punc = []
        for line in data:
            if is_punc(line.strip('\n')):
                data_sans_punc.append(line.strip('\n'))
        for forme in data_sans_punc:
            key1.append(dm(forme)[0])
            key2.append(dm(forme)[1])
    # print(data)


    df = pd.DataFrame({"forme":data_sans_punc,"key1":key1,"key2":key2})
    # df = pd.DataFrame(data, columns=[''])
    # df['empty1'] = 'NaN'
    # df['empty2'] = 'NaN'

    filename = p.stem.strip('.txt')
    print(f"{filename} Processed")
    # print(df)

    out_file_path = DIR_OUT / Path(p.stem.strip('.txt') + '.csv')
    df.to_csv(out_file_path , index=None)



def main():
    txts = all_txts(DIR_IN)
    # print(txts)
    pool = Pool()
    pool.map(txt2csv, txts)


if __name__ == '__main__':
    main()

