from django.db import models
from django.core.validators import MaxLengthValidator
from django.core.exceptions import ValidationError


# Create your models here.

class Conference(models.Model):
    conference_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    THEME= [
        ("IA", "Computer science & IA"),
        ("SE", "Sciences & Engineering"),
        ("SC", "Social Sciences"),
    ]
    theme = models.CharField(max_length=255,choices=THEME)

    location = models.CharField(max_length=50)
    description=models.TextField(validators=[
            MaxLengthValidator(30,"vous avez utuliser la limite des mots autorisés")
    ])
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  
    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("la date de debut  ne doit pas etre superieur a la date de fin")


class Submission(models.Model):
    submission_id=models.CharField(max_length=255,primary_key=True,unique=True,editable=False)
    title=models.CharField(max_length=50)
    abstract=models.TextField()
    keywords=models.TextField()
    paper=models.FileField(
        upload_to="paper/"
    )
    STATUS=[
        ("submitted","submitted"),
        ("under review ","under review"),
        ("accepted","accepted"),
        ("rejected","rejected"),
    ]
    status=models.CharField(max_length=50,choices=STATUS)
    payed=models.BooleanField(default=False)
    submission_date=models.DateField(auto_now_add=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)  
    user=models.ForeignKey("Userapp.User",on_delete=models.CASCADE,related_name="submissions")
    conference=models.ForeignKey(Conference,on_delete=models.CASCADE,related_name="submissions")

class Organizingcommitee(models.Model):
    commitee_role=models.CharField(max_length=255,choices=[("chair","chair"),("co-chair","co-chair"),("member","member")
    ])
    date_joined=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True) 
    user=models.ForeignKey("Userapp.User",on_delete=models.CASCADE,related_name="Organizingcommitee")
    conference=models.ForeignKey("Conferenceapp.Conference",on_delete=models.CASCADE,related_name="Organizingcommitee")



        
   

