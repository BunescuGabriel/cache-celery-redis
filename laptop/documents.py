from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Laptop


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
