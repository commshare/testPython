import codecs
import os
import sys
import shutil
import re
import chardet

convertfiletypes = [
  ".cpp",
  ".cc",
  ".h",
  ".hpp"
  ]

def check_need_convert(filename):
    for filetype in convertfiletypes:
        if filename.lower().endswith(filetype):
            return True
    return False

total_cnt = 0
success_cnt = 0
unkown_cnt = 0
def convert_encoding_to_utf_8(filename):
    global total_cnt,success_cnt,unkown_cnt
    # Backup the origin file.

    # convert file from the source encoding to target encoding
    content = codecs.open(filename, 'r').read()
    source_encoding = chardet.detect(content)['encoding']
    total_cnt+=1
    if source_encoding == None:
        print "??",filename
        unkown_cnt+=1
        return
    print "  ",source_encoding, filename
    targetpage = 'UTF-8-SIG'
    if source_encoding != targetpage:
        content = content.decode(source_encoding, 'ignore') #.encode(source_encoding)
        codecs.open(filename, 'w', encoding=targetpage).write(content)
        print "convert to " + targetpage
    success_cnt+=1

def convert_dir(root_dir):
    if os.path.exists(root_dir) == False:
        print "[error] dir:",root_dir,"do not exit"
        return
    print "work in",convertdir
    for root, dirs, files in os.walk(root_dir):
        for f in files:
            if check_need_convert(f):
                filename = os.path.join(root, f)
                try:
                    convert_encoding_to_utf_8(filename)
                except Exception, e:
                    print "WA",filename,e
    print "finish total:",total_cnt,"success:",success_cnt,"unkown_cnt",unkown_cnt

if __name__ == '__main__':
    convertdir = os.path.abspath('.')
    print "convertdir:" + convertdir
    convert_dir(convertdir)