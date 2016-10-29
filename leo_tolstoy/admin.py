from django.contrib import admin
from .models import OriginalWorks, TeiWorks, MyUser, TolstoyTexts, LemmasInverseTable

admin.site.register(OriginalWorks)
admin.site.register(TeiWorks)

admin.site.register(MyUser)
admin.site.register(TolstoyTexts)
admin.site.register(LemmasInverseTable)
