# SYNC ALOEE

Automatização do fluxo de trabalho da **Formil Química**, consumindo a **API Aloee** para sincronização de dados da aplicação Aloee com o banco de dados interno.

**Link da API utilizada:** [Aloee API v1](https://api.aloee.it/swagger/index.html?urls.primaryName=API%20Aloee%20V1)

---

## 📝 Descrição

Este projeto foi criado para otimizar o controle e monitoramento da produção da empresa, automatizando a integração entre a API Aloee e o banco de dados interno. Com isso, a equipe de TI e outros setores conseguem acessar informações atualizadas de produtos, modelos de produção, ordens e grupos de recursos sem a necessidade de consultar manualmente a aplicação oficial.

O sistema centraliza os dados, garantindo consistência, confiabilidade e rastreabilidade, e facilita o acompanhamento da produção em tempo real, reduzindo erros e retrabalho.

As principais funcionalidades do projeto incluem:

- Sincronização de dados: atualiza produtos, modelos de produção, ordens e grupos de recurso da API Aloee no banco interno.

- Registro de logs detalhados: mantém histórico de execuções, incluindo resumo final e status de cada operação.

- Controle de consistência: evita duplicidades ou dados inconsistentes usando upserts e gerenciamento de status ativo/inativo.

- Flexibilidade e confiabilidade: permite execução automática ou manual do processo, garantindo que os dados estejam sempre atualizados.

---

## ⚙️ Pré-requisitos

Antes de executar o projeto, certifique-se de que:

- Python 3.11+ instalado.
- Todas as dependências listadas em requirements.txt foram instaladas:
---

## 🚀 Como executar

Via Python (para desenvolvimento)

    python -m venv venv
    venv\Scripts\activate  # Windows
    pip install -r requirements.txt
    python main.py

---

Gerando o executável (.exe)

    pyinstaller --onefile --name sync_aloee --console --add-data ".env;." main.py

O .exe será gerado na pasta dist/ e poderá ser executado diretamente no Windows.

---

## 🛠️ Observações

- Sempre mantenha o .env atualizado com as credenciais corretas.
- Sempre que fizer uma nova alteração no código, faça outro .exe
- Certifique-se de que a porta do SQL Server esteja aberta e que a conexão seja permitida.
- Para problemas de conexão (08001 ou 11001), verifique IP, porta e firewall.



