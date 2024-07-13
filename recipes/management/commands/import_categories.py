from typing import Any
from django.core.management.base import BaseCommand

import requests

from recipes.models import Category

# populate category data to DB
def populate_category_data():
    response = requests.get("https://www.themealdb.com/api/json/v1/1/categories.php")
    if response.status_code == 200:
        print("Success!")
        categories = response.json()

        if categories:
            print(len(categories['categories']))
            for category in categories['categories']:
                current_category = Category(
                    strCategory=category['strCategory'],
                    strCategoryTumb=category['strCategoryThumb'],
                    strCategoryDescription=category['strCategoryDescription']
                )

                # print("this is category :", category)

                success = current_category.save()
                if not success:
                    print(f"something went wrong at {category}")
                else:
                    print(f"Added")


class Command(BaseCommand):
    help = 'import booms'

    def add_arguments(self, parser):
        pass

    def handle(self, *args: Any, **options):
        populate_category_data()

