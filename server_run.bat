@echo
pip install -r requirements.txt
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

REM Installation of NPM packages
cd /d "svelteSource"
start cmd.exe /c "npm install", "npm run build"
cd /d ".."

cd /d "frontend"
start cmd.exe /k "python manage.py runserver"
cd /d ".."

REM FAST API start command
cd /d "backend"
::uvicorn main:app --host 127.0.0.1 --port 8002 
start cmd.exe /k "python api.py"
cd /d ".."
cmd /k