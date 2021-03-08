from django import forms
from .models import Room


class AvailabilityForm(forms.Form):
    #ROOM_CATEGORIES=(
        #('Single','Single_Room'),
        #('Double','Double_Room'),
        #('Suite','Suite_Room'),
        #('Deluxe','Deluxe_Room'),
        #('Premier','Premier_Room'),
    #)
    #room_category = forms.ModelChoiceField(queryset=Room.objects.all(), required=True)
    check_in = forms.DateTimeField(
        required=True, input_formats=["%Y-%m-%dT%H:%M", ])
    check_out = forms.DateTimeField(
        required=True, input_formats=["%Y-%m-%dT%H:%M", ])
    
    
    
