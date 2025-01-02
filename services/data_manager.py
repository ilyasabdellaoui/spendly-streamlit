# services/data_manager.py
from typing import Dict, List
from services.api_manager import APIStorage
from services.balance_calculator import BalanceCalculator

class DataManager:
    def __init__(self, storage: APIStorage):
        self.storage = storage
        
    def get_current_balance(self) -> float:
        operations = self.get_operations()
        return BalanceCalculator.calculate_total_balance(operations)
    
    def add_operation(self, operation: Dict) -> None:
        self.storage.add_entry(operation)
    
    def delete_operation(self, entry_id: int) -> None:
        self.storage.delete_entry(entry_id)
    
    def get_operations(self) -> List[Dict]:
        return self.storage.load()
    
    def get_categories(self) -> List[str]:
        return self.storage.get_categories()

    def clear_data(self) -> None:
        # Implementation for clearing data via API if needed
        pass