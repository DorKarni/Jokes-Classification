import sys
import xlsxwriter
import xlrd

# INPUT
file_name = sys.argv[1]
wb = xlrd.open_workbook(file_name)
sheet_srt = wb.sheet_by_index(0)
len_srt = sheet_srt.nrows
sheet_srt1 = wb.sheet_by_index(1)
len_srt1 = sheet_srt1.nrows
sheet_srt2 = wb.sheet_by_index(2)
len_srt2 = sheet_srt2.nrows

workbook = xlsxwriter.Workbook(sys.argv[2])
worksheet = workbook.add_worksheet()

for i in range(len_srt):    # i stand for row in 'sheet_srt'
    line = sheet_srt.cell_value(i, 3)
    worksheet.write(i, 0, line)
    worksheet.write(i, 1, "SENTENCE")

for i in range(len_srt1):    # i stand for row in 'sheet_srt'
    line = sheet_srt1.cell_value(i, 3)
    worksheet.write(i+len_srt, 0, line)
    worksheet.write(i+len_srt, 1, "JOKE~")

for i in range(len_srt2):    # i stand for row in 'sheet_srt'
    line = sheet_srt2.cell_value(i, 3)
    worksheet.write(i+len_srt+len_srt1, 0, line)
    worksheet.write(i+len_srt+len_srt1, 1, "JOKE")

workbook.close()


