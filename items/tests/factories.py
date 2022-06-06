import factory
from faker import Faker
from items.models import Item, Category

fake = Faker()


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    category = 'test category'


class ItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Item

    title = fake.name()
    description = fake.text()
    price = 123
    status = 'Available'
    photo = 'https://res.cloudinary.com/dweuirck0/image/upload/v1642502378/nmvg73wekwwfhcjidt6c.jpg'
    category = factory.SubFactory(CategoryFactory)