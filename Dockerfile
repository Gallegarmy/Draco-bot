#We specify the python version the bot is gonna use
FROM python:3.9

#We copy every file inside the app directory
COPY . /app
#We define the app directory as the working directory 
WORKDIR /app
#We install the required libraries
RUN pip install -r requirements.txt


#We run the bot
CMD ["python","main.py"]

