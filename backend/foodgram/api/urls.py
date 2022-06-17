from django.urls import include, path
from rest_framework import routers

from api import views

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register('tags', views.TagViewset, basename='tag')
router_v1.register(
    'ingredients', views.IngredientViewSet, basename='ingredient'
)
router_v1.register('recipes', views.RecipeViewSet, basename='recipe')
router_v1.register(
    'users/subscriptions', views.SubscriptionsViewSet, basename='subscription'
)
router_v1.register('users', views.WebUserViewSet, basename='user')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include('djoser.urls.authtoken'))
]
