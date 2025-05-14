from django.shortcuts import render, redirect
from account.decorators import siswa_required
from .models import Quiz, Response
from django.db import transaction
import math
from django.urls import reverse
from account.models import CustomUser
from mongoengine.errors import NotUniqueError

# Create your views here.
def instruksi_view(request):
    return render(request, 'recom/instruksi.html')

def rekomendasi(request):
    response_data = request.session.get('response_data', {})
    likert_list = list(response_data.values())  # List jawaban skala Likert

    print(likert_list)  # Debug

    return render(request, 'recom/rekomendasi.html', {
        'likert_list': likert_list
    })

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
    start_number = (page - 1) * questions_per_page

    for question in questions:
        user_response = Response.objects(user=user, question=question).first()
        question.user_response = user_response.value if user_response else None

    if request.method == 'POST':
        with transaction.atomic():
            unanswered = []
            response_data = request.session.get('response_data', {})

            for question in questions:
                value = request.POST.get(f'question_{question.pertanyaan_id}')
                if value:
                    try:
                        existing_response = Response.objects(user=user, question=question).first()
                        if existing_response:
                            existing_response.value = int(value)
                            existing_response.save()
                        else:
                            Response(user=user, question=question, value=int(value)).save()
                    except NotUniqueError:
                        fallback_response = Response.objects(user=user, question=question).first()
                        if fallback_response:
                            fallback_response.value = int(value)
                            fallback_response.save()
                    
                    response_data[str(question.pertanyaan_id)] = int(value)
                else:
                    unanswered.append(question.pertanyaan_id)

            request.session['response_data'] = response_data

            if unanswered:
                context = {
                    'questions': questions,
                    'current_page': page,
                    'total_pages': total_pages,
                    'is_first_page': page == 1,
                    'is_last_page': page == total_pages,
                    'progress_percentage': (page / total_pages) * 100,
                    'error_message': 'Harap jawab semua pertanyaan sebelum melanjutkan.'
                }
                return render(request, 'recom/quiz.html', context)

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
        'start_number': start_number  # Tambahan
    }

    return render(request, 'recom/quiz.html', context)
