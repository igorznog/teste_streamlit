# SPEC — Validação do fiap-academic-workflow

## Objetivo

Validar se o novo workflow consegue substituir o fluxo WOLF antigo para próximas tasks FIAP, mantendo contexto histórico suficiente para orientar novos trabalhos e facilitar adoção pelos colegas.

## Escopo

- Clonar o repo oficial em `~/fiap-academic-workflow`.
- Preencher `GROUP.md` e `LOCAL.md`.
- Migrar `knowledge/` e tasks históricas para estrutura do framework.
- Criar documentação de validação para o Higor e colegas.
- Não fazer commit/push automaticamente nesta etapa.

## Critérios de sucesso

- Uma nova sessão de IA no workspace consegue ler `TASK_REGISTRY.md`, `GROUP.md` e `LOCAL.md` e entender quem é o Higor, quem é o grupo e quais foram as últimas entregas.
- A pasta `knowledge/` contém material de aula reaproveitável.
- Entregas antigas ficam em `tasks/imported/`, separadas dos exemplos do template.
- O grupo consegue seguir `SETUP.md` e criar seu próprio `LOCAL.md`.
