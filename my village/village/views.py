from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Village, UserProfile, Relationship, CommunityEvent, EventContribution, VillageService, District, Block, PoliceStation, PostOffice, Panchayat, AadhaarVerification, RelationshipRequest
from .forms import AadhaarVerificationForm, CommunityEventForm, UserProfileForm, UserSearchForm, RelationshipRequestForm
from .serializers import (
    UserSerializer, VillageSerializer, UserProfileSerializer,
    RelationshipSerializer, CommunityEventSerializer,
    EventContributionSerializer, VillageServiceSerializer
)
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
import networkx as nx
import matplotlib.pyplot as plt
import io
import base64
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm

def home(request):
    """Home page view."""
    featured_villages = Village.objects.all()[:3]
    upcoming_events = CommunityEvent.objects.filter(start_date__gte=timezone.now()).order_by('start_date')[:4]
    return render(request, 'village/home.html', {
        'featured_villages': featured_villages,
        'upcoming_events': upcoming_events
    })

def custom_login(request):
    """Custom login view with remember me functionality."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Check if remember me is checked
                if request.POST.get('remember_me'):
                    # Set session expiry to 2 weeks (in seconds)
                    request.session.set_expiry(1209600)  # 2 weeks
                else:
                    # Set session expiry to browser close
                    request.session.set_expiry(0)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'village/login.html', {'form': form})

def village_list(request):
    """List all villages."""
    # Get or create user profile if user is authenticated
    user_profile = None
    if request.user.is_authenticated:
        user_profile, created = UserProfile.objects.get_or_create(
            user=request.user,
            defaults={
                'aadhaar_verified': False
            }
        )
    
    # Get all districts for the filter
    districts = District.objects.all().order_by('name')
    
    # Get selected filters
    selected_district = request.GET.get('district')
    selected_block = request.GET.get('block')
    selected_police_station = request.GET.get('police_station')
    selected_post_office = request.GET.get('post_office')
    selected_panchayat = request.GET.get('panchayat')
    
    # Initialize querysets
    blocks = Block.objects.none()
    police_stations = PoliceStation.objects.none()
    post_offices = PostOffice.objects.none()
    panchayats = Panchayat.objects.none()
    villages = Village.objects.all()
    
    # Apply filters
    if selected_district:
        blocks = Block.objects.filter(district_id=selected_district).order_by('name')
        villages = villages.filter(panchayat__post_office__police_station__block__district_id=selected_district)
        
        if selected_block:
            police_stations = PoliceStation.objects.filter(block_id=selected_block).order_by('name')
            villages = villages.filter(panchayat__post_office__police_station__block_id=selected_block)
            
            if selected_police_station:
                post_offices = PostOffice.objects.filter(police_station_id=selected_police_station).order_by('name')
                villages = villages.filter(panchayat__post_office__police_station_id=selected_police_station)
                
                if selected_post_office:
                    panchayats = Panchayat.objects.filter(post_office_id=selected_post_office).order_by('name')
                    villages = villages.filter(panchayat__post_office_id=selected_post_office)
                    
                    if selected_panchayat:
                        villages = villages.filter(panchayat_id=selected_panchayat)
    
    context = {
        'user_profile': user_profile,
        'districts': districts,
        'blocks': blocks,
        'police_stations': police_stations,
        'post_offices': post_offices,
        'panchayats': panchayats,
        'villages': villages,
        'selected_district': selected_district,
        'selected_block': selected_block,
        'selected_police_station': selected_police_station,
        'selected_post_office': selected_post_office,
        'selected_panchayat': selected_panchayat,
    }
    
    return render(request, 'village/village_list.html', context)

def village_detail(request, pk):
    """Show village details."""
    village = get_object_or_404(Village, pk=pk)
    
    # Get or create user profile if user is authenticated
    user_profile = None
    if request.user.is_authenticated:
        user_profile, created = UserProfile.objects.get_or_create(
            user=request.user,
            defaults={
                'aadhaar_verified': False
            }
        )
    
    context = {
        'village': village,
        'user_profile': user_profile,
    }
    return render(request, 'village/village_detail.html', context)

@login_required
def village_create(request):
    """Create a new village."""
    if request.method == 'POST':
        # Handle form submission
        name = request.POST.get('name')
        district_id = request.POST.get('district')
        block_name = request.POST.get('block')
        police_station_name = request.POST.get('police_station')
        post_office_name = request.POST.get('post_office')
        panchayat_name = request.POST.get('panchayat')
        
        # Get the district
        district = get_object_or_404(District, id=district_id)
        
        # Create block
        from .models import Block
        block, _ = Block.objects.get_or_create(
            name=block_name,
            district=district
        )
        
        # Create police station
        from .models import PoliceStation
        police_station, _ = PoliceStation.objects.get_or_create(
            name=police_station_name,
            block=block
        )
        
        # Create post office
        from .models import PostOffice
        post_office, _ = PostOffice.objects.get_or_create(
            name=post_office_name,
            police_station=police_station
        )
        
        # Create panchayat
        from .models import Panchayat
        panchayat, _ = Panchayat.objects.get_or_create(
            name=panchayat_name,
            post_office=post_office
        )
        
        # Create village
        village = Village.objects.create(
            name=name,
            panchayat=panchayat
        )
        
        # Add the creator as a member
        user_profile = request.user.userprofile
        user_profile.village = village
        user_profile.save()
        
        messages.success(request, f'Village {name} created successfully!')
        return redirect('village_detail', pk=village.pk)
    
    # Get all districts for the form
    districts = District.objects.all()
    return render(request, 'village/village_form.html', {'districts': districts})

def event_list(request):
    """List all events."""
    events = CommunityEvent.objects.all()
    return render(request, 'village/event_list.html', {'events': events})

def event_detail(request, pk):
    """Show event details."""
    event = get_object_or_404(CommunityEvent, pk=pk)
    return render(request, 'village/event_detail.html', {'event': event})

@login_required
def event_create(request, village_id=None):
    """Create a new event."""
    # Get user profile
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    # Check if user has a village
    if not user_profile.village:
        messages.error(request, 'You need to be a member of a village to create events.')
        return redirect('village_list')
    
    # Initialize form with user
    form = CommunityEventForm(user=request.user)
    
    if request.method == 'POST':
        form = CommunityEventForm(user=request.user, data=request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = user_profile
            event.save()
            
            messages.success(request, f'Event "{event.title}" created successfully!')
            return redirect('event_detail', pk=event.pk)
    
    # If village_id is provided, pre-select that village
    if village_id:
        try:
            village = Village.objects.get(pk=village_id)
            # Check if the village is in the same panchayat as the user's village
            if village.panchayat == user_profile.village.panchayat:
                form.fields['village'].initial = village
            else:
                messages.warning(request, 'You can only create events for your village or other villages in the same panchayat.')
        except Village.DoesNotExist:
            pass
    
    return render(request, 'village/event_form.html', {
        'form': form,
        'user_village': user_profile.village,
        'panchayat': user_profile.village.panchayat if user_profile.village else None
    })

@login_required
def event_contribute(request, pk):
    """Contribute to an event."""
    event = get_object_or_404(CommunityEvent, pk=pk)
    
    if request.method == 'POST':
        # Handle form submission
        contribution_type = request.POST.get('contribution_type')
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        
        contribution = EventContribution.objects.create(
            event=event,
            contributor=request.user.userprofile,
            contribution_type=contribution_type,
            amount=amount,
            description=description
        )
        
        messages.success(request, 'Contribution added successfully!')
        return redirect('event_detail', pk=event.pk)
    
    return redirect('event_detail', pk=event.pk)

def service_list(request):
    """List all services."""
    services = VillageService.objects.all()
    return render(request, 'village/service_list.html', {'services': services})

def service_detail(request, pk):
    """Show service details."""
    service = get_object_or_404(VillageService, pk=pk)
    return render(request, 'village/service_detail.html', {'service': service})

@login_required
def service_create(request, village_id=None):
    """Create a new service."""
    if request.method == 'POST':
        # Handle form submission
        name = request.POST.get('name')
        service_type = request.POST.get('service_type')
        description = request.POST.get('description')
        address = request.POST.get('address')
        contact_number = request.POST.get('contact_number')
        village_id = request.POST.get('village')
        
        village = get_object_or_404(Village, pk=village_id)
        
        service = VillageService.objects.create(
            name=name,
            service_type=service_type,
            description=description,
            address=address,
            contact_number=contact_number,
            village=village
        )
        
        messages.success(request, f'Service {name} added successfully!')
        return redirect('service_detail', pk=service.pk)
    
    villages = Village.objects.all()
    context = {'villages': villages}
    
    if village_id:
        context['selected_village'] = get_object_or_404(Village, pk=village_id)
    
    return render(request, 'village/service_form.html', context)

@login_required
def profile(request):
    """User profile view."""
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            profile = form.save(commit=False)
            # Always preserve the village field value
            profile.village = user_profile.village
            profile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)
    
    return render(request, 'village/profile.html', {
        'form': form,
        'user_profile': user_profile,
        'is_editing': request.GET.get('edit') == 'true'
    })

@login_required
def my_relationships(request):
    """User relationships view with search functionality."""
    # Get user's relationships
    relationships = Relationship.objects.filter(user=request.user.userprofile)
    
    # Initialize search form
    search_form = UserSearchForm(request.GET)
    users = UserProfile.objects.exclude(user=request.user)  # Exclude current user
    
    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('search_query')
        age_min = search_form.cleaned_data.get('age_min')
        age_max = search_form.cleaned_data.get('age_max')
        gender = search_form.cleaned_data.get('gender')
        education = search_form.cleaned_data.get('education')
        profession = search_form.cleaned_data.get('profession')
        village = search_form.cleaned_data.get('village')
        
        # Apply filters
        if search_query:
            users = users.filter(
                Q(user__first_name__icontains=search_query) |
                Q(user__last_name__icontains=search_query) |
                Q(nickname__icontains=search_query) |
                Q(education__icontains=search_query) |
                Q(profession__icontains=search_query)
            )
        
        if age_min:
            users = users.filter(age__gte=age_min)
        
        if age_max:
            users = users.filter(age__lte=age_max)
        
        if gender:
            users = users.filter(gender=gender)
        
        if education:
            users = users.filter(education__icontains=education)
        
        if profession:
            users = users.filter(profession__icontains=profession)
        
        if village:
            users = users.filter(village=village)
    
    # Get existing relationships for the filtered users
    existing_relationships = {
        rel.related_user.id: rel.relationship_type 
        for rel in relationships
    }
    
    context = {
        'relationships': relationships,
        'search_form': search_form,
        'users': users,
        'existing_relationships': existing_relationships
    }
    
    return render(request, 'village/relationships.html', context)

@login_required
def join_village(request, pk):
    village = get_object_or_404(Village, pk=pk)
    
    # Create UserProfile if it doesn't exist
    userprofile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'aadhaar_verified': False
        }
    )
    
    # Check if user is already a member of any village
    if userprofile.village:
        messages.warning(request, 'You are already a member of another village.')
        return redirect('village_detail', pk=userprofile.village.pk)
    
    # Check if user has a pending verification
    pending_verification = AadhaarVerification.objects.filter(
        user_profile=userprofile,
        status='pending'
    ).first()
    
    if pending_verification:
        messages.info(request, 'Your Aadhaar verification is pending. Please wait for approval.')
        return redirect('village_detail', pk=pk)
    
    # Check if user has a rejected verification
    rejected_verification = AadhaarVerification.objects.filter(
        user_profile=userprofile,
        status='rejected'
    ).first()
    
    if rejected_verification:
        messages.error(request, 'Your previous Aadhaar verification was rejected. Please try again.')
        return redirect('village_detail', pk=pk)
    
    # If user is not verified, show verification form
    if not userprofile.aadhaar_verified:
        if request.method == 'POST':
            form = AadhaarVerificationForm(request.POST)
            if form.is_valid():
                verification = form.save(commit=False)
                verification.user_profile = userprofile
                verification.village = village
                verification.save()
                messages.success(request, 'Aadhaar verification submitted successfully. Please wait for approval.')
                return redirect('village_detail', pk=pk)
        else:
            form = AadhaarVerificationForm(initial={'village': village})
        
        return render(request, 'village/aadhaar_verification.html', {
            'form': form,
            'village': village
        })
    
    # If user is verified, add them to the village
    userprofile.village = village
    userprofile.save()
    messages.success(request, f'Welcome to {village.name}! You are now a member of this village.')
    return redirect('village_detail', pk=pk)

@login_required
def verify_aadhaar(request, verification_id):
    """Admin view to verify Aadhaar submissions."""
    verification = get_object_or_404(AadhaarVerification, pk=verification_id)
    
    # Only superusers can verify
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to verify Aadhaar submissions.')
        return redirect('home')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        notes = request.POST.get('notes', '')
        
        if action == 'approve':
            verification.status = 'approved'
            verification.reviewed_date = timezone.now()
            verification.reviewed_by = request.user
            verification.notes = notes
            verification.save()
            
            # Update user profile
            user_profile = verification.user_profile
            user_profile.village = verification.village
            user_profile.aadhaar_verified = True
            user_profile.save()
            
            messages.success(request, f'Aadhaar verification for {verification.user_profile.user.username} has been approved.')
        elif action == 'reject':
            verification.status = 'rejected'
            verification.reviewed_date = timezone.now()
            verification.reviewed_by = request.user
            verification.notes = notes
            verification.save()
            
            messages.success(request, f'Aadhaar verification for {verification.user_profile.user.username} has been rejected.')
        
        return redirect('pending_verifications')
    
    return render(request, 'village/verify_aadhaar.html', {
        'verification': verification
    })

@login_required
def pending_verifications(request):
    """List all pending Aadhaar verifications."""
    # Only superusers can view pending verifications
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to view pending verifications.')
        return redirect('home')
    
    pending_verifications = AadhaarVerification.objects.filter(status='pending').order_by('-submitted_at')
    
    return render(request, 'village/pending_verifications.html', {
        'pending_verifications': pending_verifications
    })

def member_list(request):
    """List all members."""
    members = UserProfile.objects.all()
    villages = Village.objects.all()
    return render(request, 'village/member_list.html', {'members': members, 'villages': villages})

def member_detail(request, pk):
    """Show member details."""
    member = get_object_or_404(UserProfile, pk=pk)
    return render(request, 'village/member_detail.html', {'member': member})

@login_required
def member_create(request):
    """Create a new member."""
    if request.method == 'POST':
        # Handle form submission
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        village_id = request.POST.get('village')
        address = request.POST.get('address')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        occupation = request.POST.get('occupation')
        
        # Create user
        user = User.objects.create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        
        # Create user profile
        village = get_object_or_404(Village, pk=village_id)
        user_profile = UserProfile.objects.create(
            user=user,
            village=village,
            profession=occupation
        )
        
        messages.success(request, f'Member {first_name} {last_name} added successfully!')
        return redirect('member_detail', pk=user_profile.pk)
    
    villages = Village.objects.all()
    return render(request, 'village/member_form.html', {'villages': villages})

def profile_detail(request, pk):
    """Show profile details."""
    profile = get_object_or_404(UserProfile, pk=pk)
    return render(request, 'village/profile_detail.html', {'profile': profile})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'village/register.html', {'form': form})

# Create your views here.

class VillageViewSet(viewsets.ModelViewSet):
    queryset = Village.objects.all()
    serializer_class = VillageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['get'])
    def services(self, request, pk=None):
        village = self.get_object()
        services = VillageService.objects.filter(village=village)
        serializer = VillageServiceSerializer(services, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def events(self, request, pk=None):
        village = self.get_object()
        events = CommunityEvent.objects.filter(village=village)
        serializer = CommunityEventSerializer(events, many=True)
        return Response(serializer.data)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['get'])
    def relationships(self, request, pk=None):
        profile = self.get_object()
        relationships = Relationship.objects.filter(user=profile)
        serializer = RelationshipSerializer(relationships, many=True)
        return Response(serializer.data)

class RelationshipViewSet(viewsets.ModelViewSet):
    queryset = Relationship.objects.all()
    serializer_class = RelationshipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.userprofile)

class CommunityEventViewSet(viewsets.ModelViewSet):
    queryset = CommunityEvent.objects.all()
    serializer_class = CommunityEventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.userprofile)

    @action(detail=True, methods=['post'])
    def contribute(self, request, pk=None):
        event = self.get_object()
        serializer = EventContributionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                event=event,
                contributor=request.user.userprofile
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventContributionViewSet(viewsets.ModelViewSet):
    queryset = EventContribution.objects.all()
    serializer_class = EventContributionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(contributor=self.request.user.userprofile)

class VillageServiceViewSet(viewsets.ModelViewSet):
    queryset = VillageService.objects.all()
    serializer_class = VillageServiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

@login_required
def event_edit(request, pk):
    """Edit an existing event."""
    event = get_object_or_404(CommunityEvent, pk=pk)
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    # Check if user has permission to edit
    if event.created_by != user_profile and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to edit this event.')
        return redirect('event_detail', pk=pk)
    
    if request.method == 'POST':
        form = CommunityEventForm(user=request.user, data=request.POST, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            event.save()
            messages.success(request, f'Event "{event.title}" updated successfully!')
            return redirect('event_detail', pk=event.pk)
    else:
        form = CommunityEventForm(user=request.user, instance=event)
    
    return render(request, 'village/event_form.html', {
        'form': form,
        'event': event,
        'user_village': user_profile.village,
        'panchayat': user_profile.village.panchayat if user_profile.village else None,
        'is_edit': True
    })

@login_required
def event_delete(request, pk):
    """Delete an event."""
    event = get_object_or_404(CommunityEvent, pk=pk)
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    # Check if user has permission to delete
    if event.created_by != user_profile and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to delete this event.')
        return redirect('event_detail', pk=pk)
    
    if request.method == 'POST':
        event_title = event.title
        event.delete()
        messages.success(request, f'Event "{event_title}" deleted successfully!')
        return redirect('event_list')
    
    return render(request, 'village/event_confirm_delete.html', {
        'event': event
    })

@login_required
def add_relationship(request):
    """Add a new relationship with another user."""
    if request.method == 'POST':
        related_user_id = request.POST.get('related_user_id')
        relationship_type = request.POST.get('relationship_type')
        
        try:
            related_user_profile = UserProfile.objects.get(id=related_user_id)
            user_profile = UserProfile.objects.get(user=request.user)
            
            # Check if relationship already exists
            existing_relationship = Relationship.objects.filter(
                user=user_profile,
                related_user=related_user_profile
            ).first()
            
            if existing_relationship:
                messages.warning(request, f"You already have a relationship with {related_user_profile.user.get_full_name()}.")
                return redirect('my_relationships')
            
            # Create new relationship
            Relationship.objects.create(
                user=user_profile,
                related_user=related_user_profile,
                relationship_type=relationship_type
            )
            
            messages.success(request, f"Relationship with {related_user_profile.user.get_full_name()} added successfully!")
            return redirect('my_relationships')
            
        except UserProfile.DoesNotExist:
            messages.error(request, "User profile not found.")
            return redirect('my_relationships')
    
    return redirect('my_relationships')

@login_required
def remove_relationship(request):
    """Remove an existing relationship."""
    if request.method == 'POST':
        relationship_id = request.POST.get('relationship_id')
        
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            relationship = Relationship.objects.get(id=relationship_id, user=user_profile)
            
            # Store the name for the success message
            related_user_name = relationship.related_user.user.get_full_name()
            
            # Delete the relationship
            relationship.delete()
            
            messages.success(request, f"Relationship with {related_user_name} removed successfully!")
            return redirect('my_relationships')
            
        except (UserProfile.DoesNotExist, Relationship.DoesNotExist):
            messages.error(request, "Relationship not found.")
            return redirect('my_relationships')
    
    return redirect('my_relationships')

@login_required
def send_relationship_request(request, user_id):
    if request.method == 'POST':
        form = RelationshipRequestForm(request.POST)
        if form.is_valid():
            to_user = get_object_or_404(UserProfile, id=user_id)
            
            # Check if a relationship already exists
            existing_relationship = Relationship.objects.filter(
                Q(user=request.user.userprofile, related_user=to_user) |
                Q(user=to_user, related_user=request.user.userprofile)
            ).first()
            
            if existing_relationship:
                messages.warning(request, f"You already have a relationship with {to_user.user.get_full_name() or to_user.user.username}.")
                return redirect('my_relationships')
            
            # Check if a request already exists
            existing_request = RelationshipRequest.objects.filter(
                Q(from_user=request.user.userprofile, to_user=to_user, status='pending') |
                Q(from_user=to_user, to_user=request.user.userprofile, status='pending')
            ).first()
            
            if existing_request:
                messages.warning(request, f"A relationship request already exists with {to_user.user.get_full_name() or to_user.user.username}.")
                return redirect('my_relationships')
            
            # Create new request
            relationship_request = form.save(commit=False)
            relationship_request.from_user = request.user.userprofile
            relationship_request.to_user = to_user
            relationship_request.save()
            
            messages.success(request, f'Relationship request sent to {to_user.user.get_full_name() or to_user.user.username}.')
            return redirect('my_relationships')
    else:
        form = RelationshipRequestForm()
    
    return render(request, 'village/send_request.html', {'form': form, 'to_user': get_object_or_404(UserProfile, id=user_id)})

@login_required
def relationship_requests(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    received_requests = RelationshipRequest.objects.filter(
        to_user=request.user.userprofile,
        status='pending'
    ).select_related('from_user', 'from_user__user')
    
    sent_requests = RelationshipRequest.objects.filter(
        from_user=request.user.userprofile,
        status='pending'
    ).select_related('to_user', 'to_user__user')
    
    return render(request, 'village/relationship_requests.html', {
        'received_requests': received_requests,
        'sent_requests': sent_requests
    })

@login_required
def handle_relationship_request(request, request_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        # Get the relationship request
        try:
            relationship_request = RelationshipRequest.objects.get(id=request_id)
        except RelationshipRequest.DoesNotExist:
            messages.error(request, "Relationship request not found.")
            return redirect('relationship_requests')
        
        # Check if the user is the recipient of the request
        if action in ['accept', 'reject'] and relationship_request.to_user != request.user.userprofile:
            messages.error(request, "You don't have permission to accept or reject this request.")
            return redirect('relationship_requests')
        
        # Check if the user is the sender of the request
        if action == 'cancel' and relationship_request.from_user != request.user.userprofile:
            messages.error(request, "You don't have permission to cancel this request.")
            return redirect('relationship_requests')
        
        # Handle the action
        if action == 'cancel':
            relationship_request.status = 'rejected'
            relationship_request.save()
            messages.success(request, "Request cancelled successfully.")
            return redirect('relationship_requests')
        
        if action == 'accept':
            # Check if a relationship already exists
            existing_relationship = Relationship.objects.filter(
                Q(user=relationship_request.from_user, related_user=relationship_request.to_user) |
                Q(user=relationship_request.to_user, related_user=relationship_request.from_user)
            ).first()
            
            if existing_relationship:
                messages.warning(request, f"You already have a relationship with {relationship_request.from_user.user.get_full_name() or relationship_request.from_user.user.username}.")
                relationship_request.status = 'rejected'
                relationship_request.save()
                return redirect('relationship_requests')
            
            # Create bidirectional relationships
            Relationship.objects.create(
                user=relationship_request.from_user,
                related_user=relationship_request.to_user,
                relationship_type=relationship_request.relationship_type
            )
            Relationship.objects.create(
                user=relationship_request.to_user,
                related_user=relationship_request.from_user,
                relationship_type=relationship_request.relationship_type
            )
            
            relationship_request.status = 'accepted'
            relationship_request.save()
            
            messages.success(
                request,
                f'You are now connected with {relationship_request.from_user.user.get_full_name() or relationship_request.from_user.user.username}.'
            )
            return redirect('relationship_requests')
        
        if action == 'reject':
            relationship_request.status = 'rejected'
            relationship_request.save()
            
            messages.success(
                request,
                f'You have rejected the request from {relationship_request.from_user.user.get_full_name() or relationship_request.from_user.user.username}.'
            )
            return redirect('relationship_requests')
        
        messages.error(request, "Invalid action.")
        return redirect('relationship_requests')
    
    return redirect('relationship_requests')

def relationship_graph(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Get user's profile
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        messages.error(request, 'Please complete your profile first.')
        return redirect('profile_create')
    
    # Create a new directed graph
    G = nx.DiGraph()
    
    # Add the current user as the central node
    G.add_node(request.user.id, 
               label=request.user.get_full_name() or request.user.username,
               color='#FFD700')  # Gold color for current user
    
    # Get all relationships
    relationships = Relationship.objects.filter(
        Q(from_user=request.user) | Q(to_user=request.user)
    ).select_related('from_user', 'to_user')
    
    # Color mapping for different relationship types
    color_map = {
        'family': '#FF6B6B',      # Red
        'friend': '#4ECDC4',      # Turquoise
        'classmate': '#45B7D1',   # Blue
        'colleague': '#96CEB4',   # Green
        'neighbor': '#FFEEAD',    # Yellow
        'other': '#D4A5A5'        # Pink
    }
    
    # Add nodes and edges for each relationship
    for rel in relationships:
        # Determine the other user in the relationship
        other_user = rel.to_user if rel.from_user == request.user else rel.from_user
        
        # Add the other user as a node
        G.add_node(other_user.id,
                  label=other_user.get_full_name() or other_user.username,
                  color=color_map.get(rel.relationship_type, color_map['other']))
        
        # Add edge with relationship type as label
        G.add_edge(request.user.id, other_user.id, 
                  label=rel.get_relationship_type_display())
    
    # Create the plot
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, k=1, iterations=50)
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, 
                          node_color=[G.nodes[node]['color'] for node in G.nodes()],
                          node_size=2000)
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, arrowsize=20)
    
    # Draw labels
    nx.draw_networkx_labels(G, pos, 
                          labels={node: G.nodes[node]['label'] for node in G.nodes()},
                          font_size=10)
    
    # Draw edge labels
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    
    # Save the plot to a bytes buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=300)
    buffer.seek(0)
    plt.close()
    
    # Convert the plot to base64 string
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    # Get relationship statistics
    relationship_stats = {
        'total': relationships.count(),
        'by_type': {}
    }
    
    for rel_type, _ in Relationship.RELATIONSHIP_TYPES:
        count = relationships.filter(relationship_type=rel_type).count()
        relationship_stats['by_type'][rel_type] = count
    
    context = {
        'graph_image': image_base64,
        'relationship_stats': relationship_stats,
        'color_map': color_map
    }
    
    return render(request, 'village/relationship_graph.html', context)

def custom_logout(request):
    """Custom logout view."""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')

def logout_view(request):
    """Alias for custom_logout to maintain URL pattern compatibility."""
    return custom_logout(request)

@login_required
def dismiss_banner(request):
    """Handle banner dismissal request."""
    if request.method == 'POST':
        try:
            profile = request.user.userprofile
            profile.banner_dismissed = True
            profile.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

@login_required
def aadhaar_verification(request):
    if request.user.userprofile.aadhaar_verified:
        messages.success(request, 'Your Aadhaar number is already verified.')
        return redirect('profile')
        
    if request.method == 'POST':
        # Check if there's already a pending verification
        pending_verification = AadhaarVerification.objects.filter(
            user_profile=request.user.userprofile,
            status='pending'
        ).first()
        
        if pending_verification:
            messages.warning(request, 'You already have a pending verification request. Please wait for it to be reviewed.')
            return redirect('aadhaar_verification')
            
        # Check if there's a rejected verification
        rejected_verification = AadhaarVerification.objects.filter(
            user_profile=request.user.userprofile,
            status='rejected'
        ).first()
        
        # Create new verification request
        try:
            verification = AadhaarVerification(
                user_profile=request.user.userprofile,
                aadhaar_number=request.POST.get('aadhaar_number'),
                front_image=request.FILES.get('front_image'),
                back_image=request.FILES.get('back_image'),
                status='pending'
            )
            verification.save()
            
            messages.success(request, 'Your Aadhaar verification request has been submitted. We will review it within 24-48 hours.')
            return redirect('profile')
            
        except Exception as e:
            messages.error(request, 'There was an error submitting your verification request. Please try again.')
            return redirect('aadhaar_verification')
            
    return render(request, 'village/aadhaar_verification.html')

@login_required
def approve_verification(request, verification_id):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to approve verifications.")
        return redirect('home')
    
    verification = get_object_or_404(AadhaarVerification, id=verification_id)
    verification.status = 'approved'
    verification.reviewed_by = request.user
    verification.reviewed_at = timezone.now()
    verification.save()
    
    userprofile = verification.user_profile
    userprofile.aadhaar_verified = True
    userprofile.save()
    
    messages.success(request, "Aadhaar verification approved successfully.")
    return redirect('pending_verifications')

@login_required
def reject_verification(request, verification_id):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to reject verifications.")
        return redirect('home')
    
    verification = get_object_or_404(AadhaarVerification, id=verification_id)
    verification.status = 'rejected'
    verification.reviewed_by = request.user
    verification.reviewed_at = timezone.now()
    verification.save()
    
    messages.success(request, "Aadhaar verification rejected successfully.")
    return redirect('pending_verifications')
