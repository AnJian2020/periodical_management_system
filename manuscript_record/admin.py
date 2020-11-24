from django.contrib import admin
from .models import SubjectModel,ContributionTypeModel,TradeModel

admin.site.register(SubjectModel)
admin.site.register(ContributionTypeModel)
admin.site.register(TradeModel)
