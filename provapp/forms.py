from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from provapp.models import Entity, RaveObsids

class EntityForm(forms.Form):
    #observation_id = forms.CharField(label='RAVE observation id', max_length=1024)    # An inline class to provide additional information on the form.
    entity_list = Entity.objects.all()
#    observation_id = forms.ChoiceField(choices=[(x.id, x.name+" ("+x.type+")") for x in entity_list])
    observation_id = forms.ChoiceField(choices=[(x.id, x.id+" ("+x.type+")") for x in entity_list])

    def clean_observation_id(self):
        desired_id = self.cleaned_data['observation_id']
        if desired_id not in [e.id for e in self.entity_list]:
            print "id: " + desired_id
            raise ValidationError(
                _('Invalid value: %(value)s is not a valid obsId'),
                code='invalid',
                params={'value': desired_id},
            )

        # always return data!
        return desired_id

    #class Meta:
    #    # Provide an association between the ModelForm and a model
    #    model = Entity

class ObservationIdForm(forms.Form):
    observation_id = forms.CharField(label='RAVE_OBS_ID',
                        max_length=1024,
                        help_text="e.g. 20030411_1507m23_001, 20121220_0752m38_089")    # An inline class to provide additional information on the form.
    #entity_list = Entity.objects.all()
    #observation_id = forms.ChoiceField(choices=[(x.id, x.label+" ("+x.type+")") for x in entity_list])

    detail_flag = forms.ChoiceField(
        label="Level of detail",
        choices=[('basic', 'basic'), ('detailed','detailed'), ('all', 'all')],
        widget=forms.RadioSelect(),
        help_text="basic: only entity-collections, detailed: exclude entity-collections, all: include entities and collections"
    )

    def clean_observation_id(self):
        desired_obs = self.cleaned_data['observation_id']
        queryset = RaveObsids.objects.filter(rave_obs_id=desired_obs)
        if not queryset.exists():
        #if desired_obs not in [e.label for e in self.entity_list]:
            raise ValidationError(
                _('Invalid value: %(value)s is not a valid RAVE_OBS_ID or it cannot be found.'),
                code='invalid',
                params={'value': desired_obs},
            )

        #desired_detail = self.cleaned_data['detail_flag']

        # always return the data!
        return desired_obs #{'rave_obsid': desired_obs, 'detail_flag': desired_detail}

class ProvDalForm(forms.Form):
    entity_id = forms.CharField(
        label='Entity ID',
        max_length=1024,
        help_text="Please enter the identifier for an entity, e.g. rave:20030411_1507m23_001 or rave:20121220_0752m38_089",
    )

    step_flag = forms.ChoiceField(
        label="Step flag",
        choices=[('LAST', 'last'), ('ALL','all')],
        widget=forms.RadioSelect(),
        help_text="Specify if just one or all previous steps shall be retrieved",
        initial='ALL'
    )

    format = forms.ChoiceField(
        label="Format",
        choices=[('PROV-N', 'PROV-N'), ('PROV-JSON','PROV-JSON')],
        widget=forms.RadioSelect(),
        help_text="Format of returned provenance record",
        initial='PROV-JSON'
    )

    model = forms.ChoiceField(
        label="Data model",
        choices=[('IVOA','IVOA'), ('W3C', 'W3C')],
        widget=forms.RadioSelect(),
        help_text="Choose W3C for W3C Prov-DM compliant serialization",
        initial='W3C'
    )
