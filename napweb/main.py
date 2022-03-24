from flask_assets import Environment
from webassets import Bundle

from .app import app

# Side effect: register routes
# noinspection PyUnresolvedReferences
from napweb import routes

app.jinja_options["autoescape"] = lambda _: True
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

assets = Environment(app)
# js = Bundle(...,
#             filters='jsmin', output='static/js/main.min.js')
# assets.register('js_all', js)

sass = Bundle('sass/main.scss', filters='libsass', output='css/sass.css')
all_css = Bundle(sass, filters='rcssmin', output="css/main.min.css")
assets.register('css_all', all_css)
