import sys
import xlsxwriter
import xlrd
import random

# Manipulation on text
def takeOnly2to3ofSentences ():
    x = random.randint(0, 2)
    if (x == 0): return False
    else:        return True


# INPUT
# file_name = r"C:\Users\משפחת\Downloads\אוניברסיטה\שנה ד\פרוייקט\laugh Times+srt- sorted episodes\S08E02.xls"
file_name = sys.argv[1]
wb = xlrd.open_workbook(file_name)
sheet_srt = wb.sheet_by_index(0)  # simple sentences
len_srt = sheet_srt.nrows
sheet_srt1 = wb.sheet_by_index(2)  # best jokes
len_srt1 = sheet_srt1.nrows
sheet_srt2 = wb.sheet_by_index(1)
len_srt2 = sheet_srt2.nrows


# OUTPUT
# write_file_name = r"C:\Users\משפחת\Downloads\אוניברסיטה\שנה ד\פרוייקט\laugh Times+srt- sorted episodes\S08E02all.xlsx"
write_file_name = sys.argv[2]
workbook = xlsxwriter.Workbook(write_file_name)
worksheet = workbook.add_worksheet()


joke_index = 0
for i in range(len_srt1):  # i stand for row in 'sheet_srt1'
    line = sheet_srt1.cell_value(i, 3)
    speaker = sheet_srt1.cell_value(i, 2)
    if (speaker != '???'):
        worksheet.write(joke_index, 0, speaker + " - " + line)
        worksheet.write(joke_index, 1, "JOKE")
        joke_index += 1

		
x = True				# take all data
sentence_index = 0
for i in range(len_srt):  # i stand for row in 'sheet_srt'
    #x = takeOnly2to3ofSentences()
    if(x == True):                                    ### take Only 1 to 3 of Sentences ~ 40
        line = sheet_srt.cell_value(i, 3)
        speaker = sheet_srt.cell_value(i, 2)
        if (speaker != '???'):
            worksheet.write(joke_index + sentence_index, 0, speaker + " - " + line)
            worksheet.write(joke_index + sentence_index, 1, "SENTENCE")
            sentence_index += 1
        
print(f"joke_index: {joke_index}")


# declere half funny jokes as SENTENCE
middle_index = 0
for i in range(len_srt2):  # i stand for row in 'sheet_srt2'
    #x = takeOnly2to3ofSentences()
    if(x == True):                                    ### take Only 1 to 3 of Sentences ~ 40
        line = sheet_srt2.cell_value(i, 3)
        speaker = sheet_srt2.cell_value(i, 2)
        if (speaker != '???'):
            worksheet.write(joke_index + sentence_index + middle_index, 0, speaker + " - " + line)
            worksheet.write(joke_index + sentence_index + middle_index, 1, "SENTENCE")
            middle_index += 1
workbook.close()


