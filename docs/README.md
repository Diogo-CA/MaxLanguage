# 🌍 MaxLanguage

Plataforma interativa e gamificada de aprendizado de idiomas desenvolvida em Python, com arquitetura baseada em **Arquivos Indexados com Registros de Tamanho Fixo** e indexação em memória RAM através de **Árvore Binária de Busca (BST)**.

---

## 📌 Sobre o Projeto

O **MaxLanguage** foi desenvolvido como parte dos projetos acadêmicos do curso de Ciência da Computação (Algoritmos e Estruturas de Dados II - FEMA). O objetivo principal é unir conceitos modernos de usabilidade para aprendizagem linguística (inspirados no *Duolingo* e *Busuu*) a fundamentos rigorosos de estruturas de dados e armazenamento persistente em disco.

### Principais Funcionalidades

#### 🎓 Área do Estudante
* 📊 **Meu Perfil & Progresso:** Dashboard com métricas de XP, nível atual, idioma em estudo e barra de progresso para promoção de nível.
* ⚡ **Prática Gamificada:** Questões com alternativas em botões clicáveis, badges de dificuldade, feedback instantâneo de acerto/erro (+XP ou penalidade de 10%) e promoção de nível a cada 100 pontos.
* 🏆 **Classificação da Turma:** Ranking geral dos estudantes ordenados por XP com destaque no pódio (Ouro 🥇, Prata 🥈, Bronze 🥉) e destaque da posição do aluno logado.
* 📜 **Certificado de Proficiência:** Emissão e visualização do diploma formatado em HTML quando o estudante conclui todos os níveis das lições do idioma.

#### ⚙️ Painel de Gestão (Admin / CRUD)
* 🌐 **Gestão de Idiomas:** Inclusão e listagem com chaves primárias indexadas.
* 📚 **Gestão de Lições:** Inclusão e listagem de módulos com resolução de chaves estrangeiras.
* ✍️ **Gestão de Exercícios:** Cadastro de questões, níveis de dificuldade, opções e gabarito.
* 👥 **Gestão de Usuários:** Cadastro e Exclusão Lógica de estudantes (preservando a integridade dos ponteiros de disco e removendo da árvore em memória).

---

## 🛠️ Arquitetura e Estruturas de Dados

1. **Área de Índices (RAM):**
   * Estruturada via **Árvore Binária de Busca (BST)** em memória.
   * Cada nó armazena a chave primária (`codigo`) e o número do registro/offset físico (`posicao`) correspondente na área de dados ($O(\log n)$ na busca).
2. **Área de Dados (Disco):**
   * Armazenamento em arquivos formatados com registros de tamanho fixo em bytes (`TAM_REGISTRO`), permitindo acesso direto (`seek`), leitura e alteração in-place sem corrupção.
   * Exclusão lógica com marcador de status (`*`).

---

## 🚀 Como Executar

### Pré-requisitos
* Python 3.10 ou superior instalado.
* `customtkinter` instalado no ambiente virtual.

### Instalação e Execução
```bash
# 1. Clone o repositório
git clone https://github.com/Diogo-CA/MaxLanguage.git

# 2. Acesse a pasta do projeto
cd MaxLanguage

# 3. Crie e ative o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# 4. Instale as dependências
pip install -r requirements.txt

# 5. (Opcional) Popular banco de dados com idiomas, lições e exercícios de teste
python3 src/seed_dados.py

# 6. Iniciar a aplicação gráfica
cd src
python3 main_gui.py
```

---

## 👥 Autores
* **Diogo Cardoso Arantes** - [GitHub](https://github.com/Diogo-CA)
* **João Felipe Oliveira Condulucci** - [GitHub](https://github.com/JoaoCondulucci)