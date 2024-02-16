import ftplib
import glob
import tempfile
import os

from html.parser import HTMLParser
from html.entities import name2codepoint
from zipfile import ZipFile

import urllib.request


class MyHTMLParser(HTMLParser):
    lists = []
    def __init__(self):
        super().__init__()
        self.in_cell = False
        self.cell_index = -1

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.cell_index = -1
        if tag == 'td':
            self.in_cell = True
            self.cell_index += 1

    def handle_endtag(self, tag):
        if tag == 'td':
            self.in_cell = False

    def handle_data(self, data):
        if self.in_cell and self.cell_index == 0:
            value = data.strip()
            if value != 'Parent directory/':
                self.lists.append(value)

class Myrient:
    # location of myrient server
    myrient_host = "ftp.myrient.erista.me"
    myrient_http = "https://myrient.erista.me/files"

    def __init__(self):
        # Init
        self.ftp_connected = self.connectFTP()
        print("Myrient initialized")

    def createZip(self,name):
        """Create a zipfile"""
        if not os.path.isfile(name):
            with ZipFile(name, "w") as file:
                pass

    def addFileToZip(self, zipfile, content, name):
        """Add file to games archive"""
        zip = ZipFile(zipfile, "r")
        list = zip.namelist()
        zip.close()
        if name not in list:
            zip = ZipFile(zipfile, "a")
            zip.writestr(name, content)
            zip.close()

    def connectFTP(self):
        """Connect to FTP server"""
        try:
            self.ftp = ftplib.FTP(self.myrient_host, timeout=1)
            self.ftp.login()
            return True
        except ftplib.all_errors as e:
            return False

    def _ftpList(self, system):
        """List games using FTP"""
        # Connect FTP
        print("Get remote game list")
        try:
            # Change ftp directory
            self.ftp.cwd(system)
            # Get file list
            files = self.ftp.nlst()
            self.ftp.close()
        except:
            raise Exception("FTP ERROR")
        else:
            return files

    def _httpList(self, system):
        """List games using HTTP"""
        url = self.myrient_http + urllib.parse.quote(system,safe='/')
        with urllib.request.urlopen(url) as response:
            html = response.read().decode("utf8")
            parser = MyHTMLParser()
            parser.feed(html)
            return parser.lists

    def listForSystem(self, system):
        """List games"""
        if self.ftp_connected:
            try:
                files = self._ftpList(system)
                return files
            except Exception as e:
                print("ERROR Listing games " + str(e))
                exit(1)
        else: 
            try:
                files = self._httpList(system)
                return files
            except Exception as e:
                print("ERROR Listing games " + str(e))
                exit(1)

    def getRomlist(self, rompath):
        """Get list of roms"""
        files = {}
        local_files = []
        for file in glob.glob(rompath + "/*"):
            if os.path.splitext(file)[1] == ".zip":
                zip = ZipFile(file, "r")
                tmp = zip.namelist()
                zip.close()
                local_files += tmp
                files[os.path.basename(file)] = tmp
            else:
                local_files.append(os.path.basename(file))
                if '' not in files:
                    files[''] = []
                files[''].append(os.path.basename(file))
        local_files.sort()
        return local_files, files

    def _ftpGet(self, system, file):
        """Get game using ftp"""
        filename = system + file
        try:
            f = tempfile.TemporaryFile()
            ftp = self.connectFTP()
            ftp.retrbinary("RETR " + filename, f.write)
            return f
        except ftplib.all_errors as e:
            f.close()
            raise Exception("FTP ERROR: "+ str(e))
    
    def _httpGet(self, system, file):
        """Get game using http"""
        filename = urllib.parse.quote(system + '/' + file,safe='/')
        try:
            url = self.myrient_http + filename
            f = tempfile.TemporaryFile()
            with urllib.request.urlopen(url) as response:
                file = response.read()
                f.write(file)
            return f
        except Exception as e:
            f.close()
            print(url)
            raise Exception("HTTP ERROR: "+ str(e))

    def getFile(self, system, file, destination):
        """Get game"""
        if self.ftp_connected:
            try:
                f = self._ftpGet(system,file)
            except Exception as e:
                print("ERROR Getting game: "+str(e))
                exit(1)
        else:
            try:
                f = self._httpGet(system,file)
            except Exception as e:
                print("ERROR Getting game: "+str(e))
                exit(1)

        if os.path.splitext(destination)[1] == '.zip':
            # Add file to games archive
            with ZipFile(f, "r") as tmpzip:
                tmpzip_files = tmpzip.namelist()
                self.createZip(destination)
                if len(tmpzip_files) > 1:
                    tmpfile = ""
                    # Create a dummy with file name
                    self.addFileToZip(destination, tmpfile, os.path.splitext(file)[0]+".dummy")
                    for tmpzip_files_name in tmpzip_files:
                        # Add files to zip
                        tmpfile = tmpzip.read(tmpzip_files_name)
                        self.addFileToZip(destination, tmpfile, tmpzip_files_name)
                        # Create a dummy with file name
                        tmpfile = ""
                        self.addFileToZip(destination, tmpfile, os.path.splitext(tmpzip_files_name)[0]+".keep")
                else:
                    for tmpzip_files_name in tmpzip_files:
                        tmpfile = tmpzip.read(tmpzip_files_name)
                        destination_filename = os.path.splitext(file)[0] + os.path.splitext(tmpzip_files_name)[1]
                        self.addFileToZip(destination, tmpfile, destination_filename)
        else: 
             # Unzip to destination
            with ZipFile(f, "r") as tmpzip:
                tmpzip_files = tmpzip.namelist()
                if len(tmpzip_files) > 1:
                    tmpfile = ""
                    # Create a dummy with file name
                    fi = open(destination+"/"+os.path.splitext(file)[0]+".dummy", "w")
                    fi.write(tmpfile)
                    fi.close()
                    for tmpzip_files_name in tmpzip_files:
                        # Unzip to destination
                        tmpfile = tmpzip.read(tmpzip_files_name)
                        fi = open(destination+"/"+tmpzip_files_name, "wb")
                        fi.write(tmpfile)
                        fi.close()
                        # Create a dummy with file name
                        tmpfile = ""
                        fi = open(destination+"/"+os.path.splitext(tmpzip_files_name)[0]+".keep", "w")
                        fi.write(tmpfile)
                        fi.close()
                else:
                    for tmpzip_files_name in tmpzip_files:
                        tmpfile = tmpzip.read(tmpzip_files_name)
                        destination_filename = os.path.splitext(file)[0] + os.path.splitext(tmpzip_files_name)[1]
                        fi = open(destination+"/"+destination_filename, "wb")
                        fi.write(tmpfile)
                        fi.close()