# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 18:38:23 2020

@author: Kshitij
"""

import tkinter as tk
from tkinter import ttk
from tkinter import font,colorchooser,filedialog,messagebox
import os,subprocess, json, string
import io

root=tk.Tk()
root.geometry("800x680")
TITLE="KDtor"
root.title(TITLE)
#root.attributes("-fullscreen",True)
def cut():
    text_editor.event_generate(("<<Cut>>"))
    
def copy():
    text_editor.event_generate(("<<Copy>>"))
    
def paste():
    text_editor.event_generate(("<<Paste>>"))
    
def bgcolor():#to change background color
    global text_editor
    coloring=colorchooser.askcolor()
    text_editor.config(bg=coloring[1])
    
def fgcolor():#to change foreground color
    global text_editor
    fcoloring=colorchooser.askcolor()
    text_editor.config(fg=fcoloring[1])
    
    
main_menu=tk.Menu()



#file menu

file_path=None

def save_if_modified(event=None):
        if text_editor.edit_modified(): #modified
            response = messagebox.askyesnocancel("Save?", "This document has been modified. Do you want to save changes?") #yes = True, no = False, cancel = None
            if response: #yes/save
                result =file_save()
                if result == "saved": #saved
                    return True
                else: #save cancelled
                    return None
            else:
                return response #None = cancel/abort, False = no/discard
        else: #not modified
            return True
    
def file_new(event=None):
    global file_path
    result = save_if_modified()
    if result != None: #None => Aborted or Save cancelled, False => Discarded, True = Saved or Not modified
        text_editor.delete(1.0, "end")
        text_editor.edit_modified(False)
        text_editor.edit_reset()
        file_path = None
        set_title()
            

def file_open(event=None, filepath=None):
    global file_path
    result = save_if_modified()
    if result != None: #None => Aborted or Save cancelled, False => Discarded, True = Saved or Not modified
        if filepath == None:
            filepath = filedialog.askopenfilename()
        if filepath != None  and filepath != '':
            with open(filepath, encoding="utf-8") as f:
                fileContents = f.read()# Get all the text from file.           
            # Set current text to file contents
            text_editor.delete(1.0, "end")
            text_editor.insert(1.0, fileContents)
            text_editor.edit_modified(False)
            file_path = filepath
            set_title()

def file_save(event=None):
    if file_path == None:
        result = file_save_as()
    else:
        result = file_save_as(filepath=file_path)
    return result

def file_save_as( event=None, filepath=None):
    global file_path
    if filepath == None:
        filepath = filedialog.asksaveasfilename(filetypes=(('Text files', '*.txt'), ('Python files', '*.py *.pyw'), ('All files', '*.*'))) #defaultextension='.txt'
    try:
        with open(filepath, 'wb') as f:
            text = text_editor.get(1.0, "end-1c")
            f.write(bytes(text, 'UTF-8'))
            text_editor.edit_modified(False)
            file_path = filepath
            set_title()
            return "saved"
    except FileNotFoundError:
        print('FileNotFoundError')
        return "cancelled"

def file_quit(event=None):
    result = save_if_modified()
    if result != None: #None => Aborted or Save cancelled, False => Discarded, True = Saved or Not modified
        root.destroy() #sys.exit(0)

def set_title(event=None):
    global file_path
    if file_path != None:
        title = os.path.basename(file_path)
    else:
        title = "Untitled"
    root.title(title + " - " + TITLE)
        
def undo(event=None):
    text_editor.edit_undo()
        
def redo(event=None):
    text_editor.edit_redo()
    
def run_file(event=None):
        subprocess.run(['python',file_path])
        with io.open('a.bat','w') as f:
              f.write('python ')
              f.write(os.path.basename(file_path))


new_icon=tk.PhotoImage(file="F:\python again\editor_pics/new.png")
open_icon=tk.PhotoImage(file="F:\python again\editor_pics/open.png")
save_icon=tk.PhotoImage(file="F:\python again\editor_pics/save.png")
save_as_icon=tk.PhotoImage(file="F:\python again\editor_pics/save_as.png")
exit_icon=tk.PhotoImage(file="F:\python again\editor_pics/exit.png")

file=tk.Menu(main_menu,tearoff=False)

#Edit menu

copy_icon=tk.PhotoImage(file="F:\python again\editor_pics/copy.png")
cut_icon=tk.PhotoImage(file="F:\python again\editor_pics/cut.png")
paste_icon=tk.PhotoImage(file="F:\python again\editor_pics/paste.png")
clear_icon=tk.PhotoImage(file="F:\python again\editor_pics/clear.png")
font_icon=tk.PhotoImage(file="F:\python again\editor_pics/font.png")

edit=tk.Menu(main_menu,tearoff=False)

#Color Menu

background_icon=tk.PhotoImage(file="F:\python again\editor_pics/background.png")
foreground_icon=tk.PhotoImage(file="F:\python again\editor_pics/foreground.png")

color=tk.Menu(main_menu,tearoff=False)

#Execute Menu

execute_icon=tk.PhotoImage(file="F:\python again\editor_pics/execute.png")

execute=tk.Menu(main_menu,tearoff=False)

main_menu.add_cascade(label="File",menu=file)
main_menu.add_cascade(label="Edit",menu=edit)
main_menu.add_cascade(label="Color",menu=color)
main_menu.add_cascade(label="Execute",menu=execute)

#Tool Bar

tool_bar_label=ttk.Label(root)
tool_bar_label.pack(side=tk.TOP,fill=tk.X)

font_tuple=tk.font.families()
font_family=tk.StringVar()
font_box=ttk.Combobox(tool_bar_label,width=30,textvariable=font_family,state="readonly")
font_box["values"]=font_tuple
font_box.current(font_tuple.index("Arial"))
font_box.grid(row=0,column=0,padx=5,pady=4)

size_variable=tk.IntVar()
font_size=ttk.Combobox(tool_bar_label,width=20,textvariable=size_variable,state="readonly")
font_size["values"]=tuple(range(8,100,2))
font_size.current(4)
font_size.grid(row=0,column=1,padx=5,pady=4)

bold_icon=tk.PhotoImage(file="F:\python again\editor_pics/bold.png")
bold_btn=ttk.Button(tool_bar_label,image=bold_icon)
bold_btn.grid(row=0,column=2,padx=5)

italic_icon=tk.PhotoImage(file="F:\python again\editor_pics/italic.png")
italic_btn=ttk.Button(tool_bar_label,image=italic_icon)
italic_btn.grid(row=0,column=3,padx=5)

underline_icon=tk.PhotoImage(file="F:\python again\editor_pics/underline.png")
underline_btn=ttk.Button(tool_bar_label,image=underline_icon)
underline_btn.grid(row=0,column=4,padx=5)

align_left_icon=tk.PhotoImage(file="F:\python again\editor_pics/left.png")
align_left_btn=ttk.Button(tool_bar_label,image=align_left_icon)
align_left_btn.grid(row=0,column=5,padx=5)

align_center_icon=tk.PhotoImage(file="F:\python again\editor_pics/center.png")
align_center_btn=ttk.Button(tool_bar_label,image=align_center_icon)
align_center_btn.grid(row=0,column=6,padx=5)

align_right_icon=tk.PhotoImage(file="F:\python again\editor_pics/right.png")
align_right_btn=ttk.Button(tool_bar_label,image=align_right_icon)
align_right_btn.grid(row=0,column=7,padx=5)

#Execute

execute.add_command(label="Run File",underline=0,image=execute_icon,compound="left",accelerator="Ctrl+rf",command=run_file)

#color

color.add_command(label="Background Color",underline=0,image=background_icon,compound="left",command=bgcolor)
color.add_command(label="Foreground Color",underline=0,image=foreground_icon,compound="left",command=fgcolor)

#Edit

edit.add_command(label="Copy",underline=0,image=copy_icon,compound="left",accelerator="Ctrl+C",command=copy)
edit.add_command(label="Cut",underline=0,image=cut_icon,compound="left",accelerator="Ctrl+X",command=cut)
edit.add_command(label="Paste",underline=0,image=paste_icon,compound="left",accelerator="Ctrl+V",command=paste)
edit.add_command(label="Clear-All",underline=0,image=clear_icon,compound="left",command=lambda:text_editor.delete(1.0,tk.END))
edit.add_separator()
#edit.add_command(label="Find",underline=0,image=font_icon,compound="left",accelerator="Ctrl+F",command=find_fun)

#File

file.add_command(label="New",underline=0,image=new_icon,compound="left",accelerator="Ctrl+N",command=file_new)
file.add_command(label="Open",underline=0,image=open_icon,compound="left",accelerator="Ctrl+O",command=file_open)
file.add_command(label="Save",underline=0,image=save_icon,compound="left",accelerator="Ctrl+S",command=file_save)
file.add_command(label="Save as",underline=0,image=save_as_icon,compound="left",accelerator="Ctrl+Alt+S",command=file_save_as)
file.add_separator()
file.add_command(label="Exit",underline=0,image=exit_icon,compound="left",accelerator="Ctrl+E",command=file_quit)

#Text Editor

text_editor=tk.Text(root)
text_editor.config(wrap="word",relief=tk.FLAT)
scroll_bar=tk.Scrollbar(root)
text_editor.focus_set()
scroll_bar.pack(side="right",fill=tk.Y)
text_editor.pack(fill=tk.BOTH,expand=True)
scroll_bar.config(command=text_editor.yview)
text_editor.config(yscrollcommand= scroll_bar.set)

#status bar

status_bar=ttk.Label(root,text="Status Bar")
status_bar.pack(side=tk.BOTTOM)

text_change=False

def change_word(event=None):#function to calculate no of characters and words
    global text_change
    if text_editor.edit_modified():
        text_change=True
        word=len(text_editor.get(1.0,"end-1c").split())
        character= len(text_editor.get(1.0,"end-1c").replace(" ",""))
        status_bar.config(text=f"character :{character} word :{word}")
    text_editor.edit_modified(False)
text_editor.bind("<<Modified>>",change_word)

#font and font size

font_now="Arial"
font_size_now=16

def change_font(root):
    global font_now
    font_now=font_family.get()
    text_editor.configure(font=(font_now,font_size_now))

def change_size(root):
    global font_size_now
    font_size_now=size_variable.get()
    text_editor.configure(font=(font_now,font_size_now))

font_box.bind("<<ComboboxSelected>>",change_font)
font_size.bind("<<ComboboxSelected>>",change_size)

#bold function

def bold_fun():
    text_get=tk.font.Font(font=text_editor["font"])
    if text_get.actual()["weight"]=='normal':
        text_editor.configure(font=(font_now,font_size_now,"bold"))
    
    if text_get.actual()["weight"]=='bold':
        text_editor.configure(font=(font_now,font_size_now,"normal"))

bold_btn.configure(command=bold_fun)

#italic function

def italic_fun():
    text_get=tk.font.Font(font=text_editor["font"])
    if text_get.actual()["slant"]=='roman':
        text_editor.configure(font=(font_now,font_size_now,"italic"))
    
    if text_get.actual()["slant"]=='italic':
        text_editor.configure(font=(font_now,font_size_now,"roman"))
italic_btn.configure(command=italic_fun)

#underline function

def underline_fun():
    text_get=tk.font.Font(font=text_editor["font"])
    if text_get.actual()["underline"]==0:
        text_editor.configure(font=(font_now,font_size_now,"underline"))
    
    if text_get.actual()["underline"]==1:
        text_editor.configure(font=(font_now,font_size_now,"normal"))
underline_btn.configure(command=underline_fun)

#left align

def align_left():
    text_get_all=text_editor.get(1.0,"end")
    text_editor.tag_config("left",justify=tk.LEFT)
    text_editor.delete(1.0,tk.END)
    text_editor.insert(tk.INSERT,text_get_all,"left")
    
align_left_btn.configure(command=align_left)

#center align

def align_center():
    text_get_all=text_editor.get(1.0,"end")
    text_editor.tag_config("center",justify=tk.CENTER)
    text_editor.delete(1.0,tk.END)
    text_editor.insert(tk.INSERT,text_get_all,"center")
    
align_center_btn.configure(command=align_center)

#right align

def align_right():
    text_get_all=text_editor.get(1.0,"end")
    text_editor.tag_config("right",justify=tk.RIGHT)
    text_editor.delete(1.0,tk.END)
    text_editor.insert(tk.INSERT,text_get_all,"right")
    
align_right_btn.configure(command=align_right)

#find function

def find_fun(event=None):
    
    def find():
        word=find_input.get()
        text_editor.tag_remove("match","1.0",tk.END)
        matches=0
        if word:
            start_pos="1.0"
            while True:
                start_pos=text_editor.search(word,start_pos,stopindex=tk.END)
                if not start_pos:
                    break
                end_pos=f"{start_pos}+{len(word)}c"
                text_editor.tag_add("match", start_pos, end_pos)
                matches+=1
                start_pos=end_pos
                text_editor.tag_config('match',foreground="red",background="blue")
                
    def replace():
        word=find_input.get()
        replace_text=replace_input.get()
        content=text_editor.get(1.0,tk.END)
        new_content=content.replace(word,replace_text)
        text_editor.delete(1.0,tk.END)
        text_editor.insert(1.0,new_content)
        
    
    find_popup=tk.Toplevel()
    find_popup.geometry("450x200")
    find_popup.title("Find Word")
    find_popup.resizable(0,0)
    
    # frame for find
    find_frame=ttk.LabelFrame(find_popup,text="Find and Replace Word")
    find_frame.pack(pady=20)
    
    #label
    text_find=ttk.Label(find_frame,text="Find")
    text_replace=ttk.Label(find_frame,text="Replace")
    
    #entry box
    find_input=ttk.Entry(find_frame,width=30)
    replace_input=ttk.Entry(find_frame,width=30)
    
    #button
    find_button=ttk.Button(find_frame,text="Find",command=find)
    replace_button=ttk.Button(find_frame,text="Replace",command=replace)
    
    #text label grid
    text_find.grid(row=0,column=0,padx=4,pady=4)
    text_replace.grid(row=1,column=0,padx=4,pady=4)
    
    #entry box grid
    find_input.grid(row=0,column=1,padx=4,pady=4)
    replace_input.grid(row=1,column=1,padx=4,pady=4)
    
    #button grid
    find_button.grid(row=2,column=0,padx=4,pady=4)
    replace_button.grid(row=2,column=1,padx=4,pady=4)
    
edit.add_command(label="Find",underline=0,image=font_icon,compound="left",accelerator="Ctrl+F",command=find_fun)

#Making shortcuts

text_editor.bind("<Control-n>", file_new)
text_editor.bind("<Control-N>", file_new)
text_editor.bind("<Control-o>", file_open)
text_editor.bind("<Control-O>", file_open)
text_editor.bind("<Control-S>", file_save)
text_editor.bind("<Control-s>", file_save)
text_editor.bind("<Control-F>", find_fun)
text_editor.bind("<Control-f>", find_fun)
text_editor.bind("<Control-y>", redo)
text_editor.bind("<Control-Y>", redo)
text_editor.bind("<Control-Z>", undo)
text_editor.bind("<Control-z>", undo)
text_editor.bind("<Control-X>", cut)
text_editor.bind("<Control-x>", cut)
text_editor.bind("<Control-C>", copy)
text_editor.bind("<Control-c>", copy)
text_editor.bind("<Control-V>", paste)
text_editor.bind("<Control-v>", paste)


root.config(menu=main_menu)
root.mainloop()