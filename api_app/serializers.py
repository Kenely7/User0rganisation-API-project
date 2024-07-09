from rest_framework import serializers
from .models import User,Organisation

class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ['org_id', 'name', 'description']  
        extra_kwargs = {
            'name': {'required': True},
            'description': {'required': False}
        }
 
        
        


class UserSerializer(serializers.ModelSerializer):
    organisations = OrganisationSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['id', 'first_name','last_name','email','password','phone','organisations']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
            instance.save()    
        return instance
    

class OrganisationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ['org_id','name', 'description']

    def create(self, validated_data):
        user = self.context['request'].user
        organisation = Organisation.objects.create(**validated_data)
        organisation.users.add(user)
        organisation.save()
        return organisation