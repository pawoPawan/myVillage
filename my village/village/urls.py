from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from . import views

# API Router
router = DefaultRouter()
router.register(r'villages', views.VillageViewSet)
router.register(r'profiles', views.UserProfileViewSet)
router.register(r'relationships', views.RelationshipViewSet)
router.register(r'events', views.CommunityEventViewSet)
router.register(r'contributions', views.EventContributionViewSet)
router.register(r'services', views.VillageServiceViewSet)

# API URLs
api_urlpatterns = [
    path('', include(router.urls)),
]

# Template URLs
template_urlpatterns = [
    # Authentication URLs
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='village/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='village/password_change_done.html'), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='village/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='village/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='village/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='village/password_reset_complete.html'), name='password_reset_complete'),
    path('dismiss-banner/', views.dismiss_banner, name='dismiss_banner'),
    
    # Village URLs
    path('villages/', views.village_list, name='village_list'),
    path('villages/<int:pk>/', views.village_detail, name='village_detail'),
    path('villages/create/', views.village_create, name='village_create'),
    path('villages/<int:pk>/join/', views.join_village, name='join_village'),
    path('villages/<int:pk>/verify-aadhaar/', views.join_village, name='aadhaar_verification'),
    path('verify-aadhaar/<int:verification_id>/', views.verify_aadhaar, name='verify_aadhaar'),
    path('pending-verifications/', views.pending_verifications, name='pending_verifications'),
    
    # Event URLs
    path('events/', views.event_list, name='event_list'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/<int:pk>/edit/', views.event_edit, name='event_edit'),
    path('events/<int:pk>/delete/', views.event_delete, name='event_delete'),
    path('events/<int:pk>/contribute/', views.event_contribute, name='event_contribute'),
    
    # Service URLs
    path('services/', views.service_list, name='service_list'),
    path('services/create/', views.service_create, name='service_create'),
    path('services/<int:pk>/', views.service_detail, name='service_detail'),
    
    # Member URLs
    path('members/', views.member_list, name='member_list'),
    path('members/create/', views.member_create, name='member_create'),
    path('members/<int:pk>/', views.member_detail, name='member_detail'),
    
    # Profile URLs
    path('profile/', views.profile, name='profile'),
    path('aadhaar/verify/', views.aadhaar_verification, name='aadhaar_verification'),
    path('aadhaar/pending/', views.pending_verifications, name='pending_verifications'),
    path('profile/<int:pk>/', views.profile_detail, name='profile_detail'),
    
    # Relationship URLs
    path('relationships/', views.my_relationships, name='my_relationships'),
    path('relationships/graph/', views.relationship_graph, name='relationship_graph'),
    path('relationships/requests/', views.relationship_requests, name='relationship_requests'),
    path('relationships/requests/<int:request_id>/', views.handle_relationship_request, name='handle_relationship_request'),
    path('relationships/send-request/<int:user_id>/', views.send_relationship_request, name='send_relationship_request'),
    path('relationships/add/', views.add_relationship, name='add_relationship'),
    path('relationships/remove/', views.remove_relationship, name='remove_relationship'),
]

# Combined URL patterns
urlpatterns = template_urlpatterns 