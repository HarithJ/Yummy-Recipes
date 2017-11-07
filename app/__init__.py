from flask import Flask

app = Flask(__name__, static_folder='../designs/UI', template_folder='../designs/UI')

 # Load the views
from app import views

# Load the config file
app.config.from_object('config')