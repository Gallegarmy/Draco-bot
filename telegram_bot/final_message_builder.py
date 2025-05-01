from datetime import datetime

def build_final_message(event_dict):
    start_date = event_dict["start_date"]
    start_date = datetime.combine(start_date, datetime.min.time())

    # datetime.strptime(start_date, '%Y;%m;%d').date()

    message=f'''
QUEDADA JUEGOMESEO {event_dict["meeting_type"]}\n
INICIO: {start_date.strftime("%d/%m/%Y")}  {event_dict["start_time"]}\n
PARTICIPANTES:\n'''
    for user, num_guests in event_dict["players"].items():
        if num_guests > 0:
            message += f"-@{user} +{num_guests}\n"
        else:
            message += f"-@{user}\n"
    return message