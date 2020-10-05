Opel Corsa AUX
##############

:Title: Car AUX
:Date: 2014-02-14 00:28
:Category: electronics
:Tags: car audio aux cd
:Slug: car-aux-input-cd
:Authors: Nuno Leitao
:Summary: Added AUX input to autoradio

Tendo um autorádio de origem num carro de 2001, leva a que não tenha algumas
funcionalidades que é quase um absurdo não ter hoje em dia.  
 
Falo na possibilidade de ter uma entrada externa - seja um leitor de MP3 ou
similar.

Reparo que o carro tem um espaço por baixo dos controlos da ventilação interna,
então vou usar este mesmo buraco para passar os cabos, deixando o painel do
rádio intacto, e deixando em aberto a possibilidade de reverter a operação em
qualquer altura.  
  
Encontrei algumas receitas online e venho aqui fazer um registo.  
Baseei esta adaptação nesta solução:
[http://www.css-haupt.de/vectra/english.html](http://www.css-haupt.de/vectra/english.html)  
  
O principal problema foi retirar o aparelho do carro.  
Apesar de ter parafusos, estes não têm outro fim que não seja estético - tapar
literalmente os orifícios de acesso às molas que permitem extrair o rádio.  
  
Para conseguir aceder às malditas molas, usei vários métodos, todos sem
sucesso - os apetrechos ou eram muito finos ou entravam à justa, que tornava impossível
fazer a coisa. Tive sucesso usando um cabide de arame, que tive de destruir para o efeito.  

.. image:: {static}/images/aux/raux_final01.jpg

Passo a apresentar o material que utilizei:  

.. image:: {static}/images/aux/raux_material.jpg

Por ordem de utilização:

*   alicate
*   cabide de arame
*   chave de fendas pequena
*   mini-berbequim (e lima circular de agulha - não aparece na foto)
*   ferros de soldar (solda 60/40, resina de soldar)
*   fio audio (veio a ser ser substituido por cabo blindado)
*   multímetro (usado unicamente para verificar qualidade da soldadura)

  

Com a chave de fendas pequena retirei a tampa que protege a placa de circuito
impresso e identifiquei os conectores responsáveis pelo áudio.

Procurei fazer um buraco, não por cima dos conectores, mas um pouco mais
afastado, para que o cabo pudesse esticar, prevenindo curto circuitos.

.. image:: {static}/images/aux/raux_tampa.jpg

Ora os pinos são estes dois, do que apurei noutros sites, o A é o canal
esquerdo, o B é o canal direito.

Falta o sinal terra, ainda não resolvi essa questão no momento em que escrevo
isto, mas pretendo fazer uma solução mais elegante do que as que já encontrei.

.. image:: {static}/images/aux/raux_conectoresAlvo.jpg

Este texto dedica-se a quem nunca fez este tipo de trabalhos.

O primeiro passo nestas coisas é simplificar a coisa e minimizar o estragos,
quer devido à tremedeira, ou aplicação de excesso de calor nos componentes.

Vamos para isso estanhar as peças a soldar.

A receita que apresento consiste em primeiramente, mergulhar os conectores na
resina. Isto faz-se mergulhando a ponta do ferro na resina (durante este
processo deve-se soprar devagar na direcção da resina para afastar o fumo e
evitar respirar os vapores). Quando a resina estiver liquefeita, então
retira-se o ferro e mergulha-se as pontas descarnadas.

.. image:: {static}/images/aux/raux_estanharFio1.jpg

A resina serve somente para baixar o ponto de fusão da solda. Pessoalmente dou
preferência à solda 60-40  pois é muito fácil de utilizar.  
A técnica para estanhar o fio, baseia-se na técnica de capilaridade. Juntando
o ferro e a solda ao fio encharcado em resina, a resina irá evaporar e a solda
irá ocupar o seu lugar.  
  

.. image:: {static}/images/aux/raux_estanharFio2.jpg

  
Seguidamente corta-se as pontas para a dimensão que melhor se adequa.  
  

.. image:: {static}/images/aux/raux_estanharFio3.jpg

Mergulha-se a solda na resina tal como se fez com o fio, e estanha-se os
conectores

.. image:: {static}/images/aux/raux_estanharConectores.jpg

  

Agora o processo de soldadura é muito mais simples. Basta encostar os dois
elementos e encostar o ferro ligeiramente.

.. image:: {static}/images/aux/raux_soldar.jpg


Devidamente validada a soldadura com o multímetro,agora é só fechar tudo.
Repare-se o fio devidamente entalado, e o selo de garantia quebrado.  

.. image:: {static}/images/aux/raux_fechado.jpg

  
Uma vez fechado, quis dar uma vista de olhos melhor ao sistema de fecho do
rádio.

.. image:: {static}/images/aux/raux_retirar1.jpg

.. image:: {static}/images/aux/raux_retirar2.jpg

Falta  
  

*   Fazer chegar um sinal de terra ao exterior;
*   Adaptar uma ficha audio na extremidade do fio
*   Criar um CD com 80 minutos de silêncio

  
.. image:: {static}/images/aux/raux_ferro.jpg


Resultados
**********

O rádio funciona perfeitamente, contudo a ligação externa tem demasiado ruído
causado cada vez que se toca no fio. Substituí o fio por um cabo blindado.  
Claro que não pude utilizar o ponto de massa que tinha escolhido, pois está
demasiado afastado e perdia o propósito da blindagem.  
  

.. image:: {static}/images/aux/raux_fix01.jpg

A seta amarela indica onde estava o a massa soldada, e onde está soldada
actualmente.


.. image:: {static}/images/aux/raux_fix02.jpg

  
Caixa do rádio fechada. Agora com o cabo blindado.  
  

.. image:: {static}/images/aux/raux_fix03.jpg

  
Rádio colocado no sítio, colocando os parafusos estéticos.  
  

.. image:: {static}/images/aux/raux_fix04.jpg

  
E em funcionamento! :D


