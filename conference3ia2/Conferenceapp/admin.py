from django.contrib import admin
from .models import Conference, Submission, Organizingcommitee


# --- Inline pour afficher les soumissions liées à une conférence ---
class SubmissionStackedInline(admin.StackedInline):
    model = Submission
    extra = 0  # ne pas afficher de lignes vides supplémentaires
    fields = ("submission_id", "title", "abstract", "user", "status", "payed", "submission_date")
    readonly_fields = ("submission_id", "submission_date")  # champs en lecture seule


# --- Admin pour le modèle Conference ---
@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    # Colonnes affichées dans la liste
    list_display = ("name", "theme", "location", "start_date", "end_date", "duration")

    # Méthode pour calculer la durée (en jours)
    def duration(self, obj):
        if obj.start_date and obj.end_date:
            return (obj.end_date - obj.start_date).days
        return "-"
    duration.short_description = "Durée (jours)"

    # Filtres
    list_filter = ("theme", "location", "start_date")

    # Recherche
    search_fields = ("name", "description", "location")

    # Organisation du formulaire
    fieldsets = (
        ("Informations générales", {
            "fields": ("name", "theme", "description")
        }),
        ("Logistique", {
            "fields": ("location", "start_date", "end_date")
        }),
    )

    # Ordre et navigation par date
    ordering = ("start_date",)
    date_hierarchy = "start_date"

    # Ajout de l'inline pour les soumissions
    inlines = [SubmissionStackedInline]


# --- Admin pour le modèle Submission ---
@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "status",
        "user",
        "conference",
        "submission_date",
        "payed",
        "short_abstract",
    )

    # Filtres et recherche
    list_filter = ("status", "payed", "conference", "submission_date")
    search_fields = ("title", "keywords", "user__username")

    # Lecture seule pour certains champs
    readonly_fields = ("submission_id", "submission_date", "created_at", "updated_at")

    # Organisation du formulaire par sections
    fieldsets = (
        ("Infos générales", {
            "fields": ("submission_id", "title", "abstract", "keywords")
        }),
        ("Fichier et conférence", {
            "fields": ("paper", "conference")
        }),
        ("Suivi", {
            "fields": ("status", "payed", "submission_date", "user")
        }),
    )

    # Actions personnalisées
    actions = ["mark_as_payed", "accept_submissions"]

    # Méthodes d'action
    def mark_as_payed(self, request, queryset):
        queryset.update(payed=True)
    mark_as_payed.short_description = "Marquer les soumissions sélectionnées comme payées"

    def accept_submissions(self, request, queryset):
        queryset.update(status="accepted")
    accept_submissions.short_description = "Accepter les soumissions sélectionnées"

    # Méthode pour tronquer l'abstract
    def short_abstract(self, obj):
        return obj.abstract[:50] + "..." if len(obj.abstract) > 50 else obj.abstract
    short_abstract.short_description = "Abstract (court)"


# --- Admin pour le modèle Organizingcommitee ---
admin.site.register(Organizingcommitee)


# --- Personnalisation du site d’administration ---
admin.site.site_title = "Gestion Conférence 25/26"
admin.site.site_header = "Gestion des conférences"
admin.site.index_title = "Application Django Conférences"
