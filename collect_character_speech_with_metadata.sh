#!/usr/bin/env bash

# run per-play extraction if needed

#./commands/command_list_pre_treatment.sh

# collect per-play dataframes into a single df for the entire corpus

outdir=$(grep dir_path pre_treatment/script/emo_xml_treat.py | \
         head -n1 | grep -Po '".+?"' | sed 's/"//g')
echo $outdir

outdf_all=overall-per-character-speech.tsv

# write out the header once
header=$(head -n1 $outdir/* |grep -v '=' | sed 's/\n//g'| sort| uniq)
echo -e $header | sed 's/ /\t/g'
echo -e $header | sed 's/ /\t/g' > $outdf_all

# write out each play's df from line 2 onwards
for fn in $(ls $outdir); do
  tail --lines +2 $outdir/$fn | grep -Pv '^\n' >> $outdf_all
done
