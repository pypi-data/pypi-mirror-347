# pyvenDF/templates/routes.py

from pyvenDF.templates.views import welcome_view  # Importing the view function for the welcome page

routes = [
    {"pattern": "/", "handler": welcome_view}  # Default route to show the welcome page
]
