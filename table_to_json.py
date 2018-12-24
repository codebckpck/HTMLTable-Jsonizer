import json
import numpy as np

from bs4 import BeautifulSoup
from itertools import product

class TableToJSON:
    '''
    Converts table from html document to json format
    '''

    def __init__(self, file_name):
        self.table_width = 0

        try:
            with open(file_name) as fp:

                soup = BeautifulSoup(fp.read(), "lxml")

                list_of_tables = self.find_all_tables(soup)
                print(len(list_of_tables))

                self.converted_tr = soup.find_all('tr')

                # find width of the table
                for single_td in self.converted_tr[0].find_all('th'):
                    self.table_width += int(single_td.get("colspan", "1"))

                # add only td to table named temporary_table_td
                self.temporary_table_td = self.create_matrix('td')

                # add only th to table named temporary_table_th
                self.temporary_table_th = self.create_matrix('th')
        except IOError:
            print('File does not exist!')


    def find_all_tables(self, soup):
        return soup.find_all('tbody')

    #for single table cell finds spans and apply to matrix
    def cell_to_matrix(self, temporary_table, single_cell, column_shift, idx, idxtd):
        #until he finds an empty cell
        while temporary_table[idx, idxtd + column_shift] is not None:
            column_shift += 1

        colspan_range = int(single_cell.get("colspan", "1"))
        rowspan_range = int(single_cell.get("rowspan", "1"))

        #fill matching matrix cells
        cp = product(range(rowspan_range), range(colspan_range));
        for c in cp:
            while temporary_table[
                idx + c[0],
                idxtd + column_shift + c[1]
            ]:
                column_shift += 1
            temporary_table[idx + c[0], idxtd + column_shift + c[1]] \
                = single_cell.text.strip()
        column_shift += int(colspan_range) - 1
        return column_shift

    #return matrix maked from table for specified tag.
    def create_matrix(self, tag_type):
        temporary_table = np.empty(shape=(len(self.converted_tr), self.table_width), dtype=object)

        for idx, single_tr in enumerate(self.converted_tr):
            column_shift = 0  # when encouter colspan add number
            for idxtd, single_cell in enumerate(single_tr.find_all(['td', 'th'])):
                if single_cell.name == tag_type:
                    column_shift = self.cell_to_matrix(temporary_table, single_cell, column_shift, idx, idxtd)

        return temporary_table


    # search for th in each matrix row to the left from td (is_row) or in each column above td
    def __search_th(self, search_range, pos_td, is_row):
        temp_name = ''

        for s in range(search_range):
            if is_row:
                second_pos, first_pos = s, pos_td
            else:
                second_pos, first_pos = pos_td, s

            if self.temporary_table_th[first_pos,  second_pos]:
                temp_name = temp_name + self.temporary_table_th[first_pos,  second_pos] + '.'

        return temp_name


    def show_td_matrix(self):
        print('Matrix for <td>: \n', self.temporary_table_td)


    def show_th_matrix(self):
        print('\nMatrix for <th>: \n', self.temporary_table_th)


    def get_json(self):
        #return json format
        temporary_dict = {}

        # change td matrix to dictionary with key from th rows.columns
        cp = product(range(len(self.converted_tr)), range(self.table_width));
        for c in cp:
            if self.temporary_table_td[c[0], c[1]]:
                temporary_dict[
                    (self.__search_th(c[1], c[0], True)
                     + self.__search_th(c[0], c[1], False))[:-1]
                ] = self.temporary_table_td[c[0], c[1]]

        return json.dumps(temporary_dict, ensure_ascii=False)


if __name__ == "__main__":
    print(TableToJSON.__doc__)
    vivo = TableToJSON("vivo_ok.html")
    vivo.show_td_matrix()
    vivo.show_th_matrix()
    print('\noutput json:')
    print(vivo.get_json())

