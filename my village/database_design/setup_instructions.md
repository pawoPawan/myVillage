# My Village App - Database Setup Instructions

This document provides step-by-step instructions for implementing the My Village database design in a new Django project.

## Prerequisites

- Python 3.8 or higher
- Django 4.0 or higher
- PostgreSQL (recommended) or SQLite (for development)

## Step 1: Create a New Django Project

```bash
# Create a new Django project
django-admin startproject my_village
cd my_village

# Create a new app for the village functionality
python manage.py startapp village
```

## Step 2: Configure the Project

Edit `my_village/settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # If using Django REST Framework
    'village',  # Add the village app
]

# Configure media files for profile pictures and Aadhaar images
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

## Step 3: Create the Models

Create the following files in the `village/models.py` directory:

### 1. User Management Module

```python
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    village = models.ForeignKey('Village', on_delete=models.CASCADE, null=True, blank=True)
    education = models.TextField(blank=True)
    profession = models.CharField(max_length=200, blank=True)
    hobbies = models.TextField(blank=True)
    achievements = models.TextField(blank=True)
    social_contributions = models.TextField(blank=True)
    aadhaar_verified = models.BooleanField(default=False)
    banner_dismissed = models.BooleanField(default=False)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True)
    father_name = models.CharField(max_length=100, blank=True)
    mother_name = models.CharField(max_length=100, blank=True)
    nickname = models.CharField(max_length=50, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
```

### 2. Location Hierarchy Module

```python
class State(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}, {self.state.name}"

class Block(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}, {self.district.name}"

class PoliceStation(models.Model):
    name = models.CharField(max_length=100)
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class PostOffice(models.Model):
    name = models.CharField(max_length=100)
    police_station = models.ForeignKey(PoliceStation, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Panchayat(models.Model):
    name = models.CharField(max_length=100)
    post_office = models.ForeignKey(PostOffice, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Village(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, blank=True, null=True)
    panchayat = models.ForeignKey(Panchayat, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def post_office(self):
        return self.panchayat.post_office

    @property
    def police_station(self):
        return self.panchayat.post_office.police_station

    @property
    def block(self):
        return self.panchayat.post_office.police_station.block

    @property
    def district(self):
        return self.panchayat.post_office.police_station.block.district
```

### 3. Community Events Module

```python
class CommunityEvent(models.Model):
    EVENT_TYPES = [
        ('festival', 'Festival'),
        ('meeting', 'Meeting'),
        ('puja', 'Puja'),
        ('sports', 'Sports Event'),
        ('education', 'Educational Event'),
        ('health', 'Health Camp'),
        ('cultural', 'Cultural Program'),
        ('social', 'Social Gathering'),
        ('development', 'Development Work'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    village = models.ForeignKey(Village, on_delete=models.CASCADE, related_name='events')
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='created_events')
    location = models.CharField(max_length=200, blank=True)
    expected_attendees = models.PositiveIntegerField(default=0)
    is_public = models.BooleanField(default=True)
    requires_registration = models.BooleanField(default=False)
    registration_deadline = models.DateTimeField(null=True, blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    contact_person = models.CharField(max_length=100, blank=True)
    contact_phone = models.CharField(max_length=15, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.title

class EventContribution(models.Model):
    event = models.ForeignKey(CommunityEvent, on_delete=models.CASCADE)
    contributor = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.contributor.user.username} - {self.event.title}"
```

### 4. Village Services Module

```python
class VillageService(models.Model):
    SERVICE_TYPES = [
        ('school', 'School'),
        ('shop', 'Shop'),
        ('medical', 'Medical Facility'),
        ('other', 'Other'),
    ]

    village = models.ForeignKey(Village, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    description = models.TextField()
    address = models.TextField()
    contact_number = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
```

### 5. Relationships Module

```python
class Relationship(models.Model):
    RELATIONSHIP_TYPES = [
        ('family', 'Family'),
        ('friend', 'Friend'),
        ('neighbor', 'Neighbor'),
        ('colleague', 'Colleague'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='relationships')
    related_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='related_to')
    relationship_type = models.CharField(max_length=20, choices=RELATIONSHIP_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='accepted')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'related_user')

    def __str__(self):
        return f"{self.user.user.username} - {self.related_user.user.username} ({self.get_relationship_type_display()})"

class RelationshipRequest(models.Model):
    RELATIONSHIP_TYPES = [
        ('family', 'Family'),
        ('friend', 'Friend'),
        ('neighbor', 'Neighbor'),
        ('colleague', 'Colleague'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    from_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_requests')
    to_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_requests')
    relationship_type = models.CharField(max_length=20, choices=RELATIONSHIP_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('from_user', 'to_user')
    
    def __str__(self):
        return f"Request from {self.from_user.user.username} to {self.to_user.user.username}"
```

### 6. Aadhaar Verification Module

```python
class AadhaarVerification(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='aadhaar_verifications')
    aadhaar_number = models.CharField(max_length=12)
    front_image = models.ImageField(upload_to='aadhaar/front/')
    back_image = models.ImageField(upload_to='aadhaar/back/')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_verifications')
    rejection_reason = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-submitted_at']
        
    def __str__(self):
        return f"Aadhaar Verification for {self.user.username} - {self.status}"
        
    def approve(self, reviewer):
        self.status = 'approved'
        self.reviewed_at = timezone.now()
        self.reviewed_by = reviewer
        self.save()
        
        # Update user profile
        self.user.userprofile.aadhaar_verified = True
        self.user.userprofile.save()
        
    def reject(self, reviewer, reason):
        self.status = 'rejected'
        self.reviewed_at = timezone.now()
        self.reviewed_by = reviewer
        self.rejection_reason = reason
        self.save()
```

## Step 4: Create Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Step 5: Register Models in Admin

Edit `village/admin.py`:

```python
from django.contrib import admin
from .models import (
    UserProfile, State, District, Block, PoliceStation, PostOffice, 
    Panchayat, Village, CommunityEvent, EventContribution, VillageService,
    Relationship, RelationshipRequest, AadhaarVerification
)

admin.site.register(UserProfile)
admin.site.register(State)
admin.site.register(District)
admin.site.register(Block)
admin.site.register(PoliceStation)
admin.site.register(PostOffice)
admin.site.register(Panchayat)
admin.site.register(Village)
admin.site.register(CommunityEvent)
admin.site.register(EventContribution)
admin.site.register(VillageService)
admin.site.register(Relationship)
admin.site.register(RelationshipRequest)
admin.site.register(AadhaarVerification)
```

## Step 6: Create Forms

Create `village/forms.py`:

```python
from django import forms
from .models import (
    UserProfile, CommunityEvent, Village, AadhaarVerification, 
    RelationshipRequest
)

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
            'education': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'profession': forms.TextInput(attrs={'class': 'form-control'}),
            'hobbies': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'achievements': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'social_contributions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control'}),
            'nickname': forms.TextInput(attrs={'class': 'form-control'}),
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
```

## Step 7: Create Views

Create the necessary views in `village/views.py`. Refer to the existing views in the My Village app for implementation details.

## Step 8: Create URLs

Edit `my_village/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('village.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

Create `village/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:pk>/', views.profile_detail, name='profile_detail'),
    path('villages/', views.village_list, name='village_list'),
    path('villages/<int:pk>/', views.village_detail, name='village_detail'),
    path('villages/create/', views.village_create, name='village_create'),
    path('villages/<int:pk>/join/', views.join_village, name='join_village'),
    path('events/', views.event_list, name='event_list'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/<int:pk>/edit/', views.event_edit, name='event_edit'),
    path('events/<int:pk>/delete/', views.event_delete, name='event_delete'),
    path('events/<int:pk>/contribute/', views.event_contribute, name='event_contribute'),
    path('services/', views.service_list, name='service_list'),
    path('services/<int:pk>/', views.service_detail, name='service_detail'),
    path('services/create/', views.service_create, name='service_create'),
    path('aadhaar/verify/', views.aadhaar_verification, name='aadhaar_verification'),
    path('verify-aadhaar/<int:verification_id>/', views.verify_aadhaar, name='verify_aadhaar'),
    path('pending-verifications/', views.pending_verifications, name='pending_verifications'),
    path('relationships/', views.my_relationships, name='my_relationships'),
    path('relationships/graph/', views.relationship_graph, name='relationship_graph'),
    path('relationships/send-request/<int:user_id>/', views.send_relationship_request, name='send_relationship_request'),
    path('relationships/add/', views.add_relationship, name='add_relationship'),
    path('relationships/remove/', views.remove_relationship, name='remove_relationship'),
]
```

## Step 9: Create Templates

Create the necessary templates in the `village/templates/village/` directory. Refer to the existing templates in the My Village app for implementation details.

## Step 10: Run the Development Server

```bash
python manage.py runserver
```

## Additional Considerations

1. **Authentication**: Implement user authentication using Django's built-in authentication system.

2. **Permissions**: Set up appropriate permissions for different user roles.

3. **API**: If needed, create a REST API using Django REST Framework.

4. **Data Migration**: Create a data migration script to populate the database with initial data.

5. **Testing**: Write tests for the models, views, and forms.

6. **Deployment**: Configure the application for production deployment.

By following these steps, you can implement the My Village database design in a new Django project. The design is modular and can be extended as needed to accommodate additional functionality. 