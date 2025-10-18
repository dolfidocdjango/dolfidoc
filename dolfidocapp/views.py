# views.py
from collections import defaultdict
from django.conf import settings
from django.db.models import Q, F, Value
from django.db.models.functions import Concat
from django.http import JsonResponse, FileResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .models import Cardiologista


def obter_imagem_foto(request, medico_id):
    """
    Retorna a imagem armazenada no banco (campo bytea / BinaryField).
    """
    medico = get_object_or_404(Cardiologista, id=medico_id)

    if medico.foto:
        # Envia o conteúdo binário diretamente ao navegador
        return HttpResponse(medico.foto, content_type='image/png')

    return HttpResponse(status=404)

def medInfo(request):
    """
    View de listagem e filtragem de médicos, com agrupamento por CRM e paginação.
    Performance otimizada: uso de .values(), cache de lista e paginação.
    """

    # Parâmetros GET (filtragem dinâmica)
    nome_completo = request.GET.get('nome_completo', '').strip()
    especialidade = request.GET.get('especialidade', '').strip()
    cidade = request.GET.get('cidade', '').strip()
    page_number = request.GET.get('page', 1)

    # Filtros dinâmicos com Q()
    filtros = Q(valor__gte=1)
    if nome_completo:
        filtros &= Q(nome__icontains=nome_completo)
    if especialidade:
        filtros &= Q(especialidade__iexact=especialidade)
    if cidade:
        filtros &= Q(cidade__iexact=cidade)

    # Consulta otimizada — seleciona apenas os campos necessários
    medicos_qs = (
        Cardiologista.objects
        .filter(filtros)
        .annotate(cidade_uf=Concat(F('cidade'), Value(' - '), F('uf')))
        .values(
            'id', 'nome', 'crm', 'cidade', 'uf', 'especialidade',
            'nome_fantasia', 'cnpj', 'valor', 'numero', 'logradouro',
            'complemento', 'cidade_uf'
        )
        .order_by('valor')
    )

    # Paginação — evita carregar todos de uma vez
    paginator = Paginator(medicos_qs, 50)  # 50 registros por página
    page_obj = paginator.get_page(page_number)

    # Converte para lista (evita nova query no count)
    medicos_list = list(page_obj.object_list)
    total_results = paginator.count

    # Agrupar médicos por CRM (feito em memória de forma leve)
    grouped_medicos = defaultdict(list)
    for medico in medicos_list:
        grouped_medicos[medico['crm']].append({
            'medico_id': medico['id'],
            'nome': medico['nome'],
            'crm': medico['crm'],
            'cidade': medico['cidade'],
            'uf': medico['uf'],
            'especialidade': medico['especialidade'],
            'nome_fantasia': medico['nome_fantasia'],
            'cnpj': medico['cnpj'],
            'valor': str(medico['valor']),
            'numero': medico['numero'],
            'logradouro': medico['logradouro'],
            'complemento': medico['complemento'] or '',
        })

    response_data = {
        'especialidade': especialidade,
        'cidade': cidade,
        'medicos': grouped_medicos,
        'total_results': total_results,
        'page': page_obj.number,
        'total_pages': paginator.num_pages,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
    }

    return JsonResponse(response_data, safe=False)


def index(request):
    """
    Página inicial.
    """
    return render(request, 'pagina_inicial.html')
