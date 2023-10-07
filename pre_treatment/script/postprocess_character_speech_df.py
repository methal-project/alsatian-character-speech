import os
import pandas as pd
from pathlib import Path

indf_path = Path("../../overall-per-character-speech.tsv")
# relative path to parent's parent ok to execute this module standalone,
# the second relative path to same directory is when called with
# ../../collect_character_speech_with_metadata.sh (main script)
try:
  assert indf_path.exists()
except AssertionError:
  print("Look for df in same directory")
  indf_path = Path("overall-per-character-speech.tsv")
  assert(indf_path.exists())
print(f"Input at {indf_path.absolute()}")

outdf_path = indf_path.with_stem(indf_path.stem + "-postpro3")
print(f"Output at {outdf_path.absolute()}")

indf = pd.read_csv(indf_path)

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

# out
outdf.to_csv(outdf_path, index=False)
