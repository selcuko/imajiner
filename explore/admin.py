from django.contrib import admin
from .models import Feedback

class FeedbackAdmin(admin.ModelAdmin):
    model = Feedback
    field = '__all__'
    readonly_fields = ['ua', 'user', 'session', 'referrer', 'message', 'location', 'created_at']

admin.site.register(Feedback, FeedbackAdmin)
