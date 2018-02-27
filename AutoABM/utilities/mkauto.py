import socket
import check_mk_web_api as mka
import utilities.conf

utilities.conf.check_file()

config = utilities.conf.info("check_mk")
folder = config["folder"]
user = config['user']
password = config['password']
url = config['url']

def mk(host,folder = folder):
    exist=''
    try:
        ipaddress = socket.gethostbyname(host)
    except:
        return ['El host '+ host +' no se ha podido agregar, ya que no se puede conectar por la red','','','']
    api = mka.WebApi(url, username=user, secret=password)
    try:
        a = api.add_host(host,folder=folder, tags={"tag_agent":"cmk-agent"})
        print(a)
    except mka.CheckMkWebApiException as ea:
        a=ea
        exist = a
        print("excepcion",a)
    try:
        b = api.discover_services(host)
        print(b)
    except mka.CheckMkWebApiException as ed:
        b=ed
        print(b)
        if  'Cannot get data from' in str(ed):
            try:
                a = api.edit_host(host, ipaddress = ipaddress)
                print(a)
            except mka.CheckMkWebApiException as ea:
                a=ea
                print(a)
            try:
                b = api.discover_services(host)
                print(b)
            except mka.CheckMkWebApiException as ed:
                b=ed
                print(b)
    try:
        c = api.activate_changes(allow_foreign_changes=True)
        print(c)
    except mka.CheckMkWebApiException as eac:
        c=eac
        print(c)
    print(b)
    if "already exists in the folder" in str(a) or "already exists in the folder" in str(exist):
        if "request timed out" in str(b):
            return ["El host "+ host +" ya existía en la carpeta, no se ha podido realizado un rediscover de los servicios",a,b,c]
        return ["El host "+ host +" ya existía en la carpeta, se ha realizado un rediscover de los servicios",a,b,c]
    elif ("Cannot get data from TCP" in str(b) and "{'sites': {}}" == str(c)):
        return ["El host "+ host +" se ha agregado/editado, y no se ha podido realizado un discover de los servicios, ni activar los cambios",a,b,c]
    elif "Check_MK exception" in str(b):
        return ["El host "+ host +" se ha agregado/editado, y no se ha podido realizado un discover de los servicios, verificar si el host posee el agente",a,b,c]
    return ["El host "+ host +" ha sido agregado exitosamente",a,b,c]
#mk("g500603ntkae")
#mk("g500603sv811")
