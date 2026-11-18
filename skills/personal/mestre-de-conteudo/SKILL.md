---
name: mestre-de-conteudo
description: Produz conteúdo orgânico para o Instagram do projeto sob demanda. Use para selecionar fotos de festa ou evento e escrever a legenda, criar uma arte informativa ou preparar um lote editorial.
---

# Mestre de Conteúdo

Atenda ao pedido na escala solicitada. Uma festa rende uma seleção e uma legenda. Um pedido de arte rende uma peça pronta para revisar. Para um lote semanal, use a cadência combinada com quem pediu. Na ausência de outra referência, sugira dois posts com uma revisão conjunta. O comando funciona sob demanda.

Comece pelas orientações do projeto em que a skill foi acionada. Consulte o painel editorial, a descrição do negócio e o acervo indicado pela pessoa responsável. Use as regras da marca e os fatos do negócio para distinguir o que o buffet oferece do que foi servido naquele evento. Consulte o que já estiver preparado para a mesma pauta em `work/instagram/`.

## Quando o material é de um evento

1. Localize a pasta indicada no acervo autorizado do projeto, ou a cópia local com origem conhecida. Abra as fotos antes de escolher. Se as fotos ainda não estiverem acessíveis, peça o link ou os arquivos e identifique o que consegue adiantar.
2. Escolha a melhor foto se ela conta a história sozinha. Para um carrossel, selecione uma capa legível no celular e uma sequência que acrescente algo a cada imagem, como mesa inteira, detalhe e serviço. Respeite a ordem de uma seleção já aprovada para a pauta. Mantenha as fotos do mesmo evento juntas. Dê preferência a comida, mesa e serviço de quem prestou o serviço. Observe foco, corte, repetições e pessoas identificáveis.
3. Escreva a legenda em português brasileiro com um detalhe que o leitor consiga ver. Use o contexto confirmado para citar tipo de festa, prato ou ocasião. Escolha uma chamada que faça sentido para a pauta. Uma festa pode pedir apenas uma boa legenda e as fotos na ordem certa. Registre a origem de cada foto e qualquer liberação ainda pendente.

## Quando o pedido é uma arte

Parta da mensagem que alguém precisa entender, por exemplo o que informar para pedir orçamento. Faça uma peça gráfica ou um carrossel quando houver etapas que mereçam páginas próprias. Aplique os SVGs originais e a paleta do projeto. Para fotografar um evento só vale o material real do acervo. Gere e abra o arquivo final (PNG ou JPG), confira texto, contato, logo, legibilidade e cortes em tamanho de celular. Entregue também a legenda e a fonte editável quando criada. Para um card tipográfico simples, há um gerador local, com parâmetros em `--help`. Ele recebe o SVG e três cores da marca em hexadecimal e usa Python 3 e um navegador Chromium instalado. [Gerador de cards](scripts/criar_card.py).

## O que entregar

Salve a seleção ordenada ou a arte, a legenda e as pendências em `work/instagram/<pauta>/revisao.md`, ao lado das exportações quando existirem. Use um nome estável para a pauta ou, para um lote, a segunda-feira da semana em `AAAA-MM-DD`. Se a pasta já existe, leia a revisão e retome as peças de lá, preservando os ajustes da revisão. Os dois aplicativos usam a mesma pasta local.

Mostre a quem pediu uma prévia de cada peça e aponte somente o que ainda exige decisão. Para uma sequência, entregue os nomes ou links das fotos na ordem de publicação. Registre quem liberou o material e quem poderá aprovar a versão e o horário. Entregue o rascunho para revisão. Programação recorrente e postagem dependem de pedido próprio.
