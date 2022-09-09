import csv
import os
import sys
import subprocess
import pandas as pd


NOID_TEMPLATE = 'eeddeede'
NOID_YML = 'noid.yml'
ERC_WHO = 'UCLA Library'
MAPPINGS = 'mappings.txt'


def get_session_id():
    username = input('EZID username: ')
    password = input('EZID password: ')
    cmd = ['python', 'ezid3.py', f'{username}:{password}', 'login']
    response = subprocess.run(cmd, capture_output=True)
    #from response, take session ID (4th element) and strip extra bytestring quote characters
    return response.stdout.split()[4][2:-1].decode()


def logout(session_id):
    cmd = ['python', 'ezid3.py', session_id, 'logout']
    response = subprocess.run(cmd, capture_output=True)


def create_noid_yml(parent_ark):
    scheme = parent_ark[0:11]
    naa = parent_ark[11:]
    text = f'template: {NOID_TEMPLATE}\nscheme: {scheme}\nnaa: {naa}'
    with open(NOID_YML, 'w+') as noid_yml:
        noid_yml.write(text)


def create_mappings(title):
    text = f'erc.who: {ERC_WHO}\nerc.what: {title}'
    with open(MAPPINGS, 'w+') as mappings_file:
        mappings_file.write(text)


def find_works_file(directory):
    for filename in os.listdir(directory):
        if filename.startswith('works') and filename.endswith('.csv'):
            return filename


def find_nonworks_csvs(directory):
    return [f for f in os.listdir(directory) if f.endswith('csv') and not f.startswith('works')]


def mint_ark(session_id, shoulder, title=None, noid=False, parent_ark=None):
    if noid is True:
        create_noid_yml(parent_ark)
        cmd = ['noid', '-f', NOID_YML]
    else:
        create_mappings(title)
        cmd = ['python', 'ezid3.py', session_id, 'mint', shoulder, '@', 'mappings.txt']
    ark = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
    return ark.decode("utf-8").strip().replace('success: ', '')

def process_works_file(path, session_id, shoulder):
    ark_dict = {}
    parent_ark_list = []
    with open(path) as works_file:
        rows = csv.DictReader(works_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        for row in rows:
            shelfmark = row['Shelfmark']
            if row['Object Type'] == 'Work' and row['Item ARK'] == '':
                ark = mint_ark(session_id, shoulder, title=shelfmark)[2:-1]
                ark_dict[shelfmark] = ark
                parent_ark_list.append(ark)
            elif row['Object Type'] == '':
                parent_ark_list.append('')
            elif row['Item ARK'] != '':
                ark_dict[shelfmark] = row['Item ARK']
                parent_ark_list.append(row['Item ARK'])
    data = pd.read_csv(path, sep=',', delimiter=None, header='infer')
    data = data.drop('Item ARK', axis=1)
    data.insert(7, 'Item ARK', parent_ark_list)
    data.to_csv(path_or_buf=(path), sep=',', na_rep='', float_format=None, index=False)
    return ark_dict


def process_nonworks_csv(filepath, ark_dict, session_id, shoulder):
    with open(filepath) as csv_file:
        cursor = csv.DictReader(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        item_ark_list = []
        local_parent_ark_list = []
        index = 2
        for row in cursor:
            title = row['Title']
            if row['Object Type'] == 'Page':
                source = row['Source']
                if source in ark_dict.keys():
                    parent_ark = ark_dict[source].strip()
                    if row['Item ARK'] == '':
                        item_ark = mint_ark(session_id, shoulder, noid=True, parent_ark=parent_ark)
                    else:
                        item_ark = row['Item ARK']
                    item_ark = item_ark.strip()
                    item_ark_list.append(item_ark)
                    local_parent_ark_list.append(parent_ark)
                elif source not in ark_dict.keys():
                    print(('Item ARK not minted for page:{} from Manuscript:{} at row {}').format(title, filename, index))
                    item_ark_list.append('')
                    local_parent_ark_list.append('')
            index +=1
    data = pd.read_csv(filepath, sep=',', delimiter=None, header='infer')
    data = data.drop("Item ARK", axis=1)
    data = data.drop("Parent ARK", axis=1)
    data.insert(6, 'Parent ARK', local_parent_ark_list)
    data.insert(7, 'Item ARK', item_ark_list)
    data.to_csv(path_or_buf=(filepath), sep=',', na_rep='', float_format=None, index=False)


def cleanup():
    for f in (NOID_YML, MAPPINGS):
        if os.path.exists(f):
            os.remove(f)


def main():
    directory = input('File directory: ').strip()
    works_filename = find_works_file(directory)
    if works_filename is None:
        print('Works file not found. Aborting')
        sys.exit(1)
    shoulder = input('ARK shoulder: ')
    session_id = get_session_id()
    works_path = os.path.join(directory, works_filename)
    try:
        ark_dict = process_works_file(works_path, session_id, shoulder)
        for filename in find_nonworks_csvs(directory):
            path = os.path.join(directory, filename)
            process_nonworks_csv(path, ark_dict, session_id, shoulder)
    except Exception as e:
        #Possible exceptions caught (but not handled):
        #HTTPErrors from EZID requests,
        #OSErrors from missing or incorrect csv files, and
        #Exceptions raised by subprocess module 
        print(e)
    finally:
        logout(session_id)
        cleanup()


if __name__ == "__main__":
    main()
