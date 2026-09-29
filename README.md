Item 1)

(a) Previsão de demanda que roda uma vez por dia:
Parcialmente observável, porque ele só tem o histórico de vendas e alguns dados de fora, não enxerga tudo que faz o cliente comprar.
Agente único, não tem outro agente disputando ou cooperando com ele.
Estocástico, a demanda depende de coisas que ele não controla (clima, promoção do concorrente, economia).
Episódico, cada previsão do dia é independente, errar hoje não muda a decisão de amanhã.
Estático, os dados não mudam enquanto ele calcula, ele roda uma vez e acabou.
Contínuo, as quantidades previstas e as variáveis de entrada são números que variam de forma suave.

(b) Drone de inspeção de linhas de transmissão:
Parcialmente observável, a câmera e os sensores têm alcance limitado e ruído (vento, neblina, partes da linha escondidas).
Agente único, a tarefa é só dele, mas pode ter pássaro ou outra aeronave no caminho que ele precisa desviar.
Estocástico, uma rajada de vento ou erro de GPS faz ele não ir exatamente para onde mandou.
Sequencial, o caminho que ele escolhe agora afeta a bateria e o que falta inspecionar depois.
Dinâmico, o ambiente muda enquanto ele está decidindo.
Contínuo, posição, altura e velocidade variam de forma contínua.

(c) Bot que negocia ações na bolsa:
Parcialmente observável, ele vê os preços e as ofertas, mas não sabe o que os outros investidores pretendem fazer.
Multiagente competitivo, os outros investidores e robôs estão disputando o mesmo lucro.
Estocástico, o preço depois da ordem não depende só do que o bot fez.
Sequencial, cada compra ou venda muda a carteira e o risco das próximas decisões.
Dinâmico, o preço muda enquanto ele pensa, se demorar perde a oportunidade.
Discreto, porque preço e quantidade andam em centavos e lotes, mas como são muitos valores dá pra tratar quase como contínuo.

(d) Corretor ortográfico:
Completamente observável, o texto inteiro está disponível para ele.
Agente único, ninguém mais está corrigindo o texto.
Determinístico, trocar uma palavra por outra sempre dá o mesmo resultado.
Episódico, cada palavra é corrigida praticamente sem depender das outras.
Estático, o texto não muda enquanto ele verifica (se for corrigindo enquanto a pessoa digita, aí seria semidinâmico).
Discreto, palavras e letras são um conjunto finito.

Item 2)

(a) Previsão de demanda: agente baseado em utilidade. O que decidiu foi ser estocástico. Como a demanda nunca é certa, ele tem que escolher a previsão com melhor valor esperado, pesando o prejuízo de sobrar estoque contra o de faltar produto. Isso não é um objetivo de sim ou não.

(b) Drone: agente reflexo baseado em modelo. O que decidiu foi ser parcialmente observável. Ele precisa guardar um estado interno (onde está, o que já inspecionou, quanto de bateria sobrou) porque os sensores não mostram tudo de uma vez.

(c) Bot da bolsa: agente com aprendizagem. O que decidiu foi ser multiagente competitivo e dinâmico. Os outros investidores mudam o comportamento o tempo todo, então regra fixa para de funcionar e ele precisa ir aprendendo com o resultado das operações.

(d) Corretor ortográfico: agente reflexo simples. O que decidiu foi ser completamente observável e episódico. Só a palavra atual já basta para decidir, uma regra do tipo "se a palavra não está no dicionário, sugere a mais parecida" resolve.

Item 3)

(a) Falso. O aspirador do livro só enxerga o quadrado onde ele está e mesmo assim é racional, porque aspira quando está sujo e troca de lado quando está limpo. Ser racional é fazer o melhor com o que percebe, e não saber de tudo.

(b) Verdadeiro. Se no ambiente todas as ações dão a mesma nota na medida de desempenho (ou só existe uma ação possível), qualquer agente é racional, já que não tem como fazer melhor que outro.

(c) Falso. A medida de desempenho é em cima dos estados do ambiente e não das percepções. No aspirador que só vê o próprio quadrado, dois mundos podem dar exatamente as mesmas percepções, um com o outro quadrado sujo e outro com ele limpo, e a nota vai ser diferente.

Item 4) O código está no arquivo aspirador.py.

```
função AGENTE-BASEADO-EM-OBJETIVOS(percepção) retorna uma ação
    persistente: estado, plano (vazio no início)
                 objetivo = A limpo e B limpo

    estado <- ATUALIZAR-ESTADO(estado, percepção)
    se estado satisfaz objetivo então retorna NoOp
    se plano vazio então
        plano <- BUSCA(estado, objetivo)
    ação <- PRIMEIRO(plano)
    plano <- RESTO(plano)
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

UTILIDADE = 10 por quadrado limpo - 1 por movimento - 0,5 por aspirada
```

O de objetivos só quer saber se chegou em tudo limpo ou não. O de utilidade compara quanto cada ação vale, então quando está tudo limpo ele para, porque andar e aspirar gastam energia.

Item 5) Ele tem o comportamento certo porque a tabela já tem a ação para qualquer sequência de percepções, o problema é o tamanho. Precisa de uma linha para cada sequência possível, e isso cresce exponencialmente com o tempo. Não tem memória para guardar, ninguém consegue montar essa tabela e o agente também não conseguiria aprender todas as entradas.

Com 10 bits são 2^10 = 1024 percepções diferentes por segundo. Em uma hora são 3600 percepções, então a tabela fica com mais ou menos 1024^3600 = 2^36000, que dá por volta de 10^10837 entradas. Só para comparar, o universo observável tem uns 10^80 átomos. A conta está no arquivo tabela.py.

Item 6) O freio ABS do carro. Ele funciona com a regra "se a roda travou, alivia a pressão do freio", olhando só a leitura atual do sensor da roda. Faz sentido ser reflexo simples porque precisa responder em milissegundos, a leitura atual já é suficiente para decidir, o comportamento tem que ser previsível e fácil de testar por ser um sistema de segurança, e roda num hardware simples. Uma arquitetura mais sofisticada deixaria mais lento e mais difícil de testar sem ganhar nada com isso.
