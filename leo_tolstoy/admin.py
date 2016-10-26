from django.contrib import admin
from .models import Works, MyUser, TolstoyTexts, LemmasInverseTable

admin.site.register(Works)

admin.site.register(MyUser)
admin.site.register(TolstoyTexts)
admin.site.register(LemmasInverseTable)
