from datetime import datetime, timedelta

class Catalog:
    def __init__(self):
        self.items = {
            1: {"name": "Item 1", "available": True, "on_hold": False, "hold_expires": None},
            2: {"name": "Item 2", "available": True, "on_hold": False, "hold_expires": None},
            # Add more items here...
        }

    def put_on_hold(self, item_id, hold_duration_days=1):
        if item_id in self.items:
            item = self.items[item_id]
            if item["available"] and not item["on_hold"]:
                item["on_hold"] = True
                item["hold_expires"] = datetime.now() + timedelta(days=hold_duration_days)
                print(f"Item {item_id} is now on hold until {item['hold_expires']}")
            else:
                print("Item is not available or already on hold.")
        else:
            print("Item not found in the catalog.")

    def release_hold(self, item_id):
        if item_id in self.items:
            item = self.items[item_id]
            if item["on_hold"]:
                item["on_hold"] = False
                item["hold_expires"] = None
                print(f"Hold released for Item {item_id}")
            else:
                print("Item is not on hold.")
        else:
            print("Item not found in the catalog.")

    def check_availability(self, item_id):
        if item_id in self.items:
            item = self.items[item_id]
            if item["on_hold"] and item["hold_expires"] > datetime.now():
                print(f"Item {item_id} is on hold until {item['hold_expires']}")
            elif item["available"] and not item["on_hold"]:
                print(f"Item {item_id} is available.")
            else:
                print(f"Item {item_id} is not available.")
        else:
            print("Item not found in the catalog.")

# Example usage:
catalog = Catalog()

catalog.put_on_hold(1, 3)  # Put Item 1 on hold for 3 days
catalog.check_availability(1)  # Check availability of Item 1
catalog.release_hold(1)  # Release hold on Item 1
catalog.check_availability(1)  # Check availability of Item 1 after release