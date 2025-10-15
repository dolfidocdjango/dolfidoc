# Changelog - Melhorias Dolfidoc

## Data: Outubro 2025

### Resumo das Alterações

Este documento detalha todas as melhorias implementadas no projeto Dolfidoc, seguindo as especificações do documento de análise fornecido. **Todas as alterações mantiveram integralmente a paleta de cores original do projeto.**

---

## 1. Logo / Header

### Alterações Implementadas
- **Aumento do tamanho da logo**: Alterado de `max-width: 150px` para `max-width: 200px` no arquivo `header.css`
- **Container do header otimizado**: Garantido que o container permita proporções adequadas com `flex: 0 0 auto`
- **Responsividade**: Em telas menores (768px), a logo reduz para 150px; em telas muito pequenas (480px), reduz para 120px

### Arquivos Modificados
- `dolfidocapp/static/css/header.css` (novo arquivo)
- `dolfidocapp/templates/includes/header.html` (novo arquivo)

---

## 2. Título Superior Direito

### Alterações Implementadas
- **Negrito aplicado**: Adicionado `font-weight: bold` aos links do header (Ajuda, Contato, Sobre)
- **Classe BEM**: Utilizada nomenclatura `.header__nav-link` para padronização

### Arquivos Modificados
- `dolfidocapp/static/css/header.css` (linhas 33-44)

---

## 3. Rodapé

### Alterações Implementadas
- **Remoção de negrito**: Tag `<b>` removida do HTML
- **Estilo CSS**: Definido `font-weight: normal` explicitamente na classe `.footer__text`
- **Modularização**: Footer separado em arquivo include próprio

### Arquivos Modificados
- `dolfidocapp/templates/includes/footer.html` (novo arquivo)
- `dolfidocapp/static/css/footer.css` (novo arquivo)

---

## 4. Formulário de Busca / Inputs

### Alterações Implementadas
- **Texto do botão**: Alterado de "Pesquisar" para "Enviar"
- **Espaçamento entre campos**: Adicionado `margin-bottom: 0.625rem` (10px) em cada `.form-group`
- **Uniformização**: 
  - Padding consistente: `0.625rem` (10px)
  - Border-radius: `0.5rem` (8px) para campos intermediários
  - Border-radius especial para primeiro campo (topo arredondado) e último campo (base arredondada)
- **Alinhamento**: Todos os campos centralizados com `text-align: center`

### Arquivos Modificados
- `dolfidocapp/templates/includes/search_form.html` (novo arquivo)
- `dolfidocapp/static/css/forms.css` (novo arquivo)

---

## 5. Responsividade

### Alterações Implementadas
- **Media queries adicionadas**:
  - `@media (max-width: 768px)`: Tablets e telas médias
  - `@media (max-width: 480px)`: Smartphones
- **Unidades relativas**: Convertido de pixels para `rem`, `em` e `%` em todo o CSS
- **Ajustes específicos**:
  - Logo redimensiona proporcionalmente
  - Formulários aumentam largura em telas menores (70% → 85% → 95%)
  - Imagens e carrossel adaptam-se ao tamanho da tela
  - Footer reduz tamanho de fonte em dispositivos móveis

### Arquivos Modificados
- Todos os arquivos CSS criados incluem seções de responsividade

---

## 6. Modularização

### Alterações Implementadas
- **Templates separados em includes**:
  - `includes/header.html`: Cabeçalho do site
  - `includes/footer.html`: Rodapé do site
  - `includes/search_form.html`: Formulário de busca
- **CSS dividido em módulos**:
  - `style.css`: Estilos base e reset
  - `header.css`: Estilos do cabeçalho
  - `footer.css`: Estilos do rodapé
  - `forms.css`: Estilos de formulários
  - `carousel.css`: Estilos do carrossel
  - `results.css`: Estilos da seção de resultados

### Estrutura de Arquivos
```
dolfidocapp/
├── static/
│   └── css/
│       ├── style.css (base)
│       ├── header.css (novo)
│       ├── footer.css (novo)
│       ├── forms.css (novo)
│       ├── carousel.css (novo)
│       └── results.css (novo)
└── templates/
    ├── includes/
    │   ├── header.html (novo)
    │   ├── footer.html (novo)
    │   └── search_form.html (novo)
    └── pagina_inicial.html (refatorado)
```

---

## 7. Padronização CSS

### Alterações Implementadas
- **Convenção BEM aplicada**:
  - `.header__logo`, `.header__nav`, `.header__nav-link`
  - `.footer__text`
  - `.search-form`, `.form-control--rounded-top`, `.form-control--error`
- **Eliminação de estilos inline**: Todos os estilos movidos do `<style>` no HTML para arquivos CSS apropriados
- **Remoção de `!important`**: Mantidos apenas os essenciais para arredondamento de bordas específicas
- **Organização**: Propriedades CSS agrupadas logicamente (layout, tipografia, cores, efeitos)

### Arquivos Modificados
- Todos os arquivos CSS

---

## 8. Feedback Visual

### Alterações Implementadas
- **Classe de erro**: `.form-control--error` criada com borda vermelha e sombra
- **Validação JavaScript**: Adicionada validação básica que aplica classe de erro em campos vazios
- **Remoção automática de erro**: Classe removida quando usuário preenche o campo
- **Mensagem de erro AJAX**: Alert adicionado em caso de falha na requisição

### Arquivos Modificados
- `dolfidocapp/static/css/forms.css` (linhas 35-38, 89-96)
- `dolfidocapp/templates/pagina_inicial.html` (JavaScript, linhas 185-199, 218-222)

---

## 9. Acessibilidade

### Alterações Implementadas
- **Atributos ARIA**:
  - `aria-label` em todos os campos de formulário
  - `aria-label` em botões e links de navegação
  - `role="navigation"`, `role="main"`, `role="search"`, `role="region"`
  - `aria-live="polite"` na seção de resultados
- **Alt text descritivo**: 
  - Logo: "Logotipo Dolfidoc - Sistema de busca de consultas médicas"
  - Imagem de médicos: "Ilustração de médicos - Dolfidoc"
  - Fotos de resultados: "Foto do Dr(a). [Nome] - Fonte: CRMS/CFM"
- **Labels para screen readers**: Classe `.sr-only` criada para labels invisíveis mas acessíveis
- **Foco visível**: Estilos de `:focus` adicionados com `outline` de 2px
- **Contraste**: Revisado e mantido conforme paleta original (contraste adequado)

### Arquivos Modificados
- `dolfidocapp/templates/includes/header.html`
- `dolfidocapp/templates/includes/search_form.html`
- `dolfidocapp/templates/pagina_inicial.html`
- `dolfidocapp/static/css/forms.css` (classe `.sr-only`)
- Todos os arquivos CSS (estilos `:focus`)

---

## 10. Limpeza e Otimização

### Alterações Implementadas
- **CSS redundante removido**:
  - Regras duplicadas de `.btn-invisible` eliminadas
  - Estilos repetidos de `header` consolidados
  - Propriedades conflitantes resolvidas
- **Divisão em módulos**: CSS organizado em 6 arquivos temáticos
- **Unidades relativas**: Conversão completa para `rem`, `em` e `%`
- **Comentários organizacionais**: Seções claramente identificadas
- **Otimização de seletores**: Uso de classes específicas em vez de seletores genéricos

### Arquivos Modificados
- Todos os arquivos CSS

---

## Paleta de Cores Preservada

Conforme solicitado, **todas as cores originais foram mantidas**:

| Elemento | Cor | Código |
|----------|-----|--------|
| Background principal | Cinza azulado claro | `#D3DAE0` |
| Texto principal | Azul escuro | `#2f3061` |
| Texto secundário | Verde escuro | `#15473b` |
| Background footer | Cinza claro | `#f8f9fa` |
| Botões | Cinza claro | `#e9ebed` |
| Hover botão | Azul | `#0056b3` |
| Texto branco | Branco | `#ffffff` |
| Bordas | Cinza | `#e9ecef`, `#e0e0e0` |

---

## Compatibilidade

- **Navegadores**: Chrome, Firefox, Safari, Edge (versões modernas)
- **Dispositivos**: Desktop, Tablet, Smartphone
- **Breakpoints**: 768px (tablet), 480px (mobile)

---

## Próximos Passos Recomendados

1. Testar em diferentes navegadores e dispositivos
2. Validar acessibilidade com ferramentas como WAVE ou Lighthouse
3. Considerar adicionar mais opções de especialidades e cidades
4. Implementar mensagens de erro mais específicas por campo
5. Adicionar animações sutis para melhorar UX (opcional)

---

## Notas Técnicas

- Todas as alterações são compatíveis com Django 3.x+
- Bootstrap 4.5.2 mantido conforme original
- jQuery 3.5.1 mantido conforme original
- Flatpickr mantido para seleção de datas
- Google Analytics e reCAPTCHA preservados

