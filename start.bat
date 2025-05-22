@echo off
setlocal

::  1. 使用するPythonのパスを指定（例：C:\Python311\python.exe）
set PYTHON_EXE=

::  2. 仮想環境の名前（任意）
set VENV_DIR=.venv

echo [1] 仮想環境を作成中...
%PYTHON_EXE% -m venv %VENV_DIR%

echo [2] 仮想環境をアクティブ化...
call %VENV_DIR%\Scripts\activate.bat

echo [3] pip をアップグレード...
python -m pip install --upgrade pip

echo [4] requirements.txt を使って依存関係をインストール...
python -m pip install -r requirements.txt

echo [5] マイグレーションを実行...
python manage.py migrate

echo [6] 起動します（http://127.0.0.1:9200）...
python manage.py runserver 9200

endlocal
pause
