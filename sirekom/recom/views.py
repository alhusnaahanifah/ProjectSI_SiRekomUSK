from django.shortcuts import render
from django.shortcuts import render, redirect
from account.decorators import siswa_required
from .models import Quiz
from django.db import transaction
import math
from django.urls import reverse
from account.models import CustomUser
from .models import Response

# Create your views here.
def instruksi_view(request):
    return render(request, 'recom/instruksi.html')

def rekomendasi(request):
    return render(request, 'recom/rekomendasi.html')

@siswa_required
def quiz(request, page=1):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect(f"{reverse('login')}?next={request.path}")
    
    user = CustomUser.objects.get(id=user_id)
    questions_per_page = 6

    all_questions = list(Quiz.objects.all())
    total_questions = len(all_questions)
    total_pages = math.ceil(total_questions / questions_per_page)

    if page < 1:
        return redirect('quiz', page=1)
    if page > total_pages:
        return redirect('quiz', page=total_pages)

    start_idx = (page - 1) * questions_per_page
    end_idx = start_idx + questions_per_page
    questions = all_questions[start_idx:end_idx]

    # Modifikasi bagian ini untuk menyertakan response langsung di question object
    for question in questions:
        response = Response.objects.filter(user=user, question=question).first()
        question.user_response = response.value if response else None

    if request.method == 'POST':
        with transaction.atomic():
            for question in questions:
                value = request.POST.get(f'question_{question.pertanyaan_id}')
                if value:
                    Response.objects.update_or_create(
                        user=user,
                        question=question,
                        defaults={'value': value}
                    )

            if 'next' in request.POST and page < total_pages:
                return redirect('quiz', page=page+1)
            elif 'prev' in request.POST and page > 1:
                return redirect('quiz', page=page-1)
            elif 'finish' in request.POST:
                return redirect('rekomendasi')

    context = {
        'questions': questions,
        'current_page': page,
        'total_pages': total_pages,
        'is_first_page': page == 1,
        'is_last_page': page == total_pages,
        'progress_percentage': (page / total_pages) * 100,
    }

    return render(request, 'recom/quiz.html', context)