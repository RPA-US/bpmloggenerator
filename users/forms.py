from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm 
from django.contrib.auth.models import User
 
class UserCreationForm(UserCreationForm):    
    class Meta:        
        model = User        
        fields = ('email', )  
        
        
class UserChangeForm(UserChangeForm):
    class Meta:        
        model = User        
        fields = UserChangeForm.Meta.fields