from dataclasses import dataclass, field
from typing import Dict, Any, List
import requests
import datetime
import re

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

    def category_report(self,start_date: datetime.date, end_date: datetime.date) -> List[Dict[str, float]]:
        header = {"Authorization": f"Bearer {self.access_token}"}
        categories_url = f"{self.url}/api/v1/categories"

        with requests.Session() as session:
            session.headers.update(header)
            totals = list()

            for category in self.get_categories():
                url = f"{categories_url}/{category['id']}?start={start_date}&end={end_date}"
                category_data = session.get(url).json()["data"]
                category_name = category_data["attributes"]["name"]
                try:
                    category_spent = category_data["attributes"]["spent"][0]["sum"]
                except (KeyError, IndexError):
                    category_spent = 0
                try:
                    category_earned = category_data["attributes"]["earned"][0]["sum"]
                except (KeyError, IndexError):
                    category_earned = 0
                category_total = float(category_spent) + float(category_earned)
                totals.append(
                    {
                        "name": category_name,
                        "spent": category_spent,
                        "earned": category_earned,
                        "total": category_total,
                    }
                )

        return totals

    def summary_report(self,start_date: datetime.date, end_date: datetime.date) -> Dict[str, float]:
        header = {"Authorization": f"Bearer {self.access_token}"}
        summary_url = f"{self.url}/api/v1/summary/basic?start={start_date}&end={end_date}"

        with requests.Session() as session:
            session.headers.update(header)
            summary = session.get(summary_url).json()

        for key in summary:
            if re.match(r"spent-in-.*", key):
                currency_name = key.replace("spent-in-", "")
        spent = summary["spent-in-" + currency_name]["monetary_value"]
        earned = summary["earned-in-" + currency_name]["monetary_value"]
        net_change = summary["balance-in-" + currency_name]["monetary_value"]

        return {
            "spent": spent,
            "earned": earned,
            "net_change": net_change,
        }