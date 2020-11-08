from tkinter import Tk
from tkinter import filedialog
import os
from csv import reader
import shutil
import pathlib
import errno
import configparser

#pattop
docs_mods_path =""   
steam_mods_path = ""    


def get_saved_paths():
    global docs_mods_path
    global steam_mods_path
    config = configparser.ConfigParser()
    config.read('config.ini')
    steam_mods_path = config.get("PATHS","steam_mods_path")

    if steam_mods_path == "notSet":
        steam_mods_path = user_path_prompt("--SELECT STEAM MODS FOLDER--")
        store_path(steam_mods_path)

    docs_mods_path = config.get("PATHS","docs_mods_path")

    if docs_mods_path == "notSet":
        docs_mods_path = user_path_prompt("--SELECT DOCUMENTS MODS FOLDER--")
        store_path(docs_mods_path)



def user_path_prompt(title):
    root = Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(title = title)


    return folder_selected


def store_path(path):
    config_variable = ""
    if "Steam" in path:
        config_variable = "steam_mods_path"

    elif "Documents" in path:
        config_variable = "docs_mods_path"

    config = configparser.ConfigParser()
    config.read('config.ini')
    config.set("PATHS", config_variable, path )
    
    with open('config.ini', 'w') as configfile:
        config.write(configfile)




def get_size(directory):
    """Returns the `directory` size in bytes."""
    total = 0
    try:
        # print("[+] Getting the size of", directory)
        for entry in os.scandir(directory):
            if entry.is_file():
                # if it's a file, use stat() function
                total += entry.stat().st_size
            elif entry.is_dir():
                # if it's a directory, recursively call this function
                total += get_size(entry.path)
    except NotADirectoryError:
        # if `directory` isn't a directory, get the file size then
        return os.path.getsize(directory)
    except PermissionError:
        # if for whatever reason we can't open the folder, return 0
        return 0
    return total


def dir_to_text(path,filename):
    Tk().withdraw()
    dirList = os.listdir(path)
    data = ((fname, str(get_size(path + "/" + fname)))  for fname in dirList)

    outputFile = open(filename, 'w')
    for entry in data:
        outputFile.write(','.join(entry) + '\n')

    outputFile.close()



def compare_files(host_file_name, client_file_name):
    mods_to_download = []
    with open(client_file_name, 'r') as client_file:
        # pass the file object to reader() to get the reader object
        client_csv_reader = reader(client_file)
        client_mod_list = list(client_csv_reader)
        

    with open(host_file_name, 'r') as host_file:
        host_csv_reader = reader(host_file)

        for row in host_csv_reader:

            if not row in client_mod_list:
                mods_to_download.append(row)
    
    return mods_to_download


def copy(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('Directory not copied. Error: %s' % e)


def create_documents_mods_folder(mods_to_download):
        docs_folder_path  = str(pathlib.Path().absolute()) +"\\Mods\\Documents"
        os.mkdir(docs_folder_path)
        
        for mod in mods_to_download:
            source_path = docs_mods_path + "\\" + mod[0]
            mod_name = mod[0]
            destination_path = str(pathlib.Path().absolute()) +"\\Mods\\Documents\\"+ mod_name
            shutil.copyfile(source_path , destination_path)


def create_steam_mods_folder(mods_to_download):
        steam_folder_path  = str(pathlib.Path().absolute()) +"\\Mods\\Steam"
        os.mkdir(steam_folder_path)
        
        for mod in mods_to_download:
            source_path = steam_mods_path + "\\" + mod[0]
            mod_name = mod[0]
            destination_path = str(pathlib.Path().absolute()) +"\\Mods\\Steam\\"+ mod_name

            copy(source_path, destination_path)
            
  

def wipe_folders():
    #wipe output folders at start of run
    docs_folder_path = str(pathlib.Path().absolute()) +"\\Mods\\Documents"
    steam_folder_path = str(pathlib.Path().absolute()) +"\\Mods\\Steam"
    shutil.rmtree(docs_folder_path)
    shutil.rmtree(steam_folder_path)


get_saved_paths()

dir_to_text(docs_mods_path,"host_csv_files\\host_document_mods.csv")
dir_to_text(steam_mods_path,"host_csv_files\\host_steam_mods.csv")

document_files_to_download = compare_files('host_csv_files\\host_document_mods.csv', "client_csv_files\\client_document_mods.csv")
steam_files_to_download = compare_files('host_csv_files\\host_steam_mods.csv', "client_csv_files\\client_steam_mods.csv")

wipe_folders()

create_documents_mods_folder(document_files_to_download)
create_steam_mods_folder(steam_files_to_download)
