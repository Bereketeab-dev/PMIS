import frappe
from frappe.model.document import Document
from frappe.utils import flt

class PaymentCertificateProgressItem(Document):
    def validate(self):
        self.calculate_item_amounts()

    def calculate_item_amounts(self):
        # 1. Cumulative Quantity
        self.cumulative_quantity_executed = flt(self.previous_quantity_executed) + flt(self.quantity_executed_this_period)

        # 2. Cumulative Value
        self.cumulative_value_of_work_done = flt(self.cumulative_quantity_executed) * flt(self.unit_rate)

        # 3. Value this period (can also be calculated as Qty this period * Rate)
        self.value_of_work_this_period = flt(self.quantity_executed_this_period) * flt(self.unit_rate)

        # 4. Quantity variance (Contract Qty - Cumulative Qty)
        self.quantity_variance = flt(self.contract_quantity) - flt(self.cumulative_quantity_executed)

        # 5. % Complete (Cumulative Qty / Contract Qty)
        if flt(self.contract_quantity) > 0:
            self.percent_complete = (flt(self.cumulative_quantity_executed) / flt(self.contract_quantity)) * 100
        else:
            self.percent_complete = 0
