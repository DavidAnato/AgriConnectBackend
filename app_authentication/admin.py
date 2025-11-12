from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Configuration de base
    model = User
    list_display = ['email', 'get_full_name', 'role_badge', 'status_badge', 'date_joined_formatted', 'actions_column']
    list_filter = ['role', 'is_active', 'is_staff', 'verified_email', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name', 'phone_number']
    ordering = ['-date_joined']
    list_per_page = 25
    
    # Configuration des fieldsets pour le formulaire
    fieldsets = (
        ('👤 Informations personnelles', {
            'fields': ('email', 'first_name', 'last_name', 'phone_number', 'profile_picture')
        }),
        ('🔐 Authentification', {
            'fields': ('password', 'code_pin', 'google_id', 'otp_code', 'otp_generated_at'),
            'classes': ('collapse',)
        }),
        ('🏊 Rôle et permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser'),
        }),
        ('✉️ Vérification email', {
            'fields': ('verified_email',),
            'classes': ('collapse',)
        }),
        ('📅 Dates', {
            'fields': ('date_joined', 'last_login'),
            'classes': ('collapse',)
        }),
    )
    
    # Configuration pour la création d'un nouvel utilisateur
    add_fieldsets = (
        ('👤 Nouvel utilisateur', {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )
    
    # Champs en lecture seule
    readonly_fields = ['date_joined', 'last_login', 'otp_generated_at']
    
    # Méthodes personnalisées pour l'affichage
    def get_full_name(self, obj):
        """Affiche le nom complet de l'utilisateur"""
        if obj.first_name and obj.last_name:
            return f"{obj.first_name} {obj.last_name}"
        return obj.email.split('@')[0]
    get_full_name.short_description = "Nom complet"
    get_full_name.admin_order_field = 'first_name'
    
    def role_badge(self, obj):
        """Affiche le rôle avec un badge coloré"""
        if not obj.role:
            return format_html('<span class="badge" style="background-color: #6c757d; color: white; padding: 3px 8px; border-radius: 12px;">Non défini</span>')
        
        colors = {
            'admin': '#dc3545',
            'maitre_nageur': '#007bff', 
            'piscine': '#28a745'
        }
        color = colors.get(obj.role, '#6c757d')
        role_name = dict(User.ROLE_CHOICES).get(obj.role, obj.role)
        
        return format_html(
            '<span class="badge" style="background-color: {}; color: white; padding: 3px 8px; border-radius: 12px;">{}</span>',
            color, role_name
        )
    role_badge.short_description = "Rôle"
    role_badge.admin_order_field = 'role'
    
    def status_badge(self, obj):
        """Affiche le statut avec des icônes"""
        badges = []
        
        if obj.is_active:
            badges.append('<span style="color: #28a745;">✅ Actif</span>')
        else:
            badges.append('<span style="color: #dc3545;">❌ Inactif</span>')
            
        if obj.verified_email:
            badges.append('<span style="color: #007bff;">📧 Vérifié</span>')
        else:
            badges.append('<span style="color: #ffc107;">⚠️ Non vérifié</span>')
            
        return format_html(' | '.join(badges))
    status_badge.short_description = "Statut"
    
    def date_joined_formatted(self, obj):
        """Affiche la date d'inscription formatée"""
        return obj.date_joined.strftime("%d/%m/%Y à %H:%M")
    date_joined_formatted.short_description = "Inscrit le"
    date_joined_formatted.admin_order_field = 'date_joined'
    
    def actions_column(self, obj):
        """Affiche des boutons d'actions rapides"""
        actions = []
        
        # Bouton pour voir les détails
        view_url = reverse('admin:app_authentication_user_change', args=[obj.pk])
        actions.append(f'<a href="{view_url}" style="color: #007bff; text-decoration: none;">👁️ Voir</a>')
        
        # Bouton pour activer/désactiver
        if obj.is_active:
            actions.append('<span style="color: #dc3545; cursor: pointer;">⏸️ Désactiver</span>')
        else:
            actions.append('<span style="color: #28a745; cursor: pointer;">▶️ Activer</span>')
            
        return format_html(' | '.join(actions))
    actions_column.short_description = "Actions"
    
    # Actions personnalisées
    actions = ['activate_users', 'deactivate_users', 'verify_emails']
    
    def activate_users(self, request, queryset):
        """Active les utilisateurs sélectionnés"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} utilisateur(s) activé(s) avec succès.")
    activate_users.short_description = "✅ Activer les utilisateurs sélectionnés"
    
    def deactivate_users(self, request, queryset):
        """Désactive les utilisateurs sélectionnés"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} utilisateur(s) désactivé(s) avec succès.")
    deactivate_users.short_description = "❌ Désactiver les utilisateurs sélectionnés"
    
    def verify_emails(self, request, queryset):
        """Vérifie les emails des utilisateurs sélectionnés"""
        updated = queryset.update(verified_email=True)
        self.message_user(request, f"{updated} email(s) vérifié(s) avec succès.")
    verify_emails.short_description = "📧 Vérifier les emails sélectionnés"
    
    # Personnalisation du formulaire
    def get_form(self, request, obj=None, **kwargs):
        """Personnalise le formulaire selon l'utilisateur connecté"""
        form = super().get_form(request, obj, **kwargs)
        
        # Si l'utilisateur n'est pas superuser, on limite les options
        if not request.user.is_superuser:
            if 'role' in form.base_fields:
                # Limiter les choix de rôles
                form.base_fields['role'].choices = [
                    choice for choice in User.ROLE_CHOICES 
                    if choice[0] != 'admin'
                ]
        
        return form
    
    # Méthodes pour les permissions
    def has_delete_permission(self, request, obj=None):
        """Contrôle les permissions de suppression"""
        if obj and obj.is_superuser and not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)
    
    def get_queryset(self, request):
        """Filtre les résultats selon les permissions"""
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            # Les non-superusers ne voient pas les autres admins
            qs = qs.exclude(is_superuser=True).exclude(role='admin')
        return qs


# Configuration CSS personnalisée pour l'admin
admin.site.site_header = "🏊 Administration Piscine"
admin.site.site_title = "Admin Piscine"
admin.site.index_title = "Tableau de bord"