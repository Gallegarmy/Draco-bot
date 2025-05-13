from datetime import datetime

def build_final_message(event_dict):
    start_date = event_dict["start_date"]
    start_date = datetime.combine(start_date, datetime.min.time())

    # datetime.strptime(start_date, '%Y;%m;%d').date()

    message=f'''
{event_dict["meeting_name"]} {event_dict["meeting_type"]}\n
{event_dict["meeting_description"]}\n
{start_date.strftime("%d/%m/%Y")}  {event_dict["start_time"]}\n
PARTICIPANTES (max {event_dict["max_players"]}):\n'''
    for user, num_guests in event_dict["players"].items():
        if num_guests > 0:
            message += f"-@{user} +{num_guests}\n"
        else:
            message += f"-@{user}\n"
    return message