@echo off
call venv_win\Scripts\activate.bat
echo.
echo.===================================================================================================
echo.Starting pytest with coverage html report
echo.===================================================================================================
echo.
call python -m coverage  run --source=src --omit=src/hx711py/* -m pytest
call python -m coverage report
call python -m coverage html
echo.
echo.
echo.===================================================================================================
echo.interrogate results
echo.===================================================================================================
call python -m interrogate src tests
echo.
echo.
echo.===================================================================================================
echo.flake8 results
echo.===================================================================================================
call python -m flake8 src tests
::call venv_win\Scripts\deactivate.bat