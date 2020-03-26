import csv
import os
import subprocess
import pandas as pd


def clean(dirty):
    '''
    Returns a cleaned string, stripped of all newlines and carriage returns.
    '''
    return dirty.replace('\r', '').replace('\n', '')

#creates a noid format file that suplies the parent ark for the NOID to be appended to

def create_noid_yml(parent_ark):

    noid_file = open("Noid_test.yml", "w+")
    string = ['template: eeddeede \n',('scheme: ' + str(parent_ark[0:11])), ('\nnaa: ' + str(parent_ark[11:]))]
    for s in string:
        noid_file.write(s)

#creates a mappings file that provides metadata to EZID
def create_mappings():

    title = row['Title']
    mappings_file = open("mappings.txt", "w+")
    string = 'erc.who: UCLA Library', ('\nerc.what: '+str(title))
    for s in string:
        mappings_file.write(s)

directory = (str(raw_input('File directory:')).strip())+'/'
works_file = directory+'works.csv'
ark_shoulder = raw_input('ARK shoulder:')
ezid_input = raw_input('EZID username and password:')
ark_dict = {}
parent_ark_list = []
output_file = 'works.csv'
works_cursor = csv.DictReader(open(works_file),
    delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

for row in works_cursor:

    altidentifer = row['AltIdentifier.local']
    if row['Object Type'] == 'Work' and row['Item ARK'] == '':
        create_mappings()
        cmd_ezid = ['python', 'ezid.py', ezid_input, 'mint', ark_shoulder, '@', 'mappings.txt']
        parent_ark = subprocess.Popen(cmd_ezid, stdout=subprocess.PIPE).communicate()[0]
        parent_ark = clean(str(parent_ark)).replace('success: ', '')
        parent_ark_list.append(parent_ark)
        ark_dict[altidentifer] = parent_ark
    if row['Object Type'] == '':
    	parent_ark_list.append('')
    elif row['Item ARK'] != '':
        parent_ark = row['Item ARK']
        parent_ark_list.append(parent_ark)
        ark_dict[altidentifer] = parent_ark
data= pd.read_csv(works_file, sep=',', delimiter=None, header='infer')
data = data.drop("Item ARK", axis=1)
data.insert(7, 'Item ARK', parent_ark_list)
data.to_csv(path_or_buf=(directory+output_file), sep=',', na_rep='', float_format=None, index=False)

#loops through files in a directory 
check_ark_list = []
for filename in os.listdir(directory):
    print(filename)
    if '.csv' in filename and filename != 'works.csv':
        file_path = directory + (str(filename))
        cursor = csv.DictReader(open(file_path),
            delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        item_ark_list = []
        local_parent_ark_list = []
        index = 2
        for row in cursor:
            title = row['Title']
            if row['Object Type'] == 'ChildWork':
                source = row['Source']
                if source in ark_dict.keys():
                    parent_ark = clean(ark_dict[source])
                    create_noid_yml(parent_ark)
                    cmd = ['noid', '-f', 'Noid_test.yml']
                    item_ark = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
                    item_ark = clean(item_ark)
                    item_ark_list.append(item_ark)
                    local_parent_ark_list.append(parent_ark)
                    check_ark_list.append(parent_ark_list)

                elif source not in ark_dict.keys():
                    print(('Item ARK not minted for page:{} from Manuscript:{} at row {}').format(title, filename, index))
                    item_ark_list.append('')
                    local_parent_ark_list.append('')
                    check_ark_list.append(parent_ark_list)
            index +=1
            
        data = pd.read_csv(file_path, sep=',', delimiter=None, header='infer')
        data = data.drop("Item ARK", axis=1)
        data = data.drop("Parent ARK", axis=1)
        data.insert(6, 'Parent ARK', local_parent_ark_list)
        data.insert(7, 'Item ARK', item_ark_list)
        data.to_csv(path_or_buf=(directory+filename), sep=',', na_rep='', float_format=None, index=False)
"""
ark_counter = 0
for ark[ark_counter] in check_ark_list:
    if ark not in ark_dict.items():
        print('This manuscript ark is in the page csv but not the work csv: {}'.format(ark))
ark_counter+=1
"""
