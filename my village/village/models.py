from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class District(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100, default='Bihar')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

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

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    village = models.ForeignKey(Village, on_delete=models.CASCADE, null=True, blank=True)
    education = models.TextField(blank=True)
    profession = models.CharField(max_length=200, blank=True)
    hobbies = models.TextField(blank=True)
    achievements = models.TextField(blank=True)
    social_contributions = models.TextField(blank=True)
    aadhaar_verified = models.BooleanField(default=False)
    banner_dismissed = models.BooleanField(default=False, help_text="Whether the user has dismissed the Aadhaar verification banner")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # New fields
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True)
    father_name = models.CharField(max_length=100, blank=True)
    mother_name = models.CharField(max_length=100, blank=True)
    nickname = models.CharField(max_length=50, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class AadhaarVerification(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='aadhaar_verifications')
    aadhaar_number = models.CharField(max_length=12)
    front_image = models.ImageField(upload_to='aadhaar/front/')
    back_image = models.ImageField(upload_to='aadhaar/back/')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_verifications')
    notes = models.TextField(blank=True)
    rejection_reason = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"Aadhaar Verification for {self.user_profile.user.username}"
    
    def approve(self, reviewer):
        self.status = 'approved'
        self.reviewed_at = timezone.now()
        self.reviewed_by = reviewer
        self.save()
        
        # Update user profile
        self.user_profile.aadhaar_verified = True
        self.user_profile.save()
    
    def reject(self, reviewer, reason):
        self.status = 'rejected'
        self.reviewed_at = timezone.now()
        self.reviewed_by = reviewer
        self.rejection_reason = reason
        self.save()

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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # New fields
    location = models.CharField(max_length=200, blank=True, help_text="Specific location within the village")
    expected_attendees = models.PositiveIntegerField(default=0, help_text="Expected number of attendees")
    is_public = models.BooleanField(default=True, help_text="Whether the event is open to all village members")
    requires_registration = models.BooleanField(default=False, help_text="Whether attendees need to register")
    registration_deadline = models.DateTimeField(null=True, blank=True, help_text="Deadline for registration if required")
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Estimated budget for the event")
    contact_person = models.CharField(max_length=100, blank=True, help_text="Person to contact for more information")
    contact_phone = models.CharField(max_length=15, blank=True, help_text="Contact phone number")
    notes = models.TextField(blank=True, help_text="Additional notes or instructions")

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

    def __str__(self):
        return f"{self.contributor.user.username} - {self.event.title}"

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
        return f"{self.name} - {self.get_service_type_display()}"
