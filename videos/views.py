from rest_framework import viewsets, permissions, parsers

from videos.models import Video
from videos.serializer import VideoSerializer


class VideoViewSet(viewsets.ModelViewSet):
	queryset = Video.objects.all().order_by("-created_at")
	serializer_class = VideoSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
	parser_classes = (parsers.MultiPartParser, parsers.FormParser)
	
	def perform_create(self, serializer):
		serializer.save(author=self.request.user)
