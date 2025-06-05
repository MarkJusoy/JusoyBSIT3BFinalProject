from django.urls import path
from . import views

urlpatterns = [
    # API endpoints
    path('api/uploads/', views.uploads_list, name='uploads_list'),
    path('api/uploads/<int:upload_id>/', views.get_upload, name='get_upload'),
    path('api/uploads/add/', views.add_upload, name='add_upload'),
    path('api/uploads/update/<int:upload_id>/', views.update_upload, name='update_upload'),
    path('api/uploads/delete/<int:upload_id>/', views.delete_upload, name='delete_upload'),

    path('api/signup/', views.signup, name='api_signup'),
    path('api/login/', views.user_login, name='api_login'),

    # Frontend pages
    path('', views.signup_page, name='signup_page'),
    path('login/', views.login_page, name='login_page'),
]
