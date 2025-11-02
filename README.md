# Minerva: Organização que Impera!
#### Um aplicativo feito para trazer ordem ao caos universitário, ajudando estudantes a organizar disciplinas, notas, faltas, arquivos e tarefas. 

### 📚 Tabela de Conteúdos

#### 📖 Sobre o Projeto

#### ✨ Principais Funcionalidades

#### 🚀 Acesso ao App (Nuvem)

#### 📸 Imagens do App

#### 🛠️ Tecnologias Utilizadas

#### ⚙️ Instruções para Testagem Local  
<br>

# 📖 Sobre o Projeto

## O Problema

A desorganização é um dos maiores desafios enfrentados pelos estudantes universitários. Uma pesquisa da Universidade do Alabama revelou que a falta de organização é um dos principais fatores para a má qualidade do sono entre os estudantes. Além disso, estudos sobre aprendizagem autorregulada mostram que mais da metade dos estudantes (53,7%) apresentam falhas significativas no planejamento do tempo, impactando diretamente seu desempenho e bem-estar.

## A Solução

Minerva nasceu com o propósito de ajudar o estudante a planejar melhor sua rotina acadêmica. Inspirado na deusa da sabedoria, o aplicativo oferece um espaço único para que o aluno possa organizar suas disciplinas, conteúdos, notas, faltas e arquivos.

O grande diferencial do Minerva é ser uma solução de estudantes para estudantes, com foco total na experiência real do universitário brasileiro.

### ✨ Principais Funcionalidades

#### Gestão de Disciplinas: Crie e organize todas as suas matérias, definindo créditos, carga horária e média necessária.

#### Controle de Notas e Média: Adicione notas com pesos e acompanhe sua média em tempo real.

#### Controle de Faltas: Registre suas faltas e saiba quantas ainda restam antes de atingir o limite (calculado com base na carga horária).

#### Agenda de Tarefas: Um calendário integrado para organizar suas tarefas, provas e prazos.

#### Gestão de Arquivos: (Seção de arquivos do app)
<br>

# 🚀 Acesso ao App (Nuvem)

Você pode acessar a versão de produção (deploy) do Minerva através do link abaixo:

➡️ https://minerva-app-api.onrender.com
<br>
<br>

# 📸 Imagens do App

### Página Inicial (Calendário)

<img width="2068" height="888" alt="image" src="https://github.com/user-attachments/assets/17d8624c-467f-4aa4-bf59-7d6b0fb177c2" />

### Página de Matérias

<img width="2068" height="904" alt="image" src="https://github.com/user-attachments/assets/2cb53e7c-0acd-4341-b06e-a3af6b4f247d" />

### Controle de Notas (Expander)

<img width="2058" height="743" alt="image" src="https://github.com/user-attachments/assets/5d626f29-df53-4049-89c5-cb2e65c28480" />

### Controle de Tarefas

<img width="2066" height="743" alt="image" src="https://github.com/user-attachments/assets/e872371e-55d9-4a5f-8c45-f70969f396a7" />

<br>
<br>

# 🛠️ Tecnologias Utilizadas

Este projeto foi construído utilizando as seguintes tecnologias:

### Back-end:
![Java](https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white)
![Spring](https://img.shields.io/badge/Spring-6DB33F?style=for-the-badge&logo=spring&logoColor=white)

### Front-end:   
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

### Banco de Dados:   
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![H2 Database](https://img.shields.io/badge/H2%20Database-FFFFFF?style=for-the-badge&logo=h2database&logoColor=black)

### Autenticação:  
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)

### Design e Prototipagem:   
![Diagrams.net](https://img.shields.io/badge/Diagrams.net-F08705?style=for-the-badge&logo=diagramsdotnet&logoColor=white)
![Figma](https://img.shields.io/badge/Figma-F24E1E?style=for-the-badge&logo=figma&logoColor=white)
<br>
<br>

# ⚙️ Instruções para Testagem Local

Para rodar este projeto na sua máquina local, siga os passos abaixo.

### Pré-requisitos

Você precisará ter as seguintes ferramentas instaladas:

- Git
- Java JDK 21+
- Python 3.12+
- PostgreSQL (ou um container Docker com PostgreSQL)
- Docker

### 1. Clonar o Repositório

- git clone https://github.com/Luis-coelho30/minerva-app.git
- cd minerva-app

### 2. Configurando o Back-end (Java/Spring)

- cd backend-minerva

### 3. Configurar Variáveis de Ambiente:

- Defina as variáveis de ambiente necessárias  
  -> JWT_SECRET = {Base64Key}  
  -> SPRING_PROFILES_ACTIVE = dev 

### 4. Rodar o Back-end:

- Verifique se está na pasta backend-minerva
- O terminal deve estar na mesma sessão onde foram definidas as variáveis de ambiente
- Execute o comando: **docker compose up --build**

### 5. Configurando o Front-end (Python/Streamlit)

O Front-end é a interface do usuário construída com Streamlit.

- cd frontend-minerva

### 6. Criar e Ativar o Ambiente Virtual:

- python -m venv .venv

#### Ativação no Linux/Mac
source .venv/bin/activate

#### Ativação no Windows
.\.venv\Scripts\activate

### 7. Instalar as Dependências:

- pip install -r requirements.txt

### 8. Configurar os Segredos (Secrets):

- Crie uma arquivo na pasta .streamlit chamado secrets.toml.

├── backend-minerva/  
└── frontend-minerva/  
    ├── **.streamlit/**  
    ├── api_client/  
    ├── app.py  
    ├── components/  
    ├── images/  
    ├── init_session.py  
    ├── menu.py  
    ├── pages  
    ├── requirements.txt  
    ├── styles  
    └── utils.py  

- Adicione a URL da API local:  
API_URL = "http://localhost:8080"

### 9. Rodar o Front-end:
- cd ..  
- streamlit run frontend-minerva/app.py  
  
O aplicativo estará disponível em http://localhost:8501.
<br>
<br>

# 🧑‍💻 Autores
- Kauã Bezerra Brito
- Luis Augusto Coelho de Souza
- Tulio Goncalves Vieira

Feito como parte do projeto First Steps [PUC TECH - Liga De Ciência E Tecnologia Da PUC-SP].
