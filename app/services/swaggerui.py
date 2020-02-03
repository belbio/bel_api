from falcon_swagger_ui import StaticSinkAdapter, register_swaggerui_app

# Add Swagger docs
SCHEMA_URL = "/swagger"
SWAGGERUI_URL = "/swaggerui"  # without trailing '/'


def register_swaggerui(app):
    # Register Swagger
    # api.add_sink(StaticSinkAdapter('./swagger.json'), SCHEMA_URL)

    page_title = "BEL API Swagger"  # defaults to Swagger UI
    register_swaggerui_app(
        app,
        SWAGGERUI_URL,
        SCHEMA_URL,
        page_title=page_title,
        config={"supportedSubmitMethods": ["get"]},
    )
