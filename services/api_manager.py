# services/api_manager.py
import requests
from typing import List, Dict, Optional
from datetime import datetime
import streamlit as st

class APIStorage:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def login(self, username: str, password: str) -> bool:
        """Authenticate and store the access token and user details in session state."""
        try:
            response = requests.post(
                f"{self.base_url}/auth/login",
                json={"email": username, "password": password}
            )
            response.raise_for_status()
            auth_data = response.json()
            st.session_state["logged_in"] = True
            st.session_state["currency_symbol"] = auth_data.get("currency")  # Set currency from auth response
            st.session_state["user_id"] = auth_data.get("user_id")  # Store user_id
            st.session_state["access_token"] = auth_data.get("access_token")  # Store access_token
            return True
        except requests.exceptions.RequestException as e:
            print(f"Login failed: {e}")
            return False

    def _make_request(self, method: str, endpoint: str, **kwargs):
        """Make an authenticated API request using the access token from session state."""
        if not st.session_state.get("access_token") or not st.session_state.get("user_id"):
            raise Exception("Not authenticated. Please log in first.")
        
        headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        return response.json()

    def load(self) -> List[Dict]:
        user_id = st.session_state.get("user_id")
        operations = self._make_request("GET", f"/balance/{user_id}/my-operations")
        # Add 'type' field based on the 'amount' value
        for operation in operations:
            operation["type"] = "income" if operation["amount"] > 0 else "expense"
        return operations

    def add_entry(self, entry_data: Dict) -> None:
        user_id = st.session_state.get("user_id")
        endpoint = f"/operations/{user_id}/add-income" if entry_data['type'] == 'income' else f"/operations/{user_id}/add-expense"
        self._make_request("POST", endpoint, json=entry_data)

    def delete_entry(self, entry_id: int) -> None:
        user_id = st.session_state.get("user_id")
        self._make_request("DELETE", f"/operations/{user_id}/delete-operation/{entry_id}")

    def get_categories(self) -> List[str]:
        response = self._make_request("GET", "/categories/all")
        return [cat['category_name'] for cat in response]