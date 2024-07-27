from django.shortcuts import render
from django.http import JsonResponse
from django.core.serializers import serialize
from django.core.paginator import Paginator
from django.db.models import Q

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

import random

from users.models import CustomUser
from recipes.models import Category, Meal
from .serializers import MealSerializer

# gets all the meals with paginator
# /recipes/?page_num=1&per_page=10
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def all_meals(request):
    meals = Meal.objects.all().order_by('strMeal')

    # sets pagination using django_rest and it's global settings from the settings.py file under REST_FRAMEWORK list
    paginator = PageNumberPagination()
    paginated_meals = paginator.paginate_queryset(meals, request)
    serialized_meals = MealSerializer(paginated_meals, many=True)

    return paginator.get_paginated_response(serialized_meals.data)


# gets random 10 meals
# /recipes/random/
@api_view(['GET'])
def random_meals(request):
    meals = Meal.objects.all()
    meals_amount = meals.count()
    random_nums = []
    random_meals = []
    
    # controls util it generates 12 unique random numbers
    while len(random_nums) < 12:
        generated_num = random.randrange(meals_amount)
        if not generated_num in random_nums:
            random_nums.append(generated_num)

            # fills random meal corresponds the generated random number
            random_meals.append(meals[generated_num])

    return JsonResponse(serialize('json', random_meals), safe=False)

# search meals by name and category
# /recipers/search/?name=meal_name&category=meal_category
def search_by(request):
    
    # required_parm_fields = ("name", "category")
    # for more improvements with large number of params
    # https://forum.djangoproject.com/t/parsing-and-validating-query-params-from-get-request/24308

    meal_name = request.GET.get('name')
    meal_category = request.GET.get('category')

    # returns param response as paginated json
    def serialized_paginator_response(data):
        page_number = int(request.GET.get('page_num', 1))
        items_per_page = int(request.GET.get('per_page', 12))

        paginator = Paginator(data, items_per_page)
        page_obj = paginator.get_page(page_number)

        serialized_data = serialize('json', page_obj)
    
        return JsonResponse({
            'data': serialized_data,
            'meta': {
                'page': page_obj.number,
                'per_page': items_per_page,
                'total_pages': paginator.num_pages,
                'total_items': paginator.count
            }
        })
    
    if meal_name and meal_category:
        # filters and gets as a list of categorise according to name similarities
        categories = Category.objects.filter(strCategory__contains=meal_category)

        # joins multiples querysets into a unique list by provided category name
        meals = []
        if categories:
            for category in categories:
                meals.extend(Meal.objects.filter(Q(strCategory__strCategory__contains=meal_category) & 
                                                 Q(strMeal__contains=meal_name)))

            return serialized_paginator_response(meals)

        # when no meal found with the provided name and category
        if not meals:
            return JsonResponse({"message": f"No meal found for corresponding name: '{meal_name}' and category: '{meal_category}'"}, status=404)
        
        return serialized_paginator_response(meals)       
    
    if meal_name:
        meals = Meal.objects.filter(strMeal__contains=meal_name).order_by('strMeal')

        # when thre are no meals to provided name
        if not meals:
            print("running inside statement")
            return JsonResponse({"message": f"No meal found for: {meal_name}"}, status=404)
        
        return serialized_paginator_response(meals)
        

    if meal_category:
        # filters and gets as a list of categorise according to name similarities
        categories = Category.objects.filter(strCategory__contains=meal_category)

        # joins multiples querysets into a unique list by provided category name
        meals = []
        if categories:
            for category in categories:
                meals.extend(Meal.objects.filter(strCategory=category))

            return serialized_paginator_response(meals)
        
        # when thre are no categories for provide category
        return JsonResponse({"message": f"No category found for: {meal_category}"}, status=404)
    
    # returns when request doesn't match with any required params
    return JsonResponse({"error": "Missing query params"}, 
            status=404
        )

# add new meal 
# /recipers/add/
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_meal(request):

    # get data as a copy and modify according to the category and logged user
    data = request.data.copy()

    user = CustomUser.objects.get(id=request.user.id)
    category = Category.objects.filter(strCategory=data['strCategory']).first()

    data["user"] = user
    data["strCategory"] = category

    # check data validity before saving
    meal_serializer = MealSerializer(data=data)
    if not meal_serializer.is_valid(): 

        return Response(meal_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # save data
    meal = Meal.objects.create(**data)
    saved_meal_serializer = MealSerializer(meal)

    return Response(saved_meal_serializer.data, status=status.HTTP_200_OK)


# edit or delete meal
# /recipes/<uuid:id>
@api_view(['DELETE', 'PATCH'])
@permission_classes([IsAuthenticated])
def meal_edit_delete(request, meal_id):

    meal = Meal.objects.get(pk=meal_id)
    meal_user = meal.user
    logged_user = request.user

    # check weather user has access to modify his own listed data
    if meal_user.id != logged_user.id:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'PATCH':
        data = request.data.copy()

        print(f"this is data: {data}")
        category = None
        custom_errors = {}

        # check if request data provided a category
        meal_category = data['strCategory']

        if meal_category:
            print(f"category is: {data['strCategory']}")
            category = Category.objects.filter(strCategory=meal_category).first()

            print(f"new catogory: {category}")
            print(f"set new category: {data['strCategory']}")

            if category is None:
                custom_errors['Category error'] = "Provided category doesn't found. Please create a new category before adding it!"

            else:    
                data['strCategory'] = category.strCategory

        meal_serializer = MealSerializer(meal, data=data)
        
        # validate data
        if not meal_serializer.is_valid():

            # update custom errors because if there is already an error in category, I don't want to loose that error from the 'custom_errors' dictionary
            custom_errors.update(meal_serializer.errors)
            return Response(custom_errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            print("data valid")
        
        meal_serializer.save()
        # update meal

        
        print(f"update meal")
        print(f"meal saved")
        print(f"modified data: {meal_serializer.data}")

        return Response({
            "message": "Meal modified successfully!",
            "data": meal_serializer.data
        }, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        print("this is patch req")
        return Response(status=status.HTTP_200_OK)


    return Response(status=status.HTTP_400_BAD_REQUEST)



