FROM python:3.9-slim

# Allow service to handle stops gracefully
STOPSIGNAL SIGQUIT

# Install pipenv
RUN pip install pipenv

# Install dependencies
COPY Pipfile* ./
RUN pipenv lock
RUN pipenv install --system

COPY manage.py ./

# Start the server
CMD ["gunicorn", "--preload", "-b", "0.0.0.0:8020", "project.wsgi:application", "--threads", "8", "-w", "4"]