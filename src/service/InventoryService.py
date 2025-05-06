from src.shemas.MedicationInventory import *
from src.api.dependencies import DBDep
from datetime import datetime

class InventoryService:
    def __init__(self, db: DBDep):
        self.db = db
    
    async def check_and_order_medications(self, clinic_id: int):
        medications = await self.db.medInvent.get_filtred(clinic_id=clinic_id)
        for med in medications:
            if med.quantity < med.min_stock:
                order_quantity = med.min_stock * 2
                update_data = MedUpdate(
                    quantity=order_quantity,
                    last_ordered=datetime.now()
                )
                # med.quantity = order_quantity
                # med.last_ordered = datetime.now()
                await self.db.medInvent.edit(
                    update_data,
                    exclude_unset=True,
                    id=med.id
                )
                await self.db.commit()
        return 0

        