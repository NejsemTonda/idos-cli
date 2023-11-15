
def is_time(time):
    return len(time) > 3 and len(time) < 6 and ':' in time and time.replace(':', '').isdigit()
