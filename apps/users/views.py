import csv
import datetime
import os
import json

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.conf import settings
from django.contrib.auth import authenticate, login, logout

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

from apps.users.decorators import admin_required

DEFAULT_PASSWORD = 'Aa@123456'


class AdminDashboardView(View):
    template_name = 'base.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class UserPositionCreateView(View):
    template_name = 'user/position/position_add.html'
    form_class = UserPositionCreatUpdateForm

    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    @method_decorator(admin_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('users:position-list'))
        return render(request, self.template_name, {'form': form})


class UserPositionListView(View):
    template_name = 'user/position/position_list.html'
    paginate_by = 10

    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        positions = UserPosition.objects.filter(delete_flg=False).order_by('name')
        paginator = Paginator(positions, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'positions': page_obj})


class UserPositionUpdateView(View):
    template_name = 'user/position/position_edit.html'
    form_class = UserPositionCreatUpdateForm

    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        position_id = kwargs.get('id')
        position = UserPosition.objects.filter(id=position_id).first()
        if not position:
            return render(request, '404.html', {})
        return render(request, self.template_name, {'position': position})

    @method_decorator(admin_required)
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

    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    @method_decorator(admin_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('users:team-list'))
        return render(request, self.template_name, {'form': form})


class UserTeamListView(View):
    template_name = 'user/team/team_list.html'
    paginate_by = 10

    @method_decorator(admin_required)
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

    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'team': self.team})

    @method_decorator(admin_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.team)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('users:team-list'))
        return render(request, self.template_name, {'form': form, 'team_id': kwargs.get('id')})


class UserProjectJoinedCreateView(View):
    template_name = 'user/project_joined/project_joined_add.html'
    form_class = UserProjectJoinedCreateUpdateForm

    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        teams = UserTeam.objects.filter(delete_flg=False)
        return render(request, self.template_name, {'teams': teams})

    @method_decorator(admin_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            members = form.cleaned_data['members']
            form.cleaned_data['members'] = members.split(';')
            obj = UserProjectJoined(**form.cleaned_data)
            obj.save()
            return redirect(reverse_lazy('users:project-joined-list'))
        return render(request, self.template_name, {'form': form})


class UserProjectJoinedListView(View):
    template_name = 'user/project_joined/project_joined_list.html'
    paginate_by = 10

    @method_decorator(admin_required)
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

    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        teams = UserTeam.objects.filter(delete_flg=False)
        return render(request, self.template_name, {'project_joined': self.project_joined, 'teams': teams})

    @method_decorator(admin_required)
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

    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

    @method_decorator(admin_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create(
                username=data.get('username'),
                email=data.get('username'),
                role=data.get('role'),
                is_activate=data.get('is_activate'),
                position=data.get('position'),
                team=data.get('team')
            )
            user.set_password(DEFAULT_PASSWORD)
            user.save()

            input_skills = data.get('skills')
            for skill in json.loads(input_skills):
                user_skill = UserSkill.objects.create(
                    name=skill.get('name'),
                    level=skill.get('level'),
                    years_experience=skill.get('exp')
                )
                user_skill.user.add(user)
                user_skill.save()
            return redirect(reverse_lazy('users:member-list'))
        self.context.update({'form': form})
        return render(request, self.template_name, self.context)


class UserMemberUpdateView(View):
    template_name = 'user/member/member_edit.html'
    form_class = UserMemberCreateUpdateForm

    def dispatch(self, request, *args, **kwargs):
        teams = UserTeam.objects.filter(delete_flg=False)
        positions = UserPosition.objects.filter(delete_flg=False)
        user_project_joined = UserProjectJoined.objects.filter(delete_flg=False)

        member = User.objects.filter(id=kwargs.get('id')).first()
        if not member:
            return render(request, '404.html', {})

        skills = UserSkill.objects.filter(user=member)
        self.context = {
            'teams': teams,
            'positions': positions,
            'user_project_joined': user_project_joined,
            'member': member,
            'skills': skills
        }
        return super().dispatch(request, *args, **kwargs)

    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

    @method_decorator(admin_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = self.context['member']
            user.update(**dict(
                username=data.get('username'),
                email=data.get('username'),
                role=data.get('role'),
                is_activate=data.get('is_activate'),
                position=data.get('position'),
                team=data.get('team')
            ))
            return redirect(reverse_lazy('users:member-list'))
        self.context.update({'form': form})
        return render(request, self.template_name, self.context)


class UserMemberListView(View):
    template_name = 'user/member/member_list.html'
    paginate_by = 10

    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        members = User.objects.filter(delete_flg=False).order_by('username')
        paginator = Paginator(members, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'members': page_obj})


class UserExportCSVCreateView(View):
    form_class = UserExportCSVCreateForm

    @method_decorator(admin_required)
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
