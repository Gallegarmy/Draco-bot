from datetime import datetime

def build_final_message(context):
    message=f'''
QUEDADA JUEGOMESEO {context.chat_data["status"]}\n
INICIO: {datetime.strptime(context.chat_data["start_date"], '%Y;%m;%d').date()}  {context.chat_data["start_time"]}\n
FIN: {datetime.strptime(context.chat_data["end_date"], '%Y;%m;%d').date()}  {context.chat_data["end_time"]}\n
PARTICIPANTES:\n'''
    for user in context.chat_data["joined"]:
            if user[1] == 0:
                message += f"-@{user[0]}\n"
            else:
                 message += f"-@{user[0]} +{user[1]}\n"
    return message