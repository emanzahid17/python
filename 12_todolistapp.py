# tasks = []
# def addTask():
#     task = input("Please enter a task: ")
#     tasks.append(task)
#     print(f"Task '{task}' added to the list.")

# def listTasks():
#     if not tasks:
#         print("No tasks in the list.")
#     else:
#         print("Your tasks:")
#         for index, task in enumerate(tasks):
#             print(f"{index + 1}. {task}")

# def deleteTask():
#     listTasks()
#     try:
#         tasktodelete = int(input("Enter the # of the task you want to delete: "))
#         if tasktodelete >= 0 and tasktodelete < len(tasks):
#             tasks.pop(tasktodelete)
#             print(f"Task '{tasktodelete}' deleted from the list.")
#         else:
#             print(f"Task # {tasktodelete} does not exist.") 
#     except:
#         print("Invalid task number.")
    
# if __name__ == "__main__":
#     ### create a loop to run the app
#     print("Welcome to My To Do List App")
#     while True:
#         print("\n")
#         print("Please select one of the following options")
#         print("-"* 30)
#         print("1. Add a task")
#         print("2. Delete a task")
#         print("3. List the tasks")
#         print("4. Exit the app")

#         choice = input("Enter your choice: ")
#         if (choice == '1'):
#             addTask()

#         elif (choice == '2'):
#             deleteTask()

#         elif (choice == '3'):
#             listTasks()
        
#         elif (choice == '4'):
#             break

#         else:
#             print("Invalid inout. Please Try Again")  
#     print("GoodBye 👋👋")
        
import streamlit as st

# Initialize session state for tasks
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Streamlit App
st.title("📝 My To-Do List App")

# Input field for adding a task
new_task = st.text_input("Enter a new task:", value="")  # Avoid modifying session_state directly
if st.button("Add Task"):
    if new_task.strip():  # Prevent empty tasks
        st.session_state.tasks.append(new_task.strip())
        st.rerun()
    else:
        st.warning("Please enter a valid task before adding.")

# Display tasks
st.subheader("Your Tasks:")
if st.session_state.tasks:
    for index, task in enumerate(st.session_state.tasks):
        col1, col2 = st.columns([4, 1])
        col1.write(f"{index + 1}. {task}")
        if col2.button("❌ Delete", key=f"del_{index}"):
            st.session_state.tasks.pop(index)
            st.rerun()
else:
    st.write("No tasks in the list.")






