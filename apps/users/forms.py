from django import forms

from apps.users.models import UserPosition


class UserPositionForm(forms.ModelForm):
    class Meta:
        model = UserPosition
        fields = ['name', 'short_name']
