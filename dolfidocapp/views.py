# views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Cardiologista
from django.db.models import Q, F, Value
from django.db.models.functions import Concat
from django.core.paginator import Paginator
from collections import defaultdict

def medInfo(request):
    nome_completo = request.GET.get('nome_completo')
    especialidade = request.GET.get('especialidade')
    cidade = request.GET.get('cidade')

    medicos = Cardiologista.objects.annotate(
        cidade_uf=Concat(F('cidade'), Value(' - '), F('uf'))
    ).filter(
        Q(nome__icontains=nome_completo) if nome_completo else Q(),
        Q(especialidade__iexact=especialidade) if especialidade else Q(),
        Q(cidade__iexact=cidade) if cidade else Q(),
        valor__gte=1  # Filtra apenas médicos com valor maior ou igual a 1
    ).order_by('valor')  # Ordena pelo menor valor

    # Paginação
    paginator = Paginator(medicos, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

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
            'valor': str(medico.valor),
            'numero': medico.numero,
            'logradouro': medico.logradouro,
            'complemento': medico.complemento or ''
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

    return JsonResponse(response_data)

    context = {
        'medicos': page_obj,
        'nome_completo': nome_completo,
        'especialidade': especialidade,
        'cidade': cidade,
    }

    return render(request, 'med_info.html', context)

def index(request):
    return render(request, 'pagina_inicial.html')

def medInfo_test(request):
    nome_completo = request.GET.get('nome_completo')
    especialidade = request.GET.get('especialidade')
    cidade = request.GET.get('cidade')

    context = {
        'nome_completo': nome_completo,
        'especialidade': especialidade,
        'cidade': cidade,
    }
    return render(request, 'med_info.html', context)