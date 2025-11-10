from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from Conferenceapp.models import Conference

# Create your models here.
class Session(models.Model):
    session_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    topic=models.CharField(max_length=255)
    session_day=models.DateField()
    start_time=models.TimeField()
    end_time=models.TimeField()
    room = models.CharField(
        max_length=255,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z0-9]+$',
                message="Le nom de la salle ne doit contenir que des lettres et des chiffres (sans espaces ni caractères spéciaux)."
            )
        ]
    )
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)  
    conference=models.ForeignKey("Conferenceapp.Conference",on_delete=models.CASCADE,related_name="sessions")
    #conference=models.ForeignKey(conference,on_delete=models.CASCADE) and add from Conferenceapp .models import conference
    def clean(self):
        """Validation personnalisée pour vérifier les heures de session."""
        if self.end_time <= self.start_time:
            raise ValidationError("L'heure de fin doit être supérieure à l'heure de début.")
       # Vérifier que la date de la session appartient à l'intervalle de la conférence
        if self.conference:
            if not (self.conference.start_date <= self.session_day <= self.conference.end_date):
                raise ValidationError(
                    "La date de la session doit être comprise entre les dates de début et de fin de la conférence."
                )
    
    def __str__(self):
        return f"{self.title} ({self.session_day})"

