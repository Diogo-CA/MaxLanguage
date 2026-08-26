# 🌍 MaxLanguage

Plataforma interativa de aprendizado de idiomas desenvolvida em Python, com arquitetura baseada em **Arquivos Indexados** e indexação em memória através de **Árvore Binária de Busca (BST)**.

---

## 📌 Sobre o Projeto

O **MaxLanguage** foi desenvolvido como parte dos projetos acadêmicos do curso de Ciência da Computação. O objetivo principal é unir conceitos de usabilidade para aprendizagem linguística a fundamentos rigorosos de estruturas de dados e armazenamento persistente em disco.

### Principais Funcionalidades
* 📚 **Lições Progressivas:** Conteúdos modulares de vocabulário, gramática e pronúncia.
* ✍️ **Testes Interativos:** Exercícios de fixação e questionários práticos.
* ⚡ **Indexação em Memória:** Pesquisa otimizada de registros utilizando Árvore Binária ($O(\log n)$ na busca).
* 💾 **Persistência em Disco:** Armazenamento contínuo das lições e dados sem depender de SGBDs externos.

---

## 🛠️ Arquitetura e Estruturas de Dados

1. **Área de Índices (RAM):**
   * Estruturada via **Árvore Binária**.
   * Cada nó armazena a chave de indexação (ex: `ID_Licao` ou `Palavra_Chave`) e o deslocamento de bytes (*offset/endereço*) correspondente no arquivo de dados.
2. **Área de Dados (Disco):**
   * Armazenamento em arquivos estruturados (texto ou binário).
   * Recuperação direta via leitura por endereço físico (`seek`), reduzindo o I/O em disco.

---

## 🚀 Como Executar

### Pré-requisitos
* Python 3.10 ou superior instalado.

### Instalação e Execução
```bash
# 1. Clone o repositório
git clone [https://github.com/Diogo-CA/MaxLanguage.git](https://github.com/Diogo-CA/MaxLanguage.git)

# 2. Acesse a pasta do projeto
cd MaxLanguage

# 3. Crie e ative o ambiente virtual (opcional)
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# 4. Execute a aplicação
python3 main.py

```
---

## 👥 Autores
* Diogo Cardoso Arantes - https://github.com/Diogo-CA
* João Felipe Oliveira Condulucci - https://github.com/JoaoCondulucci