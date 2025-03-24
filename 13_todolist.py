import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Database setup
def init_db():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks 
                 (id INTEGER PRIMARY KEY, title TEXT, description TEXT, category TEXT, priority TEXT, 
                  due_date TEXT, completed BOOLEAN)''')
    conn.commit()
    conn.close()

# Add new task
def add_task(title, description, category, priority, due_date):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("INSERT INTO tasks (title, description, category, priority, due_date, completed) VALUES (?, ?, ?, ?, ?, ?)",
              (title, description, category, priority, due_date, False))
    conn.commit()
    conn.close()

# Get tasks
def get_tasks(filter_by=None, sort_by=None):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    query = "SELECT * FROM tasks"
    if filter_by:
        query += f" WHERE category = '{filter_by}'"
    if sort_by == "Deadline":
        query += " ORDER BY due_date ASC"
    elif sort_by == "Priority":
        query += " ORDER BY CASE priority WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 ELSE 3 END"
    c.execute(query)
    tasks = c.fetchall()
    conn.close()
    return tasks

# Mark task as complete
def complete_task(task_id):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

# Delete task
def delete_task(task_id):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

# UI Setup
st.set_page_config(page_title="Advanced To-Do List", layout="wide")
st.title("📌My To-Do List")
init_db()

# Task Input Form
with st.sidebar:
    st.header("Add New Task")
    title = st.text_input("Title")
    description = st.text_area("Description")
    category = st.selectbox("Category", ["Work", "Personal", "Other"])
    priority = st.selectbox("Priority", ["High", "Medium", "Low"], index=1)
    due_date = st.date_input("Due Date", min_value=datetime.today())
    if st.button("Add Task"):
        add_task(title, description, category, priority, due_date.strftime('%Y-%m-%d'))
        st.success("Task added successfully!")

# Task Filtering & Sorting
st.sidebar.subheader("Filters")
filter_by = st.sidebar.selectbox("Filter by Category", [None, "Work", "Personal", "Other"])
sort_by = st.sidebar.selectbox("Sort by", [None, "Deadline", "Priority"])

# Display Tasks
tasks = get_tasks(filter_by, sort_by)

def display_task(task):
    col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
    with col1:
        st.markdown(f"**{task[1]}** ({task[3]})")
        st.write(task[2])
    with col2:
        st.markdown(f"Due: `{task[5]}`")
        st.markdown(f"Priority: `{task[4]}`")
    with col3:
        if not task[6]:
            st.button("✔ Complete", key=f"comp_{task[0]}", on_click=complete_task, args=(task[0],))
    with col4:
        st.button("❌ Delete", key=f"del_{task[0]}", on_click=delete_task, args=(task[0],))
    st.divider()

for task in tasks:
    display_task(task)

# Progress Tracker
total_tasks = len(tasks)
completed_tasks = sum(1 for task in tasks if task[6])
if total_tasks > 0:
    progress = (completed_tasks / total_tasks) * 100
    st.sidebar.progress(progress / 100)
    st.sidebar.write(f"✅ {completed_tasks}/{total_tasks} tasks completed")

st.sidebar.markdown("---")
st.sidebar.write("Built with ❤️ using Streamlit")
