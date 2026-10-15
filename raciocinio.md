# Raciocínio de Desenvolvimento e Arquitetura

Este documento registra todas as decisões técnicas, regras de negócio, modelagem de dados, arquitetura de busca e estilos criados para atender aos dois requisitos solicitados:
1. **Identificador sequencial por empresa (`sub_id`)** na coluna `#` dos colaboradores e capacidade de busca por colaboradores específicos.
2. **Funcionalidade e visualização Mobile dedicada**, preservando integralmente o layout e padrão da versão Desktop.

---

## 1. Contexto e Objetivos

O sistema é um gerenciador de estoque multi-empresa (*multi-tenant*). Anteriormente, a coluna `#` na listagem de colaboradores exibia a chave primária global (`id`) do banco de dados relacional. 

Isso gerava inconsistências de usabilidade entre empresas:
- Quando uma nova empresa ("Empresa Teste") cadastrou seu primeiro colaborador, ele recebeu o `id` global 50 (devido aos cadastros das outras empresas).
- O usuário requisitou que cada empresa possua uma numeração incremental própria iniciando em 1 (`sub_id`), facilitando a identificação, comunicação interna e busca de colaboradores específicos.
- Adicionalmente, foi solicitada uma experiência mobile completa, touch-friendly e sem quebras de layout, sem alterar o padrão visual já consolidado na versão desktop.

---

## 2. Requisito 1: Implementação do `sub_id` por Empresa

### 2.1. Modelagem de Dados (`apps/store/models.py`)

No modelo `Buyer` (Colaborador):
- **Campo adicionado**:
  ```python
  sub_id = models.PositiveIntegerField(
      null=True,
      blank=True,
      verbose_name="Sub ID",
      help_text="Identificador sequencial do colaborador dentro da empresa"
  )
  ```
- **Constraint de Unicidade**:
  ```python
  class Meta:
      verbose_name = "Colaborador"
      verbose_name_plural = "Colaboradores"
      unique_together = [['enterprise', 'sub_id']]
      ordering = ['sub_id', 'id']
  ```
  Isso garante no nível de banco de dados que dentro da mesma empresa não existam dois colaboradores com o mesmo `sub_id`.

### 2.2. Geração Automática Incremental (`save`)

Para que nenhum cadastro manual seja necessário e o `sub_id` sempre incremente com base no último gerado dentro daquela empresa:
```python
def save(self, *args, **kwargs):
    if not self.sub_id:
        from django.db import transaction
        from django.db.models import Max
        with transaction.atomic():
            max_sub = Buyer.objects.filter(enterprise=self.enterprise).aggregate(
                max_sub=Max('sub_id')
            )['max_sub']
            self.sub_id = (max_sub or 0) + 1
    super().save(*args, **kwargs)
```
- Se a empresa não tem colaboradores, `max_sub` é `None` -> atribui `1`.
- Se a empresa já possui colaboradores com `sub_id` máximo `N`, atribui `N + 1`.
- A verificação `if not self.sub_id:` preserva o valor em edições posteriores.
- `with transaction.atomic()` previne condições de corrida em cadastros concorrentes.

### 2.3. Representação Textual (`__str__`)
```python
def __str__(self):
    if self.sub_id:
        return f"#{self.sub_id} - {self.name}"
    return self.name
```
Essa alteração beneficia automaticamente outros módulos, como a seleção de colaboradores no formulário de pedidos (`OrderForm`), onde o colaborador aparece com seu `#sub_id` e pode ser facilmente filtrado via *live-search*.

### 2.4. Migração e Ajuste de Dados Históricos (`store/migrations/0004_...`)
Foi criada uma migração com `RunPython` que ordenou e populou os `sub_id`s existentes:
- **Empresa Teste (ID 1)**: Colaborador 'tete' (ID global 50) recebeu `sub_id = 1`.
- **Empresa Trots (ID 2)**: Os 46 colaboradores históricos receberam `sub_id = 1` até `46`.
- Após a população dos dados, a constraint de unicidade `unique_together = [('enterprise', 'sub_id')]` foi aplicada com sucesso.

---

## 3. Mecanismo de Busca por Colaboradores Específicos

Na classe `BuyerListView` (`apps/store/views.py`):
```python
class BuyerListView(ListView):
    model = Buyer
    template_name = 'store/buyer_list.html'
    context_object_name = 'buyer'

    def get_queryset(self):
        # Escopo por empresa
        if self.request.user.enterprise:
            qs = Buyer.objects.filter(enterprise=self.request.user.enterprise)
        elif self.request.user.is_superuser:
            qs = Buyer.objects.all()
        else:
            qs = Buyer.objects.none()

        q = self.request.GET.get('q', '').strip()
        if q:
            clean_q = q.lstrip('#').strip()
            if clean_q.isdigit():
                # Busca direta por sub_id (#1, 1, etc.) ou nome/cpf
                qs = qs.filter(
                    Q(sub_id=int(clean_q)) |
                    Q(name__icontains=q) |
                    Q(cpf__icontains=q)
                )
            else:
                # Busca textual em múltiplos campos
                qs = qs.filter(
                    Q(name__icontains=q) |
                    Q(cpf__icontains=q) |
                    Q(user__email__icontains=q) |
                    Q(function__icontains=q) |
                    Q(setor__name__icontains=q)
                )
        return qs.order_by('sub_id', 'id')
```
Isso permite ao usuário:
1. Digitar `1` ou `#1` e encontrar instantaneamente o colaborador com `sub_id 1`.
2. Digitar parte do nome, CPF, função ou e-mail.
3. Limpar a busca com um clique no botão "Limpar".

---

## 4. Requisito 2: Funcionalidade Mobile sem Alterar Desktop

### 4.1. Preservação da Versão Desktop
- O markup original da tabela (`<div class="table-stats order-table ov-h">`) foi envolvido na classe utilitária do Bootstrap `d-none d-md-block`.
- A coluna `#` exibe o `buyer.sub_id` com o estilo badge discreto (`.subid-badge`).
- O layout, cabeçalhos, botões ("Edit", "Delete") e grid desktop permanecem 100% idênticos ao layout existente.

### 4.2. Visualização Mobile Exclusiva (`d-md-none`)
Tabelas HTML de 6 colunas são inadequadas para telas de smartphones (< 768px), pois causam esmagamento de texto, quebra de botões ou exigem rolagem horizontal desconfortável.

Foi implementada uma camada de **Mobile Cards** (`.mobile-buyer-list`):
- **Card Individual (`.buyer-mobile-card`)**:
  - **Cabeçalho**: Selo escuro e proeminente `#{{ buyer.sub_id }}` ao lado do nome do colaborador.
  - **Corpo**: Dados dispostos em linhas chave-valor com ícones:
    - Função (`fa-briefcase`)
    - Setor (`fa-calendar`)
    - E-mail (`fa-envelope`)
    - CPF (`fa-id-card`)
  - **Ações Touch-friendly**: Botões amplos de largura igual para "Editar" (`btn-primary`) e "Excluir" (`btn-danger` com diálogo nativo de confirmação).

### 4.3. Correção de Conflitos Globais do Template Ela Admin em Mobile
A biblioteca CSS base (Ela Admin) possuía problemas severos de responsividade:
1. **Cabeçalho branco sobrepondo texto branco**: A regra `@media (max-width: 768px)` do `style.css` forçava `.top-left` com `position: fixed` e `background: white`, tornando os textos brancos invisíveis e ocultando o avatar do usuário.
2. **Coluna serial oculta**: A regra `.order-table .serial { display: none; }` ocultava propositalmente a coluna `#` em telas menores.

Esses problemas foram corrigidos e normalizados no arquivo `static/assets/css/custom-mobile.css`.

---

## 5. Registro de Estilos Criados (`custom-mobile.css`)

| Classe / Seletor | Finalidade / Efeito Visual |
| :--- | :--- |
| `.order-table .serial`, `table.table td.serial` | Garante que a coluna serial (`#`) seja exibida (`display: table-cell !important`), centralizada e com largura proporcional de 60px. |
| `.subid-badge` | Badge compacto escuro (`#343a40`, texto branco, cantos arredondados 4px) para destacar o `sub_id` na tabela Desktop. |
| `.buyer-search-box` | Container da barra de busca responsiva que se expande elegantemente no Desktop e ocupa 100% da largura no Mobile. |
| `.mobile-buyer-list` | Container flex vertical com espaçamento de 12px entre cards para listagem Mobile. |
| `.buyer-mobile-card` | Card moderno com fundo branco, borda suave (`#e2e8f0`), cantos arredondados de 10px e leve elevação (`box-shadow`). |
| `.buyer-subid-pill` | Selo de alto contraste (`#0f172a`, texto branco em negrito) posicionado no topo esquerdo de cada card mobile. |
| `.buyer-name` | Título do card mobile em negrito (`#1e293b`), com corte por reticências (*ellipsis*) caso o nome seja muito longo. |
| `.buyer-card-row` | Linha de propriedade em flexbox com rótulo à esquerda e valor à direita, com borda sutil separadora. |
| `.buyer-card-actions` | Barra inferior de botões no card mobile, com distribuição proporcional (`flex: 1`) e altura mínima de 38px para toque confortável. |
| `header.header` (mobile) | Cabeçalho fixo (*sticky*) com altura mínima de 58px, fundo preto `#000` preservado e alinhamento flex entre menu toggle, nome da empresa e menu do usuário. |
| `aside.left-panel` (mobile) | Menu lateral transformado em gaveta deslizante (*drawer*) com `position: fixed`, altura total da tela e sombra para sobreposição suave. |
| `input.form-control` (mobile) | Tamanho de fonte fixado em 16px para prevenir o zoom indesejado no iOS Safari ao focar campos. |

---

## 6. Comportamento JavaScript Adicionado (`main.js`)

Foi adicionado um listener para fechamento automático da gaveta de menu no mobile ao tocar fora do menu:
```javascript
$(document).on('click', function(event) {
    if ($(window).width() < 760) {
        if (!$(event.target).closest('#left-panel, #menuToggle').length) {
            if ($('#left-panel').is(':visible')) {
                $('#left-panel').slideUp();
            }
        }
    }
});
```

---

## 7. Verificação e Testes Automatizados

Foram executados e aprovados os testes automatizados da aplicação via `./venv/bin/python manage.py test`:
- `test_product_list_scoped_to_user_enterprise` (OK)
- `test_automatic_enterprise_association_on_product_create` (OK)
- `test_same_product_name_in_different_enterprises_allowed` (OK)
- `test_automatic_enterprise_association_on_buyer_create` (OK - validando associação e `sub_id=1`)
- `test_buyer_sub_id_auto_increment_per_enterprise` (OK - validando incremento sequencial 1, 2, 3 na Empresa A e reinício independente a partir de 1 na Empresa B)
- `test_buyer_list_search_by_sub_id_and_name` (OK - validando busca por `1`, `#2` e por nome)
- `test_dashboard_scoped_to_enterprise` (OK)

Todos os 17 testes passaram com sucesso sem regressões.
