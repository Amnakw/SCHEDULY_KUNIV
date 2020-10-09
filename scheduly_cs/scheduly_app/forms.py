from django import forms
from django.contrib.auth.models import User
from .models import Instructor, Student, DateTimeInterval, Course, ElectiveCourse, Progress
from django.core.validators import RegexValidator


class UserLogin(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email'})) # (attrs={'placeholder': 'Email'}) changes placeholder from username to email
    password = forms.CharField(required=True, widget=forms.PasswordInput())


# Specify the fields that are required in the form that is used to create a user when creating an instructor or student
class UserCreate(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

        widgets={
        'password': forms.PasswordInput(),
        }

# used to update profile 
class UserUpdate(forms.ModelForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput())
    confirm_password=forms.CharField(required=True, widget=forms.PasswordInput())
    
    class Meta:
        model=User
        fields=('username', 'password')



# Specify the fields that are required in the form that is used to create an instructor user
# the user field is excluded so that it will be created using UserCreate form
class AddUpdateInstructor(forms.ModelForm):
    class Meta:
        model = Instructor
        exclude = ['user']


# Specify the fields that are required in the form that is used to create a student user
# the user field is excluded so that it will be created using UserCreate form
class AddUpdateStudent(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['user']


# Specify the fields that are required in the form that is used to create a DateTimeInterval
class AddDateTimeInterval(forms.ModelForm):
    class Meta:
        model = DateTimeInterval
        fields = '__all__'


# Specify the fields that are required in the form that is used to create a Course
class AddCourse(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'


class AddElectiveCourse(forms.ModelForm):
    class Meta:
        model = ElectiveCourse
        fields = '__all__'


class UpdateCourse(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['number', 'name', 'credits']


class ProgressForm(forms.Form):
    name = forms.CharField(required=False)
    is_completed = forms.BooleanField(required=False)
    course_id = forms.IntegerField(required=False)

    # class Meta:
    #     model = Progress
    #     fields = '__all__'


ProgressFormSet = forms.formset_factory(ProgressForm, extra=0)
