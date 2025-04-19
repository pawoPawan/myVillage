from django.contrib import admin
from .models import (
    District, Block, PoliceStation, PostOffice, Panchayat, Village,
    UserProfile, Relationship, CommunityEvent, VillageService
)

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'created_at')
    search_fields = ('name', 'state')
    list_filter = ('state',)

@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ('name', 'district', 'created_at')
    search_fields = ('name', 'district__name')
    list_filter = ('district',)

@admin.register(PoliceStation)
class PoliceStationAdmin(admin.ModelAdmin):
    list_display = ('name', 'block', 'created_at')
    search_fields = ('name', 'block__name')
    list_filter = ('block__district',)

@admin.register(PostOffice)
class PostOfficeAdmin(admin.ModelAdmin):
    list_display = ('name', 'police_station', 'created_at')
    search_fields = ('name', 'police_station__name')
    list_filter = ('police_station__block__district',)

@admin.register(Panchayat)
class PanchayatAdmin(admin.ModelAdmin):
    list_display = ('name', 'post_office', 'created_at')
    search_fields = ('name', 'post_office__name')
    list_filter = ('post_office__police_station__block__district',)

@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):
    list_display = ('name', 'panchayat', 'block', 'district', 'created_at')
    search_fields = ('name', 'panchayat__name')
    list_filter = ('panchayat__post_office__police_station__block__district',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'village', 'profession', 'created_at')
    search_fields = ('user__username', 'village__name', 'profession')
    list_filter = ('village__panchayat__post_office__police_station__block__district',)

@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    list_display = ('user', 'related_user', 'relationship_type', 'created_at')
    search_fields = ('user__user__username', 'related_user__user__username')
    list_filter = ('relationship_type',)

@admin.register(CommunityEvent)
class CommunityEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'village', 'event_type', 'start_date', 'end_date')
    search_fields = ('title', 'village__name')
    list_filter = ('event_type', 'village__panchayat__post_office__police_station__block__district')

@admin.register(VillageService)
class VillageServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'village', 'service_type', 'contact_number')
    search_fields = ('name', 'village__name')
    list_filter = ('service_type', 'village__panchayat__post_office__police_station__block__district')
