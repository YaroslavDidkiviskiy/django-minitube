from rest_framework import viewsets, parsers

from videos.models import Video
from videos.permissions import IsOwnerOrAdminOrReadOnly
from videos.serializer import VideoSerializer, VideoListSerializer


class VideoViewSet(viewsets.ModelViewSet):
	queryset = Video.objects.all().order_by("-created_at")
	serializer_class = VideoSerializer
	parser_classes = (parsers.MultiPartParser, parsers.FormParser)
	permission_classes = (IsOwnerOrAdminOrReadOnly,)
	
	def get_serializer_class(self):
		if self.action == "list":
			return VideoListSerializer
	
		return VideoSerializer
	
	def perform_create(self, serializer):
		serializer.save(author=self.request.user)
