from django import forms
from mainapp.models import *


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))


#FOR UserForm
class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email','password','first_name','last_name','phone','dob','gender','address']
        widgets ={
            'email':forms.EmailInput(attrs={
                'class':'form-control',
                'placeholder':"Email"
            }),            
            'password':forms.PasswordInput(attrs={
                'class':'form-control',
                'placeholder':"Password"
            }),
            'first_name':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':"First name"
            }),
            'last_name':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':"Last name"
            }),
            'phone':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':"Phone number"
            }),
            'dob':forms.DateInput(attrs={
                'class':'form-control',
                'placeholder':"Date of birth"
            }),
            'gender':forms.Select(attrs={
                'class':'form-control',
                'placeholder':"Artist date of birth"
            }),
            'address':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':"Address"
            }),
        }
    def clean_signup_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "This email is already used, please use different email.")
        return email



#User_UpdateForm
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','phone','dob','gender','address']
        widgets ={
            'first_name':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':"First name"
            }),
            'last_name':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':"Last name"
            }),
            'phone':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':"Phone number"
            }),
            'dob':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':"Date of birth"
            }),
            'gender':forms.Select(attrs={
                'class':'form-control',
                'placeholder':"Artist date of birth"
            }),
            'address':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':"Address"
            }),
        }

        
#News Form
class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'subtitle',  'slug','category', 'image', 'text', 'author']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'News Title'
            }),
            'subtitle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'News Subtitle'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'News Slug(format-is-like-this)'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'News Category'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Main News '
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Author'
            }),
        }


#NewsCategory
class NewsCategoryForm(forms.ModelForm):
    class Meta:
        model = NewsCategory
        fields = ['title', 'image', 'text', 'slug']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'News Title'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),

            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Main News '

            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'News Slug(format-is-like-this)'

            }),

        }

#News Comment
class NewsCommentForm(forms.ModelForm):
    class Meta:
        model = NewsComment
        fields = ['name', 'email', 'website', 'text', 'image', 'news']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'News Title'
            }),

            'email': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),

            'website': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Web site '

            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Main News '

            }),

            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'news': forms.Select(attrs={
                'class': 'form-control',
            }),

        }

#Contact
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'name'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email'
            }),

            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder':  'subject '

            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'message'

            }),

        }

#Ourcontact
class OurContactForm(forms.ModelForm):
    class Meta:
        model = OurContact
        fields = ['title', 'description', 'address', 'email', 'phone', 'maps']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'title'
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'description'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'street/city/country'
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'contact number'
            }),
            'maps': forms.URLInput(attrs={
                'class': 'form-control',

            }),

        }

#Staff Form
class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['name', 'post', 'profile', 'education', 'phone', 'DoB']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'staff name'
            }),
            'post': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'post'
            }),
            'profile': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'education': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'qualification'
            }),

            'phone': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'contact number'
            }),
            'DoB': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Date of Birth'
            }),

        }


      ####Ads####Category
class  AdsCategoryForm(forms.ModelForm):
    class Meta:
        model = AdsCategory
        fields = ['title','slug']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ads title'
            }),
            'issue_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'issue date'
            }),
        }

#Ads##
class AdsForm(forms.ModelForm):
    class Meta:
        model = Ads
        fields = ['title', 'issue_date', 'end_date', 'image', 'sponsorships','ads_category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ads title'
            }),
            'issue_date': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'issue date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'end date'

            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),

            'sponsorships': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ads sponsorship'
            }),

            'ads_category': forms.Select(attrs={
                'class': 'form-control',
            }),

        }



