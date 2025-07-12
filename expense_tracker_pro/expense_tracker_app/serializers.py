from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import User,Expense

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required = True,
                                   validators = [UniqueValidator(queryset=User.objects.all())]
                                   )
    password = serializers.CharField(write_only = True,required = True,validators = [validate_password])
    password2 = serializers.CharField(write_only = True,required = True)

    class Meta:
        model = User
        fields = ['email','password','password2','name','phone',]
    
    def validate(self,attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password":"password field didn't match"})
        return attrs
    def create(self,validate_data):
        user = User.objects.create(
            email = validate_data['email'],
            name = validate_data['name'],
            phone = validate_data['phone'],
        )
        user.set_password(validate_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=200)
    class Meta:
        model = User
        fields = ['email','password']

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'amount', 'category', 'date']