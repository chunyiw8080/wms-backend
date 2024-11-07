from db.inventoryDB import InventoryDB
from db.historyDB import HistoryDB
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

now = datetime.now()
year_str = now.strftime("%Y")
month_str = now.strftime("%m")
year_month_str = year_str + month_str


def create_history_record():
    try:
        with InventoryDB() as i_db:
            data = i_db.show_inventories()
            cargo_ids = [item['cargo_id'] for item in data]
            records = []
            for cargo_id in cargo_ids:
                inv = i_db.get_inventory_by_id(cargo_id)
                record_data = {
                    'record_id': year_month_str + str(cargo_id),
                    'year': year_str,
                    'month': month_str,
                    'cargo_name': inv['cargo_name'],
                    'model': inv['model'],
                    'categories': inv['categories'],
                    'starting_price': inv['price'],
                    'starting_count': inv['count'],
                    'starting_total_price': inv['total_price']
                }
                records.append(record_data)

            with HistoryDB() as h_db:
                for record in records:
                    res = h_db.create_record(record)
    except Exception as e:
        print(e)


def update_history_record():
    with HistoryDB() as h_db:
        ids = h_db.get_history_id_by_date(year_str, month_str)
        for record_id in ids:
            cargo_id = record_id['id'][6:]
            with InventoryDB() as i_db:
                data = i_db.get_inventory_by_id(cargo_id)
                record = {
                    'closing_count': data['count'],
                    'closing_price': data['price'],
                    'closing_total_price': data['total_price'],
                }
            res = h_db.update_record(record_id['id'], record)
            if not res:
                print("Failed")


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(create_history_record, 'cron', day=1, hour=2, minute=0)
    scheduler.add_job(update_history_record, 'cron', day='last', hour=23, minute=0)
    scheduler.start()

# if __name__ == '__main__':
#     start_scheduler()