Item 1)

(a) Sistema de previsão de demanda que roda uma vez por dia:
- Parcialmente observável: ele só enxerga o histórico de vendas e alguns dados externos, não enxerga tudo o que faz o cliente comprar.
- Agente único: não existe outro agente competindo ou cooperando com ele dentro da tarefa.
- Estocástico: a demanda real depende de fatores que o sistema não controla (clima, promoção do concorrente, economia).
- Episódico: cada previsão diária é uma decisão independente, errar hoje não muda o que ele vai prever amanhã.
- Estático: enquanto ele calcula a previsão os dados de entrada não mudam, ele roda uma vez e pronto.
- Contínuo: a quantidade prevista e as variáveis de entrada são valores numéricos que variam de forma suave.

(b) Drone de inspeção de linhas de transmissão:
- Parcialmente observável: câmera e sensores têm alcance limitado, com ruído, vento, neblina e partes da linha escondidas.
- Agente único (com outros agentes no ambiente): a tarefa é dele, mas pode existir pássaro, outro drone ou aeronave que ele precisa evitar.
- Estocástico: rajada de vento e erro de GPS fazem o drone não ir exatamente para onde mandou.
- Sequencial: a rota escolhida agora afeta a bateria e os trechos que vão faltar inspecionar depois.
- Dinâmico: o ambiente muda enquanto ele está decidindo (vento, obstáculos em movimento).
- Contínuo: posição, velocidade e altitude variam de forma contínua.

(c) Bot que negocia ações em bolsa:
- Parcialmente observável: ele vê preços e o livro de ofertas, mas não sabe a intenção dos outros investidores.
- Multiagente competitivo: os outros investidores e robôs estão disputando o mesmo lucro.
- Estocástico: o preço depois da ordem não é determinado só pela ação do bot.
- Sequencial: a compra de agora muda a posição da carteira e o risco das próximas decisões.
- Dinâmico: o preço muda enquanto o bot está pensando, se demorar perde a oportunidade.
- Discreto (na prática): ordens, lotes e preços têm valores mínimos (centavos, lotes), mas por serem muitos valores são tratados quase como contínuos.

(d) Corretor ortográfico:
- Completamente observável: o texto inteiro está disponível para ele.
- Agente único: não tem ninguém disputando a correção.
- Determinístico: trocar uma palavra por outra dá sempre o mesmo resultado no texto.
- Episódico: cada palavra (ou frase) é corrigida de forma praticamente independente das outras.
- Estático: o texto não muda enquanto ele está verificando (no caso da correção em tempo real seria semidinâmico).
- Discreto: palavras e letras são um conjunto finito de símbolos.

Item 2)

(a) Previsão de demanda: agente baseado em utilidade. A dimensão decisiva foi ser estocástico, como a demanda nunca é certa, ele precisa escolher a previsão que tem o melhor valor esperado (equilibrar o custo de sobrar estoque com o custo de faltar produto), e isso é uma função de utilidade, não um objetivo sim/não.

(b) Drone de inspeção: agente reflexo baseado em modelo. A dimensão decisiva foi ser parcialmente observável, o drone precisa guardar um estado interno (onde ele está, quais trechos já inspecionou, bateria restante) porque os sensores não mostram tudo de uma vez.

(c) Bot da bolsa: agente com aprendizagem. A dimensão decisiva foi ser multiagente competitivo e dinâmico, o comportamento dos outros investidores muda o tempo todo, então regras fixas deixam de funcionar e o bot precisa aprender com os resultados (o crítico avalia o lucro e o elemento de aprendizado ajusta a estratégia).

(d) Corretor ortográfico: agente reflexo simples. A dimensão decisiva foi ser completamente observável (junto com episódico), a palavra atual já é suficiente para decidir, então uma regra "se a palavra não está no dicionário, sugerir a mais parecida" resolve.

Item 3)

(a) Falso. O aspirador de pó do livro só enxerga o quadrado onde está e mesmo assim é racional, porque aspira quando está sujo e muda de lado quando está limpo, que é o melhor que dá para fazer com a percepção que ele tem. Racionalidade é fazer o melhor com o que se percebe, e não saber tudo.

(b) Verdadeiro. Se o ambiente tiver só uma ação possível, ou se todas as ações derem a mesma pontuação na medida de desempenho, qualquer agente é racional. Exemplo: um ambiente onde a medida de desempenho dá sempre nota 10, independente do que o agente faça.

(c) Falso. A medida de desempenho é definida sobre a sequência de estados do ambiente, e não sobre o que o agente percebe. Exemplo: no aspirador que só vê o próprio quadrado, dois mundos podem gerar as mesmas percepções, mas em um deles o outro quadrado está sujo e no outro está limpo, então a nota é diferente com as mesmas percepções.

Item 4) Pseudocódigo abaixo e código no arquivo "aspirador.py". Print no arquivo: "Prints_Aula04.pdf".

```
função AGENTE-BASEADO-EM-OBJETIVOS(percepção) retorna uma ação
    persistente: estado, plano (sequência de ações, inicialmente vazia)
                 objetivo = "A limpo e B limpo"

    estado <- ATUALIZAR-ESTADO(estado, percepção)
    se OBJETIVO-ATINGIDO(estado, objetivo) então retorna NoOp
    se plano está vazio então
        plano <- BUSCA(estado, objetivo)      // ex.: [Aspirar, Direita, Aspirar]
    ação <- PRIMEIRO(plano); plano <- RESTO(plano)
    estado <- RESULTADO(estado, ação)
    retorna ação
```

```
função AGENTE-BASEADO-EM-UTILIDADE(percepção) retorna uma ação
    persistente: estado

    estado <- ATUALIZAR-ESTADO(estado, percepção)
    melhor <- NoOp
    para cada ação em {Esquerda, Direita, Aspirar, NoOp} faça
        valor(ação) <- soma de P(s' | estado, ação) * UTILIDADE(s')
        se valor(ação) > valor(melhor) então melhor <- ação
    estado <- RESULTADO(estado, melhor)
    retorna melhor

UTILIDADE(s) = 10 * (quadrados limpos) - 1 * (movimentos) - 0,5 * (aspiradas)
```

A diferença é que o de objetivos só quer saber se chegou ou não em "tudo limpo", enquanto o de utilidade compara quanto cada ação vale, então ele não fica andando à toa quando está tudo limpo, porque andar custa energia.

Item 5) O agente dirigido por tabela tem o comportamento correto porque para cada sequência de percepções já tem a ação certa escrita na tabela, o problema é o tamanho. A tabela precisa de uma linha para cada sequência possível de percepções, e isso cresce de forma exponencial com o tempo, então não tem memória para guardar, não tem tempo para alguém montar e o agente não consegue aprender todas as entradas.

Estimativa: 10 bits dão 2^10 = 1024 percepções diferentes por segundo. Em uma hora são 3600 percepções, então a tabela tem cerca de 1024^3600 = 2^36000 ≈ 10^10837 entradas. Para comparar, o universo observável tem cerca de 10^80 átomos. Código no arquivo "tabela.py". Print no arquivo: "Prints_Aula04.pdf".

Item 6) Um exemplo é o sistema de freio ABS do carro. Ele funciona com a regra "se a roda travou, alivia a pressão do freio", usando só a leitura atual do sensor da roda. Os requisitos que justificam o reflexo simples são: precisa responder em milissegundos (não dá tempo de planejar), a percepção atual já é suficiente para decidir, o comportamento tem que ser previsível e fácil de testar por questão de segurança, e roda em um hardware simples e barato. Uma arquitetura mais sofisticada seria mais lenta e mais difícil de certificar, sem ganho real para essa tarefa.
