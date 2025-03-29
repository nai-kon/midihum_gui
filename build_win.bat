@echo off

rem build exe
uv run pyinstaller build_win.spec -y

rem copy files
xcopy /i /y "LICENSE" ".\dist\midihum_gui\"
xcopy /s /i /y "model_cache\" ".\dist\midihum_gui\model_cache\"