# MiSTer FPGA x Myrient 
 
This script download rom files from the myrient service (https://myrient.erista.me/) and organize them in a format readable by the MiSTer FPGA. 
 
## Warning 
 
Depending on your local laws and regulation, usage of this script may be prohibited, check with a local lawyer before use. 

## Installation

Add the following to the bottom of `downloader.ini`:

```ini
[willoucom/mister_myrient]
db_url = https://raw.githubusercontent.com/willoucom/MiSTer_Myrient/db/db.json.zip
```

## Usage 

run `./myrient.py` to get a list of supported sets 
 
Then run `./myrient.py` followed by a list of sets separated by a space 
 
eg: `./myrient.py Atari2600 AtariLynx` 
 
Generate some additionnal files on each folder : 
 
    gamelist.txt contains list of present roms 
    leftovers.txt contains list of roms presents locally but not on Myrient 
 
It may take a very long time depending on your internet connexion. I recommend to run the script inside a `screen`.
