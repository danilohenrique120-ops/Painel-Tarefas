import json
import streamlit as st
from datetime import datetime, timedelta
import os

TASKS_FILE = "tasks.json"

CATEGORIES = {
    "Tarefas a Fazer": [],
    "Tarefas a Delegar": {
        "Thais": [], "Patrick": [], "Willian": [], "Uanderson": [], "Gustavo Conti": [], "Matheus": [], "Talize": []
    },
    "DDS": [],
    "Projetos": [],
    "CIPA": [],
    "Operadores": {
        "Willian": [], "Conti": [], "Matheus": [], "Zanetti": [], "Valois": [], "Uanderson": [], "Pires": []
    },
    "1:1": {
        "Willian": [], "Conti": [], "Matheus": [], "Zanetti": [], "Valois": [], "Uanderson": [], "Pires": []
    }
}

if os.path.exists(TASKS_FILE):
    with open(TASKS_FILE, "r") as f:
        tasks = json.load(f)
else:
    tasks = CATEGORIES

def save_tasks():
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def add_task(category, subcategory, description, deadline):
    task = {"description": description, "done": False, "deadline": deadline if deadline else ""}
    if subcategory:
        tasks[category][subcategory].append(task)
    else:
        tasks[category].append(task)
    save_tasks()

def display_tasks():
    st.title("Painel de Tarefas")
    cols = st.columns(3)
    col_index = 0
    for category, content in tasks.items():
        with cols[col_index]:
            st.subheader(category)
            if isinstance(content, dict):
                for subcat, sub_tasks in content.items():
                    st.markdown(f"**{subcat}**")
                    for i, t in enumerate(sub_tasks):
                        deadline_alert = ""
                        if t["deadline"]:
                            try:
                                deadline_date = datetime.strptime(t["deadline"], "%Y-%m-%d")
                                if deadline_date <= datetime.now() + timedelta(days=2):
                                    deadline_alert = "⚠️"
                            except:
                                pass
                        checked = st.checkbox(f"{t['description']} {deadline_alert}", value=t['done'], key=f"{category}-{subcat}-{i}")
                        t['done'] = checked
            else:
                for i, t in enumerate(content):
                    deadline_alert = ""
                    if t["deadline"]:
                        try:
                            deadline_date = datetime.strptime(t["deadline"], "%Y-%m-%d")
                            if deadline_date <= datetime.now() + timedelta(days=2):
                                deadline_alert = "⚠️"
                        except:
                            pass
                    checked = st.checkbox(f"{t['description']} {deadline_alert}", value=t['done'], key=f"{category}-{i}")
                    t['done'] = checked
        col_index = (col_index + 1) % 3
    save_tasks()

st.sidebar.header("Adicionar Tarefa")
category = st.sidebar.selectbox("Categoria", list(CATEGORIES.keys()))
subcategory = None
if isinstance(CATEGORIES[category], dict):
    subcategory = st.sidebar.selectbox("Subcategoria", list(CATEGORIES[category].keys()))

description = st.sidebar.text_input("Descrição da Tarefa")
deadline = st.sidebar.date_input("Prazo (opcional)", value=None)
if st.sidebar.button("Adicionar"):
    add_task(category, subcategory, description, str(deadline) if deadline else "")
    st.sidebar.success("Tarefa adicionada!")

st.sidebar.header("Buscar Tarefa")
search_query = st.sidebar.text_input("Digite palavra-chave")
if search_query:
    st.subheader("Resultados da Busca")
    for category, content in tasks.items():
        if isinstance(content, dict):
            for subcat, sub_tasks in content.items():
                for t in sub_tasks:
                    if search_query.lower() in t["description"].lower():
                        st.write(f"{category} > {subcat}: {t['description']} (Prazo: {t['deadline']})")
        else:
            for t in content:
                if search_query.lower() in t["description"].lower():
                    st.write(f"{category}: {t['description']} (Prazo: {t['deadline']})")

display_tasks()