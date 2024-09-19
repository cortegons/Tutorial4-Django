from django.core.files.storage import default_storage
from django.http import HttpRequest
from.interfaces import ImageStorage  # Assuming ImageStorage is defined in an 'interfaces' module

class ImageLocalStorage(ImageStorage):
    def store(self, request: HttpRequest):
        # Retrieve the profile image from the uploaded files
        profile_image = request.FILES.get('profile_image', None)

        if profile_image:
            # Store the image in the default Django storage system
            file_name = default_storage.save('uploaded_images/' + profile_image.name, profile_image)
            # Return the URL of the stored image
            return default_storage.url(file_name)