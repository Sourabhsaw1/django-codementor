from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count
from .models import CodeSubmission
from .analyzer import analyze_code
from leaderboard.models import LeaderboardEntry
import json

def home(request):
    stats = {
        'total_users': 0,
        'total_submissions': CodeSubmission.objects.count(),
        'avg_score': CodeSubmission.objects.filter(score__isnull=False).aggregate(Avg('score'))['score__avg'] or 0,
    }
    try:
        from users.models import User
        stats['total_users'] = User.objects.count()
    except: pass
    return render(request, 'home.html', {'stats': stats})

@login_required
def dashboard(request):
    user = request.user
    recent = CodeSubmission.objects.filter(user=user)[:5]
    try:
        lb_entry = LeaderboardEntry.objects.get(user=user)
        rank = lb_entry.rank
    except:
        rank = '-'

    context = {
        'recent_submissions': recent,
        'rank': rank,
        'total_submissions': user.submissions_count,
        'avg_score': user.avg_score,
        'total_points': user.total_points,
    }
    return render(request, 'dashboard.html', context)

@login_required
def submit_code(request):
    if request.method == 'POST':
        code = request.POST.get('code', '').strip()
        language = request.POST.get('language', 'python')
        title = request.POST.get('title', 'My Code').strip() or 'My Code'

        if not code:
            messages.error(request, 'Please enter some code to analyze.')
            return render(request, 'submissions/submit.html')

        if len(code) < 5:
            messages.error(request, 'Code is too short to analyze.')
            return render(request, 'submissions/submit.html')

        # Run analysis
        result = analyze_code(code, language)

        # Save submission
        sub = CodeSubmission.objects.create(
            user=request.user,
            title=title,
            language=language,
            code=code,
            score=result['overall_score'],
            readability_score=result['readability_score'],
            performance_score=result['performance_score'],
            security_score=result['security_score'],
            best_practices_score=result['best_practices_score'],
            bugs_found=result['bugs_found'],
            points_earned=result['points_earned'],
        )
        sub.set_analysis(result)
        sub.save()

        # Update user stats
        user = request.user
        user.total_points += result['points_earned']
        user.save()
        user.update_stats()

        # Update leaderboard
        LeaderboardEntry.objects.update_or_create(
            user=user,
            defaults={
                'total_points': user.total_points,
                'submissions_count': user.submissions_count,
                'avg_score': user.avg_score,
            }
        )
        # Recalculate ranks
        for i, entry in enumerate(LeaderboardEntry.objects.order_by('-total_points'), 1):
            entry.rank = i
            entry.save()

        messages.success(request, f'Analysis complete! You earned {result["points_earned"]} points! 🎉')
        return redirect('submission_result', pk=sub.pk)

    return render(request, 'submissions/submit.html')

@login_required
def submission_result(request, pk):
    sub = get_object_or_404(CodeSubmission, pk=pk, user=request.user)
    analysis = sub.get_analysis()
    return render(request, 'submissions/result.html', {'sub': sub, 'analysis': analysis})

@login_required
def submission_history(request):
    subs = CodeSubmission.objects.filter(user=request.user)
    return render(request, 'submissions/history.html', {'submissions': subs})
