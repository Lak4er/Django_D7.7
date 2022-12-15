from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy

class PostList(ListView):
      model = Post
      ordering = '-time_in_post'
      template_name = 'news.html'
      context_object_name = 'post'
      paginate_by = 5

      # Переопределяем функцию получения списка товаров
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
          context = super().get_context_data(**kwargs)
          # Добавляем в контекст объект фильтрации.
          context['filterset'] = self.filterset
          return context



class PostDetail(DetailView):
    model = Post
    template_name = 'post_id.html'
    context_object_name = 'post'

class SearchPosts(ListView):
    paginate_by = 10
    model = Post
    ordering = 'time_in_post'
    template_name = 'search.html'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_filter'] = self.filterset
        return context


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')

class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['title'] = "Добавить статью"
        return context


class ArticleUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['title'] = "Редактировать статью"
        return context


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['title'] = "Удалить статью"
        context['previous_page_url'] = reverse_lazy('posts_list')
        return context