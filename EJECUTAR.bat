@echo off
setlocal
chcp 65001 >nul
set PYTHONUTF8=1
cd /d "%~dp0"
title Proyecto RAG SI3003

echo ============================================================
echo  Proyecto RAG - Reglamento EAFIT   [instalar y ejecutar todo]
echo ============================================================
echo.

set PY=
py -3 --version >nul 2>nul && set PY=py -3
if not defined PY python --version >nul 2>nul && set PY=python
if defined PY goto :venv
echo No encontre Python. Intentando instalarlo con winget...
winget install -e --id Python.Python.3.12 --accept-source-agreements --accept-package-agreements
echo.
echo Cuando termine la instalacion, CIERRA esta ventana y abre EJECUTAR.bat otra vez.
echo Si winget fallo, instala Python desde https://www.python.org/downloads/ marcando "Add to PATH".
pause
exit /b 1

:venv
echo [1/6] Entorno virtual...
if not exist .venv\Scripts\python.exe %PY% -m venv .venv
if not exist .venv\Scripts\python.exe goto :error
set VPY=.venv\Scripts\python.exe

echo [2/6] Instalando librerias, puede tardar unos minutos...
%VPY% -m pip install -q --disable-pip-version-check pypdf numpy openai python-dotenv
if errorlevel 1 goto :error
%VPY% -m pip install -q --disable-pip-version-check faiss-cpu
if errorlevel 1 echo AVISO: no se pudo instalar FAISS; se usara busqueda con NumPy.

:key
echo [3/6] Clave de NVIDIA...
if exist .env goto :checkkey
echo.
echo  Necesitas una clave gratuita de NVIDIA. Se abre build.nvidia.com en el navegador:
echo    1. Inicia sesion o crea la cuenta.
echo    2. Entra a cualquier modelo y pulsa "Get API Key".
echo    3. Copia la clave que empieza por nvapi-
echo.
start "" https://build.nvidia.com/
set NVKEY=
set /p NVKEY=Pega aqui la clave y presiona Enter: 
if not defined NVKEY goto :key
>.env echo NVIDIA_API_KEY=%NVKEY%

:checkkey
echo  Verificando la clave y buscando modelos disponibles...
%VPY% nim.py
if errorlevel 2 goto :badkey
if errorlevel 1 goto :error
goto :docs

:badkey
echo.
echo La clave no es valida. Vuelve a copiarla completa desde build.nvidia.com.
del .env
goto :key

:docs
echo [4/6] Verificando los documentos...
%VPY% download_docs.py
if errorlevel 1 goto :error

echo [5/6] Creando el indice...
%VPY% ingest.py
if errorlevel 1 goto :error

echo [6/6] Ejecutando los casos de prueba...
%VPY% run_eval.py
if errorlevel 1 goto :error

echo.
echo ============================================================
echo  LISTO. Se genero resultados.md en esta carpeta.
echo  Vuelve al chat con Claude y escribe:  listo
echo ============================================================
pause
exit /b 0

:error
echo.
echo ************************************************************
echo  ALGO FALLO. Copia el texto de esta ventana y pegalo en el chat.
echo ************************************************************
pause
exit /b 1
