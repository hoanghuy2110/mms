from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.users.models import (
    UserPosition,
    UserProjectJoined,
    UserTeam,
    UserSkill,
    User
)


class UserPositionCreatUpdateForm(forms.ModelForm):
    class Meta:
        model = UserPosition
        fields = ['name', 'short_name']


class UserProjectJoinedCreateUpdateForm(forms.ModelForm):
    members = forms.CharField()

    class Meta:
        model = UserProjectJoined
        fields = ['name', 'short_name', 'start_date', 'end_date', 'project_leader', 'team']


class UserTeamCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = UserTeam
        fields = ['name', 'description', 'leader']


class UserMemberCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'role',
                  'is_activate',
                  'position',
                  'team',
                  'user_project_joined']


class UserSkillCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = UserSkill
        fields = ['name', 'level', 'years_experience']


class UserExportCSVCreateForm(forms.Form):
    export_position = forms.BooleanField(required=False)
    # export_skill = forms.BooleanField(required=False)
    export_team = forms.BooleanField(required=False)


class SigninForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your Username', 'class': 'form-control'}
        )
    )
    password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your Password', 'class': 'form-control'})
    )


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your Username', 'class': 'form-control'}))
    email = forms.EmailField(max_length=100,
        help_text='Required. Inform a valid email address.',
        widget=forms.TextInput(attrs={'placeholder': 'Enter your Username', 'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your Password'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
