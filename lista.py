def display_menu():
    """Displays the main menu options to the user."""
    print("\n--- To-Do List Menu ---")
    print("1. View Tasks")
    print("2. Add Task")
    print("3. Edit Task")
    print("4. Remove Task")
    print("5. Exit")

def view_tasks(tasks):
    """Displays all tasks in the to-do list."""
    if not tasks:
        print("\nYour to-do list is empty!")
    else:
        print("\n--- Your Tasks ---")
        for i, task in enumerate(tasks, 1):
            status = "✓" if task['completed'] else " "
            print(f"{i}. [{status}] {task['description']}")

def add_task(tasks):
    """Adds a new task to the to-do list."""
    description = input("Enter the task description: ").strip()
    if description:
        tasks.append({"description": description, "completed": False})
        print(f"Task '{description}' added successfully!")
    else:
        print("Task description cannot be empty.")

def edit_task(tasks):
    """Edits an existing task in the to-do list."""
    view_tasks(tasks)
    if not tasks:
        return

    try:
        task_num = int(input("Enter the number of the task to edit: "))
        if 1 <= task_num <= len(tasks):
            new_description = input("Enter the new description for the task (leave blank to keep current): ").strip()
            if new_description:
                tasks[task_num - 1]['description'] = new_description
                print("Task updated successfully!")
            
            while True:
                mark_complete = input("Mark this task as complete? (yes/no): ").lower().strip()
                if mark_complete in ['yes', 'y']:
                    tasks[task_num - 1]['completed'] = True
                    print("Task marked as complete.")
                    break
                elif mark_complete in ['no', 'n']:
                    tasks[task_num - 1]['completed'] = False
                    print("Task marked as incomplete.")
                    break
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")

        else:
            print("Invalid task number.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def remove_task(tasks):
    """Removes a task from the to-do list."""
    view_tasks(tasks)
    if not tasks:
        return

    try:
        task_num = int(input("Enter the number of the task to remove: "))
        if 1 <= task_num <= len(tasks):
            removed_task = tasks.pop(task_num - 1)
            print(f"Task '{removed_task['description']}' removed successfully!")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def main():
    """Main function to run the to-do list program."""
    tasks = []

    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            view_tasks(tasks)
        elif choice == '2':
            add_task(tasks)
        elif choice == '3':
            edit_task(tasks)
        elif choice == '4':
            remove_task(tasks)
        elif choice == '5':
            print("Exiting to-do list. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()