FROM python:3.10

WORKDIR /app

# Expose port you want your app on
EXPOSE 8080

# Upgrade pip and install requirements
COPY requirements.txt requirements.txt
RUN pip install -U pip
RUN pip install -r requirements.txt

# Copy app code and set working directory
COPY streamlit_app.py streamlit_app.py
COPY generative.py generative.py
COPY prompts prompts
COPY .streamlit .streamlit
WORKDIR .

# Run
ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8080", "--server.address=0.0.0.0"]
