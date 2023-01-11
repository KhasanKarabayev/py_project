# Для python проектов 

Demo вариант можно посмотреть:
```
https://cooking.distro.uz/
```
* django_1 - Сайт для кулинарных рецептов
  * Авторизация и Регистрация 
  * Добавление статьи  
  * Комментарии к статьям 
  * Рекомендательная система
  * Профайл пользователя 
  * API  - https://cooking.distro.uz/posts/api/
  * Swagger - https://cooking.distro.uz/swagger-ui/
  


* django_2 - Интернет магазин 
   * celely
   ```
   celery -A conf worker -l info -P gevent   # Для фоновых задач
   celery -A conf beat -l info               # Для задач по расписанию
   ```
