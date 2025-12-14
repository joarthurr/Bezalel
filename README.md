# 🔆 Bezalel - Sistema de Quiz Educacional

## ✍ Descrição
- Bezalel (batizado assim em referência ao artesão israelita bíblico) é um simples projeto de um sistema de quiz educacional.
O objetivo é permitir que usuários criem seus próprios quizzes e perguntas, testando seus conhecimentos em qualquer área de estudo, desde disciplinas acadêmicas até assuntos gerais.

- Este repositório faz parte da disciplina de **Programação Orientada a Objetos**, ministrada pelo professor **Jayr Pereira** na **Universidade Federal do Cariri (UFCA)**.

## 📃 Objetivo
- O objetivo é oferecer uma ferramenta robusta e configurável para a aplicação de testes, aplicando conceitos avançados de programação orientada a objetos (herança múltipla, mixins, encapsulamento), persistência de dados e regras de negócio estritas configuráveis externamente.

## 🔭 Funcionalidades
- O projeto tem como objetivo permitir a *criação de perguntas* e *montagem de quizzes* pelos **usuários**.
- Cada *pergunta* possuirá um **tema**, **enunciado**, **nível de dificuldade** e um número de 3 a 5 **alternativas**.
- O *quiz* possuirá **título**, **pontuação máximo** e será composto por um banco de **perguntas**.
- Em cada *tentativa* do *usuário* de responder um *quiz*, dados como **ranking**, **desempenho**, **sua evolução** e **questões mais erradas** serão disponibilizados meio de *relatórios*.

## 🛠 Pré-requisitos
- Python 3.10 ou superior
- Pytest (módulo opcional para rodar testes)
Instalação do Pytest:
`pip install pytest`
Execução do Pytest:
`pytest`

## 🕹 Instalação e Execução
1. Clone o repositório clickando no botão verde "Code" e depois em "Download zip";
2. Extraia os arquivos e pastas para um diretório;
3. Abra o CMD e assegure-se de estar na pasta raiz do programa;
4. Execute o programa:
`python main.py`

## 🔎 Utilização
1. **Menu Principal:** Ao iniciar, você terá acesso às áreas de Usuário e Administrativa.
2. **Configuração Inicial (Admin):** No menu administrativo (Opção 2), comece cadastrando um Usuário (Opção 6) e criando um Quiz (Opção 7). Você pode usar a opção "Gerar Dados de Teste (Seed)" para popular o sistema rapidamente.
3. **Criação de Perguntas:** Ao criar um quiz, o sistema solicitará o título, limites e permitirá adicionar perguntas interativamente, definindo tema e dificuldade.
4. **Respondendo o Quiz (Usuário):** No menu principal, vá para a Área do Usuário (Opção 1), identifique-se e escolha um quiz. O sistema avisará sobre o tempo limite.
5. **Feedback Imediato:** Ao finalizar (ou se o tempo acabar), o sistema exibe sua nota ponderada e situação (Aprovado/Reprovado).
6. **Relatórios:** Volte ao menu administrativo para visualizar rankings, desempenho por tema ou a distribuição de notas (histograma). 

## ⚙ Estrutura
A seguir, a organização atual do projeto, com breve explicação de cada pasta e arquivo:
```
Bezalel/
│
├── main.py                   # Arquivo principal
├── pytest.ini                # Configurações do Pytest para executar testes
│
├── modules/                  # Pacote de classes centrais do sistema
│   ├── __init__.py
│   ├── Usuario.py            # Classe que representa o usuário do sistema
│   ├── Pergunta.py           # Classe que modela perguntas e validações
│   ├── Quiz.py               # Classe responsável pelos quizzes
│   ├── Tentativa.py          # Registro de tentativas de resolução
│   ├── Relatorio.py          # Geração de relatórios
│   └── Mixins.py             # Classes auxiliares para Herança
│
├── tests/                    # Pasta contendo testes automatizados
│   ├── test_pergunta.py
│   ├── ...
│   └── outros testes automatizados
│
├── config/                   # Arquivos de configuração
│   ├── config.py
│   └── settings.json
│
├── data/                     # Pasta utilizada para armazenar dados auxiliares
│   ├── dados.py              # Para salvar e carregar quizzes, perguntas e demais entidades, permitindo persistência.
│   └── relatorio.txt         # Arquivo simples usado utilizado no módulo Relatorio.
│
└── README.md                 # Este arquivo
```

## Definição das classes
### Class Usuario:
> Classe responsável por representar o participante que realiza as provas no sistema.
- Atributos: nome, email, matrícula, tentativas (histórico).
- Métodos principais: pode_realizar_quiz() (verifica limites), adicionar_tentativa(), obter_relatorio().

### Class Quiz:
> Classe que agrega um conjunto de perguntas e define as regras da avaliação.
- Atributos: título, perguntas, tentativasLimite, tempoLimite, pontuaçãoMaxima.
- Métodos principais: adicionar_pergunta(), métodos mágicos (__len__, __iter__) para iteração direta.

### Class Pergunta:
> A unidade fundamental do quiz. Utiliza Mixins para funcionalidades extras de serialização e exibição.
- Atributos: enunciado, alternativas, indiceCorreta, dificuldade, tema.
Mixins: Herda de JsonSerializableMixin e ExibivelMixin (Herança Múltipla).
- Métodos principais: Validações estritas via @property (impede alternativas vazias ou índices inválidos).

### Class Tentativa:
> Registra a execução de um quiz por um usuário, controlando o estado temporal da prova.
- Atributos: usuário, quiz, respostasDadas, pontuação, tempoGasto, status (concluída/incompleta).
- Métodos principais: verificar_tempo_excedido(), finalizar(), registrar_resposta(). Consome a classe Config para calcular notas ponderadas.

### Class Relatorio:
> Classe utilitária responsável por gerar estatísticas e rankings baseados nos dados persistidos.
- Atributos: usuários (lista para análise).
- Métodos: gerar_ranking(), gerar_desempenho_por_tema(), gerar_taxa_acerto_global(), gerar_distribuicao_notas().

### Class Config:
> Gerencia as preferências globais do sistema carregadas de settings.json.
- Atributos: nota_corte_aprovacao, pesos_dificuldade, tempos_padrao.
- Métodos: _carregar(), obter_peso().

## 🏗 Documentação completa:
> https://docs.google.com/document/d/17FdqXtGebrvxvWMlO1i5C7oc6OuJ7l0-N1E-ryRzm4E/edit?usp=sharing


## 📜 Observação Final
Este projeto foi criado com o propósito educacional de demonstrar boas práticas de orientação a objetos e organização de software dentro do ambiente de aula do curso de engenharia de software da UFCA.

---

### § Curso de Engenharia de Software da Universidade Federal do Cariri (UFCA)
