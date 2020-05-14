from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from apps.users.forms import (
    UserPositionCreatUpdateForm,
    UserTeamCreateUpdateForm,
    UserProjectJoinedCreateForm
)
from apps.users.models import (
    UserPosition,
    UserTeam,
    UserProjectJoined
)


class AdminDashboardView(View):
    template_name = 'base.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class UserPositionCreateView(View):
    template_name = 'user/position/position_add.html'
    form_class = UserPositionCreatUpdateForm

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
    form_class = UserPositionCreatUpdateForm

    def get(self, request, *args, **kwargs):
        position_id = kwargs.get('id')
        position = UserPosition.objects.filter(id=position_id).first()
        if not position:
            return render(request, '404.html', {})
        return render(request, self.template_name, {'position': position})

    def post(self, request, *args, **kwargs):
        position_id = kwargs.get('id')
        position = UserPosition.objects.filter(id=position_id).first()
        if not position:
            return render(request, '404.html', {})
        form = self.form_class(request.POST, instance=position)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('users:position-list'))
        return render(request, self.template_name, {'form': form, 'position_id': position_id})


class UserTeamCreateView(View):
    template_name = 'user/team/team_add.html'
    form_class = UserTeamCreateUpdateForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('users:team-list'))
        return render(request, self.template_name, {'form': form})


class UserTeamListView(View):
    template_name = 'user/team/team_list.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        teams = UserTeam.objects.filter(delete_flg=False).order_by('name')
        paginator = Paginator(teams, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'teams': page_obj})


class UserTeamUpdateView(View):
    template_name = 'user/team/team_edit.html'
    form_class = UserTeamCreateUpdateForm

    def get(self, request, *args, **kwargs):
        team_id = kwargs.get('id')
        team = UserTeam.objects.filter(id=team_id).first()
        if not team:
            return render(request, '404.html', {})
        return render(request, self.template_name, {'team': team})

    def post(self, request, *args, **kwargs):
        team_id = kwargs.get('id')
        team = UserTeam.objects.filter(id=team_id).first()
        if not team:
            return render(request, '404.html', {})
        form = self.form_class(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('users:team-list'))
        return render(request, self.template_name, {'form': form, 'team_id': team_id})


class UserProjectJoinedCreateView(View):
    template_name = 'user/project_joined/project_joined_add.html'
    form_class = UserProjectJoinedCreateForm

    def get(self, request, *args, **kwargs):
        teams = UserTeam.objects.filter(delete_flg=False)
        return render(request, self.template_name, {'teams': teams})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            members = form.cleaned_data['members']
            form.cleaned_data['members'] = members.split(';')
            x = UserProjectJoined(**form.cleaned_data)
            x.save()
            return redirect(reverse_lazy('users:project-joined-list'))
        return render(request, self.template_name, {'form': form})


class UserProjectJoinedListView(View):
    template_name = 'user/project_joined/project_joined_list.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        project_joined = UserProjectJoined.objects.filter(delete_flg=False).order_by('name')
        paginator = Paginator(project_joined, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'projects_joined': page_obj})


class UserProjectJoinedUpdateView(View):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass
