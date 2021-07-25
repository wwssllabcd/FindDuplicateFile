
import sys
from os import listdir
from os.path import isfile, join

sys.path.append(r'D:/GitHub/Python')
from EricCorePy.Utility.EricUtility import EricUtility


class FileObj:
    def __init__(self):
        self.name = ""
        self.size = 0
        self.isFile = True

def get_fileObj_colls(folderPath, fileColls):
    u = EricUtility()
    files = listdir(folderPath)

    for f in files:
        fullpath = join(folderPath, f)
        fo = FileObj()
        fo.name = fullpath
        fo.isFile = isfile(fullpath)
        fo.size = u.get_file_size(fullpath)
        fileColls.append(fo)
    
    return fileColls

def get_duplicate_file_by_compare_file_data(fileDirGroupDirBySize):
    u = EricUtility()
    dupFileList = []
    compareSize = 512*1024
    for fileSize in fileDirGroupDirBySize:
        sameSizefileList = fileDirGroupDirBySize[fileSize]
        if len(sameSizefileList) < 2:
            continue

        naneAndDatas = []
        for fileName in sameSizefileList:
            naneAndDatas.append([fileName, u.get_file_data_binary(fileName, compareSize)])
        
        for compare in naneAndDatas:
            for eachitem in naneAndDatas:
                if compare[0] == eachitem[0]:
                    continue

                print(compare[0])
                if compare[1] == eachitem[1]:
                    dupFileList.append(compare[0])
                    break
    return dupFileList

def get_file_name_by_full_path(fullPath):
    idx = fullPath.rfind("\\")
    if idx == -1:
        idx = fullPath.rfind("/")
    res = fullPath[idx+1:]
    return res

def rename_file(fileColls):
    res = ""
    for file in fileColls:
        fileName = get_file_name_by_full_path(file)
        res += 'ren "' + file + '" "_dup_' + fileName + '"' + u.crlf()
    return res

#------------------------
# window command line 切換到 utf-8
# chcp 65001
#-----------------
if __name__ == '__main__':
    u = EricUtility()
    paths = []
    for i in sys.argv:
        if u.is_dir(i):
            paths.append(i)

    if len(paths)==0:
        print("No any path")
        exit()

    print(paths)

    fileColls = []
    for path in paths:
        fdPath = path + r'\\'
        fileColls = get_fileObj_colls(fdPath, fileColls)
    
    fileDirGroupDirBySize = u.group_file_by_size(fileColls)

    dupFileList = get_duplicate_file_by_compare_file_data(fileDirGroupDirBySize)
    dupFileList.sort()
    res = rename_file(dupFileList)
    u.to_file("renameFiles.bat", res)

    print(res)
    print('Finish')
