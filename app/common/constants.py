from enum import StrEnum
import os


class Constants:
    class Microservice(StrEnum):
        PARENT_PATH = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..")
        )  

    class OdooServices(StrEnum):
        ODOO_SERVICE_BASE_URL = "ODOO_SERVICE_BASE_URL"
        ODOO_API_KEY = "ODOO_API_KEY"
        URL_SSO="URL_SSO"
        USER_SSO="USER_SSO"
        PASSWORD_SSO="PASSWORD_SSO"    

   
