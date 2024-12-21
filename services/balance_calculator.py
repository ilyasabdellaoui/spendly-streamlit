from typing import List, Dict

class BalanceCalculator:
    @staticmethod
    def calculate_total_balance(operations: List[Dict]) -> float:
        balance = 0
        for op in operations:
            if op['type'] == 'income':
                balance += op['amount']
            else:
                balance -= op['amount']
        return balance
    
    @staticmethod
    def calculate_category_totals(operations: List[Dict]) -> Dict[str, float]:
        totals = {}
        for op in operations:
            category = op['category']
            amount = op['amount']
            if category not in totals:
                totals[category] = 0
            if op['type'] == 'income':
                totals[category] += amount
            else:
                totals[category] -= amount
        return totals