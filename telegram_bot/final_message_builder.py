

def build_final_message(joined,data):
    message=f'''
QUEDADA JUEGOMESEO {data["status"]}\n
INICIO: {data["start"]}\n
FIN: {data["end"]}\n
PARTICIPANTES:\n'''
    for user_id, info in joined.items():
        name = info["name"]
        guests = info["guests"]
        if guests > 0:
            message += f"-@{name} (+{guests})\n"
        else:
            message += f"-@{name}\n"
    return message