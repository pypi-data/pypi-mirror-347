from typing import List

class Reagent:
    """
    Represents a chemical reagent.

    Args:
        name (str): Name of the reagent.
        amount (float): Amount in mol.
    """
    def __init__(self, name: str, amount: float):
        self.name = name
        self.amount = amount

class Simulator:
    """
    Chemical experiment simulator.

    Args:
        temperature (float): Temperature in °C.
    """
    def __init__(self, temperature: float = 25.0):
        self.temperature = temperature
        self.reagents: List[Reagent] = []

    def add_reagent(self, name: str, amount: float):
        """Adds a reagent to the experiment."""
        self.reagents.append(Reagent(name, amount))

    def calculate_yield(self) -> float:
        """
        Calculates the theoretical yield based on temperature and reagents.

        Returns:
            float: Estimated yield percentage.
        """
        base = sum(r.amount for r in self.reagents)
        temp_factor = 1 + (self.temperature - 25) * 0.01
        return min(100, base * temp_factor * 10)
