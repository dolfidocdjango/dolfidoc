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
    View de listagem e filtragem de médicos.

    - Se o usuário digitar um nome, agrupa por CRM (modo antigo, carrossel agrupado).
    - Se o campo nome estiver vazio, exibe todos ordenados por valor (modo novo).
    - Se a busca for geral (nenhum campo preenchido), exibe todos sem paginação.
    """

    # Parâmetros GET
    nome_completo = request.GET.get('nome_completo', '').strip()
    especialidade = request.GET.get('especialidade', '').strip()
    cidade = request.GET.get('cidade', '').strip()
    page_number = request.GET.get('page', 1)

    # Filtros dinâmicos
    filtros = Q(valor__gte=1)
    if nome_completo:
        filtros &= Q(nome__icontains=nome_completo)
    if especialidade:
        filtros &= Q(especialidade__iexact=especialidade)
    if cidade:
        filtros &= Q(cidade__iexact=cidade)

    # Query principal
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

    # Detectar busca geral (todos os campos vazios)
    busca_geral = not (nome_completo or especialidade or cidade)

    # Se busca geral → sem paginação
    if busca_geral:
        medicos_list = list(medicos_qs)
        total_results = len(medicos_list)
        page_obj = None
    else:
        # Caso contrário, paginar normalmente
        paginator = Paginator(medicos_qs, 50)
        page_obj = paginator.get_page(page_number)
        medicos_list = list(page_obj.object_list)
        total_results = paginator.count

    # Se o usuário digitou nome → modo agrupado (carrossel antigo)
    if nome_completo:
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
            'agrupado': True,  # indica modo agrupado
            'medicos': grouped_medicos,
            'total_results': total_results,
            'page': page_obj.number if page_obj else 1,
            'total_pages': paginator.num_pages if not busca_geral else 1,
            'has_next': page_obj.has_next() if page_obj else False,
            'has_previous': page_obj.has_previous() if page_obj else False,
        }

    # Caso contrário → modo lista simples (ordenado por valor)
    else:
        response_data = {
            'especialidade': especialidade,
            'cidade': cidade,
            'agrupado': False,
            'medicos': medicos_list,
            'total_results': total_results,
            'page': page_obj.number if page_obj else 1,
            'total_pages': paginator.num_pages if not busca_geral else 1,
            'has_next': page_obj.has_next() if page_obj else False,
            'has_previous': page_obj.has_previous() if page_obj else False,
        }

    return JsonResponse(response_data, safe=False)


def index(request):
    """Página inicial."""
    return render(request, 'pagina_inicial.html')


def contato(request):
    """Página de contato."""
    return render(request, 'contato.html')


def sobre(request):
    """Página sobre."""
    return render(request, 'sobre.html')
