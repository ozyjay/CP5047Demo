#!/usr/bin/env python3
"""
Personal Budget Calculator

A simple Python application for tracking income, expenses, and calculating budget summaries.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Tuple


class BudgetCalculator:
    """A simple personal budget calculator."""
    
    def __init__(self, data_file: str = "budget_data.json"):
        """Initialize the budget calculator with a data file."""
        self.data_file = data_file
        self.data = self.load_data()
    
    def load_data(self) -> Dict:
        """Load budget data from file or create new data structure."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        
        # Return default data structure
        return {
            "income": [],
            "expenses": [],
            "budget_goals": {}
        }
    
    def save_data(self) -> None:
        """Save budget data to file."""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except IOError as e:
            print(f"Error saving data: {e}")
    
    def add_income(self, amount: float, description: str = "", category: str = "salary") -> None:
        """Add income entry."""
        if amount <= 0:
            raise ValueError("Income amount must be positive")
        
        entry = {
            "amount": amount,
            "description": description,
            "category": category,
            "date": datetime.now().isoformat()
        }
        self.data["income"].append(entry)
        self.save_data()
        print(f"Added income: ${amount:.2f} - {description}")
    
    def add_expense(self, amount: float, description: str = "", category: str = "general") -> None:
        """Add expense entry."""
        if amount <= 0:
            raise ValueError("Expense amount must be positive")
        
        entry = {
            "amount": amount,
            "description": description,
            "category": category,
            "date": datetime.now().isoformat()
        }
        self.data["expenses"].append(entry)
        self.save_data()
        print(f"Added expense: ${amount:.2f} - {description}")
    
    def set_budget_goal(self, category: str, amount: float) -> None:
        """Set a budget goal for a category."""
        if amount < 0:
            raise ValueError("Budget goal must be non-negative")
        
        self.data["budget_goals"][category] = amount
        self.save_data()
        print(f"Set budget goal for {category}: ${amount:.2f}")
    
    def calculate_totals(self) -> Tuple[float, float, float]:
        """Calculate total income, expenses, and net amount."""
        total_income = sum(entry["amount"] for entry in self.data["income"])
        total_expenses = sum(entry["amount"] for entry in self.data["expenses"])
        net_amount = total_income - total_expenses
        return total_income, total_expenses, net_amount
    
    def get_expenses_by_category(self) -> Dict[str, float]:
        """Get expenses grouped by category."""
        expenses_by_category = {}
        for expense in self.data["expenses"]:
            category = expense["category"]
            expenses_by_category[category] = expenses_by_category.get(category, 0) + expense["amount"]
        return expenses_by_category
    
    def check_budget_goals(self) -> Dict[str, Dict]:
        """Check budget goals against actual spending."""
        expenses_by_category = self.get_expenses_by_category()
        goal_status = {}
        
        for category, goal in self.data["budget_goals"].items():
            spent = expenses_by_category.get(category, 0)
            remaining = goal - spent
            status = {
                "goal": goal,
                "spent": spent,
                "remaining": remaining,
                "over_budget": remaining < 0
            }
            goal_status[category] = status
        
        return goal_status
    
    def display_summary(self) -> None:
        """Display budget summary."""
        print("\n" + "="*50)
        print("         PERSONAL BUDGET SUMMARY")
        print("="*50)
        
        total_income, total_expenses, net_amount = self.calculate_totals()
        
        print(f"\nTotal Income:  ${total_income:>10.2f}")
        print(f"Total Expenses: ${total_expenses:>9.2f}")
        print("-" * 30)
        print(f"Net Amount:    ${net_amount:>10.2f}")
        
        if net_amount >= 0:
            print("✅ You're within budget!")
        else:
            print("⚠️  You're over budget!")
        
        # Show expenses by category
        expenses_by_category = self.get_expenses_by_category()
        if expenses_by_category:
            print("\nExpenses by Category:")
            print("-" * 30)
            for category, amount in sorted(expenses_by_category.items()):
                print(f"{category.capitalize():<15}: ${amount:>8.2f}")
        
        # Show budget goal status
        goal_status = self.check_budget_goals()
        if goal_status:
            print("\nBudget Goal Status:")
            print("-" * 30)
            for category, status in goal_status.items():
                goal = status["goal"]
                spent = status["spent"]
                remaining = status["remaining"]
                
                if status["over_budget"]:
                    print(f"{category.capitalize():<15}: ${spent:>8.2f} / ${goal:.2f} (⚠️  Over by ${abs(remaining):.2f})")
                else:
                    print(f"{category.capitalize():<15}: ${spent:>8.2f} / ${goal:.2f} (✅ ${remaining:.2f} remaining)")
        
        print("="*50)


def main():
    """Main application loop."""
    calculator = BudgetCalculator()
    
    print("Welcome to Personal Budget Calculator!")
    print("Type 'help' for available commands or 'quit' to exit.")
    
    while True:
        try:
            command = input("\n> ").strip().lower()
            
            if command == 'quit' or command == 'exit':
                break
            elif command == 'help':
                print("""
Available commands:
  income <amount> [description] [category] - Add income
  expense <amount> [description] [category] - Add expense  
  goal <category> <amount> - Set budget goal for category
  summary - Display budget summary
  clear - Clear all data
  help - Show this help message
  quit - Exit the application

Examples:
  income 3000 "Monthly salary" salary
  expense 50.25 "Groceries" food
  goal food 400
  summary
                """)
            elif command == 'summary':
                calculator.display_summary()
            elif command == 'clear':
                confirm = input("Are you sure you want to clear all data? (yes/no): ")
                if confirm.lower() == 'yes':
                    calculator.data = {"income": [], "expenses": [], "budget_goals": {}}
                    calculator.save_data()
                    print("All data cleared.")
            elif command.startswith('income '):
                parts = command.split()[1:]
                if len(parts) >= 1:
                    amount = float(parts[0])
                    description = parts[1].strip('"\'') if len(parts) > 1 else ""
                    category = parts[2].strip('"\'') if len(parts) > 2 else "salary"
                    calculator.add_income(amount, description, category)
                else:
                    print("Usage: income <amount> [description] [category]")
            elif command.startswith('expense '):
                parts = command.split()[1:]
                if len(parts) >= 1:
                    amount = float(parts[0])
                    description = parts[1].strip('"\'') if len(parts) > 1 else ""
                    category = parts[2].strip('"\'') if len(parts) > 2 else "general"
                    calculator.add_expense(amount, description, category)
                else:
                    print("Usage: expense <amount> [description] [category]")
            elif command.startswith('goal '):
                parts = command.split()[1:]
                if len(parts) >= 2:
                    category = parts[0]
                    amount = float(parts[1])
                    calculator.set_budget_goal(category, amount)
                else:
                    print("Usage: goal <category> <amount>")
            else:
                print("Unknown command. Type 'help' for available commands.")
        
        except ValueError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
    
    print("Thank you for using Personal Budget Calculator!")


if __name__ == "__main__":
    main()