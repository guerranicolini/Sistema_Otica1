
# Sistema de Gestão Médica

Um sistema completo de gestão médica desenvolvido em Python com interface gráfica usando Tkinter.

## Funcionalidades

### 📋 Gestão de Clientes
- Cadastro completo de clientes
- Controle de informações pessoais e contatos
- Histórico de cadastros

### 👨‍⚕️ Gestão de Médicos
- Cadastro de médicos com especialidades
- Controle de CRM
- Informações de contato

### 🏥 Gestão de Produtos
- Cadastro de produtos médicos
- Controle de estoque
- Categorização de produtos
- Precificação

### 📦 Gestão de Pedidos
- Criação de pedidos
- Associação cliente-médico-produto
- Controle de status
- Cálculo automático de valores

### 📅 Agenda
- Agendamento de consultas
- Controle de horários
- Status de agendamentos
- Histórico completo

### 📊 Relatórios
- Relatórios detalhados de todas as áreas
- Gráficos interativos
- Análise de vendas
- Estatísticas do sistema

## Tecnologias Utilizadas

- **Python 3.11+**
- **Tkinter** - Interface gráfica
- **SQLite** - Banco de dados
- **Matplotlib** - Gráficos e relatórios

## Como Executar

1. Clone o repositório
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute o sistema:
   ```bash
   python main.py
   ```

## Estrutura do Projeto

```
├── main.py                 # Arquivo principal
├── modules/                # Módulos do sistema
│   ├── __init__.py
│   ├── clientes.py        # Gestão de clientes
│   ├── medicos.py         # Gestão de médicos
│   ├── produtos.py        # Gestão de produtos
│   ├── pedidos.py         # Gestão de pedidos
│   ├── agenda.py          # Sistema de agenda
│   └── relatorios.py      # Sistema de relatórios
├── requirements.txt       # Dependências
└── README.md             # Documentação
```

## Banco de Dados

O sistema utiliza SQLite com as seguintes tabelas:
- `clientes` - Informações dos clientes
- `medicos` - Informações dos médicos
- `produtos` - Catálogo de produtos
- `pedidos` - Registros de pedidos
- `agenda` - Agendamentos

## Contribuição

Para contribuir com o projeto:
1. Faça um fork do repositório
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT.
