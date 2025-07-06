def get_base64_image(image_path):
    import base64
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()
