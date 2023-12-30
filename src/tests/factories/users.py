import factory
from django.contrib.auth import models
from factory.django import DjangoModelFactory
from faker import Faker

faker = Faker()


class User(DjangoModelFactory):
    class Meta:
        model = models.User

    username = factory.LazyAttribute(faker.user_name)
    email = factory.LazyAttribute(faker.email)
