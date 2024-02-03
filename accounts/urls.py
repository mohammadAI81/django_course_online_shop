from django.urls import path

from. import views
urlpatterns = [
    path('signup/', views.Signup.as_view(), name='signup'),
    path('logout/', views.logout_view, name='logout')
]
