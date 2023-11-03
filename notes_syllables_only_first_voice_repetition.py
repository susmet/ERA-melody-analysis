# Count of notes and syllables which includes repetitions (only first voice)

# Imports
import os
from music21 import *
import pandas as pd
import csv

# Choose the directory of your data in you Google Drive (instead of ...)
os.chdir('/content/drive/MyDrive/...')

# Funtion: Count of notes and syllables which includes repetitions (only first voice)
def notes_syllables_only_first_voice_repetition(specification1='', specification2=''): #Specifications can be added, e.g. filename contains text '2voices', default is no specifications
  results = []
  # Go through all files in directory
  for file in os.listdir():
    # Checks conditions
    if specification1 in file and specification2 in file:
      s = converter.parse(file)

      # VARIABLES
      #for counting notes and syllables
      count_notes = 0
      count_syllables = 0

      #for repetition count
      repeats = [] # repeat barline locations in score, e.g. [[1.0, 12.5]]
      repeat_started = False # Necessary condition because in corpus there is one ending barline without starting barline
      repeat_ended = False
      repeat = False

      # for remembering offsets of the notes and syllables of voice 1
      voices_nt_offsets = []
      voices_syl_offsets = []

      # GOING THROUGH STREAM ELEMENTS (i.e. mostly measures and voices)
      # Go through all measures and count notes + find all repeating barline durations
      # Go through all voices and save first voice's offsets of notes
      for el in s.recurse().getElementsByClass('Stream'):
        # Check if MEASURE type structure (here we count notes and syllables that have single voice)
        if isinstance(el, stream.Measure):
          measure_offset = el.offset #beginning of measure

          # Check if repetition has ended with previous element
          if repeat_ended == True:
            repeats[len(repeats)-1][1] = el.offset
            repeat_ended = False

          # Go through each element and find REPETITION barlines, NOTES, and VOICES
          for el_measure in el:

            # CHECK IF REPETITION
              # Check if it STARTS
            if str(el_measure) == '<music21.bar.Repeat direction=start>':
              repeat = True
              repeat_started = True
              repeats.append([el.offset, None])
              # Check if it ENDS
            elif str(el_measure) == '<music21.bar.Repeat direction=end>' and repeat_started == True:
              repeat = False
              repeat_ended = True

            # COUNT NOTES AND SYLLABLES — WITHOUT MULTIPLE VOICES
            # Check if NOTE
            elif isinstance(el_measure, note.Note) or isinstance(el_measure, chord.Chord):
              count_notes += 1 # Count note
              # Check if note is repeated, if so, double count it
              if repeat == True:
                count_notes += 1
              # Check if LYRIC (syllable)
              if el_measure.lyric is not None:
                count_syllables += 1 # Count syllable
                # Check if syllable is repeated, if so, double count it
                if repeat == True:
                  count_syllables += 1


        # REMEMBER VOICES
        # Check if VOICE
        if isinstance(el, stream.Voice):
          if str(el) == '<music21.stream.Voice 1>':
            for nt in el:
              # COUNT NOTES AND SYLLABLES — WITH MULTIPLE VOICES
              # Check if NOTE
              if isinstance (nt, note.Note) or isinstance(nt, chord.Chord):
                voices_nt_offsets.append(nt.offset + measure_offset)
                count_notes += 1
                if nt.lyric is not None:
                  count_syllables += 1
                  voices_syl_offsets.append(nt.offset + measure_offset)
      if repeat_ended == True:
        repeats[len(repeats)-1][1] = el.offset
        if measure_offset == repeats[len(repeats)-1][1] or measure_offset <= 0: # Check whether repeat ends in the end of the score
          repeats[len(repeats)-1][1] = -1 # Give it a value of -1
          repeat_ended = False

      # COUNT VOICE 1 REPEATS
      for repeat in repeats:
        # if repeat ends in the middle of the score
        if repeat[1] > 0:
          #count notes
          for note_offset in voices_nt_offsets:
            if note_offset >= repeat[0] and note_offset <= repeat[1]:
              count_notes +=1
          #count syllables
          for syllable_offset in voices_syl_offsets:
            if syllable_offset >= repeat[0] and syllable_offset <= repeat[1]:
              count_syllables +=1

        # if repeat ends in the end of the score (marked by either -1 or 0.0)
        else:
          #count notes
          for note_offset in voices_nt_offsets:
            if note_offset >= repeat[0]:
              count_notes +=1
          #count syllables
          for syllable_offset in voices_syl_offsets:
            if syllable_offset >= repeat[0]:
              count_syllables +=1

      # Append to results
      results.append([file, count_notes, count_syllables, round(count_syllables/count_notes, 3)])

  return(results)

results = notes_syllables_only_first_voice_repetition(specification1='', specification2='')

# Apply the function
df = pd.DataFrame(list(results), columns = ['Filename', 'Notes', 'Syllables', 'Syllables/Notes'])

# Save the results as a csv file
# Choose directory where to save the file in you Google Drive (instead of ...)
os.chdir('/content/drive/MyDrive/...')
df.to_csv('results.csv') #Name your file here

# Display the results
df
