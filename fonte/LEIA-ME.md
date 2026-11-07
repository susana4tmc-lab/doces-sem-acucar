# Fonte do livro "Doces sem açúcar"

Tudo o que é preciso para refazer as três versões do livro, mantendo o mesmo estilo.
Esta pasta não é publicada no site (ver `.vercelignore` na raiz).

## Onde está cada versão

| Versão | Onde |
| --- | --- |
| Documento editável (fonte do texto) | Claude Docs: https://claude.ai/code/artifact/f3fa9970-6f66-4690-8a29-eb4c9c3833f3 |
| Página online para os pais | https://doces-sem-acucar-jv.vercel.app (publicada pelo Vercel a partir da raiz deste repositório) |
| PDF A4 | gerado com `livro.py` |
| Livrinho A5 para imprimir em casa | gerado com `livro.py ... a5` + `impor.py` |
| Formulário "Partilhe a sua receita" | https://forms.gle/4NQwqCLPMVdaoxg66 (conta Google da escola; respostas na folha "Receitas recebidas — Doces sem açúcar") |

Regra combinada: **sempre que o livro muda, atualizam-se as três versões** (A4, livrinho A5 e página online).

## Como atualizar

1. Editar o documento no Claude Docs (receitas novas: secção `## Receitas`, uma `###` por receita; acrescentar também ao índice e à tabela de alergénios).
2. Exportar o documento em Markdown e guardar como `livro.md` nesta pasta.
3. Para uma receita nova: criar `<nome>.py` a partir de um dos scripts de ilustração (ex.: `tiramisu.py`), gerar `<nome>-retro.png`,
   e acrescentar a entrada em `IMAGES` (livro.py) e em `IMG` (gen_web.py), com a cor de fundo.
4. Gerar:
   ```
   python3 livro.py <pasta> livro.md "Doces sem açúcar - Receitas para a Família.pdf"
   python3 livro.py <pasta> livro.md a5.pdf a5
   python3 impor.py a5.pdf "Doces sem açúcar - Livrinho A5 para imprimir.pdf"
   python3 gen_web.py <pasta> livro.md ../index.html
   ```
   Para o site, copiar também as ilustrações novas para `../img/` em JPG (1200 px, qualidade 84).
   O ícone da app (queque retro) gera-se com `python3 icone.py <pasta> ../icons`; o `manifest.webmanifest` na raiz dá o nome "Doces" e as cores quando os pais põem o site no ecrã do telemóvel.
5. Fazer commit e push: o Vercel publica sozinho.

Verificar sempre: cada receita cabe numa página no A4 (`.long` reduz a imagem quando há mais de 9 ingredientes);
o A5 tem de ter um número de páginas múltiplo de 4 (ajustar a página "As nossas notas" se for preciso);
os códigos QR leem os links certos.

## Requisitos

- Python 3 com `cairosvg`, `weasyprint`, `markdown`, `pypdf`, `Pillow`, `qrcode`.
- Fontes (licença OFL) em `fontes-letra/`: copiar para `~/.fonts/` e correr `fc-cache -f`.

## Estilo e critérios

- Ilustrações retro anos 60 (`retro.py`): sol de raios, fundo às bolinhas, toalha aos quadrados vermelhos, etiqueta creme com título em Pacifico e subtítulo em Fredoka. Cada receita tem uma cor de fundo própria.
- Formato de cada receita: descrição curta; Tempo · Forno · Doses; Ingredientes; Preparação numerada; Dica; crédito em itálico no fim, quando há.
- Adoça-se com fruta; mel e xaropes naturais (tâmara, ácer) só com moderação. Sem açúcar, adoçantes nem xilitol.
- Cacau sempre "100%, sem açúcar"; chocolate negro 70% ou mais; bebidas vegetais "sem açúcar".
- Assinalar glúten (espelta tem glúten; aveia só sem glúten se certificada), lactose, ovo e frutos secos.
- Receitas de alunos: "Adaptado da receita de <nome>, <turma>", com nota sobre o que foi mudado.
