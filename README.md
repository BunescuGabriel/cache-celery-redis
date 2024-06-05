# Magazin
Acest proiect utilizează Django pentru a rula o aplicație web care folosește Docker, Elasticsearch pentru căutare, mai multe metode de Cache, Celery pentru task manager și Redis.

## Instrucțiuni de pornire

Pentru a rula aplicația, urmează acești pași:

### Instalare
Instalează dependințele proiectului folosind pip:
```bash
pip install -r requirements.txt
```
### Realizare migrări
Aplică migrările definite în proiectul Django pentru a actualiza structura bazei de date:
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```
### Pornirea serverului
Pentru a porni aplicația, rulează următoarea comandă:
```bash
python manage.py runserver
```

## Configurarea Caching-ului

Pentru caching, acest proiect folosește Django Cache Framework. În fișierul `settings.py`, pot fi configurate caching. Poți alege între diferite backend-uri de caching, cum ar fi `FileBasedCache`, `DatabaseCache` sau `Redis`. Asigură-te că activezi doar un singur backend pentru caching.
### DatabaseCache
Pentru a activa un backend specific, configurează secțiunea corespunzătoare din `settings.py`. De exemplu, dacă vrei să folosești caching în baza de date, asigură-te că secțiunea `DatabaseCache` este activată și rulează următoarea comandă pentru a crea tabelul de cache:

```python
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "my_cache_table",
    }
}
```
Folosind comanda se va creat tabela în baza de date:
```bash
python manage.py createcachetable
```
### FileBasedCache
Această configurație specifică că proiectul utilizează un cache de tip `FileBasedCache`, care stochează datele cache-ului într-o locație specificată pe disk, în directorul specificat de `"path/to/cache/directory"`.
```python
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "path/to/cache/directory",
    }
}
```
### Configurarea Cache-ului utilizând Redis

Pentru a utiliza `Redis` ca backend pentru cache-ul Django, un exemplu de configurare.

#### Adăugarea Aplicației `django_redis`

Pentru a utiliza funcționalitatea oferită de aplicația `django_redis` în cadrul proiectului Django, asigură-te că ai adăugat această aplicație în lista `INSTALLED_APPS` din fișierul `settings.py`.

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django_redis',
]
```
Este necesar de instalat django_redis în mediul virtual Python.
```bash
pip install django-redis
```

```python
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
    }
}
```
Această configurație specifică că proiectul utilizează `Redis` ca backend pentru cache. În acest exemplu, se utilizează o instanță `Redis locală`, care rulează la adresa `127.0.0.1` și portul `6379`.

#### Pornirea unui Server Redis în Docker

Pentru a rula un server Redis într-un container Docker, poți folosi următoarea comandă în terminal:

```bash
docker run -d -p 6379:6379 redis
```

Pentru configurații mai avansate, cum ar fi conectarea la un `server Redis` remote sau configurarea cu opțiuni suplimentare, poți utiliza o configurație similară, precum:
```python
CACHES = {
    "default": {
        'BACKEND': 'django_redis.cache.RedisCache',

        'LOCATION': 'redis://host:port/Free-db',
        
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PASSWORD': 'password',  
        }
    }
}
```
Pentru a accesa `platforma Redis Labs` și a administra bazele de date Redis, poți folosi următorul link: [https://app.redislabs.com/#/databases](https://app.redislabs.com/#/databases)

Această platformă oferă o interfață ușor de utilizat pentru gestionarea bazelor de date Redis, inclusiv posibilitatea de a crea, modifica și monitoriza baze de date, chei și multe altele.

Pentru a gestiona și vizualiza datele din baza de date `Redis`, poți utiliza aplicația Redis Insight. 

`Redis Insight` oferă o interfață prietenoasă pentru explorarea și interogarea datelor din baza de date Redis, facilitând monitorizarea cheilor și a valorilor stocate, precum și efectuarea de operații CRUD și analize complexe.


# Setările de E-mail

Pentru a configura trimiterea de e-mail-uri din aplicația Django, trebuie să adăugi următoarele setări în fișierul `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'exemplu@gmail.com'
EMAIL_HOST_PASSWORD = 'parola pentru aplicații'
```
Aceste setări specifică faptul că aplicația va utiliza serverul SMTP de la Gmail pentru a trimite e-mail-uri. Asigură-te că înlocuiești adresa de e-mail și parola cu cele reale pentru contul tău Gmail.
### Generarea de Parole de Aplicații pentru Conturile Google
Link-ul către pagina necesar: [Google App Passwords](https://myaccount.google.com/apppasswords?rapt=AEjHL4NnY5BETcFQLDGFz5s-GuhQe0eA0v6SDQDmZlBdOGYgreAulzeesSz44c6f2_vrVeRJinK6-WxEk3tcOg7Hyo6VuwgRdppUzTGh2gIbu-FeM4WDkHs)

Această pagină îți permite să generezi parole specifice aplicațiilor pentru a le utiliza în locul parolei contului tău principal Google. Această măsură este utilă pentru a îmbunătăți securitatea contului tău și pentru a limita accesul aplicațiilor la datele tale personale.

## Configurarea Elasticsearch în Docker

Pentru a rula Elasticsearch într-un container Docker, poți folosi următoarea configurare:

```yaml
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.13.0
    volumes:
      - esdata01:/usr/share/elasticsearch/data
    ports:
      - 9200:9200
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false

volumes:
  esdata01:
```
Această comandă va porni Elasticsearch într-un container Docker.
```bash
docker-compose up -d
```
Instalează pachetul
```bash
pip install django-elasticsearch-dsl  
```
Adaugă aplicația `django_elasticsearch_dsl` în lista `INSTALLED_APPS` din fișierul `settings.py` al proiectului Django:
```python
INSTALLED_APPS = [
    'django_elasticsearch_dsl',
]
```
Definește documentele Elasticsearch în fișierul `app/documents.py`:
```python
from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from laptop.models import Laptop

@registry.register_document
class LaptopDocument(Document):
    class Index:
        name = 'laptops'
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }

    class Django:
        model = Laptop
        fields = [
            'model',
            'producator',
            'procesor',
            'descriere',
        ]
```
Reconstruiește indexul de căutare folosind comanda:
```bash
python manage.py search_index --rebuild
```
## Configurarea Celery și Redis

Pentru gestionarea sarcinilor în fundal, acest proiect utilizează `Celery` în combinație cu `Redis` ca broker. 
Pașii sunt:

### Instalare

Instalează pachetul `celery` cu suport pentru Redis:
```bash
pip install celery[redis]
```
Instalează pachetul django-celery-results:
```bash
pip install django-celery-results
```
Instalează pachetul `django-celery-beat`:
    
```bash
    pip install django-celery-beat
```
Adaugă aplicațiile necesare în lista INSTALLED_APPS din fișierul settings.py:
```python
INSTALLED_APPS = [
    'django_redis',
    'django_celery_results',
    'django_celery_beat',
]
```
### Configurarea Celery
Creează un fișier `celery.py` în directorul proiectului Django `(ex. project/celery.py)` și adaugă următorul conținut:
```python
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Magazin.settings')

app = Celery('Magazin')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'get_categories_every_one_minute': {
        'task': 'laptop.tasks.send_best_email',
        'schedule': crontab(minute='*/1'),
    },
}
```
### Integrarea Celery cu Django

În fișierul `__init__.py` din directorul proiectul Django `(ex. Project/__init__.py)`, adaugă următoarele linii pentru a te asigura că `Celery` este încărcat odată cu proiectul:
```python
from __future__ import absolute_import, unicode_literals
from Magazin.celery import app as celery_app

__all__ = ('celery_app',)
```
Definirea sarcinilor (Tasks)
În fișierul `tasks.py` sau direct în fișierul în care definești logica aplicației tale, adaugă sarcinile `(tasks)` pentru `Celery`. 
Iată un exemplu de cum să trimiți e-mailuri folosind `Celery`:
```python
from Magazin.celery import app
from django.core.mail import send_mail
from laptop.models import Contact
from django.conf import settings

@app.task
def send_spam_email(email):
    send_mail(
        'Hello from Celery',
        'This is a test message from Celery',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
@app.task
def send_best_email():
    for contact in Contact.objects.all():
        send_mail(
            'Hello from Celery',
            'Hello, we will meet in a minute',
            settings.EMAIL_HOST_USER,
            [contact.email],
            fail_silently=False,
        )
```
### Pornirea Redis în Docker
Pentru a porni un container `Redis` folosind `Docker`, folosește următoarea comandă:
```bach
docker run -d -p 6379:6379 redis
```
### Configurarea în `settings.py`
Asigură-te că ai configurat corect parametrii pentru `Redis` și `Celery` în fișierul `settings.py`:

```python
# Redis settings
REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6379'
REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'

# Celery settings
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# Pentru Windows, adaugă următoarele linii:
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERYD_POOL = 'solo'
```
### Pornirea `Celery`
Pentru a porni `Celery`, folosește următoarea comandă din directorul proiectul:
```bash
celery -A Magazin worker --loglevel=info
```
Pornește Celery pentru `Windows` cu comanda:
```bash
celery -A Magazin worker --loglevel=info --pool=solo  
```

### Pornirea `Celery Beat`
Pentru a porni `Celery Beat`, folosește următoarea comandă din directorul proiectului:
```bash
celery -A Magazin beat -l INFO
```
### Configurarea Redis Labs

Pentru a utiliza platforma Redis Labs, este necesar să modifici următoarele linii în fișierul `settings.py`:

```python
REDIS_HOST = 'host'
REDIS_PORT = 'port'
REDIS_PASSWORD = 'password'

REDIS_URL = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0'
```

## Monitorizarea task-urilor Celery cu Flower

Pentru a monitoriza task-urile `Celery`, poți utiliza `Flower`. Pentru a instala și configura Flower:

Instalează Flower folosind pip:
```bash
pip install flower
```
Pornește `Flower` pentru a monitoriza task-urile `Celery`:
```bash
celery -A Magazin flower --port=5001
```

Flower va fi disponibil la adresa `http://localhost:5001` unde poți vedea detalii despre task-urile Celery, inclusiv starea acestora și alte informații relevante.
  