
from rest_framework.response import Response

from rest_framework.decorators import api_view, permission_classes



from push_notifications.models import GCMDevice



@api_view(['POST'])
@permission_classes(())
def test_func(request):
    user=request.user
    device = GCMDevice.objects.get(user=user)
    device.send_message("You've got mail")
    return Response("ok")
