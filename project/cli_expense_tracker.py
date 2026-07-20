# Name: Arjun Jaiswal
# Project: CLI Expense Tracker

import json
import datetime
import os

EXPENSES_FILE = "expenses.json"

def load_expenses():
    try:
        if os.path.exists(EXPENSES_FILE):
            with open(EXPENSES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading expenses: {e}")
    # Return empty list and create/initialize file if load failed or doesn't exist
    expenses = []
    save_expenses(expenses)
    return expenses

def save_expenses(expenses):
    try:
        with open(EXPENSES_FILE, "w", encoding="utf-8") as f:
            json.dump(expenses, f, indent=4)
    except Exception as e:
        print(f"Error saving expenses: {e}")

def add_expense(expenses):
    try:
        title = input("Enter title: ")
        amount = float(input("Enter amount: "))
        category = input("Enter category: ")
        date = datetime.date.today().isoformat()

        expense = {
            "title": title,
            "amount": amount,
            "category": category,
            "date": date
        }

        expenses.append(expense)
        save_expenses(expenses)
        print("Expense added successfully!")
    except ValueError:
        print("Invalid input! Amount must be a number.")
    except Exception as e:
        print(f"An error occurred while adding expense: {e}")

def view_expenses(expenses):
    try:
        if len(expenses) == 0:
            print("No expenses found.")
        else:
            print("\nExpenses:")
            for expense in expenses:
                print("-" * 40)
                print(f"Title    : {expense['title']}")
                print(f"Amount   : ₹{expense['amount']}")
                print(f"Category : {expense['category']}")
                print(f"Date     : {expense['date']}")
    except Exception as e:
        print(f"An error occurred while viewing expenses: {e}")

def search_by_category(expenses):
    try:
        category = input("Enter category to search: ")

        found = False

        for expense in expenses:
            if expense["category"].lower() == category.lower():
                found = True
                print("-" * 40)
                print(f"Title    : {expense['title']}")
                print(f"Amount   : ₹{expense['amount']}")
                print(f"Category : {expense['category']}")
                print(f"Date     : {expense['date']}")

        if not found:
            print("No expenses found in this category.")
    except Exception as e:
        print(f"An error occurred while searching expenses: {e}")

def update_expense(expenses):
    try:
        title = input("Enter title to update: ")

        found = False

        for expense in expenses:
            if expense["title"].lower() == title.lower():
                expense["amount"] = float(input("Enter new amount: "))
                expense["category"] = input("Enter new category: ")
                expense["date"] = datetime.date.today().isoformat()
                save_expenses(expenses)
                print("Expense updated successfully!")
                found = True
                break

        if not found:
            print("Expense not found.")
    except ValueError:
        print("Invalid input! Amount must be a number.")
    except Exception as e:
        print(f"An error occurred while updating expense: {e}")

def delete_expense(expenses):
    try:
        title = input("Enter title to delete: ")

        found = False

        for expense in expenses:
            if expense["title"].lower() == title.lower():
                expenses.remove(expense)
                save_expenses(expenses)
                print("Expense deleted successfully!")
                found = True
                break

        if not found:
            print("Expense not found.")
    except Exception as e:
        print(f"An error occurred while deleting expense: {e}")

def show_summary(expenses):
    try:
        if len(expenses) == 0:
            print("No expenses to summarize.")
        else:
            total = 0
            highest = expenses[0]["amount"]
            lowest = expenses[0]["amount"]

            for expense in expenses:
                total += expense["amount"]

                if expense["amount"] > highest:
                    highest = expense["amount"]

                if expense["amount"] < lowest:
                    lowest = expense["amount"]

            print("\nSummary")
            print("-" * 30)
            print(f"Total Expenses : {len(expenses)}")
            print(f"Total Amount   : ₹{total}")
            print(f"Average Amount : ₹{total / len(expenses):.2f}")
            print(f"Highest Amount : ₹{highest}")
            print(f"Lowest Amount  : ₹{lowest}")
    except Exception as e:
        print(f"An error occurred while showing summary: {e}")

# Main program flow
try:
    print("===================================")
    print("      CLI Expense Tracker")
    print("===================================")

    expenses = load_expenses()

    while True:
        print("\nMenu")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Search by Category")
        print("4. Update Expense")
        print("5. Delete Expense")
        print("6. Show Summary")
        print("7. Exit")

        try:
            choice = input("\nEnter your choice: ")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting program...")
            break

        if choice == "1":
            add_expense(expenses)
            
        elif choice == "2":
            view_expenses(expenses)

        elif choice == "3":
            search_by_category(expenses)

        elif choice == "4":
            update_expense(expenses)

        elif choice == "5":
            delete_expense(expenses)

        elif choice == "6":
            show_summary(expenses)

        elif choice == "7":
            print("Thank you for using Expense Tracker!")
            break

        else:
            print("Invalid choice. Please try again.")

except Exception as main_err:
    print(f"A critical error occurred: {main_err}")