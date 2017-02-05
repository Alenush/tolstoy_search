import os, shutil
import pprint
import zipfile
from collections import defaultdict

# volums_data = defaultdict(list)
# for doc in os.listdir('./Final'):
#     vol = doc.split('.')[-2].split(' ')
#     volums_data[vol[-1]].append(doc)
#
# pprint.pprint(volums_data)
# os.mkdir('TeiData')
# for vol, docs in volums_data.items():
#     os.mkdir('./TeiData/'+vol)
#     for doc in docs:
#         shutil.copy2('./Final/'+doc, './TeiData/'+str(vol)+'/'+doc)

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


def recursive_zip(zipf, directory):
    path = './TeiData/'+directory
    list = os.listdir(path)
    for file in list:
        print(path+'/'+file)
        # if os.path.isfile(path+'/'+file):
        zipf.write(path+'/'+file, file)
    print('=======================')

os.mkdir('TeiZip')
for folder in os.listdir('TeiData'):
    zipf = zipfile.ZipFile("./TeiZip/" + str(folder) + '.zip', 'w', zipfile.ZIP_DEFLATED)
    recursive_zip(zipf, folder)
    zipf.close()