from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Village, UserProfile, Relationship, CommunityEvent, EventContribution, VillageService

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class VillageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Village
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    village = VillageSerializer(read_only=True)
    village_id = serializers.PrimaryKeyRelatedField(
        queryset=Village.objects.all(),
        source='village',
        write_only=True
    )

    class Meta:
        model = UserProfile
        fields = '__all__'

class RelationshipSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    related_user = UserProfileSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all(),
        source='user',
        write_only=True
    )
    related_user_id = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all(),
        source='related_user',
        write_only=True
    )

    class Meta:
        model = Relationship
        fields = '__all__'

class EventContributionSerializer(serializers.ModelSerializer):
    contributor = UserProfileSerializer(read_only=True)
    contributor_id = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all(),
        source='contributor',
        write_only=True
    )

    class Meta:
        model = EventContribution
        fields = '__all__'

class CommunityEventSerializer(serializers.ModelSerializer):
    village = VillageSerializer(read_only=True)
    created_by = UserProfileSerializer(read_only=True)
    contributions = EventContributionSerializer(many=True, read_only=True)
    village_id = serializers.PrimaryKeyRelatedField(
        queryset=Village.objects.all(),
        source='village',
        write_only=True
    )
    created_by_id = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all(),
        source='created_by',
        write_only=True
    )

    class Meta:
        model = CommunityEvent
        fields = '__all__'

class VillageServiceSerializer(serializers.ModelSerializer):
    village = VillageSerializer(read_only=True)
    village_id = serializers.PrimaryKeyRelatedField(
        queryset=Village.objects.all(),
        source='village',
        write_only=True
    )

    class Meta:
        model = VillageService
        fields = '__all__' 