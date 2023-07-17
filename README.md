# Foodgram, «Продуктовый помощник»

На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### Используемые технологии:
```
Python 3.11.3
Django 4.2.1
djangorestframework 3.14.0
djoser 2.2.0
requests 2.31.0
reportlab 4.0.4
PostgreSQL 15.3
gunicorn 20.1.0
nginx
Docker
```

### Для локального запуска проекта нужно:
- Клонировать репозиторий 
  ```
  git clone git@github.com:MrHyde126/foodgram.git
  ```
- Cоздать и активировать виртуальное окружение
  ```
  py -3.11 -m venv venv
  . venv/Source/activate
  ```
- Установить Docker и запустить его
- Перейти в папку infra 
  ```
  cd infra/
  ```
- Запустить контейнер с PostgreSQL
  ```
  docker compose up -d db
  ```
- Установить node.js (желательно 13 версию; если у вас более новая версия, то придется решать проблемы с зависимостями)
- Перейти в папку frontend
  ```
  cd ..
  cd frontend/
  ```
- Установить зависимости для фронтенда
  ```
  npm i
  ```
- В файле pakage.json в последней строке изменить значение "proxy" на ```"http://localhost:8000/"```
- Запустить фронтенд
  ```
  npm run start
  ```
- Перейти в папку foodgram
  ```
  cd ..
  cd backend/foodgram/
  ```
- Установить зависимости для бэкенда
  ```
  pip install -r requirements.txt
  ```
- Запустить бэкенд
  ```
  py manage.py runserver
  ```
