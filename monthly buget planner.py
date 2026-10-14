
from datetime import datetime
# =============== CUSTOM EXCEPTIONS ===============
class InvalidAmountError(Exception):
    pass
# =============== BASE CLASS ===============
class Transaction:

    def __init__(self, amount, date, description):
        if amount <= 0:
            raise InvalidAmountError(
                "Amount must be greater than zero."
            )

        self.amount = amount
        self.date = date
        self.description = description

    def display(self):
        print("Date:", self.date)
        print("Amount: Rs.", self.amount)
        print("Description:", self.description)


# =============== INCOME CLASS ===============

class Income(Transaction):

    def __init__(self, amount, date, description, source):
        super().__init__(amount, date, description)
        self.source = source

    def display(self):
        print("\n--- INCOME DETAILS ---")
        super().display()
        print("Source:", self.source)


# =============== EXPENSE CLASS ===============

class Expense(Transaction):

    def __init__(self, amount, date, description, category):
        super().__init__(amount, date, description)
        self.category = category

    def display(self):
        print("\n--- EXPENSE DETAILS ---")
        super().display()
        print("Category:", self.category)


# =============== FINANCE MANAGER ===============

class FinanceManager:

    def __init__(self):
        self.monthly_income = 0
        self.transactions = []
        self.category_budgets = {}
        self.monthly_budget = 0
        self.savings_goal = 0

    # ---------- INPUT VALIDATION ----------

    def get_amount(self, message):
        while True:
            try:
                amount = float(input(message))

                if amount <= 0:
                    raise InvalidAmountError(
                        "Amount must be greater than zero."
                    )

                return amount

            except ValueError:
                print("Please enter a valid number.")

            except InvalidAmountError as error:
                print(error)

    def get_date(self):
        while True:
            date = input(
                "Enter date (YYYY-MM-DD), "
                "or press Enter for today: "
            ).strip()

            if date == "":
                return datetime.today().strftime("%Y-%m-%d")

            try:
                datetime.strptime(date, "%Y-%m-%d")
                return date

            except ValueError:
                print("Invalid date. Try again.")

    # ---------- MONTHLY INCOME ----------

    def set_income(self):
        self.monthly_income = self.get_amount(
            "Enter monthly income: Rs. "
        )

        print("Monthly income saved successfully.")

    # ---------- ADD INCOME ----------

    def add_income(self):
        amount = self.get_amount(
            "Enter additional income: Rs. "
        )

        date = self.get_date()
        source = input("Enter income source: ").strip()
        description = input("Enter description: ").strip()

        if source == "":
            print("Income source cannot be empty.")
            return

        try:
            income = Income(
                amount, date, description, source
            )

            self.transactions.append(income)
            print("Income added successfully.")

        except InvalidAmountError as error:
            print(error)

    # ---------- ADD EXPENSE ----------

    def add_expense(self):
        amount = self.get_amount(
            "Enter expense amount: Rs. "
        )

        date = self.get_date()

        category = input(
            "Enter category (Food, Travel, Rent, Shopping): "
        ).strip().title()

        description = input("Enter description: ").strip()

        if category == "":
            print("Category cannot be empty.")
            return

        try:
            expense = Expense(
                amount, date, description, category
            )

            self.transactions.append(expense)
            print("Expense added successfully.")

            month_expenses = self.calculate_expenses(
                date[:7]
            )

            if (
                self.monthly_budget > 0
                and month_expenses > self.monthly_budget
            ):
                print("Warning: Monthly budget exceeded!")

            category_total = sum(
                transaction.amount
                for transaction in self.transactions
                if isinstance(transaction, Expense)
                and transaction.category == category
                and transaction.date.startswith(date[:7])
            )

            limit = self.category_budgets.get(category, 0)

            if limit > 0 and category_total > limit:
                print("Warning: Category budget exceeded!")

        except InvalidAmountError as error:
            print(error)

    # ---------- VIEW TRANSACTIONS ----------

    def view_transactions(self):
        if len(self.transactions) == 0:
            print("No transactions found.")
            return

        for index, transaction in enumerate(
            self.transactions, start=1
        ):
            print("\nTransaction number:", index)
            transaction.display()

    # ---------- SEARCH TRANSACTIONS ----------

    def search_transactions(self):
        keyword = input(
            "Enter category, description, or date: "
        ).strip().lower()

        found = False

        for transaction in self.transactions:
            matches = (
                keyword in transaction.description.lower()
                or keyword in transaction.date.lower()
            )

            if isinstance(transaction, Expense):
                matches = matches or (
                    keyword in transaction.category.lower()
                )

            if isinstance(transaction, Income):
                matches = matches or (
                    keyword in transaction.source.lower()
                )

            if matches:
                transaction.display()
                found = True

        if not found:
            print("No matching transaction found.")

    # ---------- UPDATE TRANSACTION ----------

    def update_transaction(self):
        self.view_transactions()

        if not self.transactions:
            return

        try:
            number = int(input(
                "Enter transaction number to update: "
            ))

            if number < 1 or number > len(self.transactions):
                print("Invalid transaction number.")
                return

            transaction = self.transactions[number - 1]

            print("1. Update amount")
            print("2. Update description")
            print("3. Update date")

            choice = input("Enter choice: ")

            if choice == "1":
                transaction.amount = self.get_amount(
                    "Enter new amount: Rs. "
                )

            elif choice == "2":
                transaction.description = input(
                    "Enter new description: "
                ).strip()

            elif choice == "3":
                transaction.date = self.get_date()

            else:
                print("Invalid choice.")
                return

            print("Transaction updated successfully.")

        except ValueError:
            print("Please enter a valid number.")

    # ---------- DELETE TRANSACTION ----------

    def delete_transaction(self):
        self.view_transactions()

        if not self.transactions:
            return

        try:
            number = int(input(
                "Enter transaction number to delete: "
            ))

            if number < 1 or number > len(self.transactions):
                print("Invalid transaction number.")
                return

            deleted = self.transactions.pop(number - 1)

            print(
                "Deleted transaction:",
                deleted.description
            )

        except ValueError:
            print("Please enter a valid number.")

    # ---------- SET BUDGET ----------

    def set_budget(self):
        print("\n1. Set monthly expense budget")
        print("2. Set savings goal")

        choice = input("Enter choice: ")

        if choice == "1":
            self.monthly_budget = self.get_amount(
                "Enter monthly budget: Rs. "
            )
            print("Monthly budget updated.")

        elif choice == "2":
            self.savings_goal = self.get_amount(
                "Enter savings goal: Rs. "
            )
            print("Savings goal updated.")

        else:
            print("Invalid choice.")

    # ---------- CATEGORY BUDGET ----------

    def set_category_budget(self):
        category = input(
            "Enter expense category: "
        ).strip().title()

        if category == "":
            print("Category cannot be empty.")
            return

        amount = self.get_amount(
            "Enter category budget: Rs. "
        )

        self.category_budgets[category] = amount

        print("Category budget saved.")

    # ---------- CALCULATE EXPENSES ----------

    def calculate_expenses(self, month=None):
        total = 0

        for transaction in self.transactions:
            if isinstance(transaction, Expense):
                if (
                    month is None
                    or transaction.date.startswith(month)
                ):
                    total += transaction.amount

        return total

    # ---------- MONTHLY REPORT ----------

    def monthly_report(self):
        month = input(
            "Enter month (YYYY-MM), or Enter for current month: "
        ).strip()

        if month == "":
            month = datetime.today().strftime("%Y-%m")

        try:
            datetime.strptime(month, "%Y-%m")
        except ValueError:
            print("Invalid month format.")
            return

        extra_income = sum(
            transaction.amount
            for transaction in self.transactions
            if isinstance(transaction, Income)
            and transaction.date.startswith(month)
        )

        expenses = [
            transaction
            for transaction in self.transactions
            if isinstance(transaction, Expense)
            and transaction.date.startswith(month)
        ]

        total_income = self.monthly_income + extra_income
        total_expenses = sum(
            transaction.amount for transaction in expenses
        )

        balance = total_income - total_expenses

        print("\n========== MONTHLY REPORT ==========")
        print("Month:", month)
        print(f"Monthly income: Rs.{self.monthly_income:.2f}")
        print(f"Additional income: Rs.{extra_income:.2f}")
        print(f"Total income: Rs.{total_income:.2f}")
        print(f"Total expenses: Rs.{total_expenses:.2f}")
        print(f"Remaining balance: Rs.{balance:.2f}")

        if total_income > 0:
            percentage = balance / total_income * 100
            print(f"Savings percentage: {percentage:.2f}%")

        category_totals = {}

        for expense in expenses:
            category = expense.category

            category_totals[category] = (
                category_totals.get(category, 0)
                + expense.amount
            )

        print("\nCategory-wise expenses:")

        for category, total in sorted(
            category_totals.items(),
            key=lambda item: item[1],
            reverse=True
        ):
            print(f"{category}: Rs.{total:.2f}")

        if expenses:
            highest = max(
                expenses,
                key=lambda transaction: transaction.amount
            )

            print("\nHighest expense:", highest.description)
            print(f"Amount: Rs.{highest.amount:.2f}")

        if self.savings_goal > 0:
            if balance >= self.savings_goal:
                print("Savings goal achieved!")
            else:
                print(
                    "Amount needed for savings goal: "
                    f"Rs.{self.savings_goal - balance:.2f}"
                )


# =============== MAIN PROGRAM ===============

def main():
    manager = FinanceManager()

    while True:
        print("\n====== SMART FINANCE MANAGER ======")
        print("1. Set Monthly Income")
        print("2. Add Additional Income")
        print("3. Add Expense")
        print("4. View Transactions")
        print("5. Search Transactions")
        print("6. Update Transaction")
        print("7. Delete Transaction")
        print("8. Set Budget or Savings Goal")
        print("9. Set Category Budget")
        print("10. Generate Monthly Report")
        print("11. Exit")

        try:
            choice = int(input("Enter your choice: "))

            if choice == 1:
                manager.set_income()

            elif choice == 2:
                manager.add_income()

            elif choice == 3:
                manager.add_expense()

            elif choice == 4:
                manager.view_transactions()

            elif choice == 5:
                manager.search_transactions()

            elif choice == 6:
                manager.update_transaction()

            elif choice == 7:
                manager.delete_transaction()

            elif choice == 8:
                manager.set_budget()

            elif choice == 9:
                manager.set_category_budget()

            elif choice == 10:
                manager.monthly_report()

            elif choice == 11:
                print("Thank you for using Finance Manager!")
                break

            else:
                print("Choose a number between 1 and 11.")

        except ValueError:
            print("Invalid input. Please enter a number.")

        except KeyboardInterrupt:
            print("\nProgram stopped.")
            break


if __name__ == "__main__":
    main()
