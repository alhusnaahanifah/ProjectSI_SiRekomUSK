from django.shortcuts import render, redirect
from account.decorators import siswa_required
from .models import Quiz, Response
from django.db import transaction
import math
from django.urls import reverse
from account.models import CustomUser
from mongoengine.errors import NotUniqueError
from pymongo import MongoClient
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Create your views here.
def instruksi_view(request):
    return render(request, 'recom/instruksi.html')

def rekomendasi(request):
    response_data = request.session.get('response_data', {})
    likert_list = list(response_data.values())  # Jawaban user
    print("Likert:", likert_list)

    client = MongoClient()  # sesuaikan jika pakai custom host/port
    db = client["sirekom"]  # ganti nama_db sesuai kebutuhan
    collection = db["skalaLikert"]

    # Ambil semua dokumen
    docs = list(collection.find())
    
    if not docs:
        return render(request, 'recom/rekomendasi.html', {
            'error': 'Data tidak ditemukan.',
            'likert_list': likert_list
        })

    # Buat urutan pertanyaan dari dokumen
    pertanyaan_order = [doc['pertanyaan_id'] for doc in docs]

    # Buat dictionary: {prodi: [nilai berdasarkan urutan pertanyaan]}
    prodi_vectors = {}
    for doc in docs:
        for prodi, value in doc.items():
            if prodi in ['_id', 'pertanyaan_id']:
                continue
            prodi_vectors.setdefault(prodi, []).append(doc[prodi])

    # Pastikan panjang jawaban user sama
    if len(likert_list) != len(pertanyaan_order):
        return render(request, 'recom/rekomendasi.html', {
            'error': 'Jumlah jawaban tidak sesuai jumlah pertanyaan.',
            'likert_list': likert_list
        })

    user_vector = np.array(likert_list).reshape(1, -1)
    similarity_scores = {}

    for prodi, vector in prodi_vectors.items():
        prodi_vector = np.array(vector).reshape(1, -1)
        similarity = cosine_similarity(user_vector, prodi_vector)[0][0]
        similarity_scores[prodi] = round(similarity * 100, 2)

    # Urutkan berdasarkan similarity
    sorted_prodi = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)
    top_prodi = sorted_prodi[:3]  # 3 prodi teratas

    return render(request, 'recom/rekomendasi.html', {
        'likert_list': likert_list,
        'top_prodi': top_prodi,
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
