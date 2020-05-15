from django import forms

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
