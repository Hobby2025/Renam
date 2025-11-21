@echo off
REM Renam 실행 파일 빌드 스크립트

echo Renam 빌드 중...

pyinstaller --name="Renam" ^
  --windowed ^
  --onefile ^
  --icon="assets/icon.ico" ^
  --add-data="assets;assets" ^
  app.py

echo.
echo 빌드 완료!
echo 실행 파일 위치: dist\Renam.exe
pause
