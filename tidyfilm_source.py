#!/usr/bin/env python
from tkinter import Tk, Label, Button, Text, filedialog, StringVar
import os
import shutil
from googlesearch import search
import urllib.request as req
import urllib.parse as parse
from bs4 import BeautifulSoup

year = ["19", "20"]
remove = ["(", ")", "[", "]", "{", "}"]
video_ext = [".mkv", ".mp4", ".avi"] #allowed video formats
sub_ext = [".sub", ".srt",]
idx_ext = [".idx"]
trash_ext = [".jpg", ".jpeg", ".nfo", ".txt"] #files that end with these extentions will be deleted

def clean(name):
	for i in remove:
		name = name.replace(i, "")
	name = name.replace(".", " ")
	indices = [name.find(year) for year in year]
	try:
		first = min (index for index in indices if index > 3)
		name = name[0:first+4]
	except:
		pass
	return(name)

def imdb_name(name): #input clean name, returns original name if IMDB record not found otherwise returns movie name and year
	name += " IMDB"
	for url in search(name, tld="com", lang="en", num=1, start=0, stop=1, pause=0):
		if "imdb" not in url:
			return(name)
		else:
			html = req.urlopen(url)
			soup = BeautifulSoup(html, "html.parser")
			raw_title = soup.find("title").contents
			raw_title = raw_title [0]
			year = raw_title[(raw_title).find("(")+1:raw_title.find(")")]
			title = raw_title[0:raw_title.find("(")]
			title = title.replace(":", "") #colons can't be in folder name
			return(title + "(" + year + ")")

def rehome_stray_video(directory): #finds videos not in folders and puts them in a folder in same directory with cleaned name
	for file in os.listdir(directory):
		if file.endswith(tuple(video_ext)):
			path = os.path.join(directory, file)
			clean_name = clean(file)
			new_folder = (directory + "\\" + clean_name)
			os.mkdir(new_folder)
			shutil.move(path, new_folder)

def simplify_folders_rename(dir): #works but a bit complicated
	for folder in os.listdir(dir):
		new_folder = imdb_name(clean(folder))
		old_folder = os.path.join(dir, folder)
		new_folder = os.path.join(dir, new_folder)
		try:
			os.rename(old_folder, new_folder)
		except:
			pass
		for root, subdirs, files in os.walk(dir + "\\" + folder):
			for file in files:
				path = os.path.join(root, file)
				try:
					shutil.move(path, new_folder) #trys to rename folder
				except:
					pass
				try:
					os.rmdir(root) #trys to delete any empty folders it finds
				except:
					pass

def remove_trash(dir): #deletes trash files from all folders in directory
	for folder in os.listdir(dir):
		video_files = []
		sub_files = []
		idx_files = []
		for file in os.listdir(dir + "\\" + folder):
			file_name = os.path.join(dir, folder, file)
			if file.endswith(tuple(trash_ext)): #removes nfo, readme, txt, pictures
				os.remove(file_name)
			elif file.endswith(tuple(video_ext)):
				video_files.append([file_name, os.path.getsize(file_name)])
			elif file.endswith(tuple(sub_ext)):
				sub_files.append(file_name)
			elif file.endswith(tuple(idx_ext)):
				idx_files.append(file_name)
		if len(video_files) > 1: #removes small sample videos that may be in main folder
			video_files = sorted(video_files, key = lambda size: size[1], reverse = True)
			for i in (video_files[1:]):
				os.remove(i[0])
		old_video_name = os.path.join(dir, folder, video_files[0][0])
		new_video_name = os.path.join(dir, folder, folder + "." +(video_files[0][0]).rsplit(".")[-1])
		os.rename(old_video_name, new_video_name)
		if len(idx_files) and len(sub_files) == 1:
			os.rename(idx_files[0], os.path.join(dir, folder, folder + ".idx"))
			os.rename(sub_files[0], os.path.join(dir, folder, folder + "." + (sub_files[0]).rsplit(".")[-1]))
		if len(sub_files) == 1 and len(idx_files) == 0:
			os.rename(sub_files[0], os.path.join(dir, folder, folder + "." + (sub_files[0]).rsplit(".")[-1]))

def move(dir1, dir2):
    for folder in os.listdir(dir1):
        for root, subdirs, files in os.walk(dir1 + "\\" + folder):
            path = os.path.join(root)
            dest = os.path.join(dir2)
            shutil.move(path, dir2)

def clean_move(dir1, dir2):
	rehome_stray_video(dir1)
	simplify_folders_rename(dir1)
	remove_trash(dir1)
	move(dir1, dir2)

def main():
	def input_dir():
		global input_path
		input_path = str(filedialog.askdirectory())
		input_dialog.set('Movie files are in: ' + input_path)
	def output_dir():
		global output_path
		output_path = str(filedialog.askdirectory())
		output_dialog.set('Movie files will be moved to: ' + output_path)
	frame = Tk()
	frame.geometry('300x150')
	frame.title('TidyFilm')
	input_button = Button(frame, text='Select Input Directory', command=input_dir).pack()
	output_button = Button(frame, text='Select Output Directory', command=output_dir).pack()
	clean_button = Button(frame, text='Clean', command=lambda: clean_move(input_path, output_path)).pack()
	input_dialog = StringVar()
	output_dialog = StringVar()
	input_label = Label(master=frame, textvariable=input_dialog).pack()
	output_label = Label(master=frame, textvariable=output_dialog).pack()
	frame.mainloop()

main()
