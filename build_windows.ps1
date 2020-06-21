mkdir .\dist
$sourceRoot = ".\man"
$destinationRoot = ".\dist"
Copy-Item -Path $sourceRoot -Recurse -Destination $destinationRoot -Container
$sourceRoot = ".\icon.png"
Copy-Item -Path $sourceRoot -Recurse -Destination $destinationRoot -Container

python -O -m PyInstaller .\main.py --onefile --name=Integrate -w