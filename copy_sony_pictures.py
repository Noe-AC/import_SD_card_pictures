"""
Noé Aubin-Cadot

Goal:
- Transfer pictures and videos from the Sony camera to the computer.

Remark that there are two file structures:
- 'old': one subfolder per date in the folder 'DCIM'.
- 'new': one subfolder '100MSDCF'.
In the function to import the pictures there's a parameter to specify the file structure.
By default it's set to 'auto' as it'll try to identify the file structure.

Log:
- 2023-06-01: Implemented the import for the old file structure.
- 2024-04-19: Implemented the import for the new file structure.

"""

################################################################################
################################################################################
# Defining functions

def make_path(
    path,
    verbose = False,
):
    import os
    path_components = path.split('/')
    if '' in path_components:
        path_components.remove('')
    for i in range(1,len(path_components)+1):
        folder = '/'.join(path_components[:i])
        if not os.path.exists(folder):
            if verbose:
                print(f"Folder '{folder}' does not exist, it is created.")
            os.mkdir(folder)
        else:
            if verbose:
                print(f"Folder '{folder}' already exists.")

def copy_camera_pictures_to_computer(
    do_make_sure_SD_card_is_detected=1,
    do_make_sure_there_is_enough_free_space_available=1,
    do_make_sure_output_directory_exists=1,
    do_make_sure_SD_card_contains_relevant_folders=1,
    do_copy_JPG=1,
    do_copy_ARW=1,
    do_copy_MTS=1,
    do_create_pictures_previews=1,
    do_show_in_Finder=1,
    file_structure='auto', # can be either 'old' or 'new' or 'auto'
):

    input_path  = '/Volumes/Untitled' # path of the external SD card
    
    import os

    if do_make_sure_SD_card_is_detected:
        # Make sure that the SD card is detected.
        # Name of the SD card: "Untitled"
        if os.path.exists(input_path):
            print('The SD card is detected. OK.')
        else:
            exception = f'The path « {input_path} » does not exist. Make sure the SD card is inserted.'
            raise Exception(exception)

    import shutil

    if do_make_sure_there_is_enough_free_space_available:

        current_working_directory = os.getcwd()
        print('\nCurrent working directory :',current_working_directory)

        paths = [
                input_path,
                current_working_directory,
                ]
        for path in paths:
            print('\npath =',path)
            total, used, free = shutil.disk_usage(path)
            print(f"- Total : {round((total/(2**30)),2)} GB")
            print(f"- Used  : {round((used /(2**30)),2)} GB")
            print(f"- Free  : {round((free /(2**30)),2)} GB")

        source_disk_usage = round(shutil.disk_usage(input_path).used/(2**30),2)
        target_disk_free  = round(shutil.disk_usage(current_working_directory).free/(2**30),2)
        print('\nsource_disk_usage =',source_disk_usage)
        print('target_disk_free  =',target_disk_free)
        if target_disk_free-source_disk_usage<20:
            print('WARNING: Low free disk to automate the import...')
        elif target_disk_free-source_disk_usage<10:
            exception = 'Free disk too low for safe copying.'
            raise Exception(exception)
        else:
            print("\nThere's enough free space to copy files. OK.")

    output_path = '/transferred_pictures' # directory (i.e. subdirectory from the current working directory) of the target folder

    if do_make_sure_output_directory_exists:
        # Create the output directory if it doesn't already exist.
        print(f'\nLooking at the output directory « {output_path} »...')
        make_path(path=output_path,verbose=True)

    if do_make_sure_SD_card_contains_relevant_folders:
        # Make sure that the SD card contains the relevant folders.
        if not os.path.exists(input_path+'/DCIM'):
            print('\nWARNING: No « /DCIM » folder in SD card. Importation of pictures will be skipped.')
            do_copy_JPG=0
            do_copy_ARW=0
            do_create_pictures_previews=0
        else:
            print('\nThe SD card contains the folder « /DCIM ». OK.')
        
        if not os.path.exists(input_path+'/PRIVATE'):
            print('\nWARNING: No « /PRIVATE » folder in SD card. Importation of videos will be skipped.')
            do_copy_MTS=0
        else:
            print('\nThe SD card contains the folder « /PRIVATE ». OK.')

    import glob

    if do_copy_JPG|do_copy_ARW:
        # Take a look at the list of pictures folders
        source_folders_pictures = glob.glob(input_path+'/DCIM/*')
        
        # Import a library that'll read the pictures metadata
        import exifread # pip install ExifRead

    if file_structure=='auto':
        # Identifying the file structure
        print("The parameter file_structure is set to 'auto'... evaluating if the file structure is 'old' or 'new'...")
        if '/Volumes/Untitled/DCIM/100MSDCF' in source_folders_pictures:
            file_structure='new'
        else:
            file_structure='old'
        print(f"The identified file structure is '{file_structure}'.")

    if do_copy_JPG:
        # Copy JPG files
        print('\nAbout to copy jpg files...')
        # Importing JPGs
        if file_structure=='old':
            for source_folder in source_folders_pictures:
                print('\nsource_folder =',source_folder)
                source_JPGs = glob.glob(source_folder+'/*.JPG')
                if len(source_JPGs)>0:
                    first_JPG       = source_JPGs[0]
                    with open(first_JPG,'rb') as f:
                        tags = exifread.process_file(f)
                    date            = tags['Image DateTime'].values.split(' ')[0].replace(':','-')
                    target_folder   = f'transferred_pictures/{date}/JPG'
                    make_path(path=target_folder)
                    names           = [source_JPG.split('/')[-1] for source_JPG in source_JPGs]
                    targets_copied  = glob.glob(target_folder+'/*.JPG')
                    for name in names:
                        source = source_folder+'/'+name
                        target = target_folder+'/'+name
                        if target in targets_copied:
                            string = f'{date}/{name} : File already exists. Skip.'
                            print(string)
                            continue
                        else:
                            string = f'{date}/{name} : File not there. Copy it.'
                            print(string)
                            shutil.copy2(source,target_folder)
        elif file_structure=='new':
            target_folders = []
            for source_folder in source_folders_pictures:
                print('\nsource_folder =',source_folder)
                source_JPGs = glob.glob(source_folder+'/*.JPG')
                if len(source_JPGs)>0:
                    for source_JPG in source_JPGs:
                        name = source_JPG.split('/')[-1]
                        with open(source_JPG,'rb') as f:
                            tags = exifread.process_file(f)
                        date            = tags['Image DateTime'].values.split(' ')[0].replace(':','-')
                        target_folder   = f'transferred_pictures/{date}/JPG'
                        if target_folder not in target_folders:
                            make_path(path=target_folder)
                            target_folders.append(target_folder)
                        source = source_folder+'/'+name
                        target = target_folder+'/'+name
                        targets_copied  = glob.glob(target_folder+'/*.JPG')
                        if target in targets_copied:
                            string = f'{date}/{name} : File already exists. Skip.'
                            print(string)
                            continue
                        else:
                            string = f'{date}/{name} : File not there. Copy it.'
                            print(string)
                            shutil.copy2(source,target_folder)
        else:
            raise Exception(f"ERROR: file_structure='{file_structure}' is not valid. Choose either 'old' or 'new' or 'auto'.")
        print('Done with jpg files...')

    if do_copy_ARW:
        # Copy ARW files
        print('\nAbout to copy raw files...')
        if file_structure=='old':
            for source_folder in source_folders_pictures:
                print('\nsource_folder =',source_folder)
                source_ARWs = glob.glob(source_folder+'/*.ARW')
                if len(source_ARWs)>0:
                    first_ARW      = source_ARWs[0]
                    with open(first_ARW,'rb') as f:
                        tags = exifread.process_file(f)
                    date           = tags['Image DateTime'].values.split(' ')[0].replace(':','-')
                    target_folder  = f'transferred_pictures/{date}/RAW'
                    make_path(path=target_folder)
                    names          = [source_ARW.split('/')[-1] for source_ARW in source_ARWs]
                    targets_copied = glob.glob(target_folder+'/*.ARW')
                    for name in names:
                        source = source_folder+'/'+name
                        target = target_folder+'/'+name
                        if target in targets_copied:
                            string = f'{date}/{name} : File already exists. Skip.'
                            print(string)
                            continue
                        else:
                            string = f'{date}/{name} : File not there. Copy it.'
                            print(string)
                            shutil.copy2(source,target_folder)
        elif file_structure=='new':
            target_folders = []
            for source_folder in source_folders_pictures:
                print('\nsource_folder =',source_folder)
                source_ARWs = glob.glob(source_folder+'/*.ARW')
                if len(source_ARWs)>0:
                    for source_ARW in source_ARWs:
                        name = source_ARW.split('/')[-1]
                        with open(source_ARW,'rb') as f:
                            tags = exifread.process_file(f)
                        date           = tags['Image DateTime'].values.split(' ')[0].replace(':','-')
                        target_folder  = f'transferred_pictures/{date}/RAW'
                        if target_folder not in target_folders:
                            make_path(path=target_folder)
                            target_folders.append(target_folder)
                        source = source_folder+'/'+name
                        target = target_folder+'/'+name
                        targets_copied = glob.glob(target_folder+'/*.ARW')
                        if target in targets_copied:
                            string = f'{date}/{name} : File already exists. Skip.'
                            print(string)
                            continue
                        else:
                            string = f'{date}/{name} : File not there. Copy it.'
                            print(string)
                            shutil.copy2(source,target_folder)
        else:
            raise Exception(f"ERROR: file_structure='{file_structure}' is not valid. Choose either 'old' or 'new' or 'auto'.")
        print('Done with raw files...')

    if do_copy_MTS:
        # Copy MTS files
        print('\nAbout to copy mts files...')
        # Import a library to read videos metadata
        import exiftool # pip install PyExifTool
        # Take a look at the list of MTS files
        source_MTSs = glob.glob(input_path+'/PRIVATE/AVCHD/BDMV/STREAM/*.MTS')
        for source in source_MTSs:
            metadata      = exiftool.ExifToolHelper().get_metadata(source)
            datetime      = metadata[0]['File:FileModifyDate']
            date          = datetime[:10].replace(':','-')
            time          = datetime[11:19]
            H,M,S         = time.split(':') # cannot have ":" in a file name in macOS
            datetime      = date+'_'+H+'h'+M+'m'+S+'s'
            target_folder = 'transferred_pictures/'+date+'/MTS'
            name          = source.split('/')[-1]
            #target        = target_folder+'/'+name # the problem with this is that if two videos of the same day have the same numbering (e.g. 0000.MTS) then one will not be imported.
            target        = target_folder+'/'+datetime+'.MTS'
            make_path(path=target_folder)
            if target in glob.glob(target_folder+'/*.MTS'):
                string = f'{date}/{name} : File already exists. Skip.'
                print(string)
                continue
            else:
                string = f'{date}/{name} : File not there. Copy it.'
                print(string)
                shutil.copy(source,target)
        print('Done with mts files...')


    if do_create_pictures_previews:

        target_folder_comp = 'transferred_pictures/temporary_compression_folder'
        target_folder_prev = 'transferred_pictures/previews'

        print('\nLooking at the the temporary compression folder exists.')
        if os.path.exists(target_folder_comp):
            print("WARNING : The temporary compression folder already exists. It is erased then created.")
            os.rmdir(target_folder_comp)
        else:
            print("The temporary compression folder doesn't exist. It is created")
        make_path(target_folder_comp)

        print('\nLooking at the final previews folder.')
        if not os.path.exists(target_folder_prev):
            print("The final previews folder doesn't exist, it is created.")
            make_path(target_folder_prev)
        else:
            print("The final previews folder already exists. OK.")

        for source_folder in source_folders_pictures:
            source_JPGs = glob.glob(source_folder+'/*.JPG')

            if len(source_JPGs)>0:
                first_JPG = source_JPGs[0]
                with open(first_JPG,'rb') as f:
                    tags = exifread.process_file(f)
                date      = tags['Image DateTime'].values.split(' ')[0].replace(':','-')
                names     = [picture_JPG.split('/')[-1] for picture_JPG in source_JPGs]

                targets_comp = glob.glob(target_folder_comp+'/*.JPG')
                targets_prev = glob.glob(target_folder_prev+'/*.JPG')               

                for name in names:
                    source      = source_folder     +'/'+name
                    target_comp = target_folder_comp+'/'+name
                    target_prev = target_folder_prev+'/'+name
                    if target_prev in targets_prev:
                        string = f'{date}/{name} : File already exists in the previews folder. Skip.'
                        print(string)
                        continue
                    else:
                        string = f'{date}/{name} : File not there. Copy it.'
                        print(string)
                        shutil.copy2(source,target_folder_comp)

        print('\nResizing and compressing the elements in the temporary compression folder.\nPlease wait as this can be long (≈3 images/second).')
        targets_comp = glob.glob(target_folder_comp+'/*.JPG')
        if len(targets_comp)>0:
            command = f"cd {target_folder_comp};sips -Z 3000 *.JPG"
            os.system(command)
            """
            Here it can be quite long.
            Just wait.
            It's approx. 3 images/second.
            So 900 images in 300 seconds, i.e. 5 minutes.
            """

        print('\nMoving all the compressed images from the temporary compression folder to the final previews folder...')
        source_JPGs = glob.glob(target_folder_comp+'/*.JPG')
        if len(source_JPGs)>0:
            names     = [picture_JPG.split('/')[-1] for picture_JPG in source_JPGs]
            targets_prev = glob.glob(target_folder_prev+'/*.JPG')
            for name in names:
                target_comp = target_folder_comp+'/'+name
                target_prev = target_folder_prev+'/'+name
                if target_prev in targets_prev:
                    string = f'{date}/{name} : (WARNING) File already exists in the previews folder (which is weird). Skip.'
                    print(string)
                    continue
                else:
                    string = f'{date}/{name} : File not there. Move it.'
                    print(string)
                    shutil.move(target_comp,target_prev)

        print('\nErasing the temporary compression folder...')
        if os.path.exists(target_folder_comp):
            print("The temporary compression folder already exists. It is erased.")
            os.rmdir(target_folder_comp)
        else:
            print("The temporary compression folder doesn't exist. OK.")
        print('Done with the previews.')

    # If we want to open the Finder folder
    if do_show_in_Finder:
        from subprocess import call
        call(["open", output_path[1:]])

    print('All done.')

################################################################################
################################################################################
# Using functions

def main():

    do_copy_camera_pictures_to_computer=1
    if do_copy_camera_pictures_to_computer:
        copy_camera_pictures_to_computer()

if __name__ == '__main__':
    main()
