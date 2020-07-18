from django.contrib import admin

# Register your models here.
from uploadapp.forms import BgFileContentForm
from uploadapp.models import BgFileToolModel

#admin.site.register(BgFileToolModel)

class MochaProjectsAdmin(admin.ModelAdmin):
    form = BgFileContentForm


admin.site.register(BgFileToolModel, MochaProjectsAdmin)