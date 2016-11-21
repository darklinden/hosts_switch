#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'darklinden'

import subprocess
import os
import shutil
import errno
import sys

def run_cmd(cmd):
    # print("run cmd: " + " ".join(cmd))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err:
        print(err)
    return out

def self_install(file, des):
    file_path = os.path.realpath(file)

    filename = file_path

    pos = filename.rfind("/")
    if pos:
        filename = filename[pos + 1:]

    pos = filename.find(".")
    if pos:
        filename = filename[:pos]

    to_path = os.path.join(des, filename)

    print("installing [" + file_path + "] \n\tto [" + to_path + "]")
    if os.path.isfile(to_path):
        os.remove(to_path)

    shutil.copy(file_path, to_path)
    run_cmd(['chmod', 'a+x', to_path])

def dir_content(folder):
    fList = os.listdir(folder)
    dirs = []
    files = []
    for f in fList:
        fPath = os.path.join(folder, f)
        if os.path.isfile(fPath):
            files.append(f)
        elif os.path.isdir(fPath):
            dirs.append(f)

    return dirs, files

def mkdir_p(path):
    # print("mkdir_p: " + path)
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def __main__():

    home = os.path.expanduser('~')
    save_path = os.path.join(home, ".hosts_switch")
    
    des_path = "/etc/hosts"

    mkdir_p(save_path)
    print("hosts_switch:")

    # self_install
    if len(sys.argv) > 1 and sys.argv[1] == 'install':
        self_install("hosts_switch.py", "/usr/local/bin")
        return

    # list
    if len(sys.argv) > 1 and str(sys.argv[1]).lower() == "-a":
        print("\tlist saved hosts:")
        dirs, hosts_files = dir_content(save_path)
        for f in hosts_files:
            file_path = os.path.join(save_path, f)
            shutil.copymode(des_path, file_path)
            print (f)

        os.system("open " + save_path)
        print("Done")
        return

    if len(sys.argv) > 2 and str(sys.argv[1]).lower() == "-l" and len(sys.argv[2]) > 0:
        print("\tload to hosts:")
        print("\t" + sys.argv[2])
        src_path = os.path.join(save_path, sys.argv[2])
        if os.path.isfile(des_path) and os.path.isfile(src_path):
            shutil.copymode(des_path, src_path)
            os.remove(des_path)
            shutil.copy(src_path, des_path)
            print("Done")
            return

    print("python hosts_switch.py install to install")
    print("hosts_switch -a to open list of all saved hosts")
    print("hosts_switch -l [name] to load [name] hosts")

__main__()
