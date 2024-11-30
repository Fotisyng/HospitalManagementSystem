from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Nurse

class AssignSupervisionNursesView(APIView):
    def post(self, request, *args, **kwargs):
        """
        The post request to assign the supervising nurse to the given nurse(s). If the supervise nurses
        list contains a charge nurse, only a "chief" nurse can supervise charge nurses.

        Args:
            request: The HTTP request containing the data.
            *args: Variable positional arguments.
            **kwargs: Variable keyword arguments.

        Returns:
            Response: A response containing the success or error message.
        """
        supervisor_nurse_id = request.data.get('supervisor_nurse_id')
        nurse_ids = request.data.get('nurse_ids')

        try:
            supervisor_nurse = Nurse.objects.get(id=supervisor_nurse_id)
            supervisee_nurses = Nurse.objects.filter(id__in=nurse_ids)
            charge_nurses = supervisee_nurses.filter(role='charge')

            if charge_nurses.exists() and supervisor_nurse.role != 'chief':
                return Response(
                    {'error': 'Only a chief nurse can supervise charge nurses.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            for supervisee in supervisee_nurses:
                supervisee.supervisor_nurses.add(supervisor_nurse)

            return Response({'message': 'Nurse supervision assigned successfully!'}, status=status.HTTP_200_OK)
        except Nurse.DoesNotExist:
            return Response({'error': 'Supervisor nurse not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)