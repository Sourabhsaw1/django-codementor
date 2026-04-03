from django.db import models
from django.conf import settings
import json

LANGUAGE_CHOICES = [
    ('python', 'Python'),
    ('javascript', 'JavaScript'),
    ('java', 'Java'),
    ('cpp', 'C++'),
    ('go', 'Go'),
]

class CodeSubmission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submissions')
    title = models.CharField(max_length=200, default='My Code')
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='python')
    code = models.TextField()
    score = models.FloatField(null=True, blank=True)
    readability_score = models.FloatField(null=True, blank=True)
    performance_score = models.FloatField(null=True, blank=True)
    security_score = models.FloatField(null=True, blank=True)
    best_practices_score = models.FloatField(null=True, blank=True)
    bugs_found = models.IntegerField(default=0)
    points_earned = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)
    analysis_data = models.TextField(default='{}')

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.user.username} - {self.title} ({self.score})"

    def get_analysis(self):
        try:
            return json.loads(self.analysis_data)
        except:
            return {}

    def set_analysis(self, data):
        self.analysis_data = json.dumps(data)
