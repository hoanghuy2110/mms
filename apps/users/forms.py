from django import forms

from apps.users.models import (
    UserPosition,
    UserProjectJoined,
    UserTeam
)


class UserPositionCreatUpdateForm(forms.ModelForm):
    class Meta:
        model = UserPosition
        fields = ['name', 'short_name']


class UserProjectJoinedCreateForm(forms.ModelForm):
    members = forms.CharField()
    class Meta:
        model = UserProjectJoined
        fields = ['name', 'short_name', 'start_date', 'end_date', 'project_leader', 'team']


class UserTeamCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = UserTeam
        fields = ['name', 'description', 'leader']
