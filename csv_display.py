#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 13:40:43 2019

@author: amogh
"""

from tkinter import *
import tkinter.ttk as ttk
import csv
import subprocess
import time

from button_clicker import *

#run_program()

root = Tk()
root.title("CPM")
 
width = 1000
height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)


TableMargin = Frame(root, width=500)
TableMargin.pack(side=TOP)
scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
tree = ttk.Treeview(TableMargin, columns=("SL","Activity", "Predecessors", "Duration","Event_Start","Event_End","ES","EF","LS","LF","TF"), height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.heading('SL', text="SL", anchor=W)
tree.heading('Activity', text="Activity", anchor=W)
tree.heading('Predecessors', text="Predecessors", anchor=W)
tree.heading('Duration', text="Duration", anchor=W)
tree.heading('Event_Start', text="Event_Start", anchor=W)
tree.heading('Event_End', text="Event_End", anchor=W)
tree.heading('ES', text="ES", anchor=W)
tree.heading('EF', text="EF", anchor=W)
tree.heading('LS', text="LS", anchor=W)
tree.heading('LF', text="LF", anchor=W)
tree.heading('TF', text="TF", anchor=W)

tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=30)
tree.column('#2', stretch=NO, minwidth=0, width=50)
tree.column('#3', stretch=NO, minwidth=0, width=100)
tree.column('#4', stretch=NO, minwidth=0, width=100)
tree.column('#5', stretch=NO, minwidth=0, width=100)
tree.column('#6', stretch=NO, minwidth=0, width=100)
tree.column('#7', stretch=NO, minwidth=0, width=50)
tree.column('#8', stretch=NO, minwidth=0, width=50)
tree.column('#9', stretch=NO, minwidth=0, width=50)
tree.column('#10', stretch=NO, minwidth=0, width=50)

tree.pack()

with open('result.csv') as f:
    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
        SL = row['']
        Activity = row['Activity']
        Predecessors = row['Predecessors']
        Duration = row['Duration']
        Event_Start = row['Event_Start']
        Event_End = row['Event_End']
        ES = row['ES']
        EF = row['EF']
        LS = row['LS']
        LF = row['LF']
        TF = row['TF']
        tree.insert("",'end', values=(SL,Activity, Predecessors, Duration,Event_Start,Event_End,ES,EF,LS,LF,TF))
        

if __name__ == '__main__':
    
    root.mainloop()
