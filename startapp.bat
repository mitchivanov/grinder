@echo off
echo Starting Trading Bot Application...

:: Установка переменных путей
set BACKEND_DIR=%~dp0backend
set FRONTEND_DIR=%~dp0frontend

:: Активация виртуального окружения
call %~dp0venv\Scripts\activate

:: Установка зависимостей Python
cd %BACKEND_DIR%
pip install -r requirements.txt

:: Применение миграций Django
python manage.py makemigrations django_bot
python manage.py migrate

:: Запуск Django сервера в фоновом режиме
start python manage.py runserver 0.0.0.0:8000

:: Переход в директорию фронтенда
cd %FRONTEND_DIR%

:: Установка зависимостей Node.js
call npm install

:: Запуск фронтенда
call npm start

echo Application started successfully!
pause