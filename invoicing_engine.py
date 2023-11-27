''' Pruebas de Invoicing Engine '''
import requests
import time
import json
import os

token = ""

''' Get a new/fresh token '''
def GetToken(token):
    url = "https://identity.primaverabss.com/connect/token"

    payload = 'grant_type=client_credentials&client_id=IE-249792-0002&scope=application%20lithium-ies%20lithium-ies-wh&client_secret=68645012-8dd9-4fff-8af8-b59b9d560e39'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': f'Bearer {token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload, timeout=30)

    return response.json()["access_token"]

def GetMemos(token):
    url = "https://invoicing-engine.primaverabss.com/api/249792/249792-0002/billing/memos/odata?$select=Company, NaturalKey, PostingDate, BuyerCustomerParty, BuyerCustomerPartyName, Currency, Id&$filter=IsActive eq true and (length('PRIAT') eq 0 or  Company eq 'PRIAT')&$inlinecount=allpages&$orderby=PostingDate"

    headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
    }

    return requests.get(url, headers=headers, timeout=30).json()

def GetInvoices(token, top):
    url = f"https://invoicing-engine.primaverabss.com/api/249792/249792-0002/billing/invoices/odata?$select=Company, NaturalKey, PostingDate, BuyerCustomerParty, BuyerCustomerPartyName, Currency, Id&$filter=IsActive eq true and (length('PRIAT') eq 0 or  Company eq 'PRIAT')&$inlinecount=allpages&$orderby=PostingDate&$top={top}"

    headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
    }

    return requests.get(url, headers=headers, timeout=30).json()


def printOriginal(id, naturalKey, template, signDocument=False):
    url = f"https://invoicing-engine.primaverabss.com/api/249792/249792-0002/billing/invoices/{id}/printOriginal?template={template}&signDocument={'true' if signDocument else 'false'}"
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}'
    }

    print(f"Printing original {naturalKey} (signDocument={'true' if signDocument else 'false'})...")
    start = time.time()
    requests.get(url, headers=headers, timeout=30)
    end = time.time()
    print(f"Printed {naturalKey}!!!\n{end - start} seconds elapsed...")

def CreateInvoices(numFacturas, requestPrintAsync, signDocument):
    url = "https://invoicing-engine.primaverabss.com/api/249792/249792-0002/billing/invoices/"

    facturas = []

    payload = json.dumps({
    "company": "PRIAT",
    "buyerCustomerParty": "0001",
    "documentType": "FRD",
    "documentDate": "2023-11-17",
    "discountInValueAmount": {
        "amount": 10
    },
    "documentLines": [
        {
        "description": "Batata",
        "salesItem": "BATATAFRITA",
        "unitPrice": {
            "amount": 10000
        },
        "quantity": 2,
        "OrderReferences": "GR.2021.125",
        "OrderReference": "GR.2021.125",
        "customerOrderId": "GR.2021.125",
        "customerOrderLine": 1
        }
    ],
    "Remarks": "O meu comentário (OCULTO/INTERNO)",
    "NoteToRecipient": "Nota ao destinatário (VISÍVEL)"
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}'
    }

    locations = []

    for i in range(numFacturas):

        print(f'A criar fatura {i + 1}...')

        response = requests.post(url, headers=headers, data=payload, timeout=30)

        print(f'Fatura {i + 1} criada ({response.text})')

        facturas.append(response.json())

        if requestPrintAsync:
        
            # Estratégia #1:
            
            # Lançar o pedido de impressão assíncrona após a criação de cada documento:
            locations.append(printOriginalAsync(response.json(), response.json(), "BILLING_SERVICESINVOICEREPORT_PRIAT", signDocument))

    return locations, facturas

def printOriginalAsync(id, naturalKey, template, signDocument=False):
    url = f"https://invoicing-engine.primaverabss.com/api/249792/249792-0002/billing/invoices/{id}/printOriginalAsync?template={template}&signDocument={'true' if signDocument else 'false'}"
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}'
    }
    print(f"Printing Async Original {naturalKey} (signDocument={'true' if signDocument else 'false'})...")
    # start = time.time()
    response = requests.get(url, headers=headers, timeout=30)
    location = response.headers.get("Location")
    # end = time.time()
    # print(f'Location: {location}!!!\n{end - start} seconds elapsed...')
    return location

def GetPDFFromLocation(location):
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    retry = 0

    response = requests.get(location, headers=headers, timeout=30) 

    while response.status_code != 200:
        time.sleep(0.1)
        retry+=1
        print (f'Erro: {response.status_code}')
        print (f'Retry {retry}')

        response = requests.get(location, headers=headers, timeout=30) 

    return response.content

def SavePDFFile(content):
    file_extension = 'pdf'
    file_name = 'temp-' +  str(time.time()) + '.' + file_extension
    file_path = os.path.join(os.getcwd(), file_name)
    print(file_path)
    with open(file_path, 'wb') as f:
        f.write(content)

def GetPDFFromAllLocations(locations):

    print("Começamos a ir buscar os PDF às locations (repositório)...")

    for location in locations:
        
        content = GetPDFFromLocation(location)
        SavePDFFile(content)

if __name__ == '__main__':
    
    token = GetToken(token)

    # memos = GetMemos(token)

    # for memo in memos["items"]:
    #     naturalKey = memo["naturalKey"]
    #     customerName = memo["buyerCustomerPartyName"]
    #     print(f"{naturalKey} ({customerName}\n")

    # num_documentos = 1

    # invoices = GetInvoices(token, num_documentos)

    # signDocument = False

    # for invoice in invoices["items"]:
    #     naturalKey = invoice["naturalKey"]
    #     customerName = invoice["buyerCustomerPartyName"]
    #     id = invoice["id"]
    #     printOriginal(id, naturalKey, "BILLING_SERVICESINVOICEREPORT_PRIAT", signDocument)
        

    # signDocument = True
    
    # for invoice in invoices["items"]:
    #     naturalKey = invoice["naturalKey"]
    #     customerName = invoice["buyerCustomerPartyName"]
    #     id = invoice["id"]
    #     printOriginal(id, naturalKey, "BILLING_SERVICESINVOICEREPORT_PRIAT", signDocument)

    # locations = []

    # for invoice in invoices["items"]:
    #     naturalKey = invoice["naturalKey"]
    #     id = invoice["id"]
    #     locations.append(printOriginalAsync(id, naturalKey, "BILLING_SERVICESINVOICEREPORT_PRIAT", signDocument))

    num_documentos = 5

    locations = []

    signDocument = True

    # INÍCIO - Estratégia #1:

    # Lançar o pedido de impressão assincrona na criação de cada documento:

    locations, invoices_created = CreateInvoices(num_documentos, requestPrintAsync=True, signDocument=signDocument)

    # start = time.time()

    # FIM - Estratégia #1:

    # INÍCIO - Estratégia #2:
    
    # Lançar o pedido de impressão assíncrona após a criação de todos os documentos:

    locations, invoices_created = CreateInvoices(num_documentos, requestPrintAsync=False, signDocument=signDocument)

    start = time.time()

    for invoice in invoices_created:
        locations.append(printOriginalAsync(invoice, invoice, "BILLING_SERVICESINVOICEREPORT_PRIAT", signDocument))

    # FIM - Estratégia #2:

    GetPDFFromAllLocations(locations)

    end = time.time()
    
    print(f'Printed {num_documentos} documents. Time elapsed: {end - start} seconds...')