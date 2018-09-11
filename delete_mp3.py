import glob, os

## Delete Downloaded Mp3-File from a Disk

os.chdir("/temp/")
for file in glob.glob("*.mp3"):
    if os.path.exists(file):
        os.remove(file)
        print('Deleted: ' + file)
    else:
        print("The file does not exist")