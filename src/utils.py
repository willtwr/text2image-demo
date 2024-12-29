import os


def create_temp_folder():
    tempfolder = "./tempfolder"
    if not os.path.exists(tempfolder):
        os.mkdir(tempfolder)

    return tempfolder
