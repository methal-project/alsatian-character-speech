import os
import pandas as pd
from pathlib import Path

# IO ==========================================================================

indf_path = Path("../../overall-per-character-speech.tsv")
play_md_path = Path("../personnages-pieces.csv")
# relative path to parent's parent ok to execute this module standalone,
# the second relative path to same directory is when called with
# ../../collect_character_speech_with_metadata.sh (main script)
print("IO")
try:
  assert indf_path.exists()
except AssertionError:
  print("- Look for df in same directory")
  indf_path = Path("overall-per-character-speech.tsv")
  assert(indf_path.exists())
print(f"- Input at {indf_path.absolute()}")

outdf_path = indf_path.with_stem(indf_path.stem + "-postpro")
print(f"- Output at {outdf_path.absolute()}")

try:
  assert play_md_path.exists()
except AssertionError:
  print("- Look for character metadata in subdirectory")
  play_md_path = Path("pre_treatment/personnages-pieces.csv")
  assert(play_md_path.exists())
print(f"- Character metadata at {play_md_path.absolute()}")

indf = pd.read_csv(indf_path)
play_df = pd.read_csv(play_md_path)

# Postpro =====================================================================

# rename some columns
outdf = indf.rename(columns={'drama_type': 'genre',
                             'sex': 'gender',
                             'short_name': "play_short_name",
                             'progress': 'segment_number'})

# reorder columns
# character - social annotation - play metadata - spoken text fields
colnames = ["speaker", "gender", "social_class", "job", "job_category", "segment_number",
            "play_short_name", "genre", "text"]
outdf = outdf[colnames]

# recode values
outdf = outdf.replace({'gender': {'MALE': 'M', 'FEMALE': 'F',
                                  'UNKNOWN': 'U', '?F': 'F'}})

volksstuecke = ["bastian-dr-hans-im-schnokeloch",
                "clemens-d-brueder",
                "clemens-dr-amerikaner",
                "fuchs-heimlichi-lieb",
                "greber-s-teschtament",
                "sengelin-d-mamsell-elis",
                "wagner-die-greifensteiner"]

outdf.loc[outdf["play_short_name"].isin(volksstuecke), "genre"] = "volksstueck"
outdf.loc[outdf["genre"] == "horreur", "genre"] = "comedy"

outdf.loc[outdf["job_category"].isin(["unknown"]), "job_category"] = "grp_char/jcat_err"

# add play metadata from the play metadata sheet
# cols to add: author, written, print, thisEdition
print("- Crossing with play metadata")
authors = []
chosen_dates = []
date_types = []
date_errors = 0
play_errors = set()
import numpy as np
for idx, row in outdf.iterrows():
  md_row = play_df.loc[play_df["shortName"] == row["play_short_name"]]
  assert not md_row.empty
  play_author = md_row.author.iloc[0]
  authors.append(play_author)
  # the following columns are dates in the original metadata df
  play_written = md_row.written.iloc[0]
  play_printed = md_row.print.iloc[0]
  play_our_edition = md_row.thisEdition.iloc[0]
  assert {play_written, play_printed, play_our_edition} != {np.nan}

  try:
    play_written = int(play_written)
  except ValueError:
    play_written = np.nan
  try:
    play_printed = int(play_printed)
  except ValueError:
    play_printed = np.nan
  try:
    play_our_edition = int(play_our_edition)
  except ValueError:
    play_our_edition = np.nan

  # i'm expecting the original orthography to be respected in later editions
  # (to a reasonable extent for the purposes of the character distinctiveness task)
  # so gonna go with the written date if available, then print (first print date),
  # and if nothing else available, the date for the edition we used
  if not pd.isna(play_written):
    chosen_date = play_written
    date_types.append("written")
  elif not pd.isna(play_printed):
    chosen_date = play_printed
    date_types.append("printed")
  elif not pd.isna(play_our_edition):
    chosen_date = play_our_edition
    date_types.append("our_edition")
  else:
    chosen_date = np.nan
    date_types.append("unknown")
    date_errors += 1
    #print(f"  - Date errors {play_written}, {play_printed}, {play_our_edition}")
    if row['play_short_name'] not in play_errors:
      print(f"  - Date error for play {row['play_short_name']}")
      play_errors.add(row["play_short_name"])
  chosen_dates.append(chosen_date)
print(f"  - Number of speech turns with date errors: {date_errors} out of {len(outdf)}")

# add the new columns
insert_at = outdf.columns.to_list().index("gender")
outdf.insert(loc=insert_at+1, column="author", value=authors)
outdf.insert(loc=insert_at+2, column="date", value=chosen_dates)
outdf.insert(loc=insert_at+3, column="date_type", value=date_types)

# other cleanups

# some speaker names had trailing whitespace
outdf['speaker'] = outdf.speaker.apply(lambda x:x.strip())

# write out
outdf.to_csv(outdf_path, index=False)
