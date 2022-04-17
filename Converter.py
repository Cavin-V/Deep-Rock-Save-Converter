from datetime import datetime
import shutil
import sys
import time
import os
import traceback

import pytz

#Full disclaimer: I am not responsible for any damage done to your system or deep rock save data due to the use of this script.
#Like if you're worried, probably backup your save(s) yourself (even though in theory the script should be doing that for you)
#There is a remote chance that this script will break your save(s) if you're not careful, or fail to backup due to file system changes.
#Disclaimer number 2: I wrote this in literally 3 hours and it looks like trash, but it works so whatever.
#Disclaimer number 3: This only works on windows (which should be obvious since it converts your WINDOWS STORE version of deep with with your steam version)


class ConfigData:
    data = {
        "quick_convert": False,
        "convert_direction": "windows",
        "steam_save_path": "",
        "windows_save_path": "",
    }
    defaultData = {
        "quick_convert": False,
        "convert_direction": "windows",
        "steam_save_path": "",
        "windows_save_path": "",
    }

#check if config exists
if os.path.isfile("config.txt")==False:
    print("Welcome to the ultra cool deep rock save game converter!\nTo start off, confirm that this file is its own seperate directory, as it will be generating a few files and folders.\ny/n")
    while True:
        try:
            answer=input()
            if answer=="y":
                break
            elif answer=="n":
                print("Then go do that nerd.")
                time.sleep(5)
                sys.exit()
            else:
                print("Please enter y or n.")
        except Exception:
            traceback.print_exc()
            print("An error occured, please try again.")
            time.sleep(5)
    try:
        #Clear the terminal
        os.system('cls' if os.name == 'nt' else 'clear')
        #Create the folders
        os.write(1, b"Cool, generating files")
        time.sleep(1)
        os.mkdir("Saves")
        os.write(1, b".")
        time.sleep(1)
        os.mkdir("Saves/Windows")
        os.write(1, b".")
        time.sleep(1)
        os.mkdir("Saves/Steam")
        os.write(1, b".\n")
        open("config.txt", "w").close()
    except Exception:
        traceback.print_exc()
        print("An error occured, please try again.")
        time.sleep(5)
    print("Done!")
#Check for data
if os.path.isfile("config.txt"):
    try:
        with open("config.txt", "r") as f:
            for line in f:
                if line.startswith("quick_convert"):
                    if line.split("=")[1].strip()=="True":
                        ConfigData.data["quick_convert"] = True
                    if line.split("=")[1].strip()=="False":
                        ConfigData.data["quick_convert"] = False
                if line.startswith("steam_save_path"):
                    ConfigData.data["steam_save_path"] = line.split("=")[1].strip()
                if line.startswith("windows_save_path"):
                    ConfigData.data["windows_save_path"] = line.split("=")[1].strip()
                if line.startswith("convert_direction"):
                    ConfigData.data["convert_direction"] = line.split("=")[1].strip()
    except Exception:
        traceback.print_exc()
        print("An error occured, please try again.")
        time.sleep(5)

#Alright, now for some user input
if ConfigData.data["quick_convert"] == True:
    if ConfigData.data["convert_direction"] == "windows":
        print("This will automatically convert save data from steam to windows.")
        print("y/n")
    if ConfigData.data["convert_direction"] == "steam":
        print("This will automatically convert save data from windows to steam.")
        print("y/n")
    while True: #The big question zone, home to changing the config
        try:
            answer = input()
            if answer=="y":
                break
            elif answer=="n":
                print("Understandable, would you like to change the direction of conversion?")
                answer = input()
                if answer=="y":
                    print("Please enter the new direction of conversion.")
                    while True:
                        try:
                            answer=input()
                            if answer=="windows":
                                ConfigData.data["convert_direction"] = "windows"
                                break
                            elif answer=="steam":
                                ConfigData.data["convert_direction"] = "steam"
                                break
                            else:
                                print("Please enter either windows or steam.")
                        except Exception:
                            traceback.print_exc()
                            print("An error occured, please try again.")
                            time.sleep(5)
                    #Write the new data to the config file
                    with open("config.txt", "w") as f:
                        f.write("quick_convert="+str(ConfigData.data["quick_convert"])+"\n")
                        f.write("steam_save_path="+str(ConfigData.data["steam_save_path"])+"\n")
                        f.write("windows_save_path="+str(ConfigData.data["windows_save_path"])+"\n")
                        f.write("convert_direction="+str(ConfigData.data["convert_direction"])+"\n")
                    break
                elif answer == "n":
                    print("Would you like to turn quick convert off, and reinput your save locations?")
                    answer = input()
                    if answer=="y":
                        ConfigData.data["quick_convert"] = "False"
                        with open("config.txt", "w") as f:
                            f.write("quick_convert="+str(ConfigData.data["quick_convert"])+"\n")
                            f.write("steam_save_path="+str(ConfigData.data["steam_save_path"])+"\n")
                            f.write("windows_save_path="+str(ConfigData.data["windows_save_path"])+"\n")
                            f.write("convert_direction="+str(ConfigData.data["convert_direction"])+"\n")
                        print("Program will now ask you on start up for new save locations.")
                        time.sleep(5)
                        sys.exit()
                    if answer=="n":
                        print("Okay, program will now exit.")
                        time.sleep(5)
                        sys.exit()
                else:
                    print("Please enter y or n.")
            else:
                print("Please enter y or n.")
        except Exception:
            traceback.print_exc()
            print("An error occured, please try again.")
            time.sleep(5)
    #Backup saves, just in case.tm
    currentTimeStr = datetime.now(pytz.timezone("UTC")).strftime("%Y-%m-%d-%H+%M+%S")
    newWindowsDir = None
    def backupSaves():
        global newWindowsDir
        if os.path.isfile(ConfigData.data["steam_save_path"])==True:
            os.mkdir("Saves/Steam/Backup-"+currentTimeStr)
            shutil.copy(ConfigData.data["steam_save_path"], "Saves/Steam/{}".format("backup-"+currentTimeStr))
        else:
            print("No steam save found.")
            time.sleep(3)
        if os.path.isdir("\\".join(ConfigData.data["windows_save_path"].split("\\")[:-1]))==True:
            i=0
            saveFile = None
            for file in os.listdir("\\".join(ConfigData.data["windows_save_path"].split("\\")[:-1])):
                if file.find(".")==-1:
                    saveFile = file
                    break
                i+=1
            if os.path.isfile("\\".join(ConfigData.data["windows_save_path"].split("\\")[:-1])+"\\"+saveFile)==True:
                os.mkdir("Saves/Windows/Backup-"+currentTimeStr)
                newWindowsDir = "\\".join(ConfigData.data["windows_save_path"].split("\\")[:-1])+"\\"+saveFile
                shutil.copy("\\".join(ConfigData.data["windows_save_path"].split("\\")[:-1])+"\\"+saveFile, "Saves/Windows/{}".format("backup-"+currentTimeStr))
        else:
            print("No windows save found.")
            time.sleep(3)
    #Actually convert the save data
    if ConfigData.data["convert_direction"] == "windows":
        os.system('cls')
        os.write(1, b"Converting from steam to windows")
        time.sleep(1)
        os.write(1, b".")
        time.sleep(0.3)
        os.write(1, b".")
        #Real conversion hours
        backupSaves()
        if os.path.isfile(newWindowsDir)==True:
            os.remove(newWindowsDir)
        shutil.copy("Saves/Steam/Backup-"+currentTimeStr+"/"+ConfigData.data["steam_save_path"].split("\\")[-1], newWindowsDir)

        time.sleep(1)
        os.write(1, b".")
        time.sleep(1)
        os.system('cls')
        print("Conversion complete.")
        time.sleep(3)
    if ConfigData.data["convert_direction"] == "steam":
        os.system('cls')
        os.write(1, b"Converting from windows to steam")
        time.sleep(1)
        os.write(1, b".")
        time.sleep(0.3)
        os.write(1, b".")
        #Real conversion hours
        backupSaves()
        if os.path.isfile(ConfigData.data["steam_save_path"])==True:
            os.remove(ConfigData.data["steam_save_path"])
        shutil.copy("Saves/Windows/Backup-"+currentTimeStr+"/"+newWindowsDir.split("\\")[-1], ConfigData.data["steam_save_path"])

        time.sleep(1)
        os.write(1, b".")
        time.sleep(1)
        os.system('cls')
        print("Conversion complete.")
        time.sleep(3)
        #TODO Put conversion stuff here
else: #If quick convert is false
    #Wheres the files sir?
    print("Step one: Please enter your steam save path\n(e.g. C:\\Program Files (x86)\\Steam\\steamapps\\common\\Deep Rock Galactic\\FSD\\Saved\\SaveGames\\(Name of the save file without Backup in the name, including the .sav))")
    while True:
        try:
            answer = input()
            if os.path.isfile(answer):
                ConfigData.data["steam_save_path"] = answer
                break
            else:
                print("That doesn't seem to be a valid file, please try again.")
        except Exception:
            traceback.print_exc()
            print("An error occured, please try again.")
            time.sleep(5)
    print("Step two: Please enter your windows save path\n(e.g. C:\\Users\\[Your Computer Username]\\AppData\\Local\\Packages\\CoffeeStainStudios.DeepRockGalactic_(String of... Stuff)\\SystemAppData\\wgs\\(The folder with a very long name)\\(The OTHER folder with a really long name)\\(Finally the file inside this folder with yet another long strange name, it should be the only file in the folder with a long name)\n")
    print("Yeah... It looks a bit scetch, but trust me, this is where the windows save data is located.\nIf by some chance you don't have a file with a long name in your funky folder with a long name, you may need to ensure you have started up deep rock on windows first.\n")
    while True:
        try:
            answer = input()
            if os.path.isfile(answer):
                ConfigData.data["windows_save_path"] = answer
                break
            else:
                print("That doesn't seem to be a valid file, please try again.")
        except Exception:
            traceback.print_exc()
            print("An error occured, please try again.")
            time.sleep(5)
    print("Step three: Please enter the direction you want to convert your save data. (steam, for if you want to convert from windows to steam, or windows if you want to convert from windows to steam.\nOnce this is set up, you may run the program again and it will automatically convert your save data.\n")
    while True:
        try:
            answer = input()
            if answer=="steam":
                ConfigData.data["convert_direction"] = "steam"
                break
            elif answer=="windows":
                ConfigData.data["convert_direction"] = "windows"
                break
            else:
                print("Please enter steam or windows.")
        except Exception:
            traceback.print_exc()
            print("An error occured, please try again.")
            time.sleep(5)
    #Write the config file
    with open("config.txt", "w") as f:
        f.write("quick_convert="+str(True)+"\n")
        f.write("steam_save_path="+str(ConfigData.data["steam_save_path"])+"\n")
        f.write("windows_save_path="+str(ConfigData.data["windows_save_path"])+"\n")
        f.write("convert_direction="+str(ConfigData.data["convert_direction"]))
    f.close()