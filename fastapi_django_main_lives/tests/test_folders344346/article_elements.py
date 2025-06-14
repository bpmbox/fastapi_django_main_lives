# Article elements
def insert_title(title):
    """
    Insert title
    """
    return f"<h1>{title}</h1>"

def insert_thumbnail(thumbnail):
    """
    Insert thumbnail
    """
    return f"<img src='{thumbnail}' />"

def insert_image_file(image_file):
    """
    Insert image file
    """
    return f"<img src='{image_file}' />"

def insert_content(content):
    """
    Insert content
    """
    return f"<p>{content}</p>"