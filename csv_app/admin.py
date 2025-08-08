from django.contrib import admin
from .models import User, UserReportData
# Register your models here.
from admincharts.admin import AdminChartMixin
from django.db.models import Count, Case, When, Value, CharField

@admin.register(UserReportData)
class UserReportAdmin(admin.ModelAdmin):
    list_display = ("uploaded_at", "total_users", "under_20", "between_20_40", "between_40_60", "over_60")

@admin.register(User)
class UserAdmin(AdminChartMixin, admin.ModelAdmin):
    list_display = ('id','name','age')
    search_fields = ('id','name')
    list_filter = ('age',)
        
    list_chart_type = 'pie'  
    list_chart_options = {
        "aspectRatio": 2
    }

    def get_list_chart_queryset(self, changelist):
        return changelist.queryset

    def get_list_chart_data(self, queryset):
        grouped = queryset.annotate(
            age_group=Case(
                When(age__lt=20, then=Value('<20')),
                When(age__gte=20, age__lte=40, then=Value('20-40')),
                When(age__gt=40, age__lte=60, then=Value('40-60')),
                When(age__gt=60, then=Value('>60')),
                default=Value('Unknown'),
                output_field=CharField()
            )
        ).values('age_group').annotate(count=Count('id')).order_by('age_group')
        total = sum(entry['count'] for entry in grouped) or 1

    
        labels = [entry['age_group'] for entry in grouped]
        # counts = [entry['count'] for entry in grouped]
        percentages = [round((entry['count'] / total) * 100, 2) for entry in grouped]
        

        return {
            "labels": labels,
            "datasets": [
                {
                    "label": "User Age Groups",
                    "data": percentages,
                    "backgroundColor": [
                        "#36A2EB", "#FFCE56", "#4BC0C0", "#FF6384", "#9966FF"
                    ]
                }
            ]
        }