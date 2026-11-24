import json
import os
from datetime import date, timedelta
from pathlib import Path

import streamlit as st

from chickflow.data.generate import read_yaml
from chickflow.data.schema import TABLES, file_hash, load_clean_bundle
from chickflow.data.validate import validate_files
from chickflow.metrics import FilterContext, build_facts, scope
from views import VIEWS, page_heading

ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "data" / "clean"
MANIFEST = CLEAN.parent / "manifest.json"
ALERT_CONFIG = ROOT / "config" / "alerts.yaml"

st.set_page_config(page_title="ChickFlow", layout="wide")
st.html(ROOT / "app" / "style.css")
st.logo(str(ROOT / "assets/brand/chickflow-wordmark.svg"), size="large")


@st.cache_data(show_spinner="Memuat data ChickFlow…")
def load_data(revision):
    verification = validate_files(CLEAN)
    if not verification["passed"]:
        raise ValueError(" · ".join(verification["errors"]))
    metadata = json.loads(MANIFEST.read_text())
    return build_facts(load_clean_bundle(CLEAN)), metadata, read_yaml(ALERT_CONFIG)


try:
    revision = (file_hash(MANIFEST), file_hash(ALERT_CONFIG),
                *((CLEAN / f"{key}.csv").stat().st_mtime_ns for key in TABLES))
    facts, metadata, settings = load_data(revision)
except (OSError, ValueError, KeyError, TypeError) as error:
    st.title("Data ChickFlow perlu disiapkan")
    st.error(str(error))
    st.code("python -m chickflow.data.generate\npython -m chickflow.data.clean\npython -m chickflow.data.validate")
    st.stop()

first = date.fromisoformat(metadata["range_start"])
last = date.fromisoformat(metadata["range_end"])
default_dates = (max(first, last - timedelta(days=6)), last)
branch_names = facts.bundle["branches"].set_index("branch_id")["city"].to_dict()
categories = sorted(facts.bundle["menu"]["category"].unique())
prototype = os.environ.get("CHICKFLOW_PROTOTYPE") == "v1"

labels = {
    "overview": "Ringkasan", "orders": "Pesanan", "kitchen": "Dapur",
    "inventory": "Stok", "sales": "Penjualan", "profit": "Biaya dan laba",
}
keys = ("overview", "kitchen", "inventory", "profit") if prototype else tuple(labels)


def reset_filters():
    st.session_state["filter_revision"] = st.session_state.get("filter_revision", 0) + 1


def page_scope(selected, branch_ids, chosen):
    cities = ", ".join(branch_names[i] for i in branch_ids) if branch_ids else "Semua cabang"
    category = ", ".join(chosen) if chosen else "Semua kategori"
    if not selected or len(selected) != 2:
        return f"Data simulasi · Pilih tanggal akhir · {cities} · {category}"
    return f"Data simulasi · {selected[0]:%d/%m/%Y}–{selected[1]:%d/%m/%Y} WIB · {cities} · {category}"


def render_page(key):
    def run():
        if not selected or len(selected) != 2:
            st.info("Pilih tanggal awal dan akhir untuk menerapkan filter.")
            return
        current = FilterContext(*selected, tuple(branch_ids), tuple(chosen))
        VIEWS[key](facts, scope(facts, current), current, first, settings, pages)
    return run


pages = {key: st.Page(render_page(key), title=labels[key], url_path=key,
                      default=key == "overview") for key in keys}
navigation = st.navigation(list(pages.values()), position="top")

revision_id = st.session_state.get("filter_revision", 0)
dates_key, branch_key, category_key = (f"{field}-{revision_id}" for field in ("dates","branches","categories"))
previous_dates = st.session_state.get(dates_key, default_dates)
previous_branches = st.session_state.get(branch_key, ())
previous_categories = st.session_state.get(category_key, ())
page_heading(navigation.url_path or "overview", page_scope(previous_dates, previous_branches, previous_categories))
has_filters = previous_dates != default_dates or bool(previous_branches or previous_categories)
with st.container(key="global-filters", border=True):
    date_cell, branch_cell, category_cell, *reset_cell = st.columns(
        [1.16, 1, 1, .56] if has_filters else [1.16, 1, 1])
    with date_cell:
        selected = st.date_input("Periode", value=default_dates, min_value=first, max_value=last,
                                 format="DD/MM/YYYY", key=dates_key)
    with branch_cell:
        branch_ids = st.multiselect("Cabang", list(branch_names), format_func=branch_names.__getitem__,
                                    placeholder="Semua cabang", key=branch_key)
    with category_cell:
        chosen = st.multiselect("Kategori menu", categories, placeholder="Semua kategori", key=category_key)
    if reset_cell:
        reset_cell[0].button("Reset filter", on_click=reset_filters, width="stretch")
if prototype:
    st.caption("Tampilan uji dengan empat modul")

navigation.run()
