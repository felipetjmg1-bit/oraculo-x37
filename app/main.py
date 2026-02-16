from flask import Flask
from app.api.routes import api_bp
from app.core.config import settings

def create_app():
    app = Flask(__name__)
    
    # Registrar Blueprints
    app.register_blueprint(api_bp, url_prefix=settings.API_V1_STR)
    
    # Rota raiz opcional para redirecionamento ou status simples
    @app.route('/')
    def index():
        return {
            "project": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "docs": f"{settings.API_V1_STR}/health"
        }

    return app

app = create_app()

if __name__ == '__main__':
    app.run(
        host=settings.HOST,
        port=settings.PORT,
        debug=settings.DEBUG
    )
