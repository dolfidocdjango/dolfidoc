# Dolfidoc - Sistema de Busca de Consultas Médicas

## Descrição

Dolfidoc é uma plataforma web desenvolvida em Django para facilitar a busca e localização de especialistas médicos. O sistema permite que usuários encontrem profissionais de saúde por especialidade e localização, visualizando informações detalhadas sobre valores e disponibilidade.

## Funcionalidades

- **Busca de Médicos**: Pesquise especialistas por nome, especialidade e cidade
- **Página de Contato**: Envie mensagens diretamente via WhatsApp
- **Página Sobre**: Conheça a missão, visão e valores da Dolfidoc
- **Design Responsivo**: Interface adaptada para mobile, tablet, desktop (1920×1080), wide (2560×1440) e ultrawide

## Tecnologias Utilizadas

- **Backend**: Django 4.2+
- **Banco de Dados**: PostgreSQL (via psycopg2-binary)
- **Servidor**: Gunicorn
- **Arquivos Estáticos**: Whitenoise
- **Frontend**: HTML5, CSS3 (unificado), JavaScript (jQuery)
- **Fontes**: Google Fonts (Lato)
- **Framework CSS**: Bootstrap 4.5.2 (via CDN)

## Estrutura do Projeto

```
dolfidoc/
├── dolfidoc/              # Configurações do projeto Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── dolfidocapp/           # Aplicação principal
│   ├── migrations/        # Migrações do banco de dados
│   ├── static/
│   │   ├── css/
│   │   │   └── dolfidoc.css  # CSS unificado e responsivo
│   │   └── images/
│   ├── templates/
│   │   ├── includes/      # Componentes reutilizáveis (header, footer)
│   │   ├── base.html      # Template base
│   │   ├── pagina_inicial.html
│   │   ├── contato.html
│   │   └── sobre.html
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── requirements.txt       # Dependências do projeto
├── manage.py
└── README.md
```

## Instalação

### Pré-requisitos

- Python 3.11+
- PostgreSQL
- pip

### Passos para Instalação

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/dolfidocdjango/dolfidoc.git
   cd dolfidoc
   ```

2. **Crie e ative um ambiente virtual**:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate  # Windows
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o banco de dados**:
   - Edite `dolfidoc/settings.py` com suas credenciais do PostgreSQL
   - Execute as migrações:
     ```bash
     python manage.py migrate
     ```

5. **Execute o servidor de desenvolvimento**:
   ```bash
   python manage.py runserver
   ```

6. **Acesse o sistema**:
   - Abra o navegador em: `http://localhost:8000`

## Validação do Projeto

Para verificar se não há problemas de configuração:

```bash
python manage.py check
```

Resultado esperado: `System check identified no issues (0 silenced).`

## Páginas Disponíveis

- **Página Inicial**: `/` - Busca de médicos
- **Contato**: `/contato/` - Formulário de contato via WhatsApp
- **Sobre**: `/sobre/` - Informações institucionais
- **Admin**: `/admin/` - Painel administrativo do Django

## CSS Unificado

O projeto utiliza um único arquivo CSS (`dolfidoc.css`) que consolida todos os estilos anteriormente fragmentados. O CSS está organizado em seções:

- **BASE / RESET**: Estilos globais e variáveis CSS
- **HEADER**: Cabeçalho e navegação
- **MAIN CONTENT**: Conteúdo principal e layout
- **FORMS / SEARCH**: Formulários e campos de busca
- **RESULTS / CAROUSEL**: Resultados da pesquisa
- **FOOTER**: Rodapé
- **UTILITIES**: Classes utilitárias

### Responsividade

O CSS garante layout consistente nas seguintes resoluções:

| Tipo de Tela | Largura | Objetivo |
|--------------|---------|----------|
| Mobile | até 767 px | Layout empilhado, menus colapsáveis |
| Tablet | 768 – 1023 px | Transição intermediária |
| Desktop (padrão) | 1920×1080 | Layout de referência principal |
| Wide / QHD | 2560×1440 | Ajuste de espaçamento e fluidez |
| Ultrawide | 2560×1080+ | Evitar distorções e vazios laterais |

## Boas Práticas Implementadas

- ✅ CSS unificado e organizado por seções
- ✅ Variáveis CSS globais para cores e espaçamentos
- ✅ Responsividade fluida com Flexbox e CSS Grid
- ✅ Uso de `rem` em vez de `vw/vh` para fontes
- ✅ Container centralizado com `max-width`
- ✅ Eliminação de margens "mágicas"
- ✅ Compatibilidade com Chrome, Edge e Firefox
- ✅ Separação clara entre camadas (views, templates, static)
- ✅ Comentários explicativos no código
- ✅ Zero warnings em `python manage.py check`

## Dependências

Conforme especificado em `requirements.txt`:

```
Django>=4.2,<5.0
psycopg2-binary>=2.9
gunicorn>=21.0
whitenoise>=6.5
```

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT.

## Contato

Para mais informações, acesse a página de contato no sistema ou visite nosso repositório no GitHub.

---

**Desenvolvido com ❤️ pela equipe Dolfidoc**
