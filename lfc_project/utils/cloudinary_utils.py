from cloudinary.uploader import destroy


def get_public_id(file_field):
    """
    Return the Cloudinary public_id stored by django-cloudinary-storage.
    """
    if not file_field:
        return None

    name = getattr(file_field, "name", "")

    if not name:
        return None

    return name


def delete_cloudinary_file(file_field):
    """
    Delete a Cloudinary asset.
    """
    public_id = get_public_id(file_field)

    if not public_id:
        return False

    try:
        result = destroy(public_id, invalidate=True, resource_type="image")
        return result.get("result") in {"ok", "not found"}
    except Exception:
        return False


def delete_cloudinary_files(*file_fields):
    """
    Delete multiple Cloudinary assets.
    """
    return all(delete_cloudinary_file(file_field) for file_field in file_fields)