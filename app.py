#!/usr/bin/env python3
"""
Flask Web Interface for Personal Budget Calculator

A web-based interface for managing income, expenses, and budget goals.
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from budget_calculator import BudgetCalculator

app = Flask(__name__)
app.secret_key = 'budget_calculator_secret_key_2024'

# Initialize calculator instance
calculator = BudgetCalculator()


@app.route('/')
def index():
    """Display budget dashboard summary."""
    # Reload data to get latest changes
    calculator.data = calculator.load_data()
    
    # Get totals
    total_income, total_expenses, net_amount = calculator.calculate_totals()
    
    # Get expenses by category
    expenses_by_category = calculator.get_expenses_by_category()
    
    # Get budget goal status
    goal_status = calculator.check_budget_goals()
    
    return render_template(
        'index.html',
        total_income=total_income,
        total_expenses=total_expenses,
        net_amount=net_amount,
        expenses_by_category=expenses_by_category,
        goal_status=goal_status,
        budget_goals=calculator.data.get('budget_goals', {})
    )


@app.route('/income', methods=['POST'])
def add_income():
    """Add income entry."""
    try:
        amount = float(request.form.get('amount', 0))
        description = request.form.get('description', '').strip()
        category = request.form.get('category', 'salary').strip() or 'salary'
        
        if amount <= 0:
            flash('Income amount must be positive', 'error')
        else:
            calculator.add_income(amount, description, category)
            flash(f'Successfully added income: ${amount:.2f} - {description}', 'success')
    except ValueError as e:
        flash(f'Error: {str(e)}', 'error')
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
    
    return redirect(url_for('index'))


@app.route('/expense', methods=['POST'])
def add_expense():
    """Add expense entry."""
    try:
        amount = float(request.form.get('amount', 0))
        description = request.form.get('description', '').strip()
        category = request.form.get('category', 'general').strip() or 'general'
        
        if amount <= 0:
            flash('Expense amount must be positive', 'error')
        else:
            calculator.add_expense(amount, description, category)
            flash(f'Successfully added expense: ${amount:.2f} - {description}', 'success')
    except ValueError as e:
        flash(f'Error: {str(e)}', 'error')
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
    
    return redirect(url_for('index'))


@app.route('/goal', methods=['POST'])
def set_goal():
    """Set or update budget goal."""
    try:
        category = request.form.get('category', '').strip()
        amount = float(request.form.get('amount', 0))
        
        if not category:
            flash('Category is required for budget goals', 'error')
        elif amount < 0:
            flash('Budget goal must be non-negative', 'error')
        else:
            calculator.set_budget_goal(category, amount)
            flash(f'Successfully set budget goal for {category}: ${amount:.2f}', 'success')
    except ValueError as e:
        flash(f'Error: {str(e)}', 'error')
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
    
    return redirect(url_for('index'))


@app.route('/clear', methods=['POST'])
def clear_data():
    """Clear all budget data with confirmation."""
    confirm = request.form.get('confirm', '').strip()
    
    if confirm == 'CLEAR':
        calculator.data = {"income": [], "expenses": [], "budget_goals": {}}
        calculator.save_data()
        flash('All data has been cleared successfully', 'success')
    else:
        flash('Data not cleared. You must type "CLEAR" to confirm.', 'error')
    
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
