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
        new_row_2 = []
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
                print(new_row)
                # print(price[2])
            elif '-' in str(row[1]) and str(row[1]).split('.')[0].isdigit():
                new_row.append(row[2])
                new_row.append(row[5])
                new_row.append(row[8])
                new_row.append(row[9])
                print(new_row)
        for ind, item in enumerate(new_row):
            ws.write(j, ind, item)
        j += 1
wb.save('new06.xls')
    # for c_el in row:
    #     print(c_el)