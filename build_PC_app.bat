REM rensa gamla cache/builds
pyinstaller --clean ^
  --log-level=DEBUG ^
  --onedir ^
  --console ^
  --name=musikmaskin ^
  musikmaskin.py
