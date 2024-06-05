from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Telefon


@registry.register_document
class TelefonDocument(Document):
    class Index:
        name = 'telefons'
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }

    class Django:
        model = Telefon
        fields = [
            'model',
            'producator',
            'procesor',
            'descriere',
        ]
