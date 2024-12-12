class Budget:
    def __init__(self, event_id=None, requirement_name=None, requirement_budget=0, requirement_quantity=0):
        self._event_id = event_id
        self._requirement_name = requirement_name
        self._requirement_budget = requirement_budget
        self._requirement_quantity = requirement_quantity

    def get_budget(self, event_id):
        if self._event_id == event_id:
            return self._requirement_budget
        else:
            return None

    def get_requirement_name(self):
        return self._requirement_name

    def get_requirement_budget(self):
        return self._requirement_budget

    def get_requirement_quantity(self):
        return self._requirement_quantity

    def requirement_total_budget(self):
        return self._requirement_budget * self._requirement_quantity

    def set_requirement_name(self, requirement_name):
        if isinstance(requirement_name, str):
            self._requirement_name = requirement_name
        else:
            raise ValueError("RequirementName harus berupa string.")

    def set_requirement_budget(self, requirement_budget):
        if isinstance(requirement_budget, (int, float)):
            self._requirement_budget = requirement_budget
        else:
            raise ValueError("RequirementBudget harus berupa angka.")

    def set_requirement_quantity(self, requirement_quantity):
        if isinstance(requirement_quantity, int):
            self._requirement_quantity = requirement_quantity
        else:
            raise ValueError("RequirementQuantity harus berupa integer.")