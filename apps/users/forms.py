from django import forms
from django.contrib.auth import authenticate

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
        fields = ['name', 'short_name', 'start_date', 'end_date', 'project_leader']


class UserTeamCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = UserTeam
        fields = ['name', 'description', 'leader']


class UserMemberCreateUpdateForm(forms.ModelForm):
    skills = forms.CharField()

    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'role',
                  'is_activate',
                  'position',
                  'team',
                  'skills']

    def clean(self):
        super().clean()
        data = self.cleaned_data
        username = data.get('password')
        user = User.objects.filter(username=username).exists()
        if user:
            raise forms.ValidationError("User already exists")


class UserSkillCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = UserSkill
        fields = ['name', 'level', 'years_experience']


class UserExportCSVCreateForm(forms.Form):
    export_position = forms.BooleanField(required=False)
    # export_skill = forms.BooleanField(required=False)
    export_team = forms.BooleanField(required=False)


class SignUpForm(forms.Form):
    email = forms.EmailField(max_length=100)
    password = forms.CharField(max_length=256)
    password1 = forms.CharField(max_length=256)

    def clean(self):
        super().clean()
        data = self.cleaned_data
        password = data.get('password')
        password1 = data.get('password1')
        if password != password1:
            raise forms.ValidationError("Password & Password Confirm not matching!")

        if User.objects.filter(email=data.get('email')).exists():
            raise forms.ValidationError("User already exists")


class SignInForm(forms.Form):
    email = forms.EmailField(max_length=100)
    password = forms.CharField(max_length=256)

    def clean(self):
        super().clean()
        data = self.cleaned_data
        password = data.get('password')
        email = data.get('email')
        user = authenticate(username=email, password=password)
        if not user:
            raise forms.ValidationError("Email & Password not matching!")
