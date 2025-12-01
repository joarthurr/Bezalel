# 🔆 Bezalel - Sistema de Quiz Educacional
Bezalel (batizado assim em referência ao artesão israelita bíblico) é um simples projeto de um sistema de quiz educacional.
O objetivo é permitir que usuários criem seus próprios quizzes e perguntas, testando seus conhecimentos em qualquer área de estudo, desde disciplinas acadêmicas até assuntos gerais.

Este repositório faz parte da disciplina de **Programação Orientada a Objetos**, ministrada pelo professor **Jayr Pereira** na **Universidade Federal do Cariri (UFCA)**.

---

## 🔭 Funcionalidades
- O projeto tem como objetivo permitir a *criação de perguntas* e *montagem de quizzes* pelos **usuários**.
- Cada *pergunta* possuirá um **tema**, **enunciado**, **nível de dificuldade** e um número de 3 a 5 **alternativas**.
- O *quiz* possuirá **título**, **pontuação máximo** e será composto por um banco de **perguntas**.
- Em cada *tentativa* do *usuário* de responder um *quiz*, dados como **ranking**, **desempenho**, **sua evolução** e **questões mais erradas** serão disponibilizados meio de *relatórios*.

## 🛠 Pré-requisitos
- Python 3.10 ou superior
- Pytest (módulo opcional para rodar testes)
Instalação do Pytest:
```pip install pytest```

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
│   └── Relatorio.py          # Geração de relatórios
│
├── tests/                    # Pasta contendo testes automatizados
│   ├── test_pergunta.py
│   └── outros testes automatizados
│
├── config/                   # Arquivos de configuração
│   └── settings.py
│
├── data/                     # Pasta utilizada para armazenar dados auxiliares
│   ├── dados.py              # Para salvar e carregar quizzes, perguntas e demais entidades, permitindo persistência.
│   └── relatorio.txt         # Arquivo simples usado utilizado no módulo Relatorio.
│
└── README.md                 # Este arquivo
```

## 📜 Observação Final
Este projeto foi criado com o propósito educacional de demonstrar boas práticas de orientação a objetos e organização de software dentro de um ambiente que se assemelhe à realidade de trabalhos que poderão ser encontrados na indústria.

---

### § Curso de Engenharia de Software da Universidade Federal do Cariri (UFCA)
