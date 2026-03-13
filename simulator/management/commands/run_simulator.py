from django.core.management.base import BaseCommand
import time
from simulator.simulator import (
    generate_DCS_data,
    generate_LAB_data,
    generate_pipeline_thickness
)
class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        try:

            minute_counter = 0

            while True:

                generate_DCS_data()

                if minute_counter % 5 == 0:
                    generate_LAB_data()

                if minute_counter % 30 == 0:
                    generate_pipeline_thickness()

                print("Synthetic data generated")
                time.sleep(60)
                minute_counter += 1


        except Exception as e:

            print(f"couldnt run the simulator: {e}")

