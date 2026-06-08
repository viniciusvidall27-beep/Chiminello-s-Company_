"""
Indústrias de Tijolos Chiminello — Sistema Web
Flask application com área pública e administrativa
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "chiminello-secret-2025")

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

# ── Arquivos de dados ─────────────────────────────────────────────────────────
ARQUIVOS = {
    "contatos":  os.path.join(DATA_DIR, "contatos.json"),
    "clientes":  os.path.join(DATA_DIR, "clientes.json"),
    "estoque":   os.path.join(DATA_DIR, "estoque.json"),
    "logs":      os.path.join(DATA_DIR, "logs_seguranca.json"),
}

for arq in ARQUIVOS.values():
    if not os.path.exists(arq):
        with open(arq, "w") as f:
            json.dump([], f)

# ── Credenciais (em prod use DB + hash) ───────────────────────────────────────
USUARIOS = {
    "admin":   {"senha": "admin123", "nivel": "Administrador"},
    "gerente": {"senha": "gerente456", "nivel": "Gerente"},
}

# ── Helpers ───────────────────────────────────────────────────────────────────
def ler(chave):
    try:
        with open(ARQUIVOS[chave], "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def salvar(chave, dados):
    with open(ARQUIVOS[chave], "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

def registrar_log(tipo, detalhe="", usuario="sistema"):
    logs = ler("logs")
    logs.insert(0, {
        "id": int(datetime.now().timestamp() * 1000),
        "tipo": tipo,
        "detalhe": detalhe,
        "usuario": usuario,
        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    })
    salvar("logs", logs[:500])

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("autenticado"):
            return jsonify({"erro": "Não autenticado"}), 401
        return f(*args, **kwargs)
    return decorated

def now_str():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def today_str():
    return datetime.now().strftime("%d/%m/%Y")

# ═════════════════════════════════════════════════════════════════════════════
# ROTAS PÚBLICAS
# ═════════════════════════════════════════════════════════════════════════════

@app.route("/")
def home():
    return render_template("public/home.html")

@app.route("/historia")
def historia():
    return render_template("public/historia.html")

@app.route("/produtos")
def produtos():
    return render_template("public/produtos.html")

@app.route("/contato")
def contato():
    return render_template("public/contato.html")

@app.route("/api/contato", methods=["POST"])
def api_contato():
    dados = request.get_json()
    if not dados.get("nome") or not dados.get("email") or not dados.get("mensagem"):
        return jsonify({"erro": "Campos obrigatórios faltando"}), 400
    contatos = ler("contatos")
    contatos.append({
        "id": int(datetime.now().timestamp() * 1000),
        "nome":      dados["nome"],
        "email":     dados["email"],
        "telefone":  dados.get("telefone", ""),
        "mensagem":  dados["mensagem"],
        "data":      now_str(),
    })
    salvar("contatos", contatos)
    registrar_log("CONTATO_RECEBIDO", dados["nome"])
    return jsonify({"ok": True})

# ═════════════════════════════════════════════════════════════════════════════
# ROTAS ADMIN
# ═════════════════════════════════════════════════════════════════════════════

@app.route("/admin")
@app.route("/admin/login")
def admin_login():
    if session.get("autenticado"):
        return redirect(url_for("admin_clientes"))
    return render_template("admin/login.html")

@app.route("/admin/clientes")
def admin_clientes():
    if not session.get("autenticado"):
        return redirect(url_for("admin_login"))
    return render_template("admin/clientes.html")

@app.route("/admin/estoque")
def admin_estoque():
    if not session.get("autenticado"):
        return redirect(url_for("admin_login"))
    return render_template("admin/estoque.html")

@app.route("/admin/seguranca")
def admin_seguranca():
    if not session.get("autenticado"):
        return redirect(url_for("admin_login"))
    return render_template("admin/seguranca.html")

# ─── Auth API ─────────────────────────────────────────────────────────────────

@app.route("/api/auth/login", methods=["POST"])
def api_login():
    dados = request.get_json()
    usuario = dados.get("usuario", "").strip()
    senha   = dados.get("senha", "")
    user    = USUARIOS.get(usuario)
    if user and user["senha"] == senha:
        session["autenticado"] = True
        session["usuario"]     = usuario
        session["nivel"]       = user["nivel"]
        session["login_time"]  = now_str()
        registrar_log("LOGIN_SUCESSO", f"Nível: {user['nivel']}", usuario)
        return jsonify({"ok": True, "usuario": usuario, "nivel": user["nivel"]})
    registrar_log("LOGIN_FALHA", f"Tentativa para: {usuario}", usuario)
    return jsonify({"erro": "Credenciais inválidas"}), 401

@app.route("/api/auth/logout", methods=["POST"])
def api_logout():
    usuario = session.get("usuario", "desconhecido")
    registrar_log("LOGOUT", "Sessão encerrada", usuario)
    session.clear()
    return jsonify({"ok": True})

@app.route("/api/auth/status")
def api_auth_status():
    if session.get("autenticado"):
        return jsonify({
            "autenticado": True,
            "usuario":    session.get("usuario"),
            "nivel":      session.get("nivel"),
            "login_time": session.get("login_time"),
        })
    return jsonify({"autenticado": False})

# ─── Clientes API ─────────────────────────────────────────────────────────────

@app.route("/api/clientes", methods=["GET"])
@login_required
def api_clientes_listar():
    return jsonify(ler("clientes"))

@app.route("/api/clientes", methods=["POST"])
@login_required
def api_clientes_criar():
    dados = request.get_json()
    if not dados.get("nome") or not dados.get("cpf"):
        return jsonify({"erro": "Nome e CPF/CNPJ obrigatórios"}), 400
    clientes = ler("clientes")
    novo = {
        "id":       int(datetime.now().timestamp() * 1000),
        "nome":     dados["nome"],
        "cpf":      dados["cpf"],
        "telefone": dados.get("telefone", ""),
        "email":    dados.get("email", ""),
        "endereco": dados.get("endereco", ""),
        "data":     today_str(),
    }
    clientes.append(novo)
    salvar("clientes", clientes)
    registrar_log("CLIENTE_CADASTRADO", dados["nome"], session["usuario"])
    return jsonify(novo), 201

@app.route("/api/clientes/<int:cid>", methods=["PUT"])
@login_required
def api_clientes_atualizar(cid):
    dados = request.get_json()
    clientes = ler("clientes")
    for i, c in enumerate(clientes):
        if c["id"] == cid:
            clientes[i].update({
                "nome":     dados.get("nome", c["nome"]),
                "cpf":      dados.get("cpf", c["cpf"]),
                "telefone": dados.get("telefone", c.get("telefone", "")),
                "email":    dados.get("email", c.get("email", "")),
                "endereco": dados.get("endereco", c.get("endereco", "")),
            })
            salvar("clientes", clientes)
            registrar_log("CLIENTE_EDITADO", dados.get("nome", ""), session["usuario"])
            return jsonify(clientes[i])
    return jsonify({"erro": "Cliente não encontrado"}), 404

@app.route("/api/clientes/<int:cid>", methods=["DELETE"])
@login_required
def api_clientes_deletar(cid):
    clientes = ler("clientes")
    novo = [c for c in clientes if c["id"] != cid]
    if len(novo) == len(clientes):
        return jsonify({"erro": "Cliente não encontrado"}), 404
    salvar("clientes", novo)
    registrar_log("CLIENTE_EXCLUIDO", f"ID: {cid}", session["usuario"])
    return jsonify({"ok": True})

# ─── Estoque API ──────────────────────────────────────────────────────────────

@app.route("/api/estoque", methods=["GET"])
@login_required
def api_estoque_listar():
    return jsonify(ler("estoque"))

@app.route("/api/estoque", methods=["POST"])
@login_required
def api_estoque_mov():
    dados   = request.get_json()
    tipo    = dados.get("tipo", "cadastro")
    produto = dados.get("produto", {})
    if not produto.get("nome"):
        return jsonify({"erro": "Nome do produto obrigatório"}), 400
    estoque = ler("estoque")
    ex = next((p for p in estoque if p["nome"].lower() == produto["nome"].lower()), None)
    qtd = int(produto.get("qtd", 0))
    if tipo == "cadastro":
        if ex:
            ex["qtd"]   = qtd
            ex["movim"] = today_str()
        else:
            estoque.append({
                "id":       int(datetime.now().timestamp() * 1000),
                "codigo":   produto.get("codigo") or f"CHI-{int(datetime.now().timestamp())%100000:05d}",
                "nome":     produto["nome"],
                "categoria":produto.get("categoria", "Tijolo Comum"),
                "qtd":      qtd,
                "obs":      produto.get("obs", ""),
                "movim":    today_str(),
            })
    elif tipo == "entrada":
        if ex:
            ex["qtd"]   = ex["qtd"] + qtd
            ex["movim"] = today_str()
        else:
            estoque.append({**produto, "id": int(datetime.now().timestamp() * 1000), "movim": today_str()})
    elif tipo == "saida":
        if ex:
            ex["qtd"]   = max(0, ex["qtd"] - qtd)
            ex["movim"] = today_str()
    salvar("estoque", estoque)
    registrar_log(f"EST_{tipo.upper()}", f"{produto['nome']} qtd:{qtd}", session["usuario"])
    return jsonify(ler("estoque"))

@app.route("/api/estoque/<codigo>", methods=["DELETE"])
@login_required
def api_estoque_deletar(codigo):
    estoque = ler("estoque")
    novo    = [p for p in estoque if p.get("codigo") != codigo]
    salvar("estoque", novo)
    registrar_log("EST_EXCLUIDO", f"COD: {codigo}", session["usuario"])
    return jsonify({"ok": True})

# ─── Logs API ─────────────────────────────────────────────────────────────────

@app.route("/api/logs", methods=["GET"])
@login_required
def api_logs():
    return jsonify(ler("logs"))

@app.route("/api/logs", methods=["DELETE"])
@login_required
def api_logs_limpar():
    salvar("logs", [])
    registrar_log("LOGS_LIMPOS", "Histórico apagado", session.get("usuario", "admin"))
    return jsonify({"ok": True})

# ═════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=os.environ.get("FLASK_DEBUG", "0") == "1", host="0.0.0.0", port=port)
