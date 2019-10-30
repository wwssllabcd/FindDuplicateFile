
import sys
sys.path.append(r'D:\GitHub\Python')

from EricCorePy.Utility.EricUtility import EricUtility
u = EricUtility()

path = r'E:\\Download\\tmp\\'
fileDsc = path + r'\\dup\\'

u.make_folder(fileDsc)

fileColls = u.get_duplicate_file_list(path)
for file in fileColls:
    u.move_file(path + file, fileDsc + file )

print('Finish')