# SYNC ALOEE

Automatização de monitoramento da **[Formil Quimica]**, consumindo a **API Aloee** para sincronização de produtos e modelos de produção.

**Link da API utilizada:** [Aloee API v1](https://api.aloee.it/swagger/index.html?urls.primaryName=API%20Aloee%20V1)

---

## 📝 Descrição

Este projeto nasceu da necessidade de controlar e monitorar a produção da minha atual empresa de forma mais ágil.
Ele integra diretamente os dados da API Aloee com nosso banco de dados, permitindo que colaboradores tenham acesso a produtos, modelos e ordens de produção sem precisar entrar manualmente na aplicação oficial.

O sistema foi desenvolvido para centralizar informações, garantir consistência nos dados e facilitar o acompanhamento da produção, tornando o fluxo mais confiável e prático para a equipe.

Este projeto foi desenvolvido para:

- Sincronizar produtos da API Aloee com o banco interno da empresa.
- Atualizar modelos de produção de forma automatizada.
- Registrar logs detalhados de execução, incluindo resumo final.
- Evitar inconsistências no banco de dados com upserts e controle de status ativo/inativo.

---
