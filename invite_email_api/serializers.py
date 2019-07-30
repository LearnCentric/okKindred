from rest_framework import serializers
from email_confirmation.models import EmailConfirmation

class InviteEmailSerializer(serializers.HyperlinkedModelSerializer):
    '''
    Defines fields to be serialized for an invite email
    '''

    username_who_invited_person = serializers.CharField(source='user_who_invited_person.name', read_only=True)

    class Meta:
        model = EmailConfirmation
        fields = ('person_id', 'email_address', 'sent', 'username_who_invited_person')