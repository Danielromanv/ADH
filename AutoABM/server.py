from utilities import db, conf, agent
from utilities.mkauto import mk
from bottle import Bottle, run, static_file, request, redirect, template, default_app, response
from socket import gethostbyaddr, gethostbyname,error
from sys import argv
import os


app = default_app()
conf.check_file()

@app.route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root = os.getcwd()+'/views/')

@app.route('/dberror')
def dberror():
    return server_static('db.html')

@app.route('/')
def default():
    if(conf.check() == 0):
        return template("configerror")
    if(db.DB_check(db.dbhost) == 0):
        return redirect('/dberror')
    return template('index')

@app.post('/')
def do_default():
    if(db.DB_check(db.dbhost) == 0):
        return redirect('/dberror')
    host_name = str(request.forms.get('host_name')).strip()
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR')
    client_host='couldn\'t resolve ip'
    i = 1
    while ((client_host == 'couldn\'t resolve ip') and (i<=50)):
        i+= 1
        try:
            client_host = gethostbyaddr(client_ip)[0]
        except error:
            client_host = 'couldn\'t resolve hostname'
    print(client_host)
    if (client_ip == '127.0.0.1'):
        client_ip = gethostbyname(client_host)
    print("host name: " + host_name,"client_ip: "+ client_ip,"client_host: "+ client_host)
    if(host_name != ""):
        r = mk(host_name)
        if (r[1] == None):
            db.DB_add(db.hosts,host_name,client_host,client_ip)
        return template('response', Respuesta = r[0],response1=r[1],response2=r[2],response3=r[3])

@app.route('/config')
def config():
    return template('config', sections = conf.sections(),section='', selected = '',seccion='')

@app.post('/config')
def do_config():
    selected = request.forms.get('configuracion')
    print(selected)
    return template('config',sections = conf.sections(), section = 'Configuarcion de la sección '+selected+':',script='form_show()',seccion =selected ,selected = conf.info(selected))

@app.post('/saveconfig')
def do_saveconfig():
    sel = request.forms.get('seccion')
    print(sel)
    attrib = conf.info(sel)
    for i in attrib: conf.set(sel,i,request.forms.get(str(i)).strip())
    conf.save()
    return template('config', sections = conf.sections(), section='Se ha guardado la configuración',script ='', selected = '',seccion = '')

@app.route('/logs')
def logs():
    if(db.DB_check(db.dbhost) == 0):
        return redirect('/dberror')
    return template('logs', find = db.DB_find(db.hosts,''))

@app.post('/logs')
def do_logs():
    host_name = str(request.forms.get('host_name')).strip()
    return template('logs', find = db.DB_find(db.hosts,host_name))

@app.route('/agentes')
def agentes():
    if(conf.check() == 0):
        return template("configerror")
    return template('agentes',msj = "",msj2="")

@app.post('/agentes')
def do_agentes():
    host = str(request.forms.get('host_name')).strip()
    a = agent.check_agent(host)
    if(a == 1):
        t = agent.teln(host)
        if (len(t) == 0):
            return template('agentes',msj2="" ,msj = "El host "+ host +" no posee el agente")
        return template('agentes',msj2="" ,msj = "El host "+ host +" posee el agente de " + t["AgentOS"]+t["Version"])

    if(a == -1):
        return template('agentes',msj2="" ,msj = "El host "+ host +" no puede ser contactado, verificar nombre del mismo")
    return template('agentes',msj2="" ,msj = "El host "+ host +" no posee el agente")

@app.post('/agentesinstall')
def do_agentesinstall():
    print("la concha de la lora")
    host = str(request.forms.get('host_name3')).strip()
    user = str(request.forms.get('user')).strip()
    password = str(request.forms.get('password')).strip()
    a = agent.check_OS(host)
    print("estoy aca")
    if(a == 1):
        return template('agentes', msj = "",msj2="Windows")
    print("no es windows")
    if (a == 0):
        tel = len(agent.teln(host))
        if (tel != 0):
            return template('agentes', msj = "",msj2= "El agente ya se encontraba instalado")
        b = agent.distro(host,user,password)
        if(b == 1):
            print(1)
            a = agent.rpm_install(host,user,password)
            return template('agentes', msj = "",msj2= a)
        elif (b == -1):
            return template('agentes', msj = "",msj2= "Error al conectarse, revise las credenciales utilizadas")
        else:
            print(3)
            a= agent.deb_install(host,user,password)
            return template('agentes', msj = "",msj2= a)
    return template('agentes', msj = "",msj2="No se puede instalar")

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', server= "paste", port = 80)
    except KeyboardInterrupt:
        print("Stopping server")
