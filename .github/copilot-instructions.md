# Instruções do projeto — FIAP (GitHub Copilot)

- Leia primeiro [`TASK_REGISTRY.md`](../TASK_REGISTRY.md), depois [`GROUP.md`](../GROUP.md) (grupo e membros). Se existir [`LOCAL.md`](../LOCAL.md), leia para saber quem usa este clone.
- O contrato completo do workflow (agnóstico de IDE) está em [`docs/FRAMEWORK.md`](../docs/FRAMEWORK.md). Integração de colegas: [`SETUP.md`](../SETUP.md).
- Para task FIAP nova, crie primeiro `specs/taskNN_nome/SPEC.md`. Se for grupo, crie também `SPLIT.md` e `INTEGRATION.md`; só depois implemente em `tasks/taskNN_nome/`.
- O usuário pode colar o enunciado inteiro da task no chat; processe requisitos, entregáveis e modo solo/grupo antes de escrever código.
- Para aula nova, aceite PDF anexado ou texto copiado da página da aula; salve pílula e flashcards em `knowledge/<disciplina>/`.
- Conteúdo didático vai para `knowledge/<disciplina>/` em Markdown; comentários ao utilizador em **português (Brasil)**; código com identificadores em inglês.
- Não sugerir commit ou push sem o utilizador pedir; nunca incluir senhas ou tokens em ficheiros.
