#!/bin/bash
clear
src_path="./man"
dest_path="./dist"
mkdir "$dest_path"
cp -r "$src_path" "$dest_path"
src_path="./icon.png"
cp "$src_path" "$dest_path"
pyinstaller ./main.py --onefile --name=Integrate -w