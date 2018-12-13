#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, codecs, sys, getopt

def convertFile(filename, sourceEncode="GBK", targetEncode="UTF-8", bak=False):
    inFile = codecs.open(filename, 'r', sourceEncode) #open(filename)
    content = inFile.read() # "".join(inFile.readlines())
    inFile.close()

    if bak:
        #bak
        if os.path.exists(filename + ".bak"):
            os.remove(filename + ".bak")
        os.rename(filename, filename + ".bak")
    #content = content.
    #print(content)
    
    outFile = codecs.open(filename, 'w', targetEncode)
    outFile.write(content)
    outFile.close()
    
    return

def convertDir(dirname, sourceEncode="GBK", targetEncode="UTF-8", bak=False):
    a = os.walk(dirname)
    print(a)
    for root, dummydirs, files in os.walk(dirname):
        for file in files:
            if file.endswith(".java") or file.endswith(".f"):
                filename = os.path.join(root, file)
                print(filename, end="\t")
                try:
                    convertFile(filename, sourceEncode, targetEncode, bak)
                    print("finish")
                except UnicodeDecodeError as e:
                    print("error:" + e.reason)

    return

def usage():
    print("""usage : %s dir [dir1 dir2 ...] [-s | --sourceEncode <sourceEncode>] [-t | --targetEncode <sourceEncode>] [-b | --bak]
    """%(os.path.basename(sys.argv[0])))

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hbs:t:", ["help", "sourceEncode=", "targetEncode=", "bak"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    
    bak = False
    paths = []
    sourceEncode = None
    targetEncode = None

    if len(opts) == 0 and len(args) == 0:
        usage()
        sys.exit(0)

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-b", "--bak"):
            bak = True
        elif o in ("-s", "--sourceEncode"):
            sourceEncode = a
        elif o in ("-t", "--targetEncode"):
            targetEncode = a
        else:
            assert False, "unhandled option"

    for arg in args:
        paths.append(arg)

    if sourceEncode is None:
        sourceEncode = "GBK"

    if targetEncode is None:
        targetEncode = "UTF-8"

    for path in paths:
        print("convert dir : " + path)
        convertDir(path, sourceEncode, targetEncode, bak)
