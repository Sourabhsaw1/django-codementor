from django.shortcuts import render
from .models import LeaderboardEntry

def leaderboard(request):
    entries = LeaderboardEntry.objects.select_related('user').order_by('rank')[:50]
    user_entry = None
    if request.user.is_authenticated:
        try:
            user_entry = LeaderboardEntry.objects.get(user=request.user)
        except: pass
    return render(request, 'leaderboard/leaderboard.html', {
        'entries': entries,
        'user_entry': user_entry
    })
