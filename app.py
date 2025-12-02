import json
import streamlit as st
from datetime import datetime, timedelta
import os
import pandas as pd

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

def export_to_excel():
    data = []
    for category, content in tasks.items():
        if isinstance(content, dict):
            for subcat, sub_tasks in content.items():
                for t in sub_tasks:
                    data.append([category, subcat, t['description'], t['done'], t['deadline']])
        else:
            for t in content:
                data.append([category, '', t['description'], t['done'], t['deadline']])
    df = pd.DataFrame(data, columns=['Categoria', 'Subcategoria', 'Descrição', 'Concluído', 'Prazo'])
    df.to_excel('tarefas_exportadas.xlsx', index=False)
    return 'tarefas_exportadas.xlsx'

def display_tasks(filter_status):
    st.title("Painel de Tarefas")
    cols = st.columns(3)
    col_index = 0
    for category, content in tasks.items():
        with cols[col_index]:
            st.markdown(f"<h3 style='color:#2E86C1; margin-bottom:15px;'>{category}</h3>", unsafe_allow_html=True)
            if isinstance(content, dict):
                for subcat, sub_tasks in content.items():
                    st.markdown(f"<b>{subcat}</b>", unsafe_allow_html=True)
                    for i, t in enumerate(sub_tasks):
                        if filter_status == 'Todos' or (filter_status == 'Feito' and t['done']) or (filter_status == 'Não Feito' and not t['done']):
                            deadline_alert = ''
                            if t['deadline']:
                                try:
                                    deadline_date = datetime.strptime(t['deadline'], '%Y-%m-%d')
                                    if deadline_date <= datetime.now() + timedelta(days=2):
                                        deadline_alert = '⚠️'
                                except:
                                    pass
                            checked = st.checkbox(f"{t['description']} {deadline_alert}", value=t['done'], key=f"{category}-{subcat}-{i}")
                            t['done'] = checked
            else:
                for i, t in enumerate(content):
                    if filter_status == 'Todos' or (filter_status == 'Feito' and t['done']) or (filter_status == 'Não Feito' and not t['done']):
                        deadline_alert = ''
                        if t['deadline']:
                            try:
                                deadline_date = datetime.strptime(t['deadline'], '%Y-%m-%d')
                                if deadline_date <= datetime.now() + timedelta(days=2):
                                    deadline_alert = '⚠️'
                            except:
                                pass
                        checked = st.checkbox(f"{t['description']} {deadline_alert}", value=t['done'], key=f"{category}-{i}")
                        t['done'] = checked
        col_index = (col_index + 1) % 3
    save_tasks()

st.sidebar.header('Adicionar Tarefa')
category = st.sidebar.selectbox('Categoria', list(CATEGORIES.keys()))
subcategory = None
if isinstance(CATEGORIES[category], dict):
    subcategory = st.sidebar.selectbox('Subcategoria', list(CATEGORIES[category].keys()))

description = st.sidebar.text_input('Descrição da Tarefa')
deadline = st.sidebar.date_input('Prazo (opcional)', value=None)
if st.sidebar.button('Adicionar'):
    add_task(category, subcategory, description, str(deadline) if deadline else '')
    st.sidebar.success('Tarefa adicionada!')

st.sidebar.header('Filtros')
filter_status = st.sidebar.radio('Filtrar por status', ['Todos', 'Feito', 'Não Feito'])

st.sidebar.header('Exportar')
if st.sidebar.button('Exportar para Excel'):
    file_path = export_to_excel()
    st.sidebar.success(f'Arquivo exportado: {file_path}')

st.sidebar.header('Buscar Tarefa')
search_query = st.sidebar.text_input('Digite palavra-chave')
if search_query:
    st.subheader('Resultados da Busca')
    for category, content in tasks.items():
        if isinstance(content, dict):
            for subcat, sub_tasks in content.items():
                for t in sub_tasks:
                    if search_query.lower() in t['description'].lower():
                        st.write(f"{category} > {subcat}: {t['description']} (Prazo: {t['deadline']})")
        else:
            for t in content:
                if search_query.lower() in t['description'].lower():
                    st.write(f"{category}: {t['description']} (Prazo: {t['deadline']})")

display_tasks(filter_status)