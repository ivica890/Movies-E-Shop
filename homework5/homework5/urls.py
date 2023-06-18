"""
URL configuration for homework5 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

from hw5 import views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('films/', views.film_list, name='film_list'),
                  path('seats/<int:film_id>/', views.seat_list, name='seat_list'),
                  path('cart/', views.shopping_cart, name='shopping_cart'),
                  path('confirmation/', views.confirmation, name='confirmation'),
                  path('seat-list/<int:film_id>/', views.seat_list, name='seat_list'),
                  path('save-seats/', views.save_seat, name='save_seat'),
                  path('remove-seat/', views.remove_seat, name='remove_seat'),
                  path('shopping_cart.html', views.shopping_cart, name='shopping_cart'),
                  path('get-film-info/', views.get_film_info, name='get_film_info'),
                  path('logout/', views.logout_view, name='logout'),
                  path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
                  path('add_movie', views.add_movie, name='add_movie'),
                  path('delete_movie/<int:movie_id>/', views.delete_movie, name='delete_movie'),
                  path('about/', views.about, name='about'),
                  path('home/', views.home, name='home'),
                  path('', RedirectView.as_view(url='/home/')),
                  path('create_order/', views.create_order, name='create_order'),
                  path('clear_shopping_cart/', views.clear_shopping_cart, name='clear_shopping_cart'),
                  path('orders/<int:order_id>/delete/', views.delete_order, name='delete_order'),
                  path('filter-movies/', views.filter_movies, name='filter_movies'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
