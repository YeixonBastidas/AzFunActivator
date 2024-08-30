from dotenv import load_dotenv
import os

from app.common.constants import Constants

env_path = os.path.join(Constants.Microservice.PARENT_PATH, ".env")
load_dotenv(dotenv_path=env_path)

class Settings():
    # Odoo proccess queue
    ODOO_SERVICE_BASE_URL: str = os.getenv(
        Constants.OdooServices.ODOO_SERVICE_BASE_URL
    )
    # SSO
    URL_SSO: str = os.getenv(
        Constants.OdooServices.URL_SSO
    )
    USER_SSO: str = os.getenv(
        Constants.OdooServices.USER_SSO
    )
    PASSWORD_SSO: str = os.getenv(
        Constants.OdooServices.PASSWORD_SSO
    )


    # Database URL
    DATABASE_URL: str = None

   


class AllSettings():
    MS = Settings()


settings = AllSettings()
