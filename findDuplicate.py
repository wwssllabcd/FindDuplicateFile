
import sys
sys.path.append(r'D:\GitHub\Python')

from EricCorePy.Utility.EricUtility import EricUtility
u = EricUtility()

#import struct

path = r'E:\\Download\\tmp\\'

fileDsc = path + r'\\dup\\'
u.make_folder(fileDsc)

fileColls = u.get_fileObj_colls(path)
fileColls.sort(key=lambda x: x.size)

dic = {}
for file in fileColls:
    if file.size not in dic:
        dic[file.size] = []
    dic[file.size].append(file.name)

for item in dic:
    fileList = dic[item]
    if len(fileList) > 1:
        cnt=0
        firstData = ''
        for f in fileList:
            if cnt == 0:
                firstData = u.get_file_data_binary(path+ f)
                cnt+=1
            else:
                data = u.get_file_data_binary(path+ f)
                if data == firstData:
                    u.move_file(path + f, fileDsc + f )

print('Finish')