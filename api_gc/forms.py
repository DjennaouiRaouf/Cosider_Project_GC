from django import forms
from .models import *
class NumBLForm(forms.ModelForm):
    num_bl = forms.IntegerField(label='N°BL',required=False,min_value=0,step_size=1)

    class Meta:
        model = BonLivraison
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(NumBLForm, self).__init__(*args, **kwargs)


        self.fields['num_bl'].initial = int(BonLivraison.objects.all_with_deleted().latest('date_modification').id.split('_')[-1])+1

        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['num_bl'].initial = instance.pk.split('_')[-1]
            self.fields['num_bl'].disabled = True

