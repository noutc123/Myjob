from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework import fields, serializers
from .models import (Job, ProfilUser, ProfilRetruteur, Competence, Formation, Postuler, Experience, Retruter)
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class SetpassSerializers(Serializer):
    """
    Description: Model Description
    """
    old_password = fields.CharField(write_only=True, required=True)
    newpassword = fields.CharField(write_only=True, required=True)


class LoginSerializer(Serializer):
    """
    Description: Model Description
    """
    username = fields.CharField()
    password = fields.CharField(write_only=True, required=True)
    token = fields.SerializerMethodField()

    def get_token(self, instance: User):
        return Token.objects.get(user=instance).key

    class Meta:
        extra_kwargs = {'password': {"write_only": True}}


class UserSerializer(ModelSerializer):
    """
    Description: Model Description
    """
    password = fields.CharField(write_only=True)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data):

        validated_data.pop('password')

        for key, value in validated_data.items():

            setattr(instance, key, value)

            instance.save()

        return instance

    class Meta:
        model = User
        read_only_fields = ['id', 'password']
        fields = ('id', 'username', 'password', 'first_name', 'email',)
        extra_kwargs = {'password': {"write_only": True}}




class FormationSerializer(ModelSerializer):
    """
    Description: Model Description
    """

    def create(self, validated_data):
        return Formation.objects.create(**validated_data)

    def update(self, instance:Formation, validated_data):
        
        for key, value in validated_data.items():

            setattr(instance, key, value)
            
            instance.save()

        return instance

    class Meta:
        model = Formation

        fields = ('id', 'date_debut', 'date_fin', 'nom', 'lieux', 'description')
        pass


class CompetenceSerializer(ModelSerializer):
    """
    Description: Model Description
    """
    def create(self, validated_data):
        return Competence.objects.create(**validated_data)
     
    def update(self, instance:Competence, validated_data):
        
        for key, value in validated_data.items():

            setattr(instance, key, value)
            
            instance.save()

        return instance

    class Meta:
        model = Competence
        fields = ('id', 'niveau', 'description', 'nom')
        pass


class ExperienceSerializer(ModelSerializer):
    """
    Description: Model Description
    """

    def create(self, validated_data):
        date_debut = validated_data.get('date_de_debut') 
        date_fin = validated_data.get('date_de_fin')
        if date_debut > date_fin :
            raise serializers.ValidationError('the creation date must be lower than the end date')

        return Experience.objects.create(**validated_data)

    def update(self, instance:Experience, validated_data):
        
        for key, value in validated_data.items():

            setattr(instance, key, value)
            
            instance.save()

    class Meta: 
         model = Experience
         fields = ('id', 'date_de_debut', 'date_de_fin', 'title','Description', 'lieux')


class ProfilRetruteurSerializer(ModelSerializer):
    """
    Description: Model Description
    """
    def create(self, validated_data):
        return ProfilRetruteur.objects.create(**validated_data)

    def update(self, instance:ProfilRetruteur, validated_data):
        validated_data.pop('user')

        for key, value in validated_data.items():

            setattr(instance, key, value)
            
            instance.save()

    class Meta:
        model = ProfilRetruteur
        fields = ('id','user', 'location','Description','adresse','nationalite',)
        

class ProfilUserSerializer(ModelSerializer):
    """
    Description: Model Description
    """
    

    def create(self, validated_data):
        #create a users instance 
        
        #creat
        

        profil =ProfilUser.objects.create(**validated_data)
        #profil.competences.add()


        

        return profil

    def update(self, instance:ProfilUser, validated_data):
        validated_data.pop('user')
        
        for key, value in validated_data.items():

            setattr(instance, key, value)
            
            instance.save()

    class Meta:
        model = ProfilUser
        fields = ('id','user', 'location','Description','adresse','nationalite','birthday','cv',)


class JobSerializer(ModelSerializer):
    """
    Description: Model Description
    """
    
    def create(self, validated_data):
        date_debut = validated_data.get('date_debut') 
        date_fin = validated_data.get('date_fin')
        salaire_min = validated_data.get('salaire_min')
        salaire_max = validated_data.get('salaire_max')

        if date_debut > date_fin :
            raise serializers.ValidationError('the creation date must be lower than the end date')
        elif salaire_max < salaire_min:
            raise serializers.ValidationError('the salaries interval is not correct')
        return Job.objects.create(**validated_data)


    def update(self, instance:Job, validated_data):
        validated_data.pop('user')
        
        for key, value in validated_data.items():

            setattr(instance, key, value)
            
            instance.save()

    class Meta:
       model = Job
       fields = ('id','titre', 'type_contrat', 'salaire_min','salaire_max','profilretruteur', 'date_debut', 'date_fin', 'description', 'work_location', 'nombres_experiences')



class FindJobSerializer(Serializer):
    """
    Description: Model Description
    """
    titre = fields.CharField(write_only=True, required=True)
    type_contrat = fields.CharField(write_only=True,required=False)
    salaire_min =  fields.IntegerField(default=0)
    date_debut = fields.DateTimeField()
    date_fin = fields.DateTimeField()
    description = fields.CharField(write_only=True, required=False)
    salaire_max = fields.IntegerField(default=0)
    work_location =  fields.CharField(max_length=200)
    nombres_experiences = fields.IntegerField(default=0)
   
    
class PostulerSerializer(ModelSerializer):
    """
    Description: Model Description
    """
    

    def create(self, validated_data):
       
       
        return Postuler.objects.create(**validated_data)


    def update(self, instance:Postuler, validated_data):
        
        for key, value in validated_data.items():

            setattr(instance, key, value)
            
            instance.save()

    class Meta:
        model =Postuler
        fields = ('id', 'user_id', 'job_id', 'motivation_letter', 'date_post')

class RetruterSerializer(ModelSerializer):
    """
    Description: Model Description
    """
    
    def create(self, validated_data):
        user_id = validated_data.get('user_id') 
        


        if date_debut > date_fin :
            raise serializers.ValidationError('the creation date must be lower than the end date')
        elif salaire_max < salaire_min:
            raise serializers.ValidationError('the salaries interval is not correct')
        return Job.objects.create(**validated_data)


    def update(self, instance:Job, validated_data):
        validated_data.pop('user')
        
        for key, value in validated_data.items():

            setattr(instance, key, value)
            
            instance.save()


    class Meta:
        model= Retruter
        fields = ('id', 'user_id', 'job_id', 'user_retruteur_id', 'date_post' )
        pass