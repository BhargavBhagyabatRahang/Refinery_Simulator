from django.shortcuts import render
from django.http import JsonResponse
from .models import SensorThickness, DCSData, LABData

def simulator_UI(request):
    return render(request,"Simulator_UI.html")

def latest_thickness(request):
    try:
        data = list(
            SensorThickness.objects.values(
                "pipeline__name",
                "thickness",
                "anomaly_type",
                "timestamp"
            ).order_by("-timestamp")[:20]
        )
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def latest_DCS(request):
    try:
        data = list(
            DCSData.objects.values(
                "unit",
                "temperature",
                "pressure",
                "flow_rate",
                "timestamp"
            ).order_by("-timestamp")[:20]
        )
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def latest_LAB(request):
    try:
        data = list(
            LABData.objects.values(
                "unit",
                "sulfur_content",
                "acidity",
                "viscosity",
                "timestamp"
            ).order_by("-timestamp")[:20]
        )
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)