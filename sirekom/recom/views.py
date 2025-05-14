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
    
    # Cegah akses langsung jika belum ada jawaban
    if not response_data:
        return redirect('quiz', page=1)

    client = MongoClient()  # sesuaikan jika pakai host/port lain
    db = client["sirekom"]
    collection = db["skalaLikert"]

    # Ambil semua dokumen dari koleksi skalaLikert
    docs = list(collection.find())
    
    if not docs:
        return render(request, 'recom/rekomendasi.html', {
            'error': 'Data tidak ditemukan.'
        })

    # Ambil urutan pertanyaan dari dokumen
    pertanyaan_order = [doc['pertanyaan_id'] for doc in docs]

    # Susun likert_list sesuai urutan pertanyaan
    likert_list = []
    for pid in pertanyaan_order:
        value = response_data.get(str(pid)) or response_data.get(int(pid))
        if value is None:
            return render(request, 'recom/rekomendasi.html', {
                'error': f'Jawaban untuk pertanyaan {pid} tidak ditemukan.'
            })
        likert_list.append(value)

    # Validasi panjang
    if len(likert_list) != len(pertanyaan_order):
        return render(request, 'recom/rekomendasi.html', {
            'error': 'Jumlah jawaban tidak sesuai jumlah pertanyaan.',
            'likert_list': likert_list
        })

    # Siapkan vektor untuk setiap prodi
    prodi_vectors = {}
    for doc in docs:
        for prodi, value in doc.items():
            if prodi in ['_id', 'pertanyaan_id']:
                continue
            prodi_vectors.setdefault(prodi, []).append(value)

    # Hitung similarity
    user_vector = np.array(likert_list).reshape(1, -1)
    similarity_scores = {}

    for prodi, vector in prodi_vectors.items():
        prodi_vector = np.array(vector).reshape(1, -1)
        similarity = cosine_similarity(user_vector, prodi_vector)[0][0]
        similarity_scores[prodi] = round(similarity * 100, 2)

    # Urutkan berdasarkan similarity
    sorted_prodi = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)

    # Ambil nama prodi dari koleksi 'prodi'
    prodi_docs = list(db["prodi"].find())
    prodi_id_to_nama = {doc['prodi_id']: doc['nama_prodi'] for doc in prodi_docs}

    # Ubah prodi ID menjadi nama
    top_prodi_named = [
        (prodi_id_to_nama.get(prodi_id, prodi_id), score)
        for prodi_id, score in sorted_prodi[:3]
    ]

    return render(request, 'recom/rekomendasi.html', {
        'likert_list': likert_list,
        'top_prodi': top_prodi_named,
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

    # Saat GET: kosongkan user_response agar tidak tampil jawaban lama
    if request.method == 'GET':
        for question in questions:
            question.user_response = None


    if request.method == 'POST':
        with transaction.atomic():
            unanswered = []
            question_errors = {}  # Tambahan

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
                    question_errors[question.pertanyaan_id] = "Pertanyaan ini wajib dijawab." 

            request.session['response_data'] = response_data

            if unanswered:
                for question in questions:
                    value = request.POST.get(f'question_{question.pertanyaan_id}')
                    question.user_response = int(value) if value else None

                context = {
                    'questions': questions,
                    'current_page': page,
                    'total_pages': total_pages,
                    'is_first_page': page == 1,
                    'is_last_page': page == total_pages,
                    'progress_percentage': (page / total_pages) * 100,
                    'error_message': 'Harap jawab semua pertanyaan sebelum melanjutkan.',
                    'question_errors': question_errors,
                    'start_number': start_number,
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
