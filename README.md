# CP5047Demo
Simple repo to demonstrate how you can work together on a shared project

## Personal Budget Calculator

A simple Python application for tracking income, expenses, and calculating budget summaries.

### Features

- **Income Tracking**: Record income entries with amounts, descriptions, and categories
- **Expense Tracking**: Track expenses with detailed categorization
- **Budget Goals**: Set spending goals for different categories and monitor progress
- **Budget Analysis**: View comprehensive summaries and category breakdowns
- **Data Persistence**: Automatically saves data to JSON file for future sessions
- **User-friendly CLI**: Interactive command-line interface with clear prompts

### Usage

Run the budget calculator:

```bash
python3 budget_calculator.py
```

### Available Commands

- `income <amount> [description] [category]` - Add income entry
- `expense <amount> [description] [category]` - Add expense entry
- `goal <category> <amount>` - Set budget goal for category
- `summary` - Display comprehensive budget summary
- `clear` - Clear all data (with confirmation)
- `help` - Show available commands
- `quit` - Exit the application

### Examples

```
> income 3000 salary salary
Added income: $3000.00 - salary

> expense 500 rent housing
Added expense: $500.00 - rent

> expense 150 groceries food
Added expense: $150.00 - groceries

> goal food 300
Set budget goal for food: $300.00

> summary
==================================================
         PERSONAL BUDGET SUMMARY
==================================================

Total Income:  $   3000.00
Total Expenses: $   650.00
------------------------------
Net Amount:    $   2350.00
✅ You're within budget!

Expenses by Category:
------------------------------
Food           : $  150.00
Housing        : $  500.00

Budget Goal Status:
------------------------------
Food           : $  150.00 / $300.00 (✅ $150.00 remaining)
==================================================
```

### Data Storage

The application automatically saves all data to `budget_data.json` in the same directory. This ensures your budget information persists between sessions.
