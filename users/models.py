from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    total_points = models.IntegerField(default=0)
    submissions_count = models.IntegerField(default=0)
    avg_score = models.FloatField(default=0.0)
    rank = models.IntegerField(default=0)
    github_url = models.URLField(blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-total_points']

    def __str__(self):
        return self.username

    def update_stats(self):
        from submissions.models import CodeSubmission
        subs = CodeSubmission.objects.filter(user=self, score__isnull=False)
        self.submissions_count = subs.count()
        if self.submissions_count > 0:
            self.avg_score = round(sum(s.score for s in subs) / self.submissions_count, 1)
        self.save()
