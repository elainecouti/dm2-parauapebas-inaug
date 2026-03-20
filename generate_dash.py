#!/usr/bin/env python3
"""
Gera dashboard de inauguração para uma unidade DM2.
Uso: python generate_dash.py <slug> <account_id> <nome> <estado>
Ex:  python generate_dash.py cuiaba 934816888951624 Cuiabá MT
"""
import sys
import os

# Inject unit config via args
if len(sys.argv) < 5:
    print("Uso: python generate_dash.py <slug> <account_id> <nome> <estado>")
    sys.exit(1)

slug = sys.argv[1]
account_id = sys.argv[2]
nome = sys.argv[3]
estado = sys.argv[4]

# Override UNITS to only process this unit
os.environ.setdefault("META_ACCESS_TOKEN", "")

# Import everything from dash_inauguracao
sys.path.insert(0, os.path.dirname(__file__))
from dash_inauguracao import (
    UNITS, meta_get, fetch_all, process, generate_html,
    ACCESS_TOKEN
)
from pathlib import Path
from datetime import datetime

# Override UNITS
unit = {"nome": nome, "estado": estado, "account_id": account_id}

print(f"⚡ Gerando dashboard para {nome} ({estado})...")
raw = fetch_all(account_id)
p = process(raw)

s = p["summary"]
b = p["balance"]
print(f"  ✓ {s['total_camps']} campanhas ({s['active']} ativas)")
print(f"  ✓ R$ {s['spend']:,.2f} investido · {s['conversations']} conversas WPP")
print(f"  ✓ Saldo: R$ {b['remaining']:,.2f} · Budget R$ {b['daily_budget']:,.0f}/dia")

html = generate_html(slug, unit, p)
Path("index.html").write_text(html, encoding="utf-8")
print("✅ index.html gerado!")
