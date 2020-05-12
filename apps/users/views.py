from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from apps.users.forms import (
    UserPositionForm
)
from apps.users.models import (
    UserPosition
)


class AdminDashboardView(View):
    template_name = 'base.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class UserPositionCreateView(View):
    template_name = 'user/position/position_add.html'
    form_class = UserPositionForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('users:position-list'))
        return render(request, self.template_name, {'form': form})


class UserPositionListView(View):
    template_name = 'user/position/position_list.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        positions = UserPosition.objects.filter(delete_flg=False).order_by('name')
        paginator = Paginator(positions, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'positions': page_obj})


class UserPositionUpdateView(View):
    template_name = 'user/position/position_edit.html'

    def get(self, request, *args, **kwargs):
        position_id = kwargs.get('id')
        position = UserPosition.objects.filter(id=position_id).first()
        if not position:
            return render(request, '404.html', {})
        return render(request, self.template_name, {'position': position})
