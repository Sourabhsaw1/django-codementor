from django.db import models
from django.conf import settings

class LeaderboardEntry(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_points = models.IntegerField(default=0)
    submissions_count = models.IntegerField(default=0)
    avg_score = models.FloatField(default=0.0)
    rank = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['rank']

    def get_medal(self):
        if self.rank == 1: return '🥇'
        if self.rank == 2: return '🥈'
        if self.rank == 3: return '🥉'
        return f'#{self.rank}'
