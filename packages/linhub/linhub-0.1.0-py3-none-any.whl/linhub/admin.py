from django.contrib import admin

from .models import *


admin.site.register(Annotation)
admin.site.register(Entity)
admin.site.register(Annotator)
admin.site.register(Corpus)
admin.site.register(Document)
admin.site.register(DocumentScore)
admin.site.register(DocumentStatus)
admin.site.register(Task)
admin.site.register(Organization)
admin.site.register(Collaborator)
