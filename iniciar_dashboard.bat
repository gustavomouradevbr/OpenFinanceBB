@echo off
setlocal

REM Entra na pasta do projeto (pasta onde este .bat está)
cd /d "%~dp0"

REM Inicia diretamente pelo executavel absoluto do Streamlit
set "STREAMLIT_EXE=%LOCALAPPDATA%\Programs\Python\Python312\Scripts\streamlit.exe"
set "PORT=8501"

if not exist "%STREAMLIT_EXE%" goto fallback_python

REM Se a porta 8501 estiver em uso, usa 8502
netstat -ano | findstr /R /C:":8501 .*LISTENING" >nul
if %errorlevel%==0 set "PORT=8502"

echo Iniciando Streamlit na porta %PORT%...
"%STREAMLIT_EXE%" run app.py --server.port %PORT%
goto :eof

REM Ultimo fallback: Python local
 :fallback_python
set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if exist "%PYTHON_EXE%" (
    netstat -ano | findstr /R /C:":8501 .*LISTENING" >nul
    if %errorlevel%==0 set "PORT=8502"
    echo Iniciando Streamlit via Python na porta %PORT%...
    "%PYTHON_EXE%" -m streamlit run app.py --server.port %PORT%
    goto :eof
)

echo.
echo Nao foi possivel iniciar o dashboard.
echo Verifique se o Python 3.12 e o Streamlit estao instalados.
echo.
pause
