from django.shortcuts import render
from .serializers import UserSerializer,OrganisationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.serializers import ValidationError
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import viewsets
from .models import  Organisation
from rest_framework import generics
from django.shortcuts import get_object_or_404
from .serializers import OrganisationCreateSerializer
# Create your views here
class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                
                # Generate JWT token
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                response_data = {
                    "status": "success",
                    "message": "Registration successful",
                    "data": {
                        "accessToken": access_token,
                        "user": {
                            "userId": user.id,
                            "firstName": user.first_name,
                            "lastName": user.last_name,
                            "email": user.email,
                            "phone": user.phone,
                        }
                    }
                }

                return Response(response_data,status=status.HTTP_201_CREATED)
            else:
                return Response(response_data.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except ValidationError as e:
            response_data = {
                "status": "Bad request",
                "message": "Registration unsuccessful",
                "statusCode": 400
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)




class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({
                "status": "Bad request",
                "message": "Email and password are required!",
                "statusCode": 400
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.filter(email=email).first()
        
        if user is None or not user.check_password(password):
            return Response({
                "status": "Bad request",
                "message": "Authentication failed",
                "statusCode": 401
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        user = User.objects.filter(email=email).first()
        
        if user is None:
            raise AuthenticationFailed('User not found!')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')
        
        # Generate JWT token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response_data = {
            "status": "success",
            "message": "Login successful",
            "data": {
                "accessToken": access_token,
                "user": {
                    "userId": user.id,
                    "firstName": user.first_name,
                    "lastName": user.last_name,
                    "email": user.email,
                    "phone": user.phone,
                }
            }
        }

        return Response(response_data,status=status.HTTP_200_OK)


class LoggedInUserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    

from .permissions import IsUserOrInSameOrganization

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsUserOrInSameOrganization]

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        data = {
            "status": "success",
            "message": "User details retrieved successfully.",
            "data": {
                "userId": user.id,
                "firstName": user.first_name,
                "lastName": user.last_name,
                "email": user.email,
                "phone": user.phone
            }
        }
        return Response(data, status=status.HTTP_200_OK)    
    


class OrganisationListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        organisations = Organisation.objects.filter(users=user)
        serializer = OrganisationSerializer(organisations, many=True)
        return Response({
            "status": "success",
            "message": "Organisations retrieved successfully",
            "data": {
                "organisations": serializer.data}
        })
    
    
    def post(self, request, *args, **kwargs):
        data = request.data.copy()  # Make a copy of request.data to modify it
        user = request.user
        first_name = user.first_name

        # Ensure the name field is present in the data
        if 'name' not in data or not data['name'].strip():
            return Response({
    "status": "Bad Request",
    "message": "Client error",
    "statusCode": 401
}, status=status.HTTP_400_BAD_REQUEST)

        serializer = OrganisationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "status": "success",
                "message": "Organisation created successfully",
                "data": {
                    "organisations": [serializer.data]
                }
            }
            return Response(response_data, status=status.HTTP_201_CREATED)



class OrganisationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, orgId):
        organisation = get_object_or_404(Organisation, org_id=orgId)

        # Check if the user belongs to or has created the organization
        if request.user not in organisation.users.all():
            return Response({
                "status": "error",
                "message": "You do not have permission to access this organisation."
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = OrganisationSerializer(organisation)
        return Response({
            "status": "success",
            "message": "Organisation retrieved successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

class AddUserToOrganizationView(APIView):
    def post(self, request, org_id):
        # Extract userId from request data
        userId = request.data.get('userId')

        # Validate userId (if needed)

        # Get organization object
        organization = get_object_or_404(Organisation, org_id=org_id)

        try:
            # Add user to organization (assuming you have a relationship like a ManyToManyField)
            user = User.objects.get(id=userId)
            organization.users.add(user)

            return Response({
                "status": "success",
                "message": "User added to organisation successfully"
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                "status": "error",
                "message": "User with provided ID does not exist",
                "statusCode": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                "status": "error",
                "message": "Failed to add user to organization",
                "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


