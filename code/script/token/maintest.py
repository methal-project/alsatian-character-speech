import argparse
import codecs
from multiprocessing.pool import Pool
import alsatian_tokeniser
from pathlib import Path


def set_up_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('inputdir', help="input directory containing TEI XML files")
    parser.add_argument('outfile',
                        help="output file as CSV with information about the TEI corpus")
    return parser

def all_corpus(input_dir):
    return sorted(Path(input_dir).rglob('*txt'))


def corpus_tokeniser(corpus_path):
    input_file = Path(corpus_path)
    corpus_text = input_file.read_text()
    ret = alsatian_tokeniser.RegExpTokeniser()
    tokens = ret.tokenise(corpus_text)

    print(f"{corpus_path.stem} Processed")
    return tokens





def main():
    parser = set_up_argparser()
    args = parser.parse_args()

    corpus = all_corpus(args.inputdir)
    pool = Pool()
    corpus_tokens = pool.map(corpus_tokeniser, corpus)

    print("Done with tokenize")
    for token in corpus_tokens:
        output_token = token.to_lines()
        outputdir = args.outfile
        Path.mkdir(outputdir)



if __name__ == '__main__':
    main()
