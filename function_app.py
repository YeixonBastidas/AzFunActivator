import aiohttp
import azure.functions as func
import logging
from logyca import APIResultDTO 

from pydantic import ValidationError

from app.common.rvc_product import products_colabora_vtex
from app.schemes.Input.orders_dto import DigitalCard_InputDTO, Order_InputDTO
from app.schemes.output.postulation_rvc import DigitalCardDTO, PostulationDTO

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="AZFuncActivator")
async def AZFuncActivator(req: func.HttpRequest) -> func.HttpResponse:
    headers = {
        'Authorization': 'Bearer {0}'.format('eyJhbGciOiJSUzI1NiIsImtpZCI6Ilg1ZVhrNHh5b2pORnVtMWtsMll0djhkbE5QNC1jNTdkTzZRR1RWQndhTmsiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiJhMjg3MjI4Zi1lY2JmLTQwNmMtOGE5Zi0zYjFlNDEwN2QzMGEiLCJpc3MiOiJodHRwczovL3Nzb2xvZ3ljYWRldi5iMmNsb2dpbi5jb20vZTNiZTIyZTEtMThkZi00YTFhLTg4ZGUtNDcxNzc5ZTA0MDBhL3YyLjAvIiwiZXhwIjoxNzI1MDU4NTAxLCJuYmYiOjE3MjUwNTQ5MDEsImlkcCI6IkxvY2FsQWNjb3VudCIsInN1YiI6IjMzNTFkZTI5LWU1NmEtNDcxZC1hMjdkLTQxZDgyODQ5M2U1YSIsIm5hbWUiOiJZZWl4b24gQmFzdGlkYXMiLCJuZXdVc2VyIjpmYWxzZSwiZXh0ZW5zaW9uX0FwcF9BbmFsaXRpY2EiOnRydWUsImV4dGVuc2lvbl9BcHBfQ29sYWJvcmEiOnRydWUsImVtYWlscyI6WyJ5ZWlzb24uYi5iQGhvdG1haWwuY29tIl0sInRmcCI6IkIyQ18xX2xvZ2lucm9wYyIsImF6cCI6ImEyODcyMjhmLWVjYmYtNDA2Yy04YTlmLTNiMWU0MTA3ZDMwYSIsInZlciI6IjEuMCIsImlhdCI6MTcyNTA1NDkwMX0.gWc8kqjrwxxS9cliGn0kpoMzWVtnCKzUvd-n_zQzLJzejV5qyqYkydfZrTsqpX9vAZv-XTdkel0OtXBNvdYT_ZJLFDNsrK5q2-O2Hz8hwp5aHeLlAb8aP7nX8Y7_JdHCWGLsC-WBfM8uupyV2lYrQV54FgYTVdUJ2tOHGyvGvIerM1SKazoNnIerIO_YeMUvuDkSb4pf_C3gO87FsP4ZYBKPtrHXuc1Bw6ZSWdFksGLsuSWwwqk28IekWEBQbttjyESwDMorhtmwDaw0AGJIlVWw3gnLY7Uew7g-v_uqiI2G8qmF4s62fZ88ppx_MBViKE1r5K_sxXD5u2w7yDSYvw')                    
    }
    try:
        order = Order_InputDTO(**req.get_json()) 
    except ValidationError as e:         
        return func.HttpResponse(body= str(e), status_code=400)          
    if order.Sponsor: # SI: primero preguntar si es RVC o mi postulacion va a ser RVC; Si lo es entonces postular
        get_id_product = await get_product_by_sku(order.OrdenDetalles[0].Sku, headers)

        if get_id_product.dataError:
            return APIResultDTO(dataError=True, resultMessage= "El SKU enviado no se encontró en el sistema.")
     
        get_product_id = products_colabora_vtex(get_id_product.resultObject[0]['x_code_type'])
        new_postulation = map_postulation(order, get_product_id)
       
        rvc_url = "https://gateway-odoo-dev-f4bzemcnbvghgxb2.eastus-01.azurewebsites.net/gateway/add_postulation"            
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(rvc_url, json=new_postulation.model_dump()) as response:
                json_body = await response.json()            
    else:
        # NO: entonces seria compra de producto
        pass

        

         


        # Publicar mensaje de Activacion de productos en plataformas       
          
   


async def get_product_by_sku(sku: int, headers: dict):    
    rvc_url = "https://app-msquery-dev-hzcqe4egf8cpf4bx.eastus-01.azurewebsites.net/api/products/by_id?product_id={}".format(sku)            
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(rvc_url) as response:
                json_body = await response.json()  
    if response.status == 200:
        return APIResultDTO(**json_body)
    else: 
        return APIResultDTO(dataError=True, resultMessage= "Error no controlado")

def map_digital_card(digital_card: DigitalCard_InputDTO) -> DigitalCardDTO:
    return DigitalCardDTO(
        contact_name=digital_card.name,
        contact_email=digital_card.email,
        contact_mobile=digital_card.phone,
        offered_service_id=0,  # Placeholder value, replace with actual mapping logic
        city_id=0,  # Placeholder value, replace with actual mapping logic
        street=digital_card.address,
        url_website=digital_card.website,
        url_facebook=digital_card.facebook,
        url_instagram=digital_card.instagram,
        postulation_id=None
    )
 
def map_postulation(order: Order_InputDTO, product_id: int) -> PostulationDTO:
    digital_cards = [map_digital_card(dc) for dc in order.Digital_cards] if order.Digital_cards else []
    return PostulationDTO(
        nit_beneficiary = order.Nit,
        nit_sponsor = order.Sponsor if order.Sponsor else None,
        product_rvc = product_id,
        codes_quantity = order.OrdenDetalles[0].Cantidad, # ???????
        origin="TV",
        contact_email = order.EmailTeleventas,
        glns_codes_quantity = None, # ?????????????????????
        invoice_codes_quantity = None, # ?????????????????????
        colabora_level = 0, # de debe cambiar cuando se implemente colabora
        digital_card_ids = digital_cards,
        crecemype_theme = None
    )
    
  
        