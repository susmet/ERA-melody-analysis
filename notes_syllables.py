# Count of all notes, count of all syllables, division of syllable count and note count

import os
from music21 import *
import pandas as pd
import csv

# Choose the directory of your data in you Google Drive (instead of ...)
# os.chdir('/content/drive/MyDrive/...')

# Returns for each file: filename, count of notes, count of syllables, division of syllable count and note count
def notes_syllables(specification1='', specification2=''): #Specifications can be added, e.g. filename contains text '2voices', default is no specifications
  results = []
  # Go through all files in directory
  for file in os.listdir():
    # Checks conditions
    if specification1 in file and specification2 in file:
      s = converter.parse(file)
      notes = s.parts[0].flat.notes
      count_notes = 0
      count_syllables = 0
      # Counts notes and syllables for each file
      for note in notes:
        count_notes += 1
        if note.lyric is not None:
          count_syllables += 1
      results.append([file, count_notes, count_syllables, round(count_syllables/count_notes, 3)])
  return(results)

# Applying the function and displaying results
results = notes_syllables(specification1='', specification2='') #Specifications can be defined here
df = pd.DataFrame(list(results), columns = ['Filename', 'Notes', 'Syllables', 'Syllables/Notes'])

# Save the results as a csv file
# Choose directory where to save the file in you Google Drive (instead of ...)
os.chdir('/content/drive/MyDrive/...')
df.to_csv('results.csv') #Name your file here

# Display the results
df
