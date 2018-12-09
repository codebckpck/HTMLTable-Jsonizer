from bs4 import BeautifulSoup
import json
import numpy as np

'''
Converts table from html document to json format
'''

html_doc = """

<table style="border: 1px solid #999999; width: 100%; background:#F6F6F6;" cellpadding="3" cellspacing="0" class="inflection-table">

<tbody><tr>
<th style="border: 1px solid #999999; background:#B0B0B0" rowspan="2">
</th>
<th style="border: 1px solid #999999; background:#D0D0D0" colspan="2">singular
</th>
<th style="border: 1px solid #999999; background:#D0D0D0" colspan="2">plural
</th></tr>
<tr>
<th style="border: 1px solid #999999; background:#D0D0D0; width:21%">masculine
</th>
<th style="border: 1px solid #999999; background:#D0D0D0; width:21%">feminine
</th>
<th style="border: 1px solid #999999; background:#D0D0D0; width:21%">masculine
</th>
<th style="border: 1px solid #999999; background:#D0D0D0; width:21%">feminine
</th></tr>
<tr>
<th style="border: 1px solid #999999; background:#b0bfd4"><a href="https://en.wiktionary.org/wiki/Appendix:Glossary#positive" title="Appendix:Glossary">positive</a>
</th>
<td style="border: 1px solid #999999;" valign="top"><span class="Latn" lang="pt"><strong class="selflink">vivo</strong></span>
</td>
<td style="border: 1px solid #999999;" valign="top"><span class="Latn" lang="pt"><a href="https://en.wiktionary.org/wiki/viva#Portuguese" title="viva">viva</a></span>
</td>
<td style="border: 1px solid #999999;" valign="top"><span class="Latn" lang="pt"><a href="https://en.wiktionary.org/wiki/vivos#Portuguese" title="vivos">vivos</a></span>
</td>
<td style="border: 1px solid #999999;" valign="top"><span class="Latn" lang="pt"><a href="https://en.wiktionary.org/wiki/vivas#Portuguese" title="vivas">vivas</a></span>
</td></tr>
<tr>
<th style="border: 1px solid #999999; background:#b0bfd4"><a href="https://en.wiktionary.org/wiki/Appendix:Glossary#comparative" title="Appendix:Glossary">comparative</a>
</th>
<td style="border: 1px solid #999999;" valign="top"><span class="Latn" lang="pt"><a href="https://en.wiktionary.org/wiki/mais#Portuguese" title="mais">mais</a> vivo</span>
</td>
<td style="border: 1px solid #999999;" valign="top"><span class="Latn" lang="pt"><a href="https://en.wiktionary.org/wiki/mais#Portuguese" title="mais">mais</a> viva</span>
</td>
<td style="border: 1px solid #999999;" valign="top"><span class="Latn" lang="pt"><a href="https://en.wiktionary.org/wiki/mais#Portuguese" title="mais">mais</a> vivos</span>
</td>
<td style="border: 1px solid #999999;" valign="top"><span class="Latn" lang="pt"><a href="https://en.wiktionary.org/wiki/mais#Portuguese" title="mais">mais</a> vivas</span>
</td></tr>
<tr>
<th style="border: 1px solid #999999; background:#b0bfd4"><a href="https://en.wiktionary.org/wiki/Appendix:Glossary#superlative" title="Appendix:Glossary">superlative</a>
</th>
<td style="border: 1px solid #999999;" valign="top"><span class="Latn" lang="pt"><a href="https://en.wiktionary.org/wiki/o#Portuguese" title="o">o</a> <a href="https://en.wiktionary.org/wiki/mais#Portuguese" title="mais">mais</a> vivo</span><br><span class="Latn" lang="pt"><a href="https://en.wiktionary.org/w/index.php?title=viv%C3%ADssimo&amp;action=edit&amp;redlink=1" class="new" title="vivíssimo (page does not exist)">vivíssimo</a></span>
</td>
<td style="border: 1px solid #999999;" valign="top"><span class="Latn" lang="pt"><a href="https://en.wiktionary.org/wiki/a#Portuguese" title="a">a</a> <a href="https://en.wiktionary.org/wiki/mais#Portuguese" title="mais">mais</a> viva</span><br><span class="Latn" lang="pt"><a href="https://en.wiktionary.org/w/index.php?title=viv%C3%ADssima&amp;action=edit&amp;redlink=1" class="new" title="vivíssima (page does not exist)">vivíssima</a></span>
</td>
<td style="border: 1px solid #999999;" valign="top"><span class="Latn" lang="pt"><a href="https://en.wiktionary.org/wiki/os#Portuguese" title="os">os</a> <a href="https://en.wiktionary.org/wiki/mais#Portuguese" title="mais">mais</a> vivos</span><br><span class="Latn" lang="pt"><a href="https://en.wiktionary.org/w/index.php?title=viv%C3%ADssimos&amp;action=edit&amp;redlink=1" class="new" title="vivíssimos (page does not exist)">vivíssimos</a></span>
</td>
<td style="border: 1px solid #999999;" valign="top"><span class="Latn" lang="pt"><a href="https://en.wiktionary.org/wiki/as#Portuguese" title="as">as</a> <a href="https://en.wiktionary.org/wiki/mais#Portuguese" title="mais">mais</a> vivas</span><br><span class="Latn" lang="pt"><a href="https://en.wiktionary.org/w/index.php?title=viv%C3%ADssimas&amp;action=edit&amp;redlink=1" class="new" title="vivíssimas (page does not exist)">vivíssimas</a></span>
</td></tr>
<tr>
<th style="border: 1px solid #999999; background:#b0bfd4"><a href="https://en.wiktionary.org/wiki/Appendix:Glossary#augmentative" title="Appendix:Glossary">augmentative</a>
</th>
<td style="border: 1px solid #999999;" valign="top">—
</td>
<td style="border: 1px solid #999999;" valign="top">—
</td>
<td style="border: 1px solid #999999;" valign="top">—
</td>
<td style="border: 1px solid #999999;" valign="top">—
</td></tr>
<tr>
<th style="border: 1px solid #999999; background:#b0bfd4"><a href="https://en.wiktionary.org/wiki/Appendix:Glossary#diminutive" title="Appendix:Glossary">diminutive</a>
</th>
<td style="border: 1px solid #999999;" valign="top"><span class="Latn" lang="pt"><a href="https://en.wiktionary.org/w/index.php?title=vivinho&amp;action=edit&amp;redlink=1" class="new" title="vivinho (page does not exist)">vivinho</a></span>
</td>
<td style="border: 1px solid #999999;" valign="top"><span class="Latn" lang="pt"><a href="https://en.wiktionary.org/w/index.php?title=vivinha&amp;action=edit&amp;redlink=1" class="new" title="vivinha (page does not exist)">vivinha</a></span>
</td>
<td style="border: 1px solid #999999;" valign="top"><span class="Latn" lang="pt"><a href="https://en.wiktionary.org/w/index.php?title=vivinhos&amp;action=edit&amp;redlink=1" class="new" title="vivinhos (page does not exist)">vivinhos</a></span>
</td>
<td style="border: 1px solid #999999;" valign="top"><span class="Latn" lang="pt"><a href="https://en.wiktionary.org/w/index.php?title=vivinhas&amp;action=edit&amp;redlink=1" class="new" title="vivinhas (page does not exist)">vivinhas</a></span>
</td></tr></tbody></table>
"""
#with open("vivo.html") as fp:
#    soup = BeautifulSoup(fp)

soup = BeautifulSoup(html_doc, "html.parser")

converted_tr = soup.find_all('tr')
table_width: int = 0

#find width of the table
for single_td in converted_tr[0].find_all('th'):
     try:
         table_width += int(single_td["colspan"])
     except (ValueError, KeyError) as e:
         table_width += 1

#temporary empty two-dimensional array for td values
temporary_table = np.empty(shape=(len(converted_tr), table_width), dtype=object)
#temporary empty two-dimensional array for th values
temporary_table_th = np.empty(shape=(len(converted_tr), table_width), dtype=object)

#add only td to table named temporary_table
for idx, single_tr in enumerate(converted_tr):
    for idxtd, single_td in enumerate(single_tr.find_all(lambda tag: tag.name == 'td' or  tag.name == 'th')):
        if single_td.name == 'td':
            temporary_table[idx, idxtd] = single_td.text.rstrip()

#add only th to table named temporary_table_th
for idx, single_tr in enumerate(converted_tr):
    for idxtd, single_td in enumerate(single_tr.find_all(lambda tag: tag.name == 'td' or  tag.name == 'th')):
        if single_td.name == 'th':
            temporary_table_th[idx, idxtd] = single_td.text.rstrip()


print('Matrix for <td>: \n', temporary_table)
print('\nMatrix for <th>: \n', temporary_table_th)
