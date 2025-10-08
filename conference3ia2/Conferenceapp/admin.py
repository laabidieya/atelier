from django.contrib import admin
from .models import Conference,Submission,Organizingcommitee
# Register your models here.
admin.site.site_title="gestion conference 25/26"
admin.site.site_header="gestion conference"
admin.site.index_title="django app conference"

admin.site.register(Conference)
admin.site.register(Submission)
admin.site.register(Organizingcommitee)




