from django.db import models


class Message(models.Model):
    class Meta:
        ordering = ['-created_at']
    name = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField(max_length=100, default="", blank=True, null=True)
    message = models.TextField(default=500, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.subject
