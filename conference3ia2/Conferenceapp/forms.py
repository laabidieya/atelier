from django import forms
from .models import Conference, Submission

class ConferenceForm(forms.ModelForm):
    class Meta:
        model = Conference
        fields = ['name', 'location', 'description', 'start_date', 'end_date']
        labels = {
            'name': "Titre de la conférence",
            'location': "Lieu",
            'description': "Description",
            'start_date': "Date de début",
            'end_date': "Date de fin",
        }
        widgets = {
            'name': forms.TextInput(
                attrs={'placeholder': "Entrez un titre pour la conférence", 'class': 'form-control'}
            ),
            'location': forms.TextInput(
                attrs={'placeholder': "Entrez le lieu", 'class': 'form-control'}
            ),
            'description': forms.Textarea(
                attrs={'placeholder': "Entrez une description", 'class': 'form-control', 'rows': 3}
            ),
            # 🟢 Ici les champs date utilisent un input HTML5 avec un sélecteur de calendrier
            'start_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'end_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
        }

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['title', 'abstract', 'keywords', 'paper', 'conference']
        labels = {
            'title': "Titre de la soumission",
            'abstract': "Résumé (Abstract)",
            'keywords': "Mots-clés",
            'paper': "Fichier PDF",
            'conference': "Conférence",
        }
        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': "Entrez le titre de votre soumission", 'class': 'form-control'}
            ),
            'abstract': forms.Textarea(
                attrs={'placeholder': "Entrez le résumé de votre soumission", 'class': 'form-control', 'rows': 5}
            ),
            'keywords': forms.TextInput(
                attrs={'placeholder': "Entrez les mots-clés séparés par des virgules (max 10)", 'class': 'form-control'}
            ),
            'paper': forms.FileInput(
                attrs={'accept': '.pdf', 'class': 'form-control'}
            ),
            'conference': forms.Select(
                attrs={'class': 'form-control'}
            ),
        }
    
    def __init__(self, *args, **kwargs):
        # Extraire l'utilisateur des kwargs s'il est passé
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Filtrer les conférences pour n'afficher que celles non encore terminées
        from datetime import date
        self.fields['conference'].queryset = Conference.objects.filter(end_date__gte=date.today())
    
    def clean(self):
        cleaned_data = super().clean()
        # Assigner l'utilisateur avant la validation si disponible
        if self.user and not self.instance.user_id:
            self.instance.user = self.user
        return cleaned_data

class SubmissionUpdateForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['title', 'abstract', 'keywords', 'paper']
        labels = {
            'title': "Titre de la soumission",
            'abstract': "Résumé (Abstract)",
            'keywords': "Mots-clés",
            'paper': "Fichier PDF",
        }
        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': "Entrez le titre de votre soumission", 'class': 'form-control'}
            ),
            'abstract': forms.Textarea(
                attrs={'placeholder': "Entrez le résumé de votre soumission", 'class': 'form-control', 'rows': 5}
            ),
            'keywords': forms.TextInput(
                attrs={'placeholder': "Entrez les mots-clés séparés par des virgules (max 10)", 'class': 'form-control'}
            ),
            'paper': forms.FileInput(
                attrs={'accept': '.pdf', 'class': 'form-control'}
            ),
        }
