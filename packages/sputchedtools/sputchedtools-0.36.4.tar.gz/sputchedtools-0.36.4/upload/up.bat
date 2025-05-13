@echo off

set "origin=%CD%"
cd "%~dp0../"

:: Build Cythonized wheel
:: call devcmd
:: set CYTHONIZE=1
:: python -m build -wn
:: set CYTHONIZE=

:: Build regular wheel
python -m build -wn --no-isolation

:: Build source distribution
python -m build -sn

echo.
choice /N /M "Upload? [Y/N]: "
if %ErrorLevel% == 1 (
	twine upload dist/*
	rmdir /S /Q dist
)

for /D %%G in (".\src\*egg-info") do rmdir /S /Q "%%G"
rmdir /S /Q  build
:: del /S /Q sputchedtools.c MANIFEST.in
cd "%origin%"