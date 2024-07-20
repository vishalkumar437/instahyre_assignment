from rest_framework import serializers
from contact_spam.models import Contact

class ContactSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Contact
        fields = ("id", "name", "phone_number", "email")

class ContactWithSpamSerialiazer(ContactSerializer):
    marked_by = serializers.StringRelatedField()
    
    class Meta:
        model = Contact
        fields = ContactSerializer.Meta.fields + ("marked_by",)