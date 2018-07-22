from falcon_swagger_ui import register_swaggerui_app
from falcon_swagger_ui import StaticSinkAdapter

# Add Swagger docs
SCHEMA_URL = '/swagger'
SWAGGERUI_URL = '/swaggerui'  # without trailing '/'


def register_swaggerui(api):
    # Register Swagger
    # api.add_sink(StaticSinkAdapter('./swagger.json'), SCHEMA_URL)

    page_title = 'BEL API Swagger'  # defaults to Swagger UI
    register_swaggerui_app(
        api,
        SWAGGERUI_URL,
        SCHEMA_URL,
        page_title=page_title,
        config={'supportedSubmitMethods': ['get'], }
    )



