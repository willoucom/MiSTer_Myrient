#!/usr/bin/env python3

# MIT License
# 
# Copyright (c) 2023 Wilfried "willoucom" JEANNIARD
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import ftplib
import os
import random
import string
import re
import sys
import tempfile
# import zipfile

from zipfile import ZipFile

myrient_host = "ftp.myrient.erista.me"

# Stucture of folders/remote
# f = Local Folder
# s = Remote/Source Folder
# z = (Optionnal) Zipfile name (default to 'games')
# o = (Optionnal) Create a Zipfile for each alphabet letter
# { "f":"", "s":""},
sets = {
    # Atari
    "Atari2600": {"f": "Atari2600", "s": "/No-Intro/Atari - 2600/", "o": True},
    "Atari5200": {"f": "Atari5200", "s": "/No-Intro/Atari - 5200/", "o": True},
    "Atari7800": {"f": "Atari7800", "s": "/No-Intro/Atari - 7800/", "o": True},
    "AtariLynx": {"f": "AtariLynx", "s": "/No-Intro/Atari - Lynx/", "o": True},
    # Bandai
    "WonderSwan" : {"f": "WonderSwan", "s": "/No-Intro/Bandai - WonderSwan/", "z": "WonderSwan", "o": True},
    "WonderSwanColor": { "f": "WonderSwan", "s": "/No-Intro/Bandai - WonderSwan Color/", "z": "WonderSwanColor", "o": True},
    # Nec
    "TGFX-16": {"f": "TGFX-16", "s": "/No-Intro/NEC - PC Engine - TurboGrafx-16/", "o": True},
    "Supergrafx": {"f": "TGFX-16", "s": "/No-Intro/NEC - PC Engine SuperGrafx/", "z": "supergrafx", "o": True},
    # Nintendo
    "Famicom": {"f": "NES", "s": "/No-Intro/Nintendo - Family Computer Disk System (FDS)", "z": "fds", "o": True},
    "NES": {"f": "NES", "s": "/No-Intro/Nintendo - Nintendo Entertainment System (Headered)", "z": "nes", "o": True},
    "GAMEBOY": {"f": "GAMEBOY", "s": "/No-Intro/Nintendo - Game Boy", "o": True},
    "GBC": {"f": "GBC", "s": "/No-Intro/Nintendo - Game Boy Color", "o": True},
    "GBA": {"f": "GBA", "s": "/No-Intro/Nintendo - Game Boy Advance", "o": True},
    "SNES": { "f": "SNES", "s": "/No-Intro/Nintendo - Super Nintendo Entertainment System", "o": True},
    "N64": {"f": "N64", "s": "/No-Intro/Nintendo - Nintendo 64 (BigEndian)", "o": True},
    "PokemonMini": {"f":"PokemonMini", "s":"/No-Intro/Nintendo - Pokemon Mini"},
    # Sega
    "GameGear": {"f": "GameGear", "s": "/No-Intro/Sega - Game Gear", "o": True},
    "SMS": {"f": "SMS", "s": "/No-Intro/Sega - Master System - Mark III", "o": True},
    "Megadrive": {"f": "Genesis", "s": "/No-Intro/Sega - Mega Drive - Genesis", "o": True},
    "S32X": {"f": "S32X", "s": "/No-Intro/Sega - 32X"},
    "SG1000":{"f":"Coleco", "s":"/No-Intro/Sega - SG-1000", "z":"SG1000"},
    # Entex
    "AVision": {"f":"AVision", "s":"/No-Intro/Entex - Adventure Vision"},
    # Emerson
    "Arcadia": {"f":"Arcadia", "s":"/No-Intro/Emerson - Arcadia 2001"},
    # Bally
    "Astrocade": {"f":"Astrocade", "s":"/No-Intro/Bally - Astrocade"},
    # Casio
    "Casio_PV-1000": {"f":"Casio_PV-1000", "s":"/No-Intro/Casio - PV-1000"},
    # Fairchild
    "ChannelF": {"f":"ChannelF", "s":"/No-Intro/Fairchild - Channel F"},
    # Coleco
    "Colecovision":{"f":"Coleco", "s":"/No-Intro/Coleco - ColecoVision", "z":"Coleco"},
    # VTech
    "CreatiVision" : { "f":"CreatiVision", "s":"/No-Intro/VTech - CreatiVision"},
    # Bit Corporation
    "Gamate" : { "f":"Gamate", "s":"/No-Intro/Bit Corporation - Gamate"},
    # Mattel
    "Intellivision" : { "f":"Intellivision", "s":"/No-Intro/Mattel - Intellivision"},
    # Weback
    "MegaDuck" : { "f":"MegaDuck", "s":"/No-Intro/Welback - Mega Duck"},
    # Nichibutsu
    "MyVision" : { "f":"MyVision", "s":"/No-Intro/Nichibutsu - My Vision"},
    # Philips
    "Videopac" : { "f":"ODYSSEY2","s":"/No-Intro/Philips - Videopac+", "z":"Videopac"},
    # Benesse
    "PocketChallengeV2" : { "f":"WonderSwan", "s":"/No-Intro/Benesse - Pocket Challenge V2", "z": "PocketChallengeV2"},
    # Watara
    "SuperVision" : { "f":"SuperVision", "s":"/No-Intro/Watara - Supervision"},
    # Interton
    "VC4000" : { "f":"VC4000", "s":"/No-Intro/Interton - VC 4000"},
    # GCE
    "Vectrex" : { "f":"VECTREX", "s":"/No-Intro/GCE - Vectrex"},
}

alphabet = [
    "#",
    "_BetaProto",
    "_Homebrew",
    "_Aftermarket",
    "A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z",
]

games_dir = "/media/fat/games/"


def main():

    if len(sys.argv) >= 2:
        options = sys.argv
        options.remove(sys.argv[0])
        for set in options:
            if set == "ALL":
                options = list(sets.keys())
                continue
            if set not in sets:
                exit("Set '%s' not found" % set)

    else:
        systems = list(sets.keys())
        systems.sort()
        print("Usage: run myrient.py set1 set2 set...")
        print("List of sets: ")
        print(' '.join(systems))
        print("Or use 'ALL' to download everything")
        exit()

    # Main loop
    options.sort()
    for sett in options:
        if sett in sets:
            set = sets[sett]
        else:
            exit("Set %s not found" % sett)

        print("* %s *" % sett)
        
        local_files = []
        # Zipfile name
        if not "z" in set:
            set["z"] = "games"

        # Check destination folder
        rompath = games_dir + set["f"]
        if not os.path.isdir(rompath):
            print(rompath + " not found, creating")
            os.makedirs(rompath, exist_ok=True)

        # Get local game list
        local_files = getRomlist(rompath, set)
        # Write game list to disk
        writeLocalRomList(rompath, set)

        # Connect FTP
        ftp = connectFTP(myrient_host)
        # Change ftp directory
        ftp.cwd(set["s"])
        # Get file list
        ftp_files = ftp.nlst()
        ftp.close()
        # Main loop
        for ftp_files_name in ftp_files:
            found = False
            # List of files to remove from local list
            to_remove = []
            ## Look for remote name in local list
            for local_files_name in local_files:
                if os.path.splitext(ftp_files_name)[0] == os.path.splitext(local_files_name)[0]:
                    found = True
                    to_remove.append(local_files_name)

            if not found:
                print("  " + ftp_files_name + " Not found, downloading")
                # Connect FTP
                ftp = connectFTP(myrient_host)
                ftp.cwd(set["s"])
                # Download file
                with tempfile.TemporaryFile() as f:
                    try:
                        ftp.retrbinary("RETR " + ftp_files_name, f.write)
                    except ftplib.all_errors as e:
                        print(str(e))
                        ftp.close()
                        continue
                    ftp.close()
                    # Read file
                    with ZipFile(f, "r") as tmpzip:
                        tmpzip_files = tmpzip.namelist()
                        if len(tmpzip_files) > 1:
                            print("   <!> Multiple files detected inside zip, creating a dummy file <!>")
                            dummyfile = os.path.splitext(ftp_files_name)[0]+".dummy"
                            if dummyfile not in tmpzip_files:
                                tmpzip_files.append(dummyfile)

                        for tmpzip_files_name in tmpzip_files:
                            print("   Adding " + tmpzip_files_name)
                            destination_filename = tmpzip_files_name
                            # Check if Zip and Content filename match (only when there is only 1 file inside the zip)
                            if os.path.splitext(ftp_files_name)[0] != os.path.splitext(tmpzip_files_name)[0] and len(tmpzip_files) == 1:
                                print("   <!> ZIP and Content mismatch <!>")
                                destination_filename = os.path.splitext(ftp_files_name)[0] + os.path.splitext(tmpzip_files_name)[1]
                                print("    > Renaming destination file to: "+ destination_filename)

                            if destination_filename in local_files:
                                print(" > " + destination_filename + " already exists")
                                to_remove.append(destination_filename)
                            else:
                                if not "o" in set or ("o" in set and set["o"] is False):
                                    # One zip for the system
                                    zipfile = rompath + "/" + set["z"] + ".zip"
                                else:
                                    # in case of split
                                    # Get destination
                                    letter = destinationLetter(destination_filename)
                                    zipfile = rompath + "/" + set["z"] + "_" + letter + ".zip"
                                # Add file to games archive
                                createZip(zipfile)
                                if os.path.splitext(tmpzip_files_name)[1] == ".dummy":
                                    print("    *** Dummy file detected, create an empty file")
                                    tmpfile = ""
                                else:
                                    tmpfile = tmpzip.read(tmpzip_files_name)
                                addFileToZip(zipfile, tmpfile, destination_filename)
            # Clean local files list
            if to_remove:
                for remove in to_remove:
                    local_files.remove(remove)
        # Cleaning zip
        # TODO: Rewrite zipfile
        # Print leftovers
        if len(local_files):
            print("  Leftovers:")
            for zip_name in local_files:
                print("     " + zip_name)
        # Write leftovers to file
        file = open(rompath + "/leftovers.txt", "w")
        for item in local_files:
            file.write(item + "\n")
        file.close()
        # Get local game list
        local_files = getRomlist(rompath, set)
        # Write game list to disk
        writeLocalRomList(rompath, set)
        print("* /%s *" % sett)
        print("---")


# Functions


def connectFTP(server):
    """ Connect to FTP server """
    ftp = ftplib.FTP(myrient_host)
    ftp.login()
    return ftp


def createZip(name):
    """ Create a zipfile """
    if not os.path.isfile(name):
        print(name + " not found, creating")
        with ZipFile(name, "w") as file:
            pass


def destinationLetter(name):
    """ Get folder for the game based on the first letter or a keyword """
    letter = name[0]
    # Check in name
    if "(Homebrew)" in name:
        return "_Homebrew"
    if (
        "(Beta)" in name
        or "(Proto)" in name
        or bool(re.search(r"\(Beta [0-9]+", name))
        or bool(re.search(r"\(Proto [0-9]+", name))
    ):
        return "_BetaProto"
    if "(Aftermarket)" in name or "(Unl)" in name:
        return "_Aftermarket"
    if letter in alphabet:
        return letter
    else:
        return "#"


def addFileToZip(zipfile: str, content: bytes, name: str):
    """ Add file to games archive """
    zip = ZipFile(zipfile, "a")
    zip.writestr(name, content)
    zip.close()


def getRomlist(rompath, set):
    """ Get list of roms """
    local_files = []
    # Option to split files
    if not "o" in set or ("o" in set and set["o"] is False):
        zipfile = rompath + "/" + set["z"] + ".zip"
        createZip(zipfile)
        # Open Zip
        zip = ZipFile(zipfile, "r")
        local_files = zip.namelist()
        zip.close()
    else:
        # If Split
        for letter in alphabet:
            zipfile = rompath + "/" + set["z"] + "_" + letter + ".zip"
            # Open Zip
            if os.path.isfile(zipfile):
                zip = ZipFile(zipfile, "r")
                local_files += zip.namelist()
                zip.close()
    local_files.sort()
    return local_files

def writeLocalRomList(rompath, set):
    """ Write list of games locally """
    # Get local game list
    local_files = getRomlist(rompath, set)
    # Write game list to disk
    file = open(rompath + "/gamelist.txt", "w")
    for item in local_files:
        file.write(item + "\n")
    file.close()

main()
