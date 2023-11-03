# ERA-melody-analysis
Code written for melody analysis in Estonian Literary Museum.
All code is written to be used in Google Colaboratory using music-xml files as the source data and it was first developed for Ukrainian ballads which contained repetition and both single-voiced scores and multiple-voiced scores.

### notes_syllables.py
Count of notes, count of syllables, division of syllable count and note count

### notes_syllables_only_first_voice.py
Only first voice used in count of notes, count of syllables, and division of syllable count and note count

### notes_syllables_only_first_voice_repetition.py
Count of notes and syllables which includes repetitions (only first voice)

### notes_durations_custom.py
Durations of notes are listed and modified according to the following rules:
1. The lengths of slurs and rests are added to the lengths of previous notes
2. Repeated notes are written out, i.e. the lenghts are added where necessary
