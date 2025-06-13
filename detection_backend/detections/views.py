from rest_framework.views import APIView
from rest_framework.response import Response
from .models import DetectionStats
from django.http import JsonResponse, StreamingHttpResponse
from rest_framework.decorators import api_view
from django.db.models import Sum, Count
from channels.layers import get_channel_layer
from django.views.generic import TemplateView
from asgiref.sync import async_to_sync
from django.forms.models import model_to_dict
from .orientation_project import scan_network, start_stream, gen_frames

people_count = 0
frames_count = 0
average_people = 0

@api_view(['POST'])

def video_feed(request):
    found, phone_ip, clients = scan_network()
    if not found:
        return JsonResponse({"Error: phone not found on network"}, status = 404)
    video_url = f"http://{phone_ip}:4747/video"
    cap, frame_queue = start_stream(video_url)

    if not cap:
        return JsonResponse({"Error: Could not open video stream"}, status = 404)
    
    return StreamingHttpResponse(gen_frames(frame_queue), content_type = 'multipart/x-mixed-replace; boundary=frame')

def detection_stats(request):
    global people_count, frames_count, average_people
    people = request.data.get('people')

    stats_box = DetectionStats.objects.create(
        detected_person = people['detected_person'],
        frame_processed = people['frame_processed']
    )

    if people['frame_processed']:
        frame_count += 1
        people_count += people['detected_person']

    average_people = (people_count / frames_count, 2) if frame_count else 0

    total_people_detected = DetectionStats.objects.aggregate(Sum('detected_person'))['detected_person__sum'] or 0
    total_frames_processed = DetectionStats.objects.filter(frame_count = True).count()
    average_people = (total_people_detected / total_frames_processed, 2) if total_frames_processed else 0

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "stats", {
            "type":"send_update",
            "stats_box": {
                "Total_People": total_people_detected,
                "Total_Frames": total_frames_processed,
                "Average_People": average_people,
                "Current_in_frame": people_count,
                "current_frame_count": frame_count,
                "average_people": average_people

            }
        }
    )
    
    return Response({"status": "okay"})

class AppView(TemplateView):
   template_name = 'index.html'


    