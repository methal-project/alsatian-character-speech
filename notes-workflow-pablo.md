# notes pablo

Notes i took while testing the workflow

In my tests I added a "2" to the normal output directories (and some file) just to have a different output (so `csv_replaced2` would normally be `csv_replaced` and so on)

## Preprocessing

 - from app root directory
	- pre_traitement/script/emo_xml_treat.py va créer treated_files2 (path hard-coded in the script)
	- This contains CSV files with the metadata and text
	- did like this `for x in $(ls ../../test-app/initial-play) ; do python pre_treatment/script/emo_xml_treat.py ../../../test-app/initial-play $x ; done`
	- path to directory seems to be relative to the directory where the script is, not to where you call the script from

 - then you move to "intermediate" directory 
	- do `python variant_idf_phrases.py` 
	- This is gonna create `csv_replaced2` with the normalized variants (it normalizes the variants)
	- If you want to weight by entire play tf-idf (not by speech-turn-based idf), also run, AFTERWARDS, `idf_file.py` (this does not normalize, it expects normalized text already)
	- Outputs will be
		- `idf_info2` for speech-turn-based weights (inside this, there's one file per play with the IDF for each word the play)
		- `idf_info2.csv` is a matrix with tf-idf values per word per play (a document-term matrix)
	- Input and output paths are hard-coded in the scripts

## Calculate emotions

Then you can calculate emotion scores cos you have the pre-treated files and the weights

For this you gotta go to `app_root_directory/emotions`

Here in emotions you execute `python avgEmoValues.py`

An example command is here (see the `analyse_emotions/commands/command_list_emotions.txt` file)

```shell
python3 avgEmoValues.py --dataPath ../pre_treatment/treated_files/am-letzte-maskebal.out.csv --lexPath ELAL-als-lexicon.csv --lexNames valence dominance arousal anger anticipation disgust fear joy sadness surprise trust --savePath am-letzte-maskebal --mode tf_idf_phrases
```

Note that `savePath` is a directory name that will be created to save the emotion analysis results (per play). BUT if i got it right it has to match the file names in the "treated_files" folder you used (minus the .out.csv ending)

So you may need to hard code a new output directory (if it is not the same output directory where the script resides) <-- **maybe this would be a priority to change**

I ran this with a loop (cos operates per file) 

```shell
for x in $(ls ../pre_treatment/treated_files2) ; do python avgEmoValues.py --dataPath ../pre_treatment/treated_files2/$x --lexPath ELAL-als-lexicon.csv --lexNames valence dominance arousal anger anticipation disgust fear joy sadness surprise trust --savePath $(basename $x | sed s'/\.out\.csv//') --mode tf_idf_phrases ; done
```

But before the loop i had hard-coded this path in the script, for output: `resdf.to_csv(os.path.join("results2/" + savePath, LEXNAME+'.csv'), index=False)` (results2)

I had this warning once in a while `/home/ruizfabo/anaconda3/envs/ajout/lib/python3.8/site-packages/numpy/core/_methods.py:188: RuntimeWarning: invalid value encountered in double_scalars
  ret = ret.dtype.type(ret / rcount)`


## Graphics

Input path is hard-coded (it's the current directory)
I changed it to `results2` just to see

All worked fine

Here's the commands I tried, from history

```
python pre-graphic.py 
python split_plays.py 
python3 graphic.py --mode single --pieces results2/weber-yo-yo,results2/greber-lucie --emotions joy,sadness
ls results2/
python3 graphic.py --mode single --pieces weber-yo-yo,bastian-dr-hans-im-schnokeloch --emotions joy,sadness
python3 graphic.py --mode single --pieces weber-yo-yo,bastian-dr-hans-im-schnokeloch --emotions joy,sadness --savepath results2
python3 graphic.py --mode single --pieces weber-yo-yo,bastian-dr-hans-im-schnokeloch --emotions joy,sadness --filters speaker --save
path results2
python3 graphic.py --mode group --pieces weber-yo-yo,bastian-dr-hans-im-schnokeloch --emotions joy,sadness --filters speaker --savep
ath results2
python3 graphic.py --mode group --emotion joy,sadness
python3 graphic.py --mode group --emotion joy,sadness --dramatype comedy
python3 graphic.py --mode group --emotion joy,sadness --dramatype drama
ls results2/
python3 graphic.py --mode group --emotion joy,sadness --dramatype drama --savepath results2
ls results2/
python3 graphic.py --mode group --emotion joy,sadness --dramatype comedy --savepath results2
python3 graphic.py --mode group --pieces all
python3 graphic.py --mode group --pieces all --savepath results2
python3 graphic.py --mode group --pieces clemens-charlot --savepath results2
python3 graphic.py --mode group --pieces riff-sainte-barbe --savepath results2
python3 graphic.py --mode group --pieces riff-sainte-barbe --savepath results2
python3 graphic.py --mode most_positive --savepath results2
python3 graphic.py --mode most_negative --savepath results2
python3 graphic.py --mode most_positive --savepath results2

```