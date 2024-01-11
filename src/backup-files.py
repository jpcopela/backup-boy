import subprocess
import shutil
from glob import glob
from threading import Thread

from rich.theme import Theme
from rich.text import Text
from rich.console import Console
from rich.table import Table

from tqdm import tqdm

success_theme = Theme({"success": "bold green", "error": "bold red", "warning": "bold yellow", "info": "bold blue"})
console = Console(theme=success_theme)

def main():
    #Run the connect_cameras.sh script
    console.print("Searching for cameras...", style="info")
    camera_connect = subprocess.run(['bash', 'connect_cameras.sh'], capture_output=True, text=True)
    device_name = camera_connect.stdout.strip()

    cam_detected = Text(f"Camera detected: {device_name}")
    cam_detected.stylize('success', 0, 15)
    console.print(cam_detected)

    #Run the connect_storage.sh script
    console.print("Searching for external storage...", style="info")
    storage_connect = subprocess.run(['bash', 'connect_storage.sh'], capture_output=True, text=True)
    mount_point = storage_connect.stdout.strip()
    total_storage = round(shutil.disk_usage(mount_point).total / 1024 / 1024 / 1024, 2)
    available_storage = round(shutil.disk_usage(mount_point).free / 1024 / 1024 / 1024, 2)

    fraction_available = available_storage / total_storage

    console.print(f"External storage detected: {mount_point}.", style="success")

    if (fraction_available > 0.66):
        console.print(f"{available_storage} GB available out of {total_storage} GB.", style="success")
    elif (fraction_available > 0.33):
        console.print(f"{available_storage} GB available out of {total_storage} GB.", style="warning")
    else:
        console.print(f"{available_storage} GB available out of {total_storage} GB.", style="error")

    #Run the backup_config.sh script
    backup_config = subprocess.run(['bash', 'backup_config.sh', device_name, mount_point], capture_output=True, text=True)

    #Run the prepare_mtb.sh script
    prepare_mtp = subprocess.run(['bash', 'prepare_mtp.sh'], capture_output=True, text=True)

    #Get a list of the files to be backed up as a table
    file_list = subprocess.run(['gphoto2', '--list-files'], capture_output=True, text=True)
    #get only the lines that start with #
    file_list = subprocess.run(['grep', '^#'], capture_output=True, text=True, input=file_list.stdout)

    #The columns we want are filename, size, and filetype
    #The columns are separated by a variable number of spaces
    #We can use awk to print the columns we want

    #First, videos and non-image files don't have a dimension column
    #we will just replace text that matches the pattern YYYYxYYYY with a blank space
    file_list = subprocess.run(['sed', 's/[0-9]\{4\}x[0-9]\{4\}//g'], capture_output=True, text=True, input=file_list.stdout)

    #get the columns we want
    file_list = subprocess.run(['awk', '{print $2, $4, $5, $6}'], capture_output=True, text=True, input=file_list.stdout)

    #split the output into lines
    file_list = file_list.stdout.splitlines()

    total_files = len(file_list)

    #Create a table
    table = Table()
    table.add_column("File name")
    table.add_column("Size")
    table.add_column("File type")

    num_files = 0 #number of files to be backed up
    total_size = 0.0 #total size of files to be backed up in MB

    #Add the rows to the table
    for row in file_list:
        filename, size, unit, filetype = row.split()

        #determine if filename exists on the external storage device
        #if so, remove it from the list
        if (glob(mount_point + '/**/' + filename, recursive=True) != []):
            file_list.remove(row)
            continue

        #convert the size to MB
        if (unit == 'GB'):
            size = str(round(float(size) * 1024, 2))
        elif (unit == 'KB'):
            size = str(round(float(size) / 1024, 2))

        unit = 'MB'

        table.add_row(filename, size + f' {unit}', filetype)
        num_files += 1
        total_size += float(size)

    #change the title of the table to include the number of files
    if (num_files == 0.0):
        console.print("There are no files to be backed up.", style="success")
    elif (num_files / total_files < 0.33):
        console.print(f"There are {num_files} files to be backed up.", style="success")
    elif (num_files / total_files < 0.66):
        console.print(f"There are {num_files} files to be backed up.", style="warning")
    else:
        console.print(f"There are {num_files} files to be backed up.", style="error")

    #Print the table
    console.print(table, style="success")

    initial_space_taken = round(shutil.disk_usage(mount_point).used / 1024 / 1024, 2)

    #Download the files
    console.print("Downloading files...", style="info")
    download_process = subprocess.Popen(['bash', 'download_files.sh', device_name, mount_point])

    with tqdm(total=total_size, unit='MB', unit_scale=True, desc='', colour='green') as pbar:
        while (download_process.poll() == None):
            #get the new space taken by the files in the backup directory
            megabytes_down = round(shutil.disk_usage(mount_point).used / 1024 / 1024, 2) - initial_space_taken

            initial_space_taken += megabytes_down
            #update the progress bar
            pbar.update(megabytes_down)

    pbar.close()
    
    #Wait for the download process to finish
    download_process.wait()

    console.log("Done!", style="success")

    #Run the cleanup.sh script
    subprocess.run(['bash', 'cleanup.sh', mount_point])

if __name__ == "__main__":
    main()