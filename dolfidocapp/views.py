# views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Cardiologista
from django.db.models import Q, F, Value
from django.db.models.functions import Concat
from django.core.paginator import Paginator
from collections import defaultdict
from django.http import HttpResponse

def obter_imagem_foto(request, medico_id):
    try:
        medico = Cardiologista.objects.get(id=medico_id)
        return HttpResponse(medico.foto, content_type="image/png")  # ou ajuste para o tipo de imagem adequado
    except Cardiologista.DoesNotExist:
        return HttpResponse(status=404)

def medInfo(request):
    # Obtendo os parâmetros do GET
    nome_completo = request.GET.get('nome_completo', '').strip()
    especialidade = request.GET.get('especialidade', '').strip()
    cidade = request.GET.get('cidade', '').strip()
    page_number = request.GET.get('page', 1)  # Padrão para a página inicial

    # Consulta de médicos com filtros dinâmicos e anotações
    medicos = Cardiologista.objects.annotate(
        cidade_uf=Concat(F('cidade'), Value(' - '), F('uf'))
    ).filter(
        Q(nome__icontains=nome_completo) if nome_completo else Q(),
        Q(especialidade__iexact=especialidade) if especialidade else Q(),
        Q(cidade__iexact=cidade) if cidade else Q(),
        valor__gte=1
    ).order_by('valor')

    # Paginação dos resultados (10 por página)
    paginator = Paginator(medicos, 10)
    
    try:
        page_obj = paginator.page(page_number)
    except:
        return JsonResponse({'error': 'Página inválida'}, status=400)

    # Agrupar médicos por CRM
    grouped_medicos = defaultdict(list)
    for medico in page_obj:
        grouped_medicos[medico.crm].append({
            'medico_id': medico.id,  # Importante: só coloca referências
            'nome': medico.nome,
            'crm': medico.crm,
            'cidade': medico.cidade,
            'uf': medico.uf,
            'especialidade': medico.especialidade,
            'nome_fantasia': medico.nome_fantasia,
            'cnpj': medico.cnpj,
            'valor': str(medico.valor),
            'numero': medico.numero,
            'logradouro': medico.logradouro,
            'complemento': medico.complemento or '',
        })

    response_data = {
        'especialidade': especialidade,
        'cidade': cidade,
        'medicos': grouped_medicos,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'num_pages': paginator.num_pages,
        'current_page': page_obj.number,
    }

    return JsonResponse(response_data, safe=False)  # Retornar dados JSON

def index(request):
    return render(request, 'pagina_inicial.html')

import requests
from django.conf import settings
from django.http import JsonResponse

def validate_recaptcha(request):
    recaptcha_token = request.POST.get('recaptcha_token')

    # ReCAPTCHA secret key deve estar em configurations
    secret_key = settings.RECAPTCHA_SECRET_KEY

    # Requisição do reCAPTCHA v3 ao Google
    data = {
        'secret': secret_key,
        'response': recaptcha_token
    }

    result = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data).json()

    # Verificar se a pontuação é suficiente e ação é reconhecida
    if result.get('success') and result.get('score', 0) > 0.5 and result.get('action') == 'homepage':
        # Validar corretamente a ação esperada e a pontuação
        return JsonResponse({'status': 'ok'}, status=200)

    return JsonResponse({'status': 'failed'}, status=400)
