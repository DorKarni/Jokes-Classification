﻿
def countQustionMark(line, counter):
    if ("?" in line):
        counter += 1
    return counter

def saveAsFile(_sheet, _index, _line, _speaker, _start, _end):
    _sheet.write(_index, 3, _line)
    _sheet.write(_index, 2, _speaker)
    _sheet.write(_index, 1, _end)
    _sheet.write(_index, 0, _start)

def saveAsFileWithLabel(_sheet, _index, _line, _speaker, _start, _end, _label, half_joke = False):
    _sheet.write(_index, 4, _label)
    _sheet.write(_index, 3, _line)
    _sheet.write(_index, 2, _speaker)
    _sheet.write(_index, 1, _end)
    _sheet.write(_index, 0, _start)

    if(half_joke == True): _sheet.write(_index, 5, "~")


import sys
import xlrd
import xlwt
import csv

# INPUT
# file_name = r"C:\Users\משפחת\Downloads\אוניברסיטה\שנה ד\פרוייקט\laugh Times+srt- sorted episodes\S02E16jokes.xls"
file_name = sys.argv[2]
wb = xlrd.open_workbook(file_name)
sheet_srt = wb.sheet_by_index(0)
len_srt = sheet_srt.nrows



laugh_arr = []
start_laugh = []
end_laugh = []
# with open(r"C:\Users\משפחת\Downloads\אוניברסיטה\שנה ד\פרוייקט\laugh Times+srt- sorted episodes\S02E16_jokes.csv", 'r') as file_name2:
with open(sys.argv[1], 'r') as file_name2:
    sheet_laugh = csv.reader(file_name2)
    for row in sheet_laugh:
        laugh_arr.append(row)


for row in laugh_arr:
    if(row != []):
        start_laugh.append(row[0])
        end_laugh.append(row[1])

    #else:
     #   start_laugh.append(row)
      #  end_laugh.append(row)


len_laugh = len(start_laugh)

# OUTPUT
# first column- speaker; second column- line

wb_write = xlwt.Workbook()
sheet_all = wb_write.add_sheet('ALL', cell_overwrite_ok=True)
index_write= 0

# wb_write = xlwt.Workbook()
# sheet_not_funny = wb_write.add_sheet('SENTENCE', cell_overwrite_ok=True)
# index_not_funny = 0
#
# sheet_all_jokes = wb_write.add_sheet('ALL JOKES', cell_overwrite_ok=True)
# index_all_jokes = 0
#
# sheet_best_jokes = wb_write.add_sheet('BEST JOKES', cell_overwrite_ok=True)
# index_best_jokes = 0

questionMARKJOKES = 0
questionMARKSENTENCE = 0

index_laugh = 1     # all laugh time files start with title line, and have empty line between each data line
last_line = ""      # remembering the last joke line
joke_counter = 0
for i in range(len_srt-1):    # i stand for row in 'sheet_srt'

    # taking a full sentence
    line = ''
    speaker_i = sheet_srt.cell_value(i, 3)
    speaker_i_first_line = i
    while (sheet_srt.cell_value(speaker_i_first_line, 3) == speaker_i) :
        speaker_i_first_line = speaker_i_first_line - 1
    for row in range(speaker_i_first_line, i):
        line = line + " " + sheet_srt.cell_value(row+1, 2)

    # CLEANING 'line'
    # remove parenthesis
    while (line.find('(') != -1):
        start = line.find('(')
        end = line.find(')')
        bad_chars = line[start:end + 1]
        line = line.replace(bad_chars, '')

    # remove songs part
    if ("♪" in line):
        line = ""
        continue

    # classify the srt row to 1 of 3 options: all jokes, funny jokes, simple sentences

    # ALL JOKES
    start_luagh_time = float(start_laugh[index_laugh]) * 1000
    #print(start_luagh_time)

    end_laugh_time = float(end_laugh[index_laugh]) * 1000
    if(sheet_srt.cell_value(i+1,0) > start_luagh_time): # -> line is a joke
        joke_counter = joke_counter+1
        # FUNNY JOKES
        space_count = 0     # DATA_CONDITION:    check numbers of words in line
        for char in line:
            if (char == " "):
                space_count += 1
        if ((end_laugh_time - start_luagh_time) > 2000 and (space_count >= 4)): # Characteristics of a funny joke
            if (last_line in line and index_write > 1):                     # remove double lines
                saveAsFileWithLabel(sheet_all, index_write - 1, line, speaker_i,
                       sheet_srt.cell_value(speaker_i_first_line + 1, 0), sheet_srt.cell_value(i, 1), "JOKE")
            else:
                saveAsFileWithLabel(sheet_all, index_write, line, speaker_i,
                    sheet_srt.cell_value(speaker_i_first_line + 1, 0), sheet_srt.cell_value(i, 1), "JOKE")

                index_write += 1


            questionMARKJOKES = countQustionMark(line, questionMARKJOKES)

        # REGULAR JOKES
        else:
            if (last_line in line and index_write > 1):                     # remove double lines
                saveAsFileWithLabel(sheet_all, index_write - 1, line, speaker_i,
                                    sheet_srt.cell_value(speaker_i_first_line + 1, 0), sheet_srt.cell_value(i, 1),
                                    "JOKE", True)

            else:
                saveAsFileWithLabel(sheet_all, index_write, line, speaker_i,
                                    sheet_srt.cell_value(speaker_i_first_line + 1, 0), sheet_srt.cell_value(i, 1),
                                    "JOKE", True)

                index_write += 1

        while (sheet_srt.cell_value(i + 1, 0) > float(start_laugh[index_laugh]) * 1000 and (i+1)<len_srt and index_laugh<len_laugh-1):
            index_laugh = index_laugh + 1


    # SIMPLE SENTENCES
    else:
        if(len(line.split()) > 4):         # DATA_CONDITION:    check numbers of words in line
            if (last_line in line and index_write > 1):  # remove double lines
                saveAsFileWithLabel(sheet_all, index_write - 1, line, speaker_i,
                                    sheet_srt.cell_value(speaker_i_first_line + 1, 0), sheet_srt.cell_value(i, 1),
                                    "SENTENCE")
            else:
                saveAsFileWithLabel(sheet_all, index_write, line, speaker_i,
                                    sheet_srt.cell_value(speaker_i_first_line + 1, 0), sheet_srt.cell_value(i, 1),
                                    "SENTENCE")

                index_write += 1

            questionMARKSENTENCE = countQustionMark(line, questionMARKSENTENCE)


    last_line = line

print(index_write)

# print(joke_counter)
#print("questionMARKSENTENCE", questionMARKSENTENCE, questionMARKSENTENCE/(index_not_funny-1))
#print("questionMARKJOKES", questionMARKJOKES, questionMARKJOKES/(index_best_jokes-1))
# print((questionMARKSENTENCE/(index_not_funny-1))-(questionMARKJOKES/(index_best_jokes-1)))


wb_write.save(sys.argv[3])
# wb_write.save(r"C:\Users\משפחת\Downloads\אוניברסיטה\שנה ד\פרוייקט\laugh Times+srt- sorted episodes\S02E16_2.xls")




# finding jokes- if this is the last line before the laugh had
# start the next line starting time is after the laugh had started



