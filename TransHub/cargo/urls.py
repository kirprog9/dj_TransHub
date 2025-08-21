from django.urls import path,include
from .views import *
app_name = 'cargo'

urlpatterns = [
    path('add_cargo/', AddCargo.as_view(), name='add_cargo'),
    path('all_cargo/', AllCargo.as_view(), name='all_cargo'),
    path('my_cargo/', MYCargo.as_view(), name='my_cargo'),
    path('ajax/load-regions/', load_regions, name='load_regions'),
    path('ajax/load-cities/', load_cities, name='load_cities'),
    path('update/<int:pk>/', Cargo_update.as_view(), name='update'),
]
