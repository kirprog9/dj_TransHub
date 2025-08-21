from django.urls import path,include
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('logout/', logout_user, name='logout'),
    path('log/', MainLogin.as_view(), name='log_good'),
    path('about/', About.as_view(), name='about'),
    path('about_cargo/', About_Cargo.as_view(), name='about_cargo'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('take_cargo/', take_cargo, name='take_cargo'),
    path('freeze_cargo/', freeze_cargo_tr, name='freeze_cargo'),
    path('delivered_cargo/', delivered_cargo, name='delivered_cargo'),
    path('unfreeze_cargo/', un_freeze_cargo_tr, name='un_freeze'),
    path('unfreeze_tr/', un_freeze_tr, name='un_freeze_tr'),
    path('create_docs/', create_docs, name='create_docs'),
    path('my_docs/', MYDoc.as_view(), name='my_doc'),
    path('download/<str:file_type>/<int:event_id>/',download_file, name='download_file'),

]
