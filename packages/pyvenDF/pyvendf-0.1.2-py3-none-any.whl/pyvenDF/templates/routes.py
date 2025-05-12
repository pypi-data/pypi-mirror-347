# pyvenDF/templates/routes.py

from pyvenDF.templates.views import blog_view, profile_view

routes = [
    {"pattern": "/blog.[id]", "handler": blog_view},
    {"pattern": "/profile.[id]", "handler": profile_view},
]
