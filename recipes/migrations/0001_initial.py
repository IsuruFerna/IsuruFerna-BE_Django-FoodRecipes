# Generated by Django 5.0.7 on 2024-07-13 15:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('idCategory', models.AutoField(primary_key=True, serialize=False)),
                ('strCategory', models.CharField(max_length=64)),
                ('strCategoryTumb', models.URLField()),
                ('strCategoryDescription', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('idMeal', models.AutoField(primary_key=True, serialize=False)),
                ('strMeal', models.CharField(max_length=200)),
                ('strDrinkAlternate', models.CharField(blank=True, max_length=64, null=True)),
                ('strArea', models.CharField(blank=True, max_length=64)),
                ('strInstructions', models.TextField(max_length=2000)),
                ('strMealThumb', models.URLField(blank=True)),
                ('strYoutube', models.URLField(blank=True)),
                ('strIngredient1', models.CharField(blank=True, max_length=64)),
                ('strIngredient2', models.CharField(blank=True, max_length=64)),
                ('strIngredient3', models.CharField(blank=True, max_length=64)),
                ('strIngredient4', models.CharField(blank=True, max_length=64)),
                ('strIngredient5', models.CharField(blank=True, max_length=64)),
                ('strIngredient6', models.CharField(blank=True, max_length=64)),
                ('strIngredient7', models.CharField(blank=True, max_length=64)),
                ('strIngredient8', models.CharField(blank=True, max_length=64)),
                ('strIngredient9', models.CharField(blank=True, max_length=64)),
                ('strIngredient10', models.CharField(blank=True, max_length=64)),
                ('strIngredient11', models.CharField(blank=True, max_length=64)),
                ('strIngredient12', models.CharField(blank=True, max_length=64)),
                ('strIngredient13', models.CharField(blank=True, max_length=64)),
                ('strIngredient14', models.CharField(blank=True, max_length=64)),
                ('strIngredient15', models.CharField(blank=True, max_length=64)),
                ('strIngredient16', models.CharField(blank=True, max_length=64)),
                ('strIngredient17', models.CharField(blank=True, max_length=64)),
                ('strIngredient18', models.CharField(blank=True, max_length=64)),
                ('strIngredient19', models.CharField(blank=True, max_length=64)),
                ('strIngredient20', models.CharField(blank=True, max_length=64)),
                ('strMeasure1', models.CharField(blank=True, max_length=15)),
                ('strMeasure2', models.CharField(blank=True, max_length=15)),
                ('strMeasure3', models.CharField(blank=True, max_length=15)),
                ('strMeasure4', models.CharField(blank=True, max_length=15)),
                ('strMeasure5', models.CharField(blank=True, max_length=15)),
                ('strMeasure6', models.CharField(blank=True, max_length=15)),
                ('strMeasure7', models.CharField(blank=True, max_length=15)),
                ('strMeasure8', models.CharField(blank=True, max_length=15)),
                ('strMeasure9', models.CharField(blank=True, max_length=15)),
                ('strMeasure10', models.CharField(blank=True, max_length=15)),
                ('strMeasure11', models.CharField(blank=True, max_length=15)),
                ('strMeasure12', models.CharField(blank=True, max_length=15)),
                ('strMeasure13', models.CharField(blank=True, max_length=15)),
                ('strMeasure14', models.CharField(blank=True, max_length=15)),
                ('strMeasure15', models.CharField(blank=True, max_length=15)),
                ('strMeasure16', models.CharField(blank=True, max_length=15)),
                ('strMeasure17', models.CharField(blank=True, max_length=15)),
                ('strMeasure18', models.CharField(blank=True, max_length=15)),
                ('strMeasure19', models.CharField(blank=True, max_length=15)),
                ('strMeasure20', models.CharField(blank=True, max_length=15)),
                ('strSource', models.URLField(blank=True)),
                ('strImageSource', models.URLField(blank=True)),
                ('strCreativeCommonsConfirmed', models.BooleanField(blank=True)),
                ('dateModified', models.DateTimeField(blank=True)),
                ('strCategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.category')),
                ('strTags', models.ManyToManyField(blank=True, related_name='categories', to='recipes.category')),
            ],
        ),
    ]
