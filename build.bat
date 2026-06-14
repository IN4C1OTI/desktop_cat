@echo off
cd /d "%~dp0"
echo ============================================
echo  Desktop Cat v1 - BUILD STANDALONE
echo ============================================
echo.

REM Detecta Python 3.12 (necessario pois PyInstaller nao suporta 3.14 ainda)
set PY=
for %%v in (3.12) do (
    for %%p in (
        "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
        "C:\Python312\python.exe"
        "C:\Program Files\Python312\python.exe"
    ) do (
        if exist %%p set PY=%%p
    )
)

if "%PY%"=="" (
    echo AVISO: Python 3.12 nao encontrado.
    echo O PyInstaller nao suporta Python 3.14 ainda.
    echo.
    echo Baixe Python 3.12 em: https://www.python.org/downloads/release/python-3120/
    echo Marque "Add Python to PATH" durante a instalacao.
    echo Depois rode este bat novamente.
    echo.
    pause
    exit /b 1
)

echo Usando Python: %PY%
echo.

echo [1/3] Instalando dependencias no Python 3.12...
%PY% -m pip install pillow pyinstaller --quiet
if errorlevel 1 (
    echo ERRO ao instalar dependencias.
    pause
    exit /b 1
)

echo [2/3] Compilando...
%PY% -m PyInstaller ^
    --onefile ^
    --windowed ^
    --name "DesktopCat" ^
    --add-data "dist;dist" ^
    --hidden-import PIL ^
    --hidden-import PIL.Image ^
    --hidden-import PIL.ImageTk ^
    --hidden-import PIL.ImageChops ^
    desktop_cat.py

if not exist "dist\DesktopCat.exe" (
    echo.
    echo ERRO: build falhou. Veja o log acima.
    pause
    exit /b 1
)

echo [3/3] Copiando assets...
xcopy /E /I /Y "dist\memes"  "dist\memes\"  >nul 2>&1
xcopy /E /I /Y "dist\sounds" "dist\sounds\" >nul 2>&1
xcopy /E /I /Y "dist\texts"  "dist\texts\"  >nul 2>&1

echo.
echo ============================================
echo  Pronto! Executavel em: dist\DesktopCat.exe
echo  Este .exe funciona em qualquer PC Windows,
echo  sem precisar de Python instalado.
echo ============================================
pause
