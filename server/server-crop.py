import os
import sys
import shutil
import subprocess
import numpy as np
# from Naked.toolshed.shell import execute_rb, muterun_rb

urlmap = {}
start_id = 201
end_id = 205
PATH = '/projects/grail/6DOF/dataset_NYPL/'
    #sys.argv[1]  # /Users/ying/documents/uw/Junior-quarter4/lab/
                    # /projects/grail/6DOF/dataset_NYPL
# COMMAND = sys.argv[2]  # '/Users/ying/documents/uw/Junior-quarter4/lab/torch-warp-master/nypl_recrop.rb'
                        # /projects/grail/6DOF/dataset_NYPL/torch-warp-master/nypl_recrop.rb

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print 'Error: Creating directory. ', +  directory


def readFile(filename):
    f = open(filename, "r")  # opens file with name of "test.txt"
    for line in f:
        url = line.split('\n')[0]
    return url


def main():
    #create tiff directory
    tifDir = PATH + 'tif/'
    cropDir = PATH + 'cropped/'
    metaDir = PATH + 'meta/'
    # createFolder(tifDir)
    # createFolder(cropDir)
    # createFolder(metaDir)

    # for id in range(start_id, end_id):
    id = 201

    idDir = PATH + 'cropped/' + str(id)
    createFolder(idDir)
    # createFolder("/Users/ying/documents/uw/Junior-quarter4/lab/" + str(id))

    # os.system call

    # command = '/Users/ying/documents/uw/Junior-quarter4/lab/torch-warp-master/nypl_recrop.rb ' + str(id)
    # os.system(command)


    # match the images that have common high-res url
    # the shell command

    command = '/projects/grail/6DOF/dataset_NYPL/torch-warp-master/server_nypl_recrop.rb'
    # from subprocess import check_output
    # url = check_output([command, str(id)])

    exist = 1

    try:
        url = check_output([command, str(id)])
        print 'yeah'
    except:
        exist = 0



    # matchName = PATH + '/url/hiurl_' + id + '.txt'
    # matchName = '/Users/ying/documents/uw/Junior-quarter4/lab/url/hiurl_' + str(id) + '.txt'
    # url = readFile(matchName)

    if exist == 0:
        url = 'null'

    if url in urlmap.keys():
        urlmap.get(url).append(id)
    else:
        idlist = [id]
        urlmap[url] = idlist

    # clean up if the imageID does not exist
    # if len(os.listdir(idDir)) == 0:
    #     shutil.rmtree(idDir)
    if len(os.listdir(cropDir + str(id))) == 0:
        shutil.rmtree(cropDir + str(id))
    else:
        remove1 = PATH + str(id) + '.jpg'
        shutil.rmtree(remove1)
        remove2 = PATH + str(id) + '_cropped.tif'
        shutil.rmtree(remove2)

    if id % 3 == 0:
        # log url map
        sys.stdout = open('urlmap_' + str(id) + '.txt', 'wt')
        print urlmap

if __name__ == '__main__':
    main()