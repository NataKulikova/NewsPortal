from django.urls import path
# Импортируем созданное нами представление
from .views import (PostView, PostCategoryView, CommentView, ArticleView, SearchView, create_post,
                    PostUpdate, PostDelete, PostCreate, subscriptions, IndexView, Index)
from django.views.decorators.cache import cache_page
from django.contrib import admin
from rest_framework import routers
from django.urls import path, include
# from news import views
#
# router = routers.DefaultRouter()
# router.register(r'schools', views.SchoolViewset)
# router.register(r'classes', views.SClassViewset)
# router.register(r'students', views.StudentViewest)

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', PostView.as_view(), name='post_list'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>', PostCategoryView.as_view()),
   path('comment<int:pk>', CommentView.as_view()),
   path('article/<int:pk>', ArticleView.as_view()),
   path('search', SearchView.as_view()),
   path('createfunc/', create_post),
   path('post/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('post/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('post/<int:pk>/', cache_page(60 * 1)(PostView.as_view()), name='post_detail'),
   path('subscriptions/', subscriptions, name='subscriptions'),
   path('hello/', Index.as_view()),
   path('i18n/', include('django.conf.urls.i18n')),  # подключаем встроенные эндопинты для работы с локализацией
   #path('admin/', admin.site.urls),
   #path('', include('basic.urls')),

]