from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

import datetime

from .forms import StihForm, NewUserForm
from .models import Stih, Author

def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    num_stihs=Stih.objects.all().count()
    num_authors=Author.objects.count()  # Метод 'all()' применён по умолчанию.

    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'num_stihs':num_stihs,'num_authors':num_authors,'num_visits':num_visits},
    )

class UncheckedStihsListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'catalog.can_validate'
    model = Stih
    template_name ='catalog/unchecked_stihs_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Stih.objects.filter(_checked=False)    

class StihsByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = Stih
    template_name ='catalog/stih_list_user.html'
    paginate_by = 10

    def get_queryset(self):
        return Stih.objects.filter(author__account=self.request.user)

class StihListView(generic.ListView):
    model = Stih
    paginate_by = 10

    def get_queryset(self):
        return Stih.objects.filter(_checked=True)

class StihDetailView(generic.DetailView):
    model = Stih

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

    def get_queryset(self):
        return Author.objects.filter().order_by('classic')

class AuthorDetailView(generic.DetailView):
    model = Author

@permission_required('catalog.can_validate')
def renew_stih(request, pk):
    stih_inst = get_object_or_404(Stih, pk=pk)

    # Если данный запрос типа POST, тогда
    if request.method == 'POST':

        # Создаём экземпляр формы и заполняем данными из запроса (связывание, binding):
        form = StihForm(request.POST)

        # Проверка валидности данных формы:
        if form.is_valid():
            # Обработка данных из form.cleaned_data
            #(здесь мы просто присваиваем их полю due_back)
            stih_inst._checked = form.cleaned_data['stih_checked']
            stih_inst.save()

            # Переход по адресу 'all-borrowed':
            return HttpResponseRedirect(reverse('unchecked-stihs'))

    # Если это GET (или какой-либо ещё), создать форму по умолчанию.
    else:
        form = StihForm(initial={'stih_checked': False,})

    return render(request, 'catalog/stih_renew.html', {'form': form, 'stihinst':stih_inst})

class AuthorCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.can_validate'
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death','classic']
    initial={'classic':True,}

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.can_validate'
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']

    def get_queryset(self):
        return Author.objects.filter(classic=True)

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.can_validate'
    model = Author
    success_url = reverse_lazy('authors')

    def get_queryset(self):
        return Author.objects.filter(classic=True)

class StihCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.can_validate'
    model = Stih
    fields = '__all__'
    initial={'_checked':True, }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['author'].queryset = Author.objects.filter(classic=True)
        return context

class StihUserCreate(PermissionRequiredMixin, CreateView):
    template_name ='catalog/stih_user_form.html'
    permission_required = 'catalog.cant_validate'
    model = Stih
    fields = ['title','content','pub_date','author']
    initial={'pub_date': datetime.date.today().strftime("%Y-%m-%d"),}

    def dispatch(self, request, *args, **kwargs):
        author = Author.objects.get(account=self.request.user)
        self.initial['author'] = author
        return super().dispatch(request, *args, **kwargs)

class StihUpdate(LoginRequiredMixin, UpdateView):
    model = Stih
    fields = ['title','content','pub_date']

    def get_queryset(self):
        if self.request.user.groups.filter(name='Redactors').exists():
            return Stih.objects.filter(author__classic=True)
        return Stih.objects.filter(author__account=self.request.user)

class StihDelete(LoginRequiredMixin, DeleteView):
    model = Stih
    success_url = reverse_lazy('my-stihs')

    def get_queryset(self):
        if self.request.user.groups.filter(name='Redactors').exists():
            return Stih.objects.filter(author__classic=True)
        return Stih.objects.filter(author__account=self.request.user)

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            my_group = Group.objects.get(name='Low create permissioners') 
            my_group.user_set.add(user)
            login(request, user)
            Author.objects.create_author(user.first_name, user.last_name, user.birth_date, request.user)
            messages.success(request, "Registration successful." )
            return redirect("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="catalog/register.html", context={"register_form":form})