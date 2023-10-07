#!/usr/bin/env bash

while getopts "xcp" opt; do
  case "$opt" in
    x) EXTRACT=1
    ;;
    c) COLLECT=1
    ;;
    p) POSTPROCESS=1
    ;;
    *)
    echo "Incorrect options"
    exit 1
    ;;
  esac
done

# run per-play extraction if needed
if [[ $EXTRACT == 1 ]]; then
    echo "Extract per play"
    ./commands/command_list_pre_treatment.sh
fi

# collect per-play dataframes into a single df for the entire corpus
if [[ $COLLECT == 1 ]]; then
    # avoid forgetting postprocess
    $POSTPROCESS=1
    echo "Collect to single dataframe"
    outdir=$(grep dir_path pre_treatment/script/emo_xml_treat.py | \
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
