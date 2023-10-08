#!/usr/bin/env bash

usage(){
  echo "Usage: $0 [-x|-c|-p]"
  echo ""
  echo " -x   Extract speech turns (without stage directions), basic character"
  echo "      metadata from TEI header and more social metadata from personography"
  echo "      (one dataframe per play)."
  echo " -c   Collect the per-play dataframes into a single dataframe for the corpus"
  echo "      This also triggers a postprocessing (recoding etc.) in the whole-corpus df."
  echo " -p   Postprocess the whole-corpus df (some recoding and corrections)"
  echo ""
}

while getopts "xcp" opt; do
  case "$opt" in
    x) EXTRACT=1
    ;;
    c) COLLECT=1
    ;;
    p) POSTPROCESS=1
    ;;
    *) usage
    ;;
  esac
done

#https://unix.stackexchange.com/a/50648
#echo $OPTIND
[[ $OPTIND -eq 1 ]] && usage

# run per-play extraction if needed
if [[ $EXTRACT == 1 ]]; then
    echo "Extract per play"
    ./commands/command_list_pre_treatment.sh
fi

# collect per-play dataframes into a single df for the entire corpus
if [[ $COLLECT == 1 ]]; then
    # avoid forgetting postprocess
    POSTPROCESS=1
    echo "Collect to single dataframe"
    outdir=$(grep dir_path pre_treatment/script/extract_character_speech.py | \
             head -n1 | grep -Po '".+?"' | sed 's/"//g')
    echo $outdir

    outdf_all=overall-per-character-speech.tsv

    # write out the header once
    header=$(head -n1 $outdir/* |grep -v '=' | sed 's/\n//g'| sort| uniq)
    echo -e "Output columns" $header | sed 's/ /\t/g'
    echo -e $header | sed 's/ /\t/g' > $outdf_all

    # write out each play's df from line 2 onwards
    for fn in $(ls $outdir); do
      tail --lines +2 $outdir/$fn | grep -Pv '^\n' >> $outdf_all
    done
fi

# postprocess df
if [[ $POSTPROCESS == 1 ]]; then
    echo "Postprocess dataframe"
    python ./pre_treatment/script/postprocess_character_speech_df.py
fi
