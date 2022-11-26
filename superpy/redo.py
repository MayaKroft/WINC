import pandas as pd
import doc_handler as dh
import json
from rich.console import Console
import csv

console =Console()
""" xl =pd.read_excel('test.xlsx', sheet_name = 0)
a = xl.columns.tolist()
console.print(a, type(a))
print('xldcitrecords', type(xl.to_dict('records')))
#xl.to_csv('test2.csv', columns = [a[1],a[0],a[3],a[2]], header = csv_h, index = False)
#print(dh.get_headers('test.xlsx'))
#print(dh.read_csv('test.csv'))
j_file_a = open('json_a_test.json')
j_file_b = open('json_b_test.json')
file_a_data = json.load(j_file_a)
#console.print(list(file_a_data)[1])
console.print('aaa', type(file_a_data[list(file_a_data)[0]]))
#print(type(json.load(j_file_b)))
console.print(type(xl))
console.print(list(xl)) #listing an xl with none will return a ditc, using the list(method will return the sheet names)
console.print(type(xl[list(xl)[0]]))
"""


""" csv_headers =['a', 'b', 'c', 'd','f']
from_headers =['a', 'c', 'd', 'e','z']
titles = []
missing = []

for x, head in enumerate(csv_headers):
    if head in from_headers:
        titles.append(head)
    else:
        titles.append(' ')
        missing.append(x)
remaining_from = [i for i in from_headers if i not in titles]

remaining_csv = [csv_headers[i] for i in missing]

dif_titles = input(f'Here are the import_file headers that still need a match,\n{remaining_from}\nPlease insert the key/column name equivalents for \n{remaining_csv} \nseparated by a comma ","\n do not add spaces after or before the comma: ')
dif_titles = dif_titles.split(',')

print(titles, missing, remaining_from, remaining_csv, dif_titles)
for x,index in enumerate(missing):
    titles[index] = dif_titles[x]
print(titles) #a, e, c, d, z


def export(csv_file, destination = False):
    title = destination if destination else csv_file[:-4]
    print(title)

export('bought.csv')
 """
with open('purchased.csv', newline='', mode="r") as buying_file:
    reader = csv.DictReader(buying_file)
    data = [row for row in reader]
    if data:
        ids= [int(i['id']) for i in data]
        last_item = data[-1]
        last_id = last_item['id']
        max_id = max(ids)
        buying_file.close()
        print(ids, max_id)
