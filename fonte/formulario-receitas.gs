/**
 * Cria o formulário "Partilhe a sua receita sem açúcar" do livro Doces sem açúcar
 * (Dia da Alimentação 2026 · EB João Villaret · Saúde Escolar, UCC Loures)
 * e uma folha Google onde ficam as respostas.
 *
 * Como usar:
 * 1. Abra https://script.google.com e carregue em "Novo projeto".
 * 2. Apague o que lá estiver, cole este código todo e guarde (ícone da disquete).
 * 3. Em cima, escolha a função "criarFormulario" e carregue em "Executar".
 * 4. Autorize o acesso quando o Google pedir (é a sua própria conta).
 * 5. Abra "Registo de execução" (em baixo): tem lá os links do formulário e da folha.
 */
function criarFormulario() {
  const form = FormApp.create('Partilhe a sua receita sem açúcar');

  form.setDescription(
    'Tem uma receita doce feita sem açúcar refinado que a sua família adora? ' +
    'Partilhe-a connosco! As receitas recebidas são revistas pela equipa de Saúde Escolar ' +
    'e algumas serão adaptadas e publicadas no livro "Doces sem açúcar — Receitas para a família", ' +
    'da EB João Villaret.\n\n' +
    'Neste livro adoçamos com fruta (banana, maçã, tâmaras…) e, com moderação, mel ou xaropes naturais. ' +
    'Não usamos açúcar, adoçantes nem xilitol.\n\n' +
    'Não é preciso conta Google para responder.'
  );
  form.setCollectEmail(false);
  form.setAllowResponseEdits(false);
  form.setShowLinkToRespondAgain(true);
  form.setProgressBar(true);
  form.setConfirmationMessage(
    'Obrigado pela sua receita! A equipa de Saúde Escolar vai lê-la com atenção. ' +
    'Se for escolhida, aparece numa próxima edição do livro "Doces sem açúcar".'
  );
  try { form.setRequireLogin(false); } catch (e) { /* só existe em contas Google Workspace */ }

  // --- A receita ---
  form.addSectionHeaderItem().setTitle('A receita');

  form.addTextItem()
    .setTitle('Nome da receita')
    .setHelpText('Por exemplo: Bolo de maçã e canela da avó')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('Ingredientes')
    .setHelpText('Um ingrediente por linha, com as quantidades. Por exemplo: 3 ovos · 2 bananas maduras · 1 chávena de farinha de aveia')
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('Modo de preparação')
    .setHelpText('Descreva os passos pela ordem em que se fazem.')
    .setRequired(true);

  form.addTextItem()
    .setTitle('Tempo de preparação e de forno')
    .setHelpText('Por exemplo: 10 minutos + 30 minutos de forno. Se não vai ao forno, indique só o tempo.');

  form.addTextItem()
    .setTitle('Temperatura do forno')
    .setHelpText('Por exemplo: 180 °C. Deixe em branco se não vai ao forno.');

  form.addTextItem()
    .setTitle('Quantas doses ou fatias dá?');

  const doce = form.addCheckboxItem();
  doce.setTitle('O que dá o sabor doce a esta receita?')
    .setChoices([
      doce.createChoice('Fruta fresca (banana, maçã, pera…)'),
      doce.createChoice('Fruta seca (tâmaras, passas, alperces…)'),
      doce.createChoice('Mel ou xarope (tâmara, ácer…)'),
      doce.createChoice('Especiarias (canela, baunilha…)')
    ])
    .showOtherOption(true)
    .setRequired(true);

  const alerg = form.addCheckboxItem();
  alerg.setTitle('A receita leva algum destes ingredientes?')
    .setHelpText('Ajuda-nos a avisar as famílias com alergias ou intolerâncias.')
    .setChoices([
      alerg.createChoice('Glúten (trigo, espelta, centeio, cevada ou aveia não certificada)'),
      alerg.createChoice('Leite ou derivados (lactose)'),
      alerg.createChoice('Ovo'),
      alerg.createChoice('Frutos secos ou amendoim'),
      alerg.createChoice('Nenhum destes')
    ]);

  form.addParagraphTextItem()
    .setTitle('Uma dica ou a história desta receita (opcional)')
    .setHelpText('Por exemplo: um truque para correr bem, ou quem a fazia lá em casa.');

  // --- Publicação ---
  form.addPageBreakItem()
    .setTitle('Como aparece no livro')
    .setHelpText('Pedimos apenas o mínimo de dados. Não indique apelidos nem dados de saúde de crianças.');

  const ident = form.addMultipleChoiceItem();
  ident.setTitle('Como quer que a receita seja identificada no livro?')
    .setChoices([
      ident.createChoice('Com o nome que indico abaixo'),
      ident.createChoice('Sem nome (receita anónima)')
    ])
    .setRequired(true);

  form.addTextItem()
    .setTitle('Nome a publicar')
    .setHelpText('Por exemplo: "Família do Tomás, 6.º D". Só usamos este nome se escolheu essa opção acima.');

  const consent = form.addCheckboxItem();
  consent.setTitle('Autorização')
    .setHelpText('As receitas podem ser adaptadas (por exemplo, para retirar açúcar ou adoçantes) antes de serem publicadas, ' +
      'nas versões em papel e online do livro. Os dados deste formulário servem apenas para preparar o livro ' +
      'e são vistos só pela equipa de Saúde Escolar.')
    .setChoices([
      consent.createChoice('Autorizo que esta receita seja adaptada e publicada no livro "Doces sem açúcar".')
    ])
    .setRequired(true);

  // Folha de respostas
  const folha = SpreadsheetApp.create('Receitas recebidas — Doces sem açúcar');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, folha.getId());

  try { form.setPublished(true); } catch (e) { /* versões antigas do Forms já ficam publicadas */ }

  const link = form.getPublishedUrl();
  let curto = link;
  try { curto = form.shortenFormUrl(link); } catch (e) {}

  Logger.log('Formulário criado!');
  Logger.log('Link para enviar aos pais: ' + curto);
  Logger.log('Editar o formulário: ' + form.getEditUrl());
  Logger.log('Folha com as respostas: ' + folha.getUrl());
}
