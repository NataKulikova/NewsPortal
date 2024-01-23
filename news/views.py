from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment
from datetime import datetime
from .filters import PostFilter
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.views.decorators.csrf import csrf_protect
from .models import Subscription, Category
from django.http import HttpResponse
from django.views import View
from .tasks import hello, printer
import logging
from django.utils.translation import gettext as _
from django.utils.translation import activate, get_supported_language_variant
from django.utils import timezone
from django.shortcuts import redirect

import pytz  # импортируем стандартный модуль для работы с часовыми поясами


from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions

#from serializers import *
#from models import *


#берет название приложение как имя логера
logger = logging.getLogger(__name__)

class Index(View):
   def get(self, request):
       # . Translators: This message appears on the home page only
       models = Post.objects.all()

       context = {
           'models': models,
           'current_time': timezone.localtime(timezone.now()),
           'timezones': pytz.common_timezones  # добавляем в контекст все доступные часовые пояса
       }

       return HttpResponse(render(request, 'post.html', context))

   #  по пост-запросу будем добавлять в сессию часовой пояс, который и будет обрабатываться написанным нами ранее middleware
   def post(self, request):
       request.session['django_timezone'] = request.POST['timezone']
       return redirect('/')

class PostView(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-dateCreation'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'post.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 2  # вот так мы можем указать количество записей на странице

    def get_queryset(self):
       # Получаем обычный запрос
       queryset = super().get_queryset()
       # Используем наш класс фильтрации.
       # self.request.GET содержит объект QueryDict, который мы рассматривали
       # в этом юните ранее.
       # Сохраняем нашу фильтрацию в объекте класса,
       # чтобы потом добавить в контекст и использовать в шаблоне.
       self.filterset = PostFilter(self.request.GET, queryset)
       # Возвращаем из функции отфильтрованный список товаров
       return self.filterset.qs

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['filterset'] = self.filterset
        return context
   # Переопределяем функцию получения списка товаров

class PostTrans(View):
    def get(self, request):
        greet = _('Работаем для вас 24 на 7') #msgid
        context = {
            'greet': greet
        }

        return HttpResponse(render(request, 'post.html', context))
class PostCategoryView(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Category
    # Используем другой шаблон — post.html
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post_detail'

class CommentView(DetailView):
   # Модель всё та же, но мы хотим получать информацию по отдельному товару
   model = Comment
   # Используем другой шаблон — post.html
   template_name = 'comment.html'
   # Название объекта, в котором будет выбранный пользователем продукт
   context_object_name = 'comment'

class ArticleView(DetailView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-dateCreation'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'article.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'Article'

class SearchView(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
        # Поле, которое будет использоваться для сортировки объектов
    ordering = '-dateCreation'
        # Указываем имя шаблона, в котором будут все инструкции о том,
        # как именно пользователю должны быть показаны наши объекты
    template_name = 'search.html'
        # Это имя списка, в котором будут лежать все объекты.
        # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'search'

    def get_queryset(self):
       # Получаем обычный запрос
       queryset = super().get_queryset()
       # Используем наш класс фильтрации.
       # self.request.GET содержит объект QueryDict, который мы рассматривали
       # в этом юните ранее.
       # Сохраняем нашу фильтрацию в объекте класса,
       # чтобы потом добавить в контекст и использовать в шаблоне.
       self.filterset = PostFilter(self.request.GET, queryset)
       # Возвращаем из функции отфильтрованный список товаров
       return self.filterset.qs

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['filterset'] = self.filterset
        return context

def create_post(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/news/')

    return render(request, 'product_edit.html', {'form': form})

class PostUpdate(UpdateView):
    form_class = PostForm
    permission_required = ('news.change_product',)
    model = Post
    template_name = 'product_edit.html'

# Представление удаляющее товар.
class PostDelete(DeleteView):
    model = Post
    permission_required = ('news.delete_product',)
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

class PostCreate(LoginRequiredMixin, CreateView):
    raise_exception = True
    permission_required = ('news.add_product',)
    form_class = PostForm
    model = Post
    template_name = 'product_edit.html'

@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )

class IndexView(View):
    def get(self, request):
        hello.delay()
        return HttpResponse('Hello!')

class IndexView(View):
    def get(self, request):
        printer.delay(10)
        hello.delay()
        return HttpResponse('Hello!')


# class SchoolViewset(viewsets.ModelViewSet):
#    queryset = School.objects.all()
#    serializer_class = SchoolSerializer
#
#
# class SClassViewset(viewsets.ModelViewSet):
#    queryset = SClass.objects.all()
#    serializer_class = SClassSerializer
#
#
# class StudentViewest(viewsets.ModelViewSet):
#    queryset = Student.objects.all()
#    serializer_class = StudentSerializer