import schedule
import time
from main import run_pipeline

# Run the pipeline every 1 hour
schedule.every(1).hours.do(run_pipeline)

while True:
    schedule.run_pending()
    time.sleep(60)
