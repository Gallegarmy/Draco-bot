

def build_message(joined):
    message='''
QUEDADA JUEGOMESEO\n
INICIO: 19:30\n
FIN: 23:00\n
PARTICIPANTES:\n'''
    for user_id, info in joined.items():
        name = info["name"]
        guests = info["guests"]
        if guests > 0:
            message += f"-@{name} (+{guests})\n"
        else:
            message += f"-@{name}\n"
    return message