# 🔆 Bezalel - Sistema de Quiz Educacional
Bezalel (batizado assim em referência ao artesão israelita bíblico) é um simples projeto de um sistema de quiz educacional voltado a usuários que desejam testar seus conhecimentos em suas áreas de estudo, sejam elas quais forem, uma vez que as perguntas e os quizzes são totalmente criados pelos próprios usuários.

Este projeto é parte constituinte da disciplina de Programação Orientada a Objetos, ministrada pelo professor Jayr Pereira na Universidade Federal do Cariri.

## 🔭 Funcionalidades
- O projeto tem como objetivo permitir a *criação de perguntas* e *montagem de quizzes* pelos **usuários**.
- Cada *pergunta* possuirá um **tema**, **enunciado**, **nível de dificuldade** e um número de 3 a 5 **alternativas**.
- O *quiz* possuirá **título**, **pontuação máximo** e será composto por um banco de **perguntas**.
- Em cada *tentativa* do *usuário* de responder um *quiz*, dados como **ranking**, **desempenho**, **sua evolução** e **questões mais erradas** serão disponibilizados meio de *relatórios*.

## 🛠 Pré-requisitos
- Python 3

## ⚙ Estrutura
```
Bezalel/
|
├── modules/             # Pacote de classes
|   ├── __init__.py
|   ├── Usuario.py
|   ├── Pergunta.py
|   ├── Quiz.py
|   ├── Tentativa.py
|   └── Relatorio.py
|
├── data/                # Pasta de informações sobre o usuário
|   ├── relatorio.txt
|   └── dados.py
|
├── config/              # Pasta de configurações do sistema
|   └── settings.py
|
├── main.py              # Arquivo principal
└── README.md            # Este arquivo
```

### § Curso de Engenharia de Software da Universidade Federal do Cariri (UFCA)
