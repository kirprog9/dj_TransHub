from django.urls import path,include
from .views import *

app_name = 'transport'

urlpatterns = [
    path('add_transport/', AddTransport.as_view(), name='add_transport'),
    path('all_transport/', AllTransport.as_view(), name='all_transport'),
    path('my_transport/', MYTransport.as_view(), name='my_transport'),
    path('ajax/load-regions/', load_regions, name='load_regions'),
    path('ajax/load-cities/', load_cities, name='load_cities'),
    path('update/<int:pk>/', Transport_update.as_view(), name='update'),
    path('detail/<int:tr_pk>/', ShowTr.as_view(), name='detail'),
]
