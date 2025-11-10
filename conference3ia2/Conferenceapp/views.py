from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from .models import Conference, Submission
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import ConferenceForm, SubmissionForm, SubmissionUpdateForm

def list_conferences(request):
    conferences_list = Conference.objects.all()
    return render(request, "conferences/liste.html", {"liste": conferences_list})

class ConferenceList(ListView):
    model = Conference
    context_object_name = "liste"
    template_name = "conferences/liste.html"

class ConferenceDetails(DetailView):
    model = Conference
    context_object_name = "conference"
    template_name = "conferences/details.html"

class ConferenceCreate(LoginRequiredMixin, CreateView):
    model = Conference
    template_name = "conferences/form.html"
    form_class = ConferenceForm
    success_url = reverse_lazy("liste_conferences")
    
    def dispatch(self, request, *args, **kwargs):
        # Vérifier que l'utilisateur est membre du comité
        if not request.user.is_authenticated or request.user.role != "comitee":
            raise PermissionDenied("Seuls les membres du comité d'organisation peuvent créer des conférences.")
        return super().dispatch(request, *args, **kwargs)

class ConferenceUpdate(LoginRequiredMixin, UpdateView):
    model = Conference
    template_name = "conferences/form.html"
    form_class = ConferenceForm
    success_url = reverse_lazy("liste_conferences")
    
    def dispatch(self, request, *args, **kwargs):
        # Vérifier que l'utilisateur est membre du comité
        if not request.user.is_authenticated or request.user.role != "comitee":
            raise PermissionDenied("Seuls les membres du comité d'organisation peuvent modifier des conférences.")
        return super().dispatch(request, *args, **kwargs)

class ConferenceDelete(LoginRequiredMixin, DeleteView):
    model = Conference
    template_name = "conferences/confirm_delete.html"
    success_url = reverse_lazy("liste_conferences")
    
    def dispatch(self, request, *args, **kwargs):
        # Vérifier que l'utilisateur est membre du comité
        if not request.user.is_authenticated or request.user.role != "comitee":
            raise PermissionDenied("Seuls les membres du comité d'organisation peuvent supprimer des conférences.")
        return super().dispatch(request, *args, **kwargs)

class ListSubmissions(LoginRequiredMixin, ListView):
    model = Submission
    template_name = "conferences/submissions_liste.html"
    context_object_name = "submissions"
    
    def get_queryset(self):
        # Filtrer les soumissions pour l'utilisateur connecté
        return Submission.objects.filter(user=self.request.user).select_related('conference', 'user').order_by('-submission_date')

class DetailSubmission(LoginRequiredMixin, DetailView):
    model = Submission
    template_name = "conferences/submissions_details.html"
    context_object_name = "submission"
    pk_url_kwarg = 'submission_id'
    
    def get_queryset(self):
        # S'assurer que l'utilisateur ne peut voir que ses propres soumissions
        return Submission.objects.filter(user=self.request.user).select_related('conference', 'user')
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Vérification supplémentaire de sécurité
        if obj.user != self.request.user:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied("Vous n'avez pas accès à cette soumission.")
        return obj

class AddSubmission(LoginRequiredMixin, CreateView):
    model = Submission
    template_name = "conferences/submissions_add.html"
    form_class = SubmissionForm
    success_url = reverse_lazy("liste_submissions")
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Passer l'utilisateur au formulaire pour qu'il puisse l'assigner avant la validation
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        # Assigner automatiquement l'utilisateur connecté comme auteur
        form.instance.user = self.request.user
        # Définir le statut par défaut à "submitted"
        form.instance.status = "submitted"
        return super().form_valid(form)

class UpdateSubmission(LoginRequiredMixin, UpdateView):
    model = Submission
    template_name = "conferences/submissions_form.html"
    form_class = SubmissionUpdateForm
    pk_url_kwarg = 'submission_id'
    success_url = reverse_lazy("liste_submissions")
    
    def get_queryset(self):
        # S'assurer que l'utilisateur ne peut modifier que ses propres soumissions
        return Submission.objects.filter(user=self.request.user).select_related('conference', 'user')
    
    def dispatch(self, request, *args, **kwargs):
        # Vérifier l'accès et le statut avant de permettre la modification
        submission_id = kwargs.get('submission_id')
        if submission_id:
            try:
                obj = Submission.objects.get(submission_id=submission_id, user=request.user)
                # Vérifier que la soumission n'est pas acceptée ou rejetée
                if obj.status in ['accepted', 'rejected']:
                    from django.contrib import messages
                    messages.error(request, "Une soumission avec l'état accepté ou rejeté ne peut pas être modifiée.")
                    from django.shortcuts import redirect
                    return redirect('liste_submissions')
            except Submission.DoesNotExist:
                raise PermissionDenied("Vous n'avez pas accès à cette soumission.")
        
        return super().dispatch(request, *args, **kwargs)





