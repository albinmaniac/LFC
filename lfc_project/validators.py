from django.core.exceptions import ValidationError
import os


def validate_image(file):

    if not file:
        return

    # Existing Cloudinary files are stored without an extension in the
    # public_id (e.g. gallery/albums/CR7_rgu63k). Skip extension validation
    # for already-saved files.
    if not getattr(file, "_file", None):
        return

    allowed_extensions = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
    }

    extension = os.path.splitext(file.name)[1].lower()

    if extension not in allowed_extensions:
        raise ValidationError(
            "Only JPG, JPEG, PNG and WEBP files are allowed."
        )

    file_size = getattr(file, "size", None)

    if file_size is not None and file_size > 5 * 1024 * 1024:
        raise ValidationError(
            "Image size cannot exceed 5 MB."
        )


def validate_document(file):

    if not file:

        return

    allowed_extensions = {

        ".pdf",

        ".doc",

        ".docx",

        ".jpg",

        ".jpeg",

        ".png",

        ".avif",

    }

    extension = os.path.splitext(file.name)[1].lower()

    if extension not in allowed_extensions:

        raise ValidationError(

            "Invalid file type."

        )

    file_size = getattr(file, "size", None)

    if file_size is not None and file_size > 10 * 1024 * 1024:

        raise ValidationError(

            "File size cannot exceed 10 MB."

        )
    
    