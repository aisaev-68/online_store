import xlrd, xlwt

list_smeta = ['ИС', 'ССОИ', 'СТН', 'СОТС', 'СКУД', 'ССО', 'СЭ', 'СОО']
rb = xlrd.open_workbook('oldsmeta.xls', formatting_info=True)
wb = xlwt.Workbook()
for i in range(8):
    ws = wb.add_sheet(list_smeta[i])
    sheet = rb.sheet_by_index(i)
    j = 0
    for rownum in range(sheet.nrows):
        new_row = []
        row = sheet.row_values(rownum)
        row_str = str(row[1])
        if not row_str.startswith('ФЕР'):
            if str(row[1]).startswith('ТЦ'):
                price = sheet.row_values(rownum + 2)
                row[9] = price[2][5:].split('/')[0] # меняю цену
                new_row.append(row[2])
                new_row.append(row[5])
                new_row.append(row[8])
                new_row.append(row[9])
                j += 1
            elif '-' in str(row[1]) and str(row[1]).split('.')[0].isdigit():
                new_row.append(row[2])
                new_row.append(row[5])
                new_row.append(row[8])
                new_row.append(row[9])
                j += 1
            for ind, item in enumerate(new_row):
                ws.write(j - 1, ind, item)

wb.save('new06.xls')
