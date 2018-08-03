import os
import sys
import shutil
import json
from subprocess import check_output
from pdb import set_trace as st
import numpy as np
# from Naked.toolshed.shell import execute_rb, muterun_rb

urlmap = {}
start_id = 80000
end_id = 100000
PATH = '/projects/grail/6DOFnb/NYPL_new/'
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
    urlDir = PATH + 'url/'
    createFolder(tifDir)
    createFolder(cropDir)
    createFolder(metaDir)
    createFolder(urlDir)

    for id in range(start_id, end_id):
    # id = 201

        idDir = PATH + 'cropped/' + str(id)
        createFolder(idDir)
        # createFolder("/Users/ying/documents/uw/Junior-quarter4/lab/" + str(id))

        # os.system call

        # command = '/Users/ying/documents/uw/Junior-quarter4/lab/torch-warp-master/nypl_recrop.rb ' + str(id)
        # os.system(command)


        # match the images that have common high-res url
        # the shell command

        command = '/projects/grail/6DOF/dataset_NYPL/6DoF/server/final_nypl_recrop.rb'
        # from subprocess import check_output
        # url = check_output([command, str(id)])

        exist = 1

        try:
            url = check_output([command, str(id)])
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

        remove1 = PATH + str(id) + '.jpg'
        if os.path.exists(remove1):
            os.remove(remove1)
        remove2 = PATH + str(id) + '_cropped.tif'
        if os.path.exists(remove2):
            os.remove(remove2)
        remove3 = PATH + str(id) + '_gif.jpg'
        if os.path.exists(remove3):
            os.remove(remove3)

        if id % 1000 == 0:
            # log url map
            jsonmap = json.dumps(urlmap)
            filename = urlDir + 'urlmap_' + str(id) + '.json'
            try:
                f = open(filename, "w+")
                f.write(jsonmap)
                f.close()
            except OSError as err:
                print("OS error: {0}".format(err))
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise

if __name__ == '__main__':
    main()