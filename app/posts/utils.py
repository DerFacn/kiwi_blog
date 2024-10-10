import time

ALLOWED_EXTENSIONS = {"jpeg", "jpg", "png", "webp"}


def count_reading_time(words: str) -> int:
    return max(1, len(words) // 1300)  # By info from internet, this is avg. reading speed


def current_timestamp():
    yield int(time.time())


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def safe_filename(*args):
    if not args:
        return str(next(current_timestamp()))
    else:
        name = [arg for arg in args]
        name.append(str(next(current_timestamp())))
        return "_".join(name)
