# ChillChair

If you wanna see on which chair you want to chill.


## How to run

1. Create .env file

```bash
cp .env.example .env
```

2. Run the project
```bash
docker compose up -d --build
```

## Swagger

You can see the swagger locally by url

```
http://localhost:39000/docs/
```

## How to create superuser 

1. cd inside of your project folder 

```bash
cd chillchair
```

2. create superuser with command

```bash
docker compose exec -it django-chillchair python manage.py createsuperuser
```

## Django admin url 

Django admin is avaliable by url 

```bash 
http://localhost:39000/secretadmin/
```