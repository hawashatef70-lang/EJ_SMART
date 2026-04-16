from django.db import models
from users.models import User # تأكد أن اسم التطبيق عندك هو users

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    
    # رقم العقار لتمييز المحادثة (مثلاً: شقة المعادي غير شقة التجمع)
    property_id = models.IntegerField(null=True, blank=True)
    
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at'] # الأحدث يظهر أولاً

    def __str__(self):
        return f"من: {self.sender.username} - إلى: {self.receiver.username}"
# Create your models here.
