from pathlib import Path
from rest_framework import serializers
from videos.models import Video


MAX_DESCRIPTION_LENGTH = 1000
MAX_FILE_MB = 500
ALLOWED_EXTS = {".mp4", ".mov", ".mkv", ".avi", ".webm"}
ALLOWED_CONTENT_TYPES = {
	"video/mp4",
	"video/quicktime",
	"video/x-matroska",
	"video/x-msvideo",
	"video/webm",
}

class VideoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Video
		fields = [
			"id",
			"title",
			"description",
			"file_original",
			"file_converted",
			"status",
			"views",
			"likes",
			"dislikes",
			"duration",
			"created_at",
			"slug",
		]
		read_only_fields = [
			"id",
			"file_converted",
			"status",
			"views",
			"likes",
			"dislikes",
			"duration",
			"created_at",
			"slug",
		]

	def validate_title(self, value: str) -> str:
		cleaned = value.strip()
		if not cleaned:
			raise serializers.ValidationError("Title cannot be empty.")
		if len(cleaned) > 120:
			raise serializers.ValidationError("Title cannot be longer than 120 characters.")
		return cleaned

	def validate_description(self, value: str | None) -> str | None:
		if value:
			if len(value) > MAX_DESCRIPTION_LENGTH:
				raise serializers.ValidationError(
					f"Description cannot be longer than {MAX_DESCRIPTION_LENGTH} characters."
				)
		return value

	def validate_file_original(self, file):
		if not file:
			raise serializers.ValidationError("Video file is required.")

		size_mb = file.size / (1024 * 1024)
		if size_mb > MAX_FILE_MB:
			raise serializers.ValidationError(f"File too large ({size_mb:.1f} MB). Max is {MAX_FILE_MB} MB.")


		ext = Path(getattr(file, "name", "")).suffix.lower()
		if ext not in ALLOWED_EXTS:
			allowed = ", ".join(sorted(ALLOWED_EXTS))
			raise serializers.ValidationError(f"Unsupported file extension '{ext}'. Allowed: {allowed}.")


		content_type = getattr(file, "content_type", None)
		if content_type and content_type not in ALLOWED_CONTENT_TYPES:
			allowed_ct = ", ".join(sorted(ALLOWED_CONTENT_TYPES))
			raise serializers.ValidationError(f"Unsupported content type '{content_type}'. Allowed: {allowed_ct}.")

		return file
