from abc import ABC, abstractmethod
from datetime import datetime
import json
from pathlib import Path
from typing import List, Dict, Optional
from services.balance_calculator import BalanceCalculator

class DataStorage(ABC):
    @abstractmethod
    def load(self) -> List[Dict]:
        pass
    
    @abstractmethod
    def save(self, data: List[Dict]) -> None:
        pass

class JSONStorage(DataStorage):
    def __init__(self, file_path: str = 'operations.json'):
        self.file_path = Path(file_path)
    
    def load(self) -> List[Dict]:
        if self.file_path.exists():
            try:
                with open(self.file_path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []
    
    def save(self, data: List[Dict]) -> None:
        with open(self.file_path, 'w') as f:
            json.dump(data, f)

class DataManager:
    def __init__(self, storage: DataStorage):
        self.storage = storage
        self.operations = self.storage.load()

    def get_current_balance(self) -> float:
        return BalanceCalculator.calculate_total_balance(self.operations)
    
    def add_operation(self, operation: Dict) -> None:
        self.operations.append(operation)
        self.storage.save(self.operations)
    
    def delete_operation(self, index: int) -> None:
        self.operations.pop(index)
        self.storage.save(self.operations)
    
    def get_operations(self) -> List[Dict]:
        return self.operations

    def clear_data(self) -> None:
        self.operations = []
        self.storage.save(self.operations)