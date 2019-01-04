import argparse
import json
import numpy as np
import sys

from bs4 import BeautifulSoup
from itertools import product

class TableToJSON:
    '''
    Converts table from html document to json format
    '''

    def __init__(self, file_name, table_number = 0):
        self.table_width = 0
        self.converted_tr = 0
        self.temp_table_td = 0
        self.temp_table_th = 0
        self.table_number = table_number

        try:
            with open(file_name, encoding="utf8") as fp:

                soup = BeautifulSoup(fp.read(), "lxml")

                self.find_all_tables(soup)

        except IOError:
            print('File does not exist!')


    def find_all_tables(self, soup):
        list_of_tables = soup.find_all('table')
        if len(list_of_tables):
            if len(list_of_tables) >= self.table_number:
                self.table_number=len(list_of_tables) - 1
            self.converted_tr = list_of_tables[int(self.table_number)] = soup.find_all('tr')

            if len(self.converted_tr):
                # find width of the table
                for single_td in self.converted_tr[0].find_all('th'):
                    self.table_width += int(single_td.get("colspan", "1"))

                # add only td to table named temp_table_td
                self.temp_table_td = self.create_matrix('td')

                # add only th to table named temp_table_th
                self.temp_table_th = self.create_matrix('th')
            else:
                print("can't parse table")
        else:
            print('no table in document')


    #for single table cell finds spans and apply to matrix
    def __cell_to_matrix(self, temp_table, single_cell, column_shift, idx, idxtd, tag_type):
        #until he finds an empty cell
        while temp_table[idx, idxtd + column_shift] is not None or 0:
            column_shift += 1

        colspan_range = int(single_cell.get("colspan", "1"))
        rowspan_range = int(single_cell.get("rowspan", "1"))

        #fill matching matrix cells
        cp = product(range(rowspan_range), range(colspan_range))
        for c in cp:
            while temp_table[
                idx + c[0],
                idxtd + column_shift + c[1]
            ]:
                column_shift += 1
            if single_cell.name == tag_type:
                temp_table[idx + c[0], idxtd + column_shift + c[1]] \
                    = single_cell.text.strip()
            else:
                temp_table[idx + c[0], idxtd + column_shift + c[1]] = 0
        column_shift += int(colspan_range) - 1
        return column_shift


    #return matrix maked from table for specified tag.
    def create_matrix(self, tag_type):
        temp_table = np.empty(shape=(len(self.converted_tr), self.table_width), dtype=object)

        for idx, single_tr in enumerate(self.converted_tr):
            column_shift = 0  # when encouter colspan add number
            for idxtd, single_cell in enumerate(single_tr.find_all(['td', 'th'])):
                column_shift = self.__cell_to_matrix(temp_table, single_cell, column_shift, idx, idxtd, tag_type)

        return temp_table


    # search for th in each matrix row to the left from td (is_row) or in each column above td
    def __search_th(self, search_range, pos_td, is_row):
        temp_name = ''
        end_of_th = 0 #variable to check is this end of th in teh middle of table
        is_span ='' #if there was row or col span don't repeat

        temp_name = ''

        for s in range(search_range):
            reverse_range = search_range - s - 1
            if is_row:
                second_pos, first_pos = reverse_range, pos_td
            else:
                second_pos, first_pos = pos_td, reverse_range

            if self.temp_table_th[first_pos, second_pos] \
                    and end_of_th != 2 \
                    and self.temp_table_th[first_pos, second_pos] != is_span:
                temp_name = self.temp_table_th[first_pos, second_pos] + '.' + temp_name
                is_span =  self.temp_table_th[first_pos, second_pos]
                end_of_th = 1
            elif end_of_th == 1:
                end_of_th = 2

        return temp_name


    def show_td_matrix(self):
        print('Matrix for <td>: \n', self.temp_table_td)


    def show_th_matrix(self):
        print('\nMatrix for <th>: \n', self.temp_table_th)


    def get_json(self):
        #return json format
        temp_dict = {}

        #check if table exist
        if self.converted_tr == 0:
            return print('no table to make json')

        # change td matrix to dictionary with key from th rows.columns
        cp = product(range(len(self.converted_tr)), range(self.table_width))
        for c in cp:
            if self.temp_table_td[c[0], c[1]]:
                temp_dict[
                    (self.__search_th(c[1], c[0], True)
                     + self.__search_th(c[0], c[1], False))[:-1]
                ] = self.temp_table_td[c[0], c[1]]

        return json.dumps(temp_dict, ensure_ascii=False)


if __name__ == "__main__":
    print(TableToJSON.__doc__)
    parser = argparse.ArgumentParser(description='Change HTML table to json.')
    parser.add_argument('filename', help="Name of HTML file to parse. Required")
    parser.add_argument('-t', '--table', help="The number of the table in the HTML file.", type=int, default=0,
                        required=False)
    args = parser.parse_args()
    vivo = TableToJSON(args.filename, args.table)

    vivo.show_td_matrix()
    vivo.show_th_matrix()
    print('\noutput json:')
    print(vivo.get_json())

