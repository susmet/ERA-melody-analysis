#DURATIONS
# Durations of notes are listed and modified according to the following rules:

# 1. The lengths of slurs and rests are added to the lengths of previous notes
# 2. Repeated notes are written out, i.e. the lenghts are added where necessary

# Output:
# filename    lengths of notes
# file.xml 	 [0.5, 1.0, 0.5, 0.75, 0.25, 0.5, ...]


# Imports
import os
from music21 import *
import pandas as pd
from fractions import Fraction
import csv

# Choose the directory of your data in you Google Drive (instead of ...)
os.chdir('/content/drive/MyDrive/...')

# Helping function for each note
def add_duration(el, durations, repeated_durations, measure_nr, some_slurs, repetition):

  previous = False # is together with previous note

  # Duration to fraction format
  if type(el.duration.quarterLength).__name__ == 'float':
    duration = Fraction.from_float(el.duration.quarterLength)
  else:
    duration = el.duration.quarterLength

  # 1) If one-voiced note
  if isinstance(el, note.Note):

    # CHECK IF TOGETHER WITH PREVIOUS NOTE
    is_slur = False

    # a) Check if contains slur by itself (i.e. slur is in the note's data structure)
    if el.tie is not None: # and element.tie.type in ['start', 'continue']:
      # Check if end of slur
      if el.tie.type == 'stop':
        # If note is not separate
        if str(el.beams) != '<music21.beam.Beams>':
          note_beams = []
          for beam in el.beams.beamsList:
            note_beams.append(beam.type)
          if 'start' in note_beams and 'continue' not in note_beams:
            previous = True
            is_slur = True
        # If note is separate
        else:
          previous = True
          is_slur = True

    # b) Check if is in some_slurs (i.e. slurs that are stored separately from the notes)
    note_offset = el.offset
    if is_slur != True:
      for slur in some_slurs:
        if slur[0] == measure_nr and slur[1] == note_offset:
          # If note is not separate
          if str(el.beams) != '<music21.beam.Beams>':
            note_beams = []
            for beam in el.beams.beamsList:
              note_beams.append(beam.type)
            if 'start' in note_beams and 'continue' not in note_beams:
              previous = True
              is_slur = True
          # If note is separate
          else:
            previous = True
            is_slur = True
            previous = True

    # c) Check if connected to the previous note
    if is_slur == False:
      if str(el.beams) != '<music21.beam.Beams>':
        note_beams = []
        for beam in el.beams.beamsList:
          note_beams.append(beam.type)
          # Note is connected to the previous note
          if 'stop' in note_beams or 'continue' in note_beams:
            previous = True
          # Note is separate
          elif 'start' in note_beams and 'continue' not in note_beams:
            previous = False


  # 2) Check if rest
  elif isinstance(el, note.Rest):
    previous = True

  # ADD DURATION TO DURATIONS LIST

  # 1) Add duration to duration of the previous note
  if previous == True:
    if len(durations) != 0: # if list not empty
      durations[-1] = durations[-1] + duration
      # If repetition
      if repetition == True:
        if len(repeated_durations) != 0:
          repeated_durations[-1] = repeated_durations[-1] + duration
        else:
          repeated_durations.append(duration)
    else: # if list is empty
      durations.append(duration)
      if repetition == True:
        repeated_durations.append(duration)
  # 2) Add new duration
  elif isinstance(el, note.Note) or isinstance(el, note.Rest):
    durations.append(duration)
    if repetition == True:
      repeated_durations.append(duration)

  return durations, repeated_durations



# MAIN FUNCTION
def notes_durations_custom(specification1='', specification2=''): #Specifications can be added, e.g. filename contains text '2voices', default is no specifications
  results = []

  for file in os.listdir():
    # Check conditions
    if specification1 in file and specification2 in file:
      s = converter.parse(file)

      # 1. Find some of the slurs
      some_slurs = [] # [[measure, offset], ...] —> all last notes of slurs in this format

      for element in s:
        if isinstance(element, stream.Part):
          for line in element:
            if isinstance(line, spanner.Slur):
              some_slurs.append([line[1].measureNumber, line[1].offset])

      # 2. Go through the file
      durations = [] # [[0.5,0.5,2,1,1], ...]
      measure_nr = 0
      repetition = False
      repeated_durations = []

      for element in s:
        if isinstance(element, stream.Part):
          for e in element:
            # Check if measure
            if isinstance(e, stream.Measure):
              measure_nr = e.measureNumber
              for el in e:

                # 1) If repetition
                if isinstance(el, bar.Repeat):
                  repeat = el.direction
                  if repeat == 'start':
                    repetition = True
                  if repeat == 'end': #elif
                    repetition = False
                    for double in repeated_durations:
                      durations.append(double)
                    repeated_durations = []

                durations, repeated_durations = add_duration(el, durations, repeated_durations, measure_nr, some_slurs, repetition)

                # VOICE 1
                if isinstance(el, stream.Voice):
                  if str(el) == '<music21.stream.Voice 1>':
                    for el_voice in el:
                      durations, repeated_durations = add_duration(el_voice, durations, repeated_durations, measure_nr, some_slurs, repetition)

      # Add to results, if needed, get the thirds into right format
      for i in range(len(durations)):
        if round(float(durations[i]), 1) == float(durations[i]) or round(float(durations[i]), 2) == float(durations[i]):
          durations[i] = float(durations[i])
      results.append([file, durations])
  return results


results = notes_durations_custom(specification1='', specification2='') # Add specifications here

# Display results:

#for result in results:
#  print(result[0], '\t', result[1])


# Or alternatively:

df = pd.DataFrame(list(results), columns = ['Filename', 'Durations'])

# Save the results as a csv file
# Choose directory where to save the file in you Google Drive (instead of ...)
os.chdir('/content/drive/MyDrive/...')
df.to_csv('results.csv') #Name your file here

# Display the results
df
