import datetime
import time

def sample_responses(input_text):
    user_message = str(input_text).lower()

    if user_message in ("hello", "hi", "sup"):
        return "Hey! How's it going?"
    
    if user_message in ("time", "time?"):
        ts = time.localtime()
        readable_ts_2 = time.strftime("%Y-%m-%d %H:%M:%S", ts)
        return str(readable_ts_2)
    
    return "I can't understand what you're saying Buddy!!"