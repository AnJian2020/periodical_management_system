from django.contrib import admin
from .models import SubjectModel,ContributionTypeModel,TradeModel

# admin.site.register(SubjectModel)
@admin.register(SubjectModel)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id','name']

# admin.site.register(ContributionTypeModel)
@admin.register(ContributionTypeModel)
class ContributionTypeAdmin(admin.ModelAdmin):
    list_display = ['id','name']

# admin.site.register(TradeModel)
@admin.register(TradeModel)
class TradeAdmin(admin.ModelAdmin):
    list_display = ['id','name']
