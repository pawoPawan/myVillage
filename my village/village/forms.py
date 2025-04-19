from django import forms
from .models import AadhaarVerification, CommunityEvent, Village, Panchayat, UserProfile, RelationshipRequest

class AadhaarVerificationForm(forms.ModelForm):
    class Meta:
        model = AadhaarVerification
        fields = ['aadhaar_number', 'front_image', 'back_image']
        widgets = {
            'aadhaar_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter 12-digit Aadhaar number',
                'pattern': '[0-9]{12}',
                'maxlength': '12'
            }),
            'front_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*,.pdf'
            }),
            'back_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*,.pdf'
            }),
        }
    
    def clean_aadhaar_number(self):
        aadhaar_number = self.cleaned_data.get('aadhaar_number')
        if not aadhaar_number.isdigit() or len(aadhaar_number) != 12:
            raise forms.ValidationError("Aadhaar number must be 12 digits")
        return aadhaar_number

class CommunityEventForm(forms.ModelForm):
    class Meta:
        model = CommunityEvent
        fields = [
            'title', 'description', 'event_type', 'start_date', 'end_date', 'village',
            'location', 'expected_attendees', 'is_public', 'requires_registration',
            'registration_deadline', 'budget', 'contact_person', 'contact_phone', 'notes'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Event Description'}),
            'event_type': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'village': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Specific location within the village'}),
            'expected_attendees': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'requires_registration': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'registration_deadline': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'budget': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact person name'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact phone number'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Additional notes or instructions'}),
        }
    
    def __init__(self, user=None, *args, **kwargs):
        super(CommunityEventForm, self).__init__(*args, **kwargs)
        if user and user.is_authenticated:
            try:
                user_village = user.userprofile.village
                if user_village:
                    panchayat = user_village.panchayat
                    villages = Village.objects.filter(panchayat=panchayat)
                    self.fields['village'].queryset = villages
                    self.fields['village'].initial = user_village
            except UserProfile.DoesNotExist:
                pass
        
        # Make registration deadline required only if registration is required
        self.fields['registration_deadline'].required = False
        
    def clean(self):
        cleaned_data = super().clean()
        requires_registration = cleaned_data.get('requires_registration')
        registration_deadline = cleaned_data.get('registration_deadline')
        
        if requires_registration and not registration_deadline:
            self.add_error('registration_deadline', 'Registration deadline is required when registration is required.')
        
        return cleaned_data 

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'village', 'education', 'profession', 'hobbies', 'achievements',
            'social_contributions', 'age', 'gender', 'father_name', 'mother_name',
            'nickname', 'profile_picture'
        ]
        widgets = {
            'village': forms.Select(attrs={'class': 'form-select'}),
            'education': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Your educational background'}),
            'profession': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your profession'}),
            'hobbies': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Your hobbies and interests'}),
            'achievements': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Your achievements'}),
            'social_contributions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Your contributions to society'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '120'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Father\'s name'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mother\'s name'}),
            'nickname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your nickname'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        
        # Always make village field read-only in profile edit form
        self.fields['village'].widget.attrs['disabled'] = 'disabled'
        self.fields['village'].widget.attrs['class'] = 'form-select bg-light'
        
        if instance and instance.aadhaar_verified:
            self.fields['village'].help_text = 'Village cannot be changed after Aadhaar verification'
        else:
            self.fields['village'].help_text = 'Village can only be set during Aadhaar verification'

class UserSearchForm(forms.Form):
    search_query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name, nickname, or address...'
        })
    )
    
    age_min = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min Age'
        })
    )
    
    age_max = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max Age'
        })
    )
    
    gender = forms.ChoiceField(
        choices=[('', 'Any')] + UserProfile.GENDER_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    education = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Education level or field'
        })
    )
    
    profession = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Profession or occupation'
        })
    )
    
    village = forms.ModelChoiceField(
        queryset=Village.objects.all(),
        required=False,
        empty_label="Any Village",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        age_min = cleaned_data.get('age_min')
        age_max = cleaned_data.get('age_max')
        
        if age_min and age_max and age_min > age_max:
            raise forms.ValidationError("Minimum age cannot be greater than maximum age")
        
        return cleaned_data 

class RelationshipRequestForm(forms.ModelForm):
    class Meta:
        model = RelationshipRequest
        fields = ['relationship_type', 'message']
        widgets = {
            'relationship_type': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add a personal message (optional)'}),
        } 