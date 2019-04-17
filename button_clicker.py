#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 13:36:41 2019

@author: amogh
"""

import tkinter

from tkinter import *
import subprocess

def run():
    #subprocess.run(["ls", "-l"])
    subprocess.run(["python3","cpm.py"])
    
def run_program():
    
    root = Tk()
    Button(root, text="Click to run your CPM Program", command=run).pack()
    root.mainloop()

run_program()