# Site Acessível do Guia Marisol

Versão web acessível do guia **Todas as Mulheres: Dignidade, Cidadania e Direitos Humanos para Travestis e Mulheres Trans**.

## Objetivo

O projeto converte o PDF original em uma experiência HTML navegável, pesquisável e compatível com teclado e leitores de tela, tendo WCAG 2.2 AA como meta de implementação.

## Estrutura

- `public/index.html`: página estática principal com o conteúdo completo pré-renderizado.
- `public/styles.css`: estilos acessíveis, responsivos e com modo alto contraste.
- `public/app.js`: busca e preferências de leitura, sem depender de JavaScript para exibir o conteúdo.
- `public/guide.json`: conteúdo extraído do PDF.
- `src/content/guide.json`: fonte estruturada do conteúdo extraído.
- Link público oficial do Ministério das Mulheres: PDF original para download.
- `scripts/build_content.py`: gerador do JSON a partir do PDF local.
- `scripts/render_index.py`: gerador do HTML estático a partir do JSON.
- `scripts/audit_static.py`: auditoria local de estrutura acessível e contraste.
- `firebase.json`: configuração do Firebase Hosting sem ID de projeto fixo.

## Desenvolvimento local

Sirva a pasta `public` com qualquer servidor estático. Exemplo:

```bash
python -m http.server 5173 -d public
```

Depois acesse `http://localhost:5173`.

## Atualizar conteúdo

Com o PDF original disponível em `C:\Users\rafac\OneDrive\Documentos\document.pdf`, execute:

```bash
python scripts/build_content.py
python scripts/render_index.py
```

## Auditoria estática

```bash
python scripts/audit_static.py
```

## Deploy Firebase

Este repositório não inclui `.firebaserc`. Selecione o projeto no ambiente local ou no CI:

```bash
firebase use <project-id>
firebase deploy --only hosting
```
