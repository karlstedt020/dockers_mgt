FROM python
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN touch input.json
CMD [ "python", "./client.py" ]