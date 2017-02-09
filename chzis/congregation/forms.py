
from django import forms

from chzis.congregation.models import CongregationMember
from chzis.users.models import PeopleProfile

# class AddCongregationMember(forms.Form):
#     first_name = forms.CharField()
#     last_name = forms.CharField()
#     congregation = forms.ChoiceField()
#     active = forms.BooleanField()
#     baptism_date = forms.DateField()

class AddCongregationMember(forms.ModelForm):

    class Meta:
        model = PeopleProfile
        fields = ['user']
