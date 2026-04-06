@echo off
echo INICIANDO DASHBOARD BB...
set "STREAMLIT_EXE=%LOCALAPPDATA%\Programs\Python\Python312\Scripts\streamlit.exe"

if exist "%STREAMLIT_EXE%" (
	"%STREAMLIT_EXE%" run app.py
) else (
	echo Caminho direto nao encontrado: %STREAMLIT_EXE%
	echo Tentando comando streamlit no PATH...
	where streamlit >nul 2>nul
	if %ERRORLEVEL%==0 (
		streamlit run app.py
	) else (
		echo ERRO: Streamlit nao encontrado.
		echo Instale com: pip install streamlit
	)
)

pause
