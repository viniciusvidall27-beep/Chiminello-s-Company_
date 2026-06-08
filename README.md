# 🧱 Indústrias de Tijolos Chiminello — Sistema Web

Sistema web institucional + área administrativa para a Chiminello.
Construído com **Python + Flask**, pronto para GitHub e deploy na nuvem.

---

## 📁 Estrutura do Projeto

```
chiminello/
├── app.py                    # Aplicação Flask principal (rotas + API)
├── requirements.txt          # Dependências Python
├── Procfile                  # Para Heroku / Render
├── render.yaml               # Config automática Render.com
├── netlify.toml              # Config Netlify (ver nota abaixo)
├── .gitignore
├── data/                     # Dados JSON (criado automaticamente)
│   ├── clientes.json
│   ├── estoque.json
│   ├── contatos.json
│   └── logs_seguranca.json
├── static/
│   ├── css/main.css          # Estilos globais
│   └── js/main.js            # Helpers JS (toast, api, nav)
└── templates/
    ├── base.html             # Template base
    ├── public/
    │   ├── home.html         # Página inicial
    │   ├── historia.html     # História da empresa
    │   ├── produtos.html     # Catálogo de produtos
    │   └── contato.html      # Formulário de contato
    └── admin/
        ├── login.html        # Login administrativo
        ├── clientes.html     # CRUD de clientes
        ├── estoque.html      # Gestão de estoque
        └── seguranca.html    # Logs e segurança
```

---

## 🚀 Rodando Localmente

### Pré-requisitos
- Python 3.10+
- pip

### Passos

```bash
# 1. Clone o repositório
git clone https://github.com/SEU-USUARIO/chiminello.git
cd chiminello

# 2. Crie um ambiente virtual
python -m venv venv

# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Rode o servidor
python app.py
```

Acesse em: **http://localhost:5000**

---

## 🔐 Credenciais Padrão

| Usuário   | Senha         | Nível          |
|-----------|---------------|----------------|
| `admin`   | `admin123`    | Administrador  |
| `gerente` | `gerente456`  | Gerente        |

> ⚠️ Troque as senhas em `app.py` → dicionário `USUARIOS` antes de colocar em produção.

---

## 🌐 Deploy no GitHub

```bash
git init
git add .
git commit -m "🧱 Chiminello — Sistema Web v1.0"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/chiminello.git
git push -u origin main
```

---

## ☁️ Deploy na Nuvem

### ✅ Opção 1 — Render.com (RECOMENDADO — gratuito)

1. Crie conta em [render.com](https://render.com)
2. **New** → **Web Service**
3. Conecte seu repositório GitHub
4. O `render.yaml` configura tudo automaticamente
5. Clique **Create Web Service**
6. Aguarde o deploy (~2 min) → seu site estará em `https://chiminello.onrender.com`

**Por que Render?** Suporta Python/Flask nativamente, tem disco persistente para os JSONs e plano gratuito generoso.

---

### ⚠️ Opção 2 — Netlify (limitado para Flask)

O Netlify foi criado para sites estáticos e funções serverless (Node.js). **Flask não roda diretamente no Netlify.**

Para usar o Netlify, é necessário converter a API para **Netlify Functions** (serverless), o que requer reescrita em Node.js ou uso de um gateway.

**Alternativa recomendada:** Use Netlify apenas para o frontend estático e hospede a API no Render.

---

### Opção 3 — Railway.app

```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

---

### Opção 4 — Heroku

```bash
heroku create chiminello-app
git push heroku main
heroku open
```

---

## 🗺️ Páginas do Sistema

### Área Pública
| Rota        | Descrição              |
|-------------|------------------------|
| `/`         | Página inicial (Home)  |
| `/historia` | História da empresa    |
| `/produtos` | Catálogo de produtos   |
| `/contato`  | Formulário de contato  |

### Área Administrativa
| Rota                | Descrição              |
|---------------------|------------------------|
| `/admin`            | Redireciona para login |
| `/admin/login`      | Tela de login          |
| `/admin/clientes`   | CRUD de clientes       |
| `/admin/estoque`    | Gestão de estoque      |
| `/admin/seguranca`  | Logs e segurança       |

### API REST
| Método | Rota                     | Descrição              |
|--------|--------------------------|------------------------|
| POST   | `/api/contato`           | Salvar mensagem        |
| POST   | `/api/auth/login`        | Fazer login            |
| POST   | `/api/auth/logout`       | Fazer logout           |
| GET    | `/api/auth/status`       | Verificar sessão       |
| GET    | `/api/clientes`          | Listar clientes        |
| POST   | `/api/clientes`          | Criar cliente          |
| PUT    | `/api/clientes/<id>`     | Atualizar cliente      |
| DELETE | `/api/clientes/<id>`     | Excluir cliente        |
| GET    | `/api/estoque`           | Listar estoque         |
| POST   | `/api/estoque`           | Movimentação           |
| DELETE | `/api/estoque/<codigo>`  | Excluir produto        |
| GET    | `/api/logs`              | Listar logs            |
| DELETE | `/api/logs`              | Limpar logs            |

---

## 📦 Tecnologias

- **Backend:** Python 3 + Flask
- **Frontend:** HTML5 + CSS3 + JavaScript puro
- **Banco de dados:** Arquivos JSON (sem dependências externas)
- **Deploy:** Render.com / Railway / Heroku
- **Fontes:** Google Fonts (Playfair Display + Source Sans 3)

---

## 📝 Licença

MIT — Livre para uso comercial e pessoal.
