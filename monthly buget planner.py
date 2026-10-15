# ========== SMART FINANCE MANAGER ==========
class Transaction:

    def __init__(self, amount, category, description):
        self.amount = amount
        self.category = category
        self.description = description

    def display(self):
        print("Amount: Rs.", self.amount)
        print("Category:", self.category)
        print("Description:", self.description)


# Child Class - Inheritance
class Expense(Transaction):

    def __init__(self, amount, category, description):
        super().__init__(amount, category, description)


# Finance Manager Class
class FinanceManager:

    def __init__(self):
        self.monthly_income = 0
        self.monthly_budget = 0
        self.expenses = []

    # Set Monthly Income
    def set_income(self):
        try:
            income = float(input("Enter monthly income: Rs. "))

            if income > 0:
                self.monthly_income = income
                print("Income saved successfully!")
            else:
                print("Income must be greater than zero.")

        except ValueError:
            print("Enter a valid amount.")

    # Add Expense
    def add_expense(self):
        try:
            amount = float(input("Enter expense amount: Rs. "))

            if amount <= 0:
                print("Amount must be greater than zero.")
                return

            category = input("Enter category: ").strip().title()
            description = input("Enter description: ").strip()

            if not category or not description:
                print("Category and description cannot be empty.")
                return

            expense = Expense(amount, category, description)
            self.expenses.append(expense)

            print("Expense added successfully!")

            if (self.monthly_budget > 0
                    and self.calculate_expenses() > self.monthly_budget):
                print("Warning: Monthly budget exceeded!")

        except ValueError:
            print("Enter a valid amount.")

    # Calculate Total Expenses
    def calculate_expenses(self):
        total = 0

        for expense in self.expenses:
            total += expense.amount

        return total

    # View Expenses
    def view_expenses(self):
        if not self.expenses:
            print("No expenses found.")
            return

        for index, expense in enumerate(self.expenses, start=1):
            print("\nExpense Number:", index)
            expense.display()

    # Update Transaction
    def update_transaction(self):
        if not self.expenses:
            print("No expenses available to update.")
            return

        self.view_expenses()

        try:
            number = int(input("\nEnter expense number to update: "))

            if number < 1 or number > len(self.expenses):
                print("Invalid expense number.")
                return

            expense = self.expenses[number - 1]

            print("\n1. Add Amount")
            print("2. Update Category")
            print("3. Update Description")

            choice = input("Enter your choice: ")

            if choice == "1":
                amount = float(
                    input("Enter additional amount: Rs. ")
                )

                if amount <= 0:
                    print("Amount must be greater than zero.")
                    return

                expense.amount += amount
                print("Amount added successfully!")

            elif choice == "2":
                category = input("Enter new category: ").strip().title()

                if not category:
                    print("Category cannot be empty.")
                    return

                expense.category = category
                print("Category updated successfully!")

            elif choice == "3":
                description = input("Enter new description: ").strip()

                if not description:
                    print("Description cannot be empty.")
                    return

                expense.description = description
                print("Description updated successfully!")

            else:
                print("Invalid choice.")
                return

            if (self.monthly_budget > 0
                    and self.calculate_expenses() > self.monthly_budget):
                print("Warning: Monthly budget exceeded!")

        except ValueError:
            print("Please enter a valid input.")

    # Set Monthly Budget
    def set_budget(self):
        try:
            budget = float(input("Enter monthly budget: Rs. "))

            if budget > 0:
                self.monthly_budget = budget
                print("Budget saved successfully!")
            else:
                print("Budget must be greater than zero.")

        except ValueError:
            print("Enter a valid amount.")

    # Generate Monthly Report
    def monthly_report(self):
        total = self.calculate_expenses()
        balance = self.monthly_income - total

        print("\n====== MONTHLY REPORT ======")
        print(f"Monthly Income: Rs. {self.monthly_income:.2f}")
        print(f"Total Expenses: Rs. {total:.2f}")
        print(f"Remaining Balance: Rs. {balance:.2f}")

        if self.monthly_budget > 0:
            print(f"Monthly Budget: Rs. {self.monthly_budget:.2f}")

            if total > self.monthly_budget:
                print("Status: Budget Exceeded")
            else:
                print("Status: Within Budget")

        print("\nCategory-wise Expenses:")

        category_totals = {}

        for expense in self.expenses:
            category = expense.category

            if category in category_totals:
                category_totals[category] += expense.amount
            else:
                category_totals[category] = expense.amount

        if not category_totals:
            print("No expenses recorded.")
        else:
            for category, amount in category_totals.items():
                print(f"{category}: Rs. {amount:.2f}")


# Main Program
def main():
    manager = FinanceManager()

    while True:
        print("\n===== SMART FINANCE MANAGER =====")
        print("1. Set Monthly Income")
        print("2. Add Expense")
        print("3. View Expenses")
        print("4. Update Transaction")
        print("5. Set Monthly Budget")
        print("6. Generate Monthly Report")
        print("7. Exit")

        try:
            choice = int(input("Enter your choice: "))

            if choice == 1:
                manager.set_income()

            elif choice == 2:
                manager.add_expense()

            elif choice == 3:
                manager.view_expenses()

            elif choice == 4:
                manager.update_transaction()

            elif choice == 5:
                manager.set_budget()

            elif choice == 6:
                manager.monthly_report()

            elif choice == 7:
                print("Thank you for using Finance Manager!")
                break

            else:
                print("Choose a number between 1 and 7.")

        except ValueError:
            print("Enter a valid menu number.")


if __name__ == "__main__":
    main()

