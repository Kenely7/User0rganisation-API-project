
from django.urls import path,include
# from rest_framework.routers import DefaultRouter
from .views import RegisterView,LoginView,LoggedInUserDetailView,UserDetailView,OrganisationDetailView,OrganisationListCreateView,AddUserToOrganizationView

# router = DefaultRouter()
# router.register(r'organisations', OrganisationViewSet)
# router.register(r'users', UserViewSet)

urlpatterns = [
    path('auth/register/',RegisterView.as_view()),
    path('auth/login/',LoginView.as_view()),
    path('api/users/<str:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('api/organisations/', OrganisationListCreateView.as_view(), name='user-organisations'),
    path('api/organisations/<str:orgId>/', OrganisationDetailView.as_view(), name='organisation-detail'),
    path('api/organisations', OrganisationListCreateView.as_view(), name='organisation-create'),
    path('api/organisation/<str:org_id>/users/', AddUserToOrganizationView.as_view(), name='add_user_to_organization' )
]
