import random
from datetime import datetime
from .models import Pipeline, SensorThickness, LABData, DCSData

def generate_process_anomaly():

    try:

        anomaly=None
        r=random.random()

        if r < 0.02:
            anomaly = "HIGH_SULFUR"
        elif r < 0.04:
            anomaly = "TEMP_SPIKE"
        elif r < 0.06:
            anomaly = "HIGH_ACIDITY"
        elif r < 0.08:
            anomaly = "HIGH_FLOW"
        elif r < 0.10:
            anomaly = "SENSOR_FAULT"

        return anomaly

    except Exception as e:

        print(f"Failed to generate anomaly : {e}")


def calculate_corrosion_rate(temp,sulfur,acidity,flow):

    try:

        base_rate = 0.002

        if temp > 450:
           base_rate += 0.01
        if sulfur > 3:
           base_rate += 0.008
        if acidity > 2:
           base_rate += 0.012
        if flow > 400:
           base_rate += 0.006

        return base_rate

    except Exception as e:

        print(f"Failed to calculate corrosion rate : {e}")


def generate_DCS_data():

    try:

        units=['CDU','Hydrocracker','Reformer']
        anomaly=generate_process_anomaly()

        for unit in units:

            temperature= random.uniform(250,450)
            pressure=random.uniform(10,80)
            flow_rate=random.uniform(100,400)

            if anomaly == "TEMP_SPIKE":
                temperature = random.uniform(450, 550)
                
            if anomaly == "HIGH_FLOW":
                flow_rate = random.uniform(400, 600)

            DCSData.objects.create(
                unit=unit,
                temperature=temperature,
                pressure=pressure,
                flow_rate=flow_rate
            )


    except Exception as e:

        print(f"Couldnt generate DCS data : {e}")



def generate_LAB_data():

    try:

        units=['CDU','Hydrocracker','Reformer']
        anomaly = generate_process_anomaly()

        for unit in units:

            sulfur=random.uniform(0.5,3.5)
            acidity=random.uniform(0.1,1.5)
            viscosity=random.uniform(5,20)

            if anomaly == "HIGH_SULFUR":
               sulfur = random.uniform(3.0, 5.0)

            if anomaly == "HIGH_ACIDITY":
               acidity = random.uniform(2.0, 4.0)

            LABData.objects.create(
                unit=unit,
                sulfur_content=sulfur,
                acidity=acidity,
                viscosity=viscosity
            )

    except Exception as e:

        print(f"Couldnt generate LAB data : {e}")


def generate_pipeline_thickness():

    try:

        pipelines=Pipeline.objects.all()

        latest_dcs = DCSData.objects.order_by("-timestamp").first()
        latest_lab = LABData.objects.order_by("-timestamp").first()

        if not latest_dcs or not latest_lab:
            return

        for pipe in pipelines:

            corrosion_rate = calculate_corrosion_rate(
                latest_dcs.temperature,
                latest_lab.sulfur_content,
                latest_lab.acidity,
                latest_dcs.flow_rate
            )

            last=SensorThickness.objects.filter(
                pipeline=pipe
            ).order_by("-timestamp").first()

            if last:
                new_thickness = last.thickness - corrosion_rate
            else:
                new_thickness = pipe.initial_thickness

            anomaly = generate_process_anomaly()

            # sensor fault simulation
            if anomaly == "SENSOR_FAULT":
                new_thickness += random.uniform(-0.5, 0.5)

            # prevent negative thickness
            new_thickness = max(new_thickness, 0)

            SensorThickness.objects.create(
                pipeline=pipe,
                thickness=new_thickness,
                anomaly_type=anomaly
            )

    except Exception as e:

        print(f"Couldnt generate thickness values : {e}")