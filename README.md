Character speech extraction
=========================

Data and code to extract character speech to plays in the Methal corpus and add character metadata from the Methal prosopography, besides plays' basic bibliographic metadata. Output format is delimited (exported pandas dataframe).

Given a TEI corpus (in one or several directories), it extracts a dataframe for the whole corpus, with each character's speech turns and the character's metadata, following speech-turn order in each play. 

# Program Structure

The program is organized as follows :

## Main scripts

- `extract_speech_main.sh`: Runs the extraction. Run without options to see the usage notes. Paths to run are hard-coded here and in the scripts it calls (it runs with the directory structure as in this repo).
- `metadata_analysis.ipynb`: After running extraction, this notebook can be run to get descriptive statistics on the metadata. 


## Output

- **The output to use for further analyses is [`overall-per-character-speech-postpro.tsv`](./overall-per-character-speech-postpro.tsv)**
- A [notebook](./metadata_analysis.ipynb) describes the **metadata distribution**
- The main script outputs two dataframes called `overall-per-character-speeech.tsv` and `overall-per-character-speech-postpro.tsv`.
- The second one, with `postpro` in its name is the one to use, as it contains some improvements (recoding etc) over the one originally output

### Annotations and content in the output

The dataframe has the fields below. Besides the description, details about possible metadata values are given below.

For the **metadata distribution**, see the [notebook](./metadata_analysis.ipynb).

For more details about the categorization, see [our paper](https://univoak.eu/islandora/object/islandora%3A157880) at the Quantitative Drama Analyis workshop.

| position | field name | description | 
| ---- | ---- | --- | 
| 0 | speaker | Character name | 
| 1 | gender | Character gender | 
| 2 | author | author name | 
| 3 | date | A date for the play | 
| 4 | date_type | When it was written, first printed, or print date for the edition we used | 
| 5 | social_class | Character social class, we estimated this based on information in the *dramatis personæ* | 
| 6 | job | Character's profession as in the *dramatis personæ* | 
| 7 | job_category | Professional category using our own taxonomy | 
| 8 | segment_number | For emotion analysis, the plays get divided into homogeneous segments. This field can be ignored for other purposes. | 
| 9 | play_short_name | Corresponds to the play's filename in the TEI directories (without *.xml*) | 
| 10 | genre | We have comedy, drama, volksstueck, tale (*Märel*) | 
| 11 | text | Each character's text. Line-breaks or interruptions are indicated with a triple pipe &#124;&#124;&#124;. These interruptions can happen e.g. if a stage direction was inserted within character speech, or in verse sections (the &#124;&#124;&#124; will separate each verse)  | 

#### Gender

Possible values for this category are:

|gender value| description|
|---|---|
|F|Female|
|M|Male|
|B|Both (group character with a speech turn, there are both male and female characters in it)|
|U|Was not possible to tell by looking at the *dramatis personæ*|
|grp_char/gdr_err|Group character we did not have a value for, or due to an error which prevents metadata assignment to this character (e.g. missing character ID). Less than 0.6% of speech turns are affected|

#### Social class

Possible values for this category are:

|social class value| comments|
|---|---|
|upper_class||
|upper_middle_class||
|middle_class|very little used|
|lower_middle_class||
|lower_class||
|grp_char/sclass_err|Group character we did not have a value for, or due to an error which prevents metadata assignment to this character (e.g. missing character ID). Less than 0.6% of speech turns are affected|


#### Professional category

Possible values for this category are below.

The professions that were assigned to each category are in the [supplemental materials](https://docs.google.com/spreadsheets/d/1ulj81Zi-EFU2mh1mqRNbXUPXKh2_QbvAe3Ij3jwbI6I/edit#gid=1929982385) to our paper. There may be some differences between those data and the [input data](./pre_treatment/methal-personography.xml) used here.

|professional category value| comments|
|---|---|
|agriculture||
|associative world||
|clergy|very little used|
|crafts||
|elementary_professions||
|government_executive_officials||
|industry_and_transportation||
|intermediate_professionals||
|military||
|professional_scientific_technical||
|rentiers||
|service_and_sales||
|grp_char/jcat_err|Group character we did not have a value for, or due to an error which prevents metadata assignment to this character (e.g. missing character ID). Less than 0.6% of speech turns are affected|

## Input data and other material

- **`commands`** subdirectory
	- `command_list.sh`
		List of commands to apply the `extract_character_speech.py` script from the `script` directory, per play

- **`pre_treatment`** subdirectory
	- `script` subdirectory:
	  - `extract_character_speech.py`:  
		Extracts speech turns (ignoring stage directions) and basic metadata for characters from the TEI plays. It crosses the information with the TEI prosopography to get character's social variables.
	  - `post_process_character_speech_df.py`: Carries out a postprocessing on the whole-corpus dataframe obtaiend with `extract_speech_main.sh`, providing the final extraction results.
	- `tei`, `tei2`, `tei-lustig`: **Input data.** TEI plays for the Methal corpus
	- `methal-personography.xml`: Part of the **input data**. Prosopography with social variable annotations for characters (gender, social class, professional category etc.)
	- `personnages-pieces.csv`:  Part of the **input data**. Methal corpus plays' bibliographic metadata. Used here to get the author's name and a date for the play.
	- `treated_files_df`:
		Dataframes output by `extract_character_speech.py`, per play

# About

The extraction is based on a subset of [Qinyue Liu's program](https://git.unistra.fr/methal/edytha) for lexicon-based emotion analysis in Alsatian plays. All parts unrelated to character speech extraction were removed. The directory structure and the script to extract text from the TEI plays and cross it with the prosopography was kept, with some modifications:
  - Stage directions are not part of the output text
  - A main bash script runs the extraction per play, then collects all results into a single dataframe per corpus and does some postprocessing (renaming some fields, recoding some values etc.)
  - Some data were corrected (e.g. some mismatched IDs across `@who` and `listPerson` children in the TEI) in order to prevent losing some character's metadata.
  - Some field names were renamed (e.g. `drama_type` renamed as `genre`)
  - The category values for speech turns where no metadata was found (given annotation errors or group characters that cannot be annotated with a single value) were changed. Before, the speaker name was *group* and the category value followed the pattern *{category-name}_unknown* (e.g. *job_unknown*). Now speaker name is *grp_char/err* and category value follows the pattern *grp_char/{category-abbreviation}_err* (e.g. *grp_char/jcat_err*) for professional category errors).
  - A notebook was added with descriptive statistics on the metadata collected

Created by Pablo Ruiz Fabo ([contact](https://lilpa.unistra.fr/theme-1-lexiques-discours-et-transpositions/membres/enseignants-chercheurs/ruiz-fabo-pablo/)).