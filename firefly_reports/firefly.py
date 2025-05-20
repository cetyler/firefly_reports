from dataclasses import dataclass
from typing import Dict, Any, List
import requests

@dataclass
class Firefly:
    url: str
    access_token: str

    def get_about(self) -> Dict[str, Any]:
        """
        Get information about the Firefly instance.
        :return: Dictionary with information about the Firefly instance.
        """
        header = {"Authorization": f"Bearer {self.access_token}"}
        about_url = f"{self.url}/api/v1/about"

        with requests.Session() as session:
            session.headers.update(header)
            about = session.get(about_url).json()["data"]

        return about

    def get_categories(self) -> List[Dict[str, Any]]:
        header = {"Authorization": f"Bearer {self.access_token}"}
        categories_url = f"{self.url}/api/v1/categories"

        with requests.Session() as session:
            session.headers.update(header)
            categories = session.get(categories_url).json()["data"]

        return categories