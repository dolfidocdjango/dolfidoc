# views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Cardiologista
from django.db.models import Q, F, Value
from django.db.models.functions import Concat
from django.core.paginator import Paginator
from collections import defaultdict
from django.http import HttpResponse
import requests
from django.conf import settings

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

    # Consulta de médicos com filtros dinâmicos e anotações
    medicos = Cardiologista.objects.annotate(
        cidade_uf=Concat(F('cidade'), Value(' - '), F('uf'))
    ).filter(
        Q(nome__icontains=nome_completo) if nome_completo else Q(),
        Q(especialidade__iexact=especialidade) if especialidade else Q(),
        Q(cidade__iexact=cidade) if cidade else Q(),
        valor__gte=1
    ).order_by('valor')

    # Número total de médicos encontrados (total de resultados)
    total_results = medicos.count()

    # Agrupar médicos por CRM
    grouped_medicos = defaultdict(list)
    for medico in medicos:
        grouped_medicos[medico.crm].append({
            'medico_id': medico.id,
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
        'total_results': total_results,
    }

    return JsonResponse(response_data, safe=False)

def index(request):
    return render(request, 'pagina_inicial.html')

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
