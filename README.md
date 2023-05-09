# fDet
Website application for fake-news detection using modified AlBERT AI

## virtual enviroment
```cmd
~\AppData\Local\Programs\Python\Python39\python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## install npm packages
```cmd
cd ./svelteSource
npm install
npm run build
cd ../
```

## run django
```cmd
cd ./frontend
python manage.py runserver
cd ../
```

## run fastapi
```cmd
# uvicorn api:app --reload
cd ./backend
python api.py
cd ../
```