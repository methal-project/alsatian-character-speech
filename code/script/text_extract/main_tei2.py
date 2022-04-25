import argparse
from pathlib import Path
from multiprocessing.pool import Pool

import pandas as pd

from tei_reader import TEIFile

# Get command-line input
def set_up_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('inputdir', help="input directory containing TEI XML files")
    parser.add_argument('outfile',
                        help="output file as CSV with information about the TEI corpus")
    return parser

# get all xml files
def all_teis(input_dir):
    return sorted(Path(input_dir).rglob('*xml'))

# Convert xml files from the corpus into metadata(.csv)
def tei_to_csv_entry(tei_file):
    tei = TEIFile(tei_file)
    print(f"{tei_file} Processed")
    return tei.idnoMtl(),tei.basename()[:-9], tei.title, tei.author, tei.publisher(), tei.pubPlace(), tei.dateWritten(), tei.datePrint(), tei.front, tei.body, tei.textBrut()

def main():
    parser = set_up_argparser()
    args = parser.parse_args()

    result_csv = pd.DataFrame(columns=['IdMtl','FileName','Title', 'Author', 'Publisher', 'PubPlace', 'dateWritten', 'datePrint','Front', 'Body','textBrut'])

    teis = all_teis(args.inputdir)

    pool = Pool()
    csv_entries = pool.map(tei_to_csv_entry, teis)
    print("Total : ", len(teis))
    # print(csv_entries)

    print("Done with parsing")
    result_csv = pd.DataFrame(csv_entries, columns=['IdMtl','FileName','Title', 'Author', 'Publisher', 'PubPlace', 'dateWritten', 'datePrint','Front', 'Body','textBrut'])
    print("Done with appending")

    result_csv.to_csv(args.outfile, index=False)
    print("Done convert csv with text brut")

    pd.set_option('display.max_columns', 100)
    pd.set_option('display.max_rows', 100)
    pd.set_option('display.max_colwidth', 100)
    pd.set_option('display.width', 100)
    # print(result_csv)
if __name__ == '__main__':
    main()