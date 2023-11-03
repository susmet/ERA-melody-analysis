# Only first voice used in count of notes, count of syllables, and division of syllable count and note count

import os
from music21 import *
import pandas as pd
import csv

# Choose the directory of your data in you Google Drive (instead of ...)
# os.chdir('/content/drive/MyDrive/...')

# Returns for each file (takes only first voice): filename, count of notes, count of syllables, division of syllable count and note count
def notes_syllabes_only_first_voice(specification1='', specification2=''): #Specifications can be added, e.g. filename contains text '2voices', default is no specifications
  results = []
  # Go through all files in directory
  for file in os.listdir():
    # Checks conditions
    if specification1 in file and specification2 in file:
      s = converter.parse(file)
      count_notes = 0
      count_syllables = 0
      # Counts only the notes and syllables of first voice for each file
      for el in s.recurse().getElementsByClass('Stream'):
        if not isinstance(el, stream.Voice): # If there is only one voice at the time
          for nt in el:
            if isinstance (nt, note.Note) or isinstance (nt, chord.Chord):
              count_notes += 1
              if nt.lyric is not None:
                count_syllables += 1
        else:
          if str(el) == '<music21.stream.Voice 1>': # Takes only first voice
            for nt in el:
              if isinstance (nt, note.Note):
                count_notes += 1
                if nt.lyric is not None:
                  count_syllables += 1
      results.append([file, count_notes, count_syllables, round(count_syllables/count_notes, 3)])
  return(results)

# Applying the function
results = notes_syllabes_only_first_voice(specification1='', specification2='')
df = pd.DataFrame(list(results), columns = ['Filename', 'Notes', 'Syllables', 'Syllables/Notes'])

# Save the results as a csv file
# Choose directory where to save the file in you Google Drive (instead of ...)
os.chdir('/content/drive/MyDrive/...')
df.to_csv('results.csv') #Name your file here

# Display the results
df
