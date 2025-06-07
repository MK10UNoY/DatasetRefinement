@echo off
REM Usage: add_id_to_json.bat input.json output.json

set INPUT=%1
set OUTPUT=%2

if "%INPUT%"=="" (
    echo Usage: add_id_to_json.bat input.json output.json
    exit /b 1
)

if "%OUTPUT%"=="" (
    echo Usage: add_id_to_json.bat input.json output.json
    exit /b 1
)

REM Use Python to add an 'id' field to each object
python -c "import json,sys; data=json.load(open(r'%INPUT%','r',encoding='utf-8')); [entry.update({'id': i+1}) for i,entry in enumerate(data)]; json.dump(data,open(r'%OUTPUT%','w',encoding='utf-8'),indent=2,ensure_ascii=False)" 

echo Done. Output written to %OUTPUT%