# SYNC ALOEE

Automatização do fluxo de trabalho da **[Formil Química]**, consumindo a **API Aloee** para sincronização de produtos e modelos de produção.

**Link da API utilizada:** [Aloee API v1](https://api.aloee.it/swagger/index.html?urls.primaryName=API%20Aloee%20V1)

---

## 📝 Descrição

Este projeto nasceu da necessidade de controlar e monitorar a produção da minha atual empresa de forma mais ágil.
Ele integra diretamente os dados da API Aloee com nosso banco de dados, permitindo que colaboradores tenham acesso a produtos, modelos e ordens de produção sem precisar entrar manualmente na aplicação oficial.

O sistema foi desenvolvido para centralizar informações, garantir consistência nos dados e facilitar o acompanhamento da produção, tornando o fluxo mais confiável e prático para a equipe.

Este projeto foi desenvolvido para:

- Sincronizar e atualizar os dados da API da aplicação Aloee com o banco interno da empresa.
- Registrar logs detalhados de execução, incluindo resumo final.
- Evitar inconsistências no banco de dados com upserts e controle de status ativo/inativo.

---

## ⚙️ Pré-requisitos

Antes de executar o projeto, certifique-se de ter:

- Python 3.11+ instalado (para rodar via script).
- Todas as libs em 'requirements.txt'.

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



