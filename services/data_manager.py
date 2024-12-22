# services/data_manager.py
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.db_schema import Budget, Category, User
from models.db_config import get_db
from services.balance_calculator import BalanceCalculator

class DataStorage(ABC):
    @abstractmethod
    def load(self) -> List[Dict]:
        pass
    
    @abstractmethod
    def save(self, data: List[Dict]) -> None:
        pass

class PostgresStorage(DataStorage):
    def __init__(self):
        self.db = next(get_db())
    
    def load(self) -> List[Dict]:
        # Query with proper joins
        stmt = select(Budget, Category).join(Category)
        result = self.db.execute(stmt).all()
        return [self._convert_to_dict(row.Budget) for row in result]
    
    def save(self, data: List[Dict]) -> None:
        # In PostgreSQL implementation, we don't need this method
        pass
    
    def add_entry(self, entry_data: Dict) -> None:
        try:
            category_id = self._get_category_id(entry_data['category'])
            new_entry = Budget(
                usr_id=1,  # Hardcoded for now as mentioned
                entry_date=datetime.strptime(entry_data['date'], '%Y-%m-%d').date(),
                description=entry_data['description'],
                category_id=category_id,
                amount=entry_data['amount'] * (-1 if entry_data['type'] == 'expense' else 1)
            )
            self.db.add(new_entry)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
    
    def delete_entry(self, entry_id: int) -> None:
        try:
            entry = self.db.query(Budget).filter(Budget.entry_id == entry_id).first()
            if entry:
                self.db.delete(entry)
                self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
    
    def _get_category_id(self, category_name: str) -> int:
        category = self.db.query(Category).filter(Category.category_name == category_name).first()
        if not category:
            category = Category(
                category_name=category_name,
                category_description=f"Category for {category_name}"
            )
            self.db.add(category)
            self.db.commit()
        return category.category_id
    
    def _convert_to_dict(self, entry: Budget) -> Dict:
        category = self.db.query(Category).filter(Category.category_id == entry.category_id).first()
        return {
            'id': entry.entry_id,
            'date': entry.entry_date.strftime('%Y-%m-%d'),
            'description': entry.description,
            'amount': abs(entry.amount),
            'type': 'expense' if entry.amount < 0 else 'income',
            'category': category.category_name if category else 'Unknown'
        }
        
    def get_categories(self) -> List[str]:
        categories = self.db.query(Category.category_name).all()
        return [cat[0] for cat in categories]

class DataManager:
    def __init__(self, storage: DataStorage):
        self.storage = storage
        
    def get_current_balance(self) -> float:
        operations = self.get_operations()
        return BalanceCalculator.calculate_total_balance(operations)
    
    def add_operation(self, operation: Dict) -> None:
        if isinstance(self.storage, PostgresStorage):
            self.storage.add_entry(operation)
        else:
            self.storage.save([operation])
    
    def delete_operation(self, entry_id: int) -> None:
        if isinstance(self.storage, PostgresStorage):
            self.storage.delete_entry(entry_id)
    
    def get_operations(self) -> List[Dict]:
        return self.storage.load()
    
    def get_categories(self) -> List[str]:
        if isinstance(self.storage, PostgresStorage):
            return self.storage.get_categories()
        return []

    def clear_data(self) -> None:
        if isinstance(self.storage, PostgresStorage):
            # Implementation for clearing data in PostgreSQL
            pass