import csv
import datetime
import os

from django.core.paginator import Paginator
from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView
from django.urls import reverse

from apps.users.forms import (
    UserPositionCreatUpdateForm,
    UserTeamCreateUpdateForm,
    UserProjectJoinedCreateUpdateForm,
    UserSkillCreateUpdateForm,
    UserMemberCreateUpdateForm,
    UserExportCSVCreateForm,
    SignUpForm,
    SignInForm
)
from apps.users.models import (
    UserPosition,
    UserTeam,
    UserProjectJoined,
    UserSkill,
    User
)


class UserDetailView(View):
    template_name = 'user/profile.html'

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = User.objects.filter(id=user_id)
        # for course in user:
        #     print(course['username'])
        # print(user.username)
        if not user:
            return render(request, '404.html', {})
        return render(request, self.template_name, {'user': user})


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

    def dispatch(self, request, *args, **kwargs):
        team_id = kwargs.get('id')
        self.team = UserTeam.objects.filter(id=team_id).first()
        if not self.team:
            return render(request, '404.html', {})
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'team': self.team})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.team)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('users:team-list'))
        return render(request, self.template_name, {'form': form, 'team_id': kwargs.get('id')})


class UserProjectJoinedCreateView(View):
    template_name = 'user/project_joined/project_joined_add.html'
    form_class = UserProjectJoinedCreateUpdateForm

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
    template_name = 'user/project_joined/project_joined_update.html'
    form_class = UserProjectJoinedCreateUpdateForm

    def dispatch(self, request, *args, **kwargs):
        project_joined_id = kwargs.get('id')
        self.project_joined = UserProjectJoined.objects.filter(id=project_joined_id).first()
        if not self.project_joined:
            return render(request, '404.html', {})
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        teams = UserTeam.objects.filter(delete_flg=False)
        return render(request, self.template_name, {'project_joined': self.project_joined, 'teams': teams})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.project_joined)
        if form.is_valid():
            members = form.cleaned_data['members']
            form.cleaned_data['members'] = members.split(';')
            self.project_joined.__dict__.update(**form.cleaned_data)
            self.project_joined.save()
            return redirect(reverse_lazy('users:project-joined-list'))
        return render(request, self.template_name, {'form': form, 'project_joined_id': kwargs.get('id')})


class UserMemberCreateView(View):
    template_name = 'user/member/member_add.html'
    form_class = UserMemberCreateUpdateForm

    def dispatch(self, request, *args, **kwargs):
        teams = UserTeam.objects.filter(delete_flg=False)
        positions = UserPosition.objects.filter(delete_flg=False)
        user_project_joined = UserProjectJoined.objects.filter(delete_flg=False)
        self.context = {
            'teams': teams,
            'positions': positions,
            'user_project_joined': user_project_joined,
        }
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('users:member-list'))
        self.context.update({'form': form})
        return render(request, self.template_name, self.context)


class UserMemberListView(View):
    template_name = 'user/member/member_list.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        members = User.objects.filter(delete_flg=False).order_by('username')
        paginator = Paginator(members, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'members': page_obj})


class UserSkillCreateView(View):
    # template_name = 'user/skill/skill_add.html'
    # form_class = UserSkillCreateUpdateForm
    #
    # def get(self, request, *args, **kwargs):
    #     return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.cleaned_data['user'] = request.user
            return redirect(reverse_lazy('users:project-joined-list'))
        return render(request, self.template_name, {'form': form})


class UserExportCSVCreateView(View):
    form_class = UserExportCSVCreateForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            model = None
            prefix = None
            if form.cleaned_data['export_position']:
                model = UserPosition
                prefix = 'position'
            elif form.cleaned_data['export_team']:
                model = UserTeam
                prefix = 'team'
            if not model:
                return render(request, '404.html', {})
            data = model.objects.filter(delete_flg=False).order_by('created_at')
            data = list(data.values())
            keys = data[0].keys()
            folder_media = os.path.join(settings.BASE_DIR, 'media/export')
            if not os.path.isdir(f'{folder_media}/{prefix}'):
                os.mkdir(f'{folder_media}/{prefix}')

            file_name = datetime.datetime.now().strftime(f'%Y%m%d_%H%M%S.csv')
            path_file = f'/{folder_media}/{prefix}/{file_name}'
            with open(path_file, 'w') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(data)
            return redirect(f'/media/export/{prefix}/{file_name}')
        return render(request, '500.html', {})


class SignInView(View):
    template_name = 'user/auth/signin.html'
    form_class = SignInForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            login(request, User.objects.get(email=form.cleaned_data.get('email')))
            return redirect('/dashboard')
        return render(request, self.template_name, {'form': form})


class SignUpView(View):
    template_name = 'user/auth/signup.html'
    form_class = SignUpForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create(
                username=data.get('email'),
                email=data.get('email')
            )
            user.set_password(data.get('password'))
            user.save()
            login(request, user)
            return redirect('/dashboard')
        return render(request, self.template_name, {'form': form})


class SignOutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse_lazy('users:signin'))
