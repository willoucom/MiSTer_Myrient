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

import os
import subprocess
import re
import sys

from zipfile import ZipFile
from Myrient import Myrient

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
    "WonderSwan": {"f": "WonderSwan", "s": "/No-Intro/Bandai - WonderSwan/", "z": "WonderSwan", "o": True},
    "WonderSwanColor": {"f": "WonderSwan", "s": "/No-Intro/Bandai - WonderSwan Color/", "z": "WonderSwanColor", "o": True},
    # Nec
    "TGFX-16": {"f": "TGFX-16", "s": "/No-Intro/NEC - PC Engine - TurboGrafx-16/", "o": True},
    "Supergrafx": { "f": "TGFX-16", "s": "/No-Intro/NEC - PC Engine SuperGrafx/", "z": "supergrafx", "o": True},
    # Nintendo
    "Famicom": {"f": "NES", "s": "/No-Intro/Nintendo - Family Computer Disk System (FDS)", "z": "fds", "o": True},
    "NES": {"f": "NES", "s": "/No-Intro/Nintendo - Nintendo Entertainment System (Headered)", "z": "nes", "o": True},
    "GAMEBOY": {"f": "GAMEBOY", "s": "/No-Intro/Nintendo - Game Boy", "o": True},
    "GBC": {"f": "GBC", "s": "/No-Intro/Nintendo - Game Boy Color", "o": True},
    "GBA": {"f": "GBA", "s": "/No-Intro/Nintendo - Game Boy Advance", "o": True},
    "SNES": {"f": "SNES", "s": "/No-Intro/Nintendo - Super Nintendo Entertainment System", "o": True},
    "N64": {"f": "N64", "s": "/No-Intro/Nintendo - Nintendo 64 (BigEndian)", "o": True},
    "PokemonMini": {"f": "PokemonMini", "s": "/No-Intro/Nintendo - Pokemon Mini"},
    # Sega
    "GameGear": {"f": "GameGear", "s": "/No-Intro/Sega - Game Gear", "o": True},
    "SMS": {"f": "SMS", "s": "/No-Intro/Sega - Master System - Mark III", "o": True},
    "Megadrive": {"f": "Genesis", "s": "/No-Intro/Sega - Mega Drive - Genesis", "o": True},
    "S32X": {"f": "S32X", "s": "/No-Intro/Sega - 32X"},
    "SG1000": {"f": "Coleco", "s": "/No-Intro/Sega - SG-1000", "z": "SG1000"},
    # Entex
    "AVision": {"f": "AVision", "s": "/No-Intro/Entex - Adventure Vision"},
    # Emerson
    "Arcadia": {"f": "Arcadia", "s": "/No-Intro/Emerson - Arcadia 2001"},
    # Bally
    "Astrocade": {"f": "Astrocade", "s": "/No-Intro/Bally - Astrocade"},
    # Casio
    "Casio_PV-1000": {"f": "Casio_PV-1000", "s": "/No-Intro/Casio - PV-1000"},
    # Fairchild
    "ChannelF": {"f": "ChannelF", "s": "/No-Intro/Fairchild - Channel F"},
    # Coleco
    "Colecovision": {"f": "Coleco", "s": "/No-Intro/Coleco - ColecoVision", "z": "Coleco"},
    # VTech
    "CreatiVision": {"f": "CreatiVision", "s": "/No-Intro/VTech - CreatiVision"},
    # Bit Corporation
    "Gamate": {"f": "Gamate", "s": "/No-Intro/Bit Corporation - Gamate"},
    # Mattel
    "Intellivision": {"f": "Intellivision", "s": "/No-Intro/Mattel - Intellivision"},
    # Weback
    "MegaDuck": {"f": "MegaDuck", "s": "/No-Intro/Welback - Mega Duck"},
    # Nichibutsu
    "MyVision": {"f": "MyVision", "s": "/No-Intro/Nichibutsu - My Vision"},
    # Philips
    "Videopac": {"f": "ODYSSEY2", "s": "/No-Intro/Philips - Videopac+", "z": "Videopac"},
    # Benesse
    "PocketChallengeV2": {"f": "WonderSwan", "s": "/No-Intro/Benesse - Pocket Challenge V2", "z": "PocketChallengeV2"},
    # Watara
    "SuperVision": {"f": "SuperVision", "s": "/No-Intro/Watara - Supervision"},
    # Interton
    "VC4000": {"f": "VC4000", "s": "/No-Intro/Interton - VC 4000"},
    # GCE
    "Vectrex": {"f": "VECTREX", "s": "/No-Intro/GCE - Vectrex"},
    # SNK
    "NGP": {"f":"NGP", "s": "/No-Intro/SNK - NeoGeo Pocket/"},
    "NGC": {"f":"NGP", "s": "/No-Intro/SNK - NeoGeo Pocket Color/", "z": "Color"},

    # Computers
    # C64
    "C64": {"f": "C64", "s": "/No-Intro/Commodore - Commodore 64", "o": True},
    # MSX
    "MSX1": {"f": "MSX1", "s": "/No-Intro/Microsoft - MSX", "o": True},
}

alphabet = [
    "#",
    "_Aftermarket",
    "_Bios",
    "_BetaProto",
    "_Demo",
    "_Homebrew",
    "_Pirate",
    "_VirtualConsole",
    "A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z",
]

# Can be configured with environment variable MYRIENT_DIR
games_dir = os.environ.get("MYRIENT_DIR", "/media/fat/games/")

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
        print(" ".join(systems))
        print("Or use 'ALL' to download everything")
        exit()

    myrient = Myrient()

    # Main loop
    options.sort()
    for system in options:
        if system in sets:
            set = sets[system]
        else:
            exit("Set %s not found" % system)

        print("* %s *" % system)

        local_files = []
        ftp_files = []
        missing = []

        # Zipfile name
        if not "z" in set:
            set["z"] = "games"
        # Splitted (off by default)
        if not "o" in set:
            set["o"] = False

        # Check destination folder
        rompath = games_dir +'/'+ set["f"]
        if not os.path.isdir(rompath):
            print(rompath + " not found, creating")
            os.makedirs(rompath, exist_ok=True)

        # Get local game list
        print("Get local game list: "+ rompath)
        local_files, _ = myrient.getRomlist(rompath)

        # Get remote
        print("Get remote files from: "+ set['s'])
        ftp_files = myrient.listForSystem(set['s'])

        print("Compare remote/local")
        missing = getMissingFiles(local_files, ftp_files)

        # Main loop
        # loop missing games
        firstchar = " "
        if len(missing) == 0:
            print("Nothing to download")
        else:
            print("Downloading:")
            for ftp_files_name in missing:
                # progress-like
                firstchar_n = ftp_files_name[0]
                if firstchar_n != firstchar:
                    print(firstchar_n + ".")
                    firstchar = firstchar_n

                print("  " + ftp_files_name)
                if not "o" in set or ("o" in set and set["o"] is False):
                    # One zip for the system
                    zipfile = rompath + "/" + set["z"] + ".zip"
                else:
                    # in case of split
                    # Get destination
                    letter = destinationLetter(ftp_files_name)
                    zipfile = rompath + "/" + set["z"] + "_" + letter + ".zip"

                # Get the file
                myrient.getFile(set['s'], ftp_files_name, zipfile)

        # Print leftovers
        todelete = {}
        _, local_files = myrient.getRomlist(rompath)
        print("Fetch leftovers")
        todelete = getLeftoverFiles(local_files, ftp_files, todelete)

        # Cleaning zip
        print("Clean zips")
        deleteFromZip(todelete) 

        local_files.clear()
        ftp_files.clear()
        missing.clear()
        todelete.clear()
        print("---\n")


# Functions

def destinationLetter(name):
    """Get folder for the game based on the first letter or a keyword"""
    letter = name[0]
    # Check in name
    if "[BIOS]" in name:
        return "_Bios"
    if "(Homebrew)" in name:
        return "_Homebrew"
    if "(Pirate)" in name:
        return "_Pirate"
    if "(Aftermarket)" in name or "(Unl)" in name:
        return "_Aftermarket"
    if ("Virtual Console") in name:
        return "_VirtualConsole"
    if "(Demo)" in name:
        return "_Demo"
    if (
        "(Beta)" in name
        or "(Proto)" in name
        or "(Possible Proto)" in name
        or "(Sample)" in name
        or bool(re.search(r"\(Beta [0-9]+", name))
        or bool(re.search(r"\(Proto [0-9]+", name))
    ):
        return "_BetaProto"
    if letter in alphabet:
        return letter
    else:
        return "#"

def checkRomDestination(rompath, setname, splitted, todelete):
    if splitted:
        for letter in alphabet:
            zipfile = rompath + "/" + setname + "_" + letter + ".zip"
            # Open Zip
            if os.path.isfile(zipfile):
                # Get file list
                zip = ZipFile(zipfile, "r")
                romlist = zip.namelist()
                zip.close()
                # loop
                for rom in romlist:
                    dest = destinationLetter(rom)
                    if dest != letter:
                        print(" "+ rom + " in " + letter + " instead of " + dest )
                        if not zipfile in todelete:
                            todelete[zipfile] = []
                        if not rom in todelete[zipfile]:
                            todelete[zipfile].append(re.escape(rom))
                        # Read 
                        zip = ZipFile(zipfile, "r")
                        tmpfile = zip.read(rom)
                        zip.close()
                        # put in correct file
                        destzipfile = rompath + "/" + setname + "_" + dest + ".zip"
                        createZip(destzipfile)
                        with ZipFile(destzipfile, "r") as checkzip:
                            if rom not in checkzip.namelist():
                                with ZipFile(destzipfile, "a") as newzip:
                                    try :
                                        newzip.writestr(rom, tmpfile)
                                    except ValueError as e:
                                        print("  duplicate in "+ destzipfile)
                                    newzip.close()
                            checkzip.close()
    return todelete

def deleteFromZip(list):
    for zipfile in list:
        if os.path.splitext(zipfile)[1] == '.zip':
            print("Cleaning: "+zipfile)
            cmd = ["zip", "-d", zipfile] + list[zipfile]
            try:
                subprocess.run(cmd)
            except subprocess.CalledProcessError as e:
                print(e)
            with ZipFile(zipfile) as zip:
                content = zip.namelist()
                zip.close()
            if len(content) == 0:
                print("removing empty "+zipfile)
                os.remove(zipfile)

def removeExtension(list):
    tmplist = []
    for item in list:
        tmplist.append(os.path.splitext(item)[0])
    return tmplist


def writeList(rompath, list, filename):
    """Write list to disk"""
    file = open(rompath + "/" + filename, "w")
    for item in list:
        file.write(item + "\n")
    file.close()


def getMissingFiles(local, remote):
    """Get list of missing files (absent from local)"""
    remote = removeExtension(remote)
    list = []
    for local_file in local:
        if os.path.splitext(local_file)[0] in remote:
            remote.remove(os.path.splitext(local_file)[0])
    for item in remote:
        list.append(item + ".zip")
    return list

def getLeftoverFiles(local, remote, todelete):
    """Get list of leftovers (absent from remote)"""
    remote = removeExtension(remote)
    for filename in local:
        for local_file in local[filename]:
            if os.path.splitext(local_file)[0] + ".dummy" in local[filename] or local_file.endswith(".dummy") or os.path.splitext(local_file)[0] + ".keep" in local[filename] or local_file.endswith(".keep"):
                continue
            if os.path.splitext(local_file)[0] not in remote:
                if not filename in todelete:
                    todelete[filename] = []
                if not local_file in todelete[filename]:
                    todelete[filename].append(re.escape(local_file))
    return todelete

main()
