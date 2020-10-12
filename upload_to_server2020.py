from os import path
import shutil

server_path = "/home/pi/server/Videos_GRETI/field_season_fall_2020"
pi_path = "/home/pi/APAPORIS/moved"
data_filename = "uploaded_files.txt"


def list_files_uploaded():
    with open(data_filename, "a+") as uploaded_files:
        uploaded_files.seek(0)
        already_uploaded = [line.strip() for line in uploaded_files]
    return already_uploaded


while __name__ == "__main__":
    
    if not path.exists(server_path):
        print("server is not connected")
        break

    else:
        already_uploaded = list_files_uploaded()
    
    to_upload = [f for f in os.listdir(pi_path)]    
    
    for f in to_upload:
        try:
            copy2(path.join(pi_path,f), path.join(server_path, f))

        except:
            print("error processing {}".format(f))
            pass
        else:
            print("finished processing {}".format(f))
            with open(data_filename, "a+") as processed_file:
                processed_file.write("{}\n".format(directory))


