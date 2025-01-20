# views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Cardiologista
from django.db.models import Q, F, Value
from django.db.models.functions import Concat
from django.core.paginator import Paginator
from collections import defaultdict

def medInfo(request):
    # Obtendo os parâmetros do GET
    nome_completo = request.GET.get('nome_completo', '').strip()
    especialidade = request.GET.get('especialidade', '').strip()
    cidade = request.GET.get('cidade', '').strip()
    page_number = request.GET.get('page', 1)  # Padrão para a página inicial

    # Consulta de médicos com filtros dinâmicos e anotações
    medicos = Cardiologista.objects.annotate(
        cidade_uf=Concat(F('cidade'), Value(' - '), F('uf'))  # Concatenar 'cidade' e 'uf'
    ).filter(
        Q(nome__icontains=nome_completo) if nome_completo else Q(),  # Filtro no nome
        Q(especialidade__iexact=especialidade) if especialidade else Q(),  # Filtro na especialidade
        Q(cidade__iexact=cidade) if cidade else Q(),  # Filtro na cidade
        valor__gte=1  # Garantir apenas médicos com valores >= 1
    ).order_by('valor')  # Ordenar do menor para maior valor
    
    # Paginação dos resultados (10 por página)
    paginator = Paginator(medicos, 10)
    
    try:
        page_obj = paginator.page(page_number)  # Obter objetos da página corrente
    except:
        return JsonResponse({'error': 'Página inválida'}, status=400)

    # Agrupar médicos por CRM
    grouped_medicos = defaultdict(list)
    for medico in page_obj:
        grouped_medicos[medico.crm].append({
            'nome': medico.nome,
            'crm': medico.crm,
            'cidade': medico.cidade,
            'uf': medico.uf,
            'especialidade': medico.especialidade,
            'fid': medico.fid,
            'nome_fantasia': medico.nome_fantasia,
            'cnpj': medico.cnpj,
            'valor': str(medico.valor),  # Garantir que valor seja transformado em string
            'numero': medico.numero,
            'logradouro': medico.logradouro,
            'complemento': medico.complemento or '',  # Garantir string vazia se o complemento não existir
        })

    # Montar dados para resposta JSON
    response_data = {
        'especialidade': especialidade,
        'cidade': cidade,
        'medicos': grouped_medicos,
        'has_next': page_obj.has_next(),  # Validar próxima página
        'has_previous': page_obj.has_previous(),  # Validar página anterior
        'num_pages': paginator.num_pages,  # Total de páginas
        'current_page': page_obj.number,  # Página corrente
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
