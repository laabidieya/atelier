from django.db import models
from django.core.validators import MinLengthValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
import string
import random
from datetime import datetime, date

# -----------------------------
# Modèle Conference
# -----------------------------
class Conference(models.Model):
    conference_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    THEME = [
        ("IA", "Computer science & IA"),
        ("SE", "Sciences & Engineering"),
        ("SC", "Social Sciences"),
    ]
    theme = models.CharField(max_length=255, choices=THEME)

    location = models.CharField(max_length=50)
    description = models.TextField(
        validators=[MinLengthValidator(30, "Vous avez utilisé la limite des mots autorisés")]
    )
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("La date de début ne doit pas être supérieure à la date de fin.")

    def __str__(self):
        return self.name


# -----------------------------
# Helpers pour Submission
# -----------------------------
def validate_keywords(value):
    keywords_list = [k.strip() for k in value.split(",") if k.strip()]
    if len(keywords_list) > 10:
        raise ValidationError("Vous ne pouvez pas dépasser 10 mots-clés séparés par des virgules.")


def generate_submission_id():
    letters = string.ascii_uppercase
    random_letters = "".join(random.choices(letters, k=8))
    return f"SUB-{random_letters}"


# -----------------------------
# Modèle Submission
# -----------------------------
class Submission(models.Model):
    submission_id = models.CharField(
        max_length=255, primary_key=True, unique=True, editable=False, default=generate_submission_id
    )
    title = models.CharField(max_length=50)
    abstract = models.TextField()
    keywords = models.TextField(validators=[validate_keywords])
    paper = models.FileField(
        upload_to="paper/",
        validators=[FileExtensionValidator(allowed_extensions=["pdf"], message="Seuls les fichiers PDF sont autorisés.")]
    )

    STATUS = [
        ("submitted", "submitted"),
        ("under review", "under review"),
        ("accepted", "accepted"),
        ("rejected", "rejected"),
    ]
    status = models.CharField(max_length=50, choices=STATUS)
    payed = models.BooleanField(default=False)
    submission_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey("Userapp.User", on_delete=models.CASCADE, related_name="submissions")
    conference = models.ForeignKey("Conferenceapp.Conference", on_delete=models.CASCADE, related_name="submissions")

    def clean(self):
        # Utiliser la date du jour si submission_date est None
        submission_date = self.submission_date or date.today()
        if isinstance(submission_date, datetime):
            submission_date = submission_date.date()

        # Vérifier que la soumission est avant la conférence
        if self.conference and self.conference.start_date and submission_date > self.conference.start_date:
            raise ValidationError("La soumission ne peut être faite que pour des conférences à venir.")

        # Limiter le nombre de soumissions par jour à 3
        if self.user:
            from django.db.models import Count
            count = (
                Submission.objects.filter(user=self.user, submission_date=submission_date)
                .exclude(pk=self.pk)
                .count()
            )
            if count >= 3:
                raise ValidationError("Vous ne pouvez pas soumettre plus de 3 conférences par jour.")

    def __str__(self):
        return f"{self.title} ({self.status})"


# -----------------------------
# Modèle Organizingcommitee
# -----------------------------
class Organizingcommitee(models.Model):
    commitee_role = models.CharField(
        max_length=255,
        choices=[("chair", "chair"), ("co-chair", "co-chair"), ("member", "member")],
    )
    date_joined = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey("Userapp.User", on_delete=models.CASCADE, related_name="Organizingcommitee")
    conference = models.ForeignKey("Conferenceapp.Conference", on_delete=models.CASCADE, related_name="Organizingcommitee")

    def __str__(self):
        return f"{self.user} - {self.commitee_role}"





        
   

