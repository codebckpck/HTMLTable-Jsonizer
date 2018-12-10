import json
import numpy as np

from bs4 import BeautifulSoup


'''
Converts table from html document to json format
'''

#return matrix maked from table for specified tag.
def create_matrix(tag_type):
    temporary_table = np.empty(shape=(len(converted_tr), table_width), dtype=object)
    for idx, single_tr in enumerate(converted_tr):
        column_shift = 0  # when encouter colspan add number
        for idxtd, single_td in enumerate(single_tr.find_all(lambda tag: tag.name == 'td' or tag.name == 'th')):
            if single_td.name == tag_type:
                while temporary_table[idx, idxtd + column_shift] is not None:
                    column_shift += 1
                try:
                    colspan_range = int(single_td["colspan"])
                except (ValueError, KeyError) as e:
                    colspan_range = 1
                try:
                    rowspan_range = int(single_td["rowspan"])
                except (ValueError, KeyError) as e:
                    rowspan_range = 1

                if colspan_range == 1 and rowspan_range == 1:
                    temporary_table[idx, idxtd + column_shift] = single_td.text.strip()
                else:
                    for j in range(rowspan_range):
                        for i in range(colspan_range):
                            while temporary_table[idx + j, idxtd + column_shift + i] is not None:
                                column_shift += 1
                            temporary_table[idx + j, idxtd + column_shift + i] = single_td.text.rstrip()
                    column_shift += (int(colspan_range) - 1)
    return temporary_table


with open("vivo_ok.html") as fp:
    soup = BeautifulSoup(fp.read(), "lxml")

converted_tr = soup.find_all('tr')
table_width = 0


#find width of the table
for single_td in converted_tr[0].find_all('th'):
     try:
         table_width += int(single_td["colspan"])
     except (ValueError, KeyError) as e:
         table_width += 1


#add only td to table named temporary_table_td
temporary_table_td = create_matrix('td')

#add only th to table named temporary_table_th
temporary_table_th = create_matrix('th')

print('Matrix for <td>: \n', temporary_table_td)
print('\nMatrix for <th>: \n', temporary_table_th)


temporary_dict = {}
temporary_name = ''
#change td matrix to dictionary with key from th rows.columns
for i in range(len(converted_tr)):
    for j in range(table_width):
        if temporary_table_td[i, j] is not None:
            temporary_name = ''
            for i_th in range(table_width):#search for th in each row to the left from td
                if temporary_table_th[i, i_th] is not None:
                     temporary_name = temporary_name + temporary_table_th[i, i_th] + '.'
            for i_th in range(len(converted_tr)):#search for th in each column above td
                if temporary_table_th[i_th, j] is not None:
                    temporary_name = temporary_name + temporary_table_th[i_th, j] + '.'
            temporary_name = temporary_name[:-1]
            temporary_dict[temporary_name] = temporary_table_td[i, j]

jsonarray = json.dumps(temporary_dict, ensure_ascii=False)

print('output json:')
print(jsonarray)