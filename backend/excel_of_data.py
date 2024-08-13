import logging
import csv
import pandas as pd

from backend.services.app_services import ApplicationServices

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Console handler for all logs
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)


class InsertDataIntoExcel:
    @staticmethod
    def admin_insert_data_excel(data, user_name, type_of_data):
        try:
            logger.info(f"Writing data for {user_name} in excel.")
            file_name = f"fetched_data/{type_of_data}.csv"
            df = pd.DataFrame(data)
            with open(file_name, "a+", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([i[0] for i in df])
                writer.writerows(df)

            df.to_csv(f'fetched_data/{type_of_data}.csv', index=False)
            logger.info(f"Data written to {file_name} for {user_name}.")

        except Exception as exception:
            logger.error(f"Error while inserting data in excel for"
                         f" {user_name}: {exception}")
            ApplicationServices.handle_exception(exception, True)
