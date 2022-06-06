from django.contrib.auth.decorators import permission_required
from django.db.models import fields
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views import View
from django.urls import reverse
from items.forms import CateoryForm, ItemForm
from items.models import *
from django.db.models import Q
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from .serializers import *
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from rest_framework.response import Response


def testAPi(request):
    stu = Item.objects.get(id = 3)
    serializer = ItemSerilizers(stu)
    json_data = JSONRenderer().render(serializer.data)
    cat = Category.objects.all()
    serializer_cat = CategorySerilizers(cat, many=True)
    json_data_cat = JSONRenderer().render(serializer_cat.data)
    # print(json_data)
    return HttpResponse(json_data, content_type='application/json')

@api_view(['GET'])
def item_json(request):
    item = Item.objects.all()
    serializer = ItemSerilizers(item, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def item_view_json(request, pk):
    item = Item.objects.filter(id = pk)
    serializer = ItemSerilizers(item, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def category_json(request):
    item = Category.objects.all()
    serializer = CategorySerilizers(item, many=True)
    return Response(serializer.data)

class AddItem(LoginRequiredMixin, View):

    login_url = '/login/'

    def get(self, request):
        if request.user.is_admin:
            form = ItemForm()
            return render(request, 'items/item_form.html', {'form': form})
        else:
            return render(request, 'error.html')

    def post(self, request):
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return render(request, 'items/error_page.html')


class AddCategory(LoginRequiredMixin, View):

    login_url = '/login/'

    def get(self, request):
        if request.user.is_admin:
            form = CateoryForm()
            return render(request, 'items/item_form.html', {'form': form})
        else:
            return render(request, 'error.html')

    def post(self, request):
        form = CateoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            return render(request, 'items/error_page.html')


class UpdateItem(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    permission_required = 'items.change_order'
    model = Item
    fields = '__all__'
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_admin:
            return render(self.request, 'error.html')
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('dashboard')


class ItemView(View):

    def get(self, request, pk):
        try:
            item = Item.objects.get(id=pk)
        except:
            item = None

        return render(request, 'items/item.html', {'item': item})


class DeleteItem(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    template_name = 'items/delete_item.html'
    permission_required = 'items.delete_order'
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_admin:
            return render(self.request, 'error.html')
        return super().get(request, *args, **kwargs)

    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Item, id=id_)

    def get_success_url(self):
        return reverse('dashboard')


class DisplayItems(View):
    def get(self, request):
        if request.GET.get('q') != None:
            category_filter = request.GET.get('q')
            items = Item.objects.filter(
                status='Available', category__category=category_filter
            )
        else:
            items = Item.objects.all()
        category = Category.objects.all()
        context = {'items': items, 'category': category}
        return render(request, 'items/home.html', context)
