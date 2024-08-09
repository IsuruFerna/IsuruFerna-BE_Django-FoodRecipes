from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError

from drf_spectacular.utils import extend_schema

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.hashers import make_password

from .serializers import CustomUserSerializer, ModifyUserSerializer
from .models import CustomUser
from .utils import ResponseUser

# Create your views here.
@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/user/api/token',
        '/user/api/token/refresh',
        '/user/register/'
    ]
    return Response(routes)

# register user 
# /user/register/
"""
{
    "username": username,
    "first_name": firstName,
    "last_name": lastName,
    "email": email,
    "password": password,
}
"""
@extend_schema(responses=CustomUserSerializer)
@api_view(['POST'])
def user_register_view(request):
    data = request.data.copy()
    
    if 'password' in data and data['password']:
        data['password'] = make_password(data['password'])

    serializer = CustomUserSerializer(data=data)

    if serializer.is_valid():

        # handle unique username
        try:
            user = serializer.save()
            serialized_user = CustomUserSerializer(user)

        except IntegrityError:
            raise serializers.ValidationError({"username": ["This username already exists."]})

        return Response(serialized_user.data, status=status.HTTP_201_CREATED)
    
    return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# get logged user details and modify them
# /user/me/
@extend_schema(responses=ModifyUserSerializer)
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def my_view(request):
    user_data = request.user

    # get's user data
    if request.method == "GET":
        userRespone = ResponseUser(
            user_data.id, 
            user_data.username,
            user_data.first_name,
            user_data.last_name,
            user_data.email
        )

        return Response(userRespone.__dict__, status=status.HTTP_200_OK)
    
    # modifies user data
    if request.method == 'PUT':
        user_old_data = CustomUser.objects.get(pk=user_data.id)

        # set instence with new data
        serializer = ModifyUserSerializer(instance=user_old_data, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)

# get user by id
# /user/<user_id>/
@extend_schema(responses=CustomUserSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request, user_id):

    # check if there's any user with the given id
    try:
        user = CustomUser.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return Response({'error': f'user id: {user_id} does not found!'}, status=status.HTTP_404_NOT_FOUND)
    
    serialized_user = CustomUserSerializer(user)
    return Response(serialized_user.data)

def index(request):
    return Response({"message": "hello world!"})

