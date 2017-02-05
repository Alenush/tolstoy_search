from django.contrib import admin
from .models import OriginalWorks, MyUser, TolstoyTexts, LemmasInverseTable, Letters

admin.site.register(OriginalWorks)
admin.site.register(Letters)

admin.site.register(MyUser)
admin.site.register(TolstoyTexts)
admin.site.register(LemmasInverseTable)
