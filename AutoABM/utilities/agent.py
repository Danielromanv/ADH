import nmap
import socket
import pexpect
import telnetlib
import pexpect
from pexpect import pxssh
import getpass
import utilities.conf
#yum install xinetd -C -y
#rpm install -U check_agent.rpm
#service xinetd restart
#copiar logwatch
#/usr/lib/check_mk/plugins    logwatch
#/etc/check_mk/   logwatch conf

rpm = utilities.conf.info("agentes")["rpm"]
deb = utilities.conf.info("agentes")["deb"]
win = utilities.conf.info("agentes")["win"]
lplugin = utilities.conf.info("logwatch")["plugin"]
lcfg = utilities.conf.info("logwatch")["cfg"]

def distro(host,user,passw):
    hostname = host
    username = user
    password = passw
    s = pxssh.pxssh()
    s.force_password = True
    try:
        s.login(hostname, username, password)
    except:
        print("auxilio")
        return(-1)
    s.sendline('dpkg')
    s.prompt()
    print("auxilio2")
    a = s.before.decode("utf-8")
    if("not found" in a.lower()):
        s.logout()
        return 1
    else:
        s.logout()
        return 0

def rpm_install(host,user,passw):
    log = list()
    try:
        if(len(teln(host)) != 0):
            return('El agente ya se encontraba instalado')
        s = pxssh.pxssh()
        s.force_password = True
        hostname = host
        username = user
        password = passw
        s.login(hostname, username, password)
        s.sendline('whoami')
        log.append("command: whoami")
        s.prompt(timeout = 5)
        log.append(s.before.decode("utf-8"))
        if (log[-1] != "root"):
            s.sendline('sudo su')
            log.append("command: sudo su")
            s.prompt(timeout = 3)
            log.append(s.before.decode("utf-8"))
            if ("passw" in log[-1].lower()):
                s.sendline(passw)
                s.prompt(timeout = 3)
                if ("passw" in s.before.decode("utf-8").lower()):
                    print("credenciales con insuficientes privilegios")
                    s.logout()
                    return("error, credenciales con insuficientes privilegios")
        s.sendline('yum install xinetd -y')
        log.append("command: yum install xinetd -y")
        s.prompt(timeout = 10)
        log.append(s.before.decode("utf-8"))
        s.sendline('rpm -i '+rpm)
        log.append("command: rpm -i "+rpm)
        s.prompt(timeout = 10)
        log.append(s.before.decode("utf-8"))
        s.sendline('service xinetd restart')
        log.append("command: service xinetd restart")
        s.prompt(timeout = 3)
        log.append(s.before.decode("utf-8"))
        s.sendline("if [ ! -f /usr/lib/check_mk/plugins/mk_logwatch ]; then wget "+lplugin+" -P /usr/lib/check_mk/plugins; fi")
        log.append("command: wget "+lplugin+" -P /usr/lib/check_mk/plugins")
        s.prompt(timeout = 5)
        log.append(s.before.decode("utf-8"))
        s.sendline("if [ ! -f /etc/check_mk/logwatch.cfg ]; then wget "+lcfg+" -P /etc/check_mk/; fi")
        log.append("command: wget "+lcfg+" -P /etc/check_mk/")
        s.prompt(timeout = 5)
        log.append(s.before.decode("utf-8"))
        s.sendline('netstat -tlpn | grep xinetd')
        s.prompt()
        log.append(s.before.decode("utf-8"))
        s.sendline('exit')
        s.prompt(timeout = 3)
        print("exit")
        return(log)
    except Exception as e:
        print(e)
        print("pxssh failed on login.")
        return("falló el login, revise las credenciales usadas")

#copiar logwatch
#/usr/lib/check_mk/plugins    logwatch
#/etc/check_mk/   logwatch conf

def deb_install(host,user,passw):
    log = list()
    try:
        if(len(teln(host)) != 0):
            return('El agente ya se encontraba instalado')
        s = pxssh.pxssh()
        s.force_password = True
        hostname = host
        username = user
        password = passw
        s.login(hostname, username, password)
        s.sendline('whoami')
        log.append("command: whoami")
        s.prompt(timeout = 5)
        log.append(s.before.decode("utf-8"))
        s.prompt()
        if (s.before.decode("utf-8") != "root"):
            s.sendline('sudo su')
            log.append("command: sudo su")
            s.prompt(timeout = 3)
            log.append(s.before.decode("utf-8"))
            if ("passw" in s.before.decode("utf-8").lower()):
                s.sendline(passw)
                s.prompt(timeout = 3)
                if ("root" not in s.before.decode("utf-8")):
                    print("credenciales con insuficientes privilegios")
                    s.logout()
                    return("error, credenciales con insuficientes privilegios")
        s.sendline('apt install xinetd ')
        log.append('command: apt install xinetd ')
        s.prompt(timeout = 10)
        log.append(s.before.decode("utf-8"))
        s.sendline('wget --output-document check_mk_agent.deb '+deb)
        log.append('command: wget --output-document check_mk_agent.deb '+deb)
        s.prompt(timeout = 10)
        log.append(s.before.decode("utf-8"))
        s.sendline('dpkg -i check_mk_agent.deb')
        log.append('command: dpkg -i check_mk_agent.deb')
        s.prompt(timeout = 3)
        log.append(s.before.decode("utf-8"))
        s.sendline('rm check_mk_agent.deb')
        log.append('command: rm check_mk_agent.deb')
        s.prompt(timeout = 5)
        log.append(s.before.decode("utf-8"))
        s.sendline('service xinetd restart')
        log.append('command: service xinetd restart')
        s.prompt(timeout = 5)
        log.append(s.before.decode("utf-8"))
        s.sendline("if [ ! -f /usr/lib/check_mk/plugin/mk_logwatch ]; then wget "+lplugin+" -P /usr/lib/check_mk/plugins; fi")
        log.append("command: wget "+lplugin+" -P /usr/lib/check_mk/plugins")
        s.prompt(timeout = 5)
        log.append(s.before.decode("utf-8"))
        s.sendline("if [ ! -f /etc/check_mk/logwatch.cfg ]; then wget "+lcfg+" -P /etc/check_mk/; fi")
        log.append("command: wget "+lcfg+" -P /etc/check_mk/")
        s.prompt(timeout = 5)
        log.append(s.before.decode("utf-8"))
        s.sendline('netstat -tlpn | grep xinetd')
        s.prompt(timeout = 3)
        log.append(s.before.decode("utf-8"))
        s.sendline('exit')
        s.prompt(timeout = 3)
        s.logout()
        return(log)
    except Exception as e:
        print(e)
        print("pxssh failed on login.")
        return("falló el login")

def teln(host):
    d={}
    tn = telnetlib.Telnet()
    tel = list()
    try:
        tn.open(host,port = 6556,timeout = 5)
    except:
        return(d)
    try:
        linea = tn.read_until(b'\n').decode('utf-8').strip()
    except EOFError:
        return d
    while 'Hostname' not in linea:
        linea = tn.read_until(b'\n').decode('utf-8').strip()
        tel.append(linea)
    for i in tel:
        print(i)
        k,v = i.split(":")
        d[str(k)] = v
    return d

def check_agent(host):
    i = 0
    try:
        ip = socket.gethostbyname(host)
    except:
        return -1
    nm = nmap.PortScanner()
    host = ip
    a = nm.scan(host,'6556',arguments='-sS')
    while (nm.scanstats()['uphosts'] == '0'):
        a= nm.scan(host,'6556',arguments='-sS -O')
        if (i == 3):
            return -1
    b = nm.all_hosts()
    print(b)
    return(nm[b[0]]['tcp'][6556]['state'] == 'open')

def check_OS(host):
    try:
        print(socket.gethostbyname(host))
    except:
        return -1
    nm = nmap.PortScanner()
    a = nm.scan(host,'22-2000',arguments='-sS -O')
    if (nm.scanstats()['uphosts'] == '0'):
        a= nm.scan(host,'22-2000',arguments='-sS -O')
    b = nm.all_hosts()
    a = nm[b[0]]['osmatch'][0]['osclass'][0]['osfamily']
    if('windows' in a or 'Windows' in a):
        return 1
    if('linux' in a or 'Linux' in a):
        print("Linux")
        return 0
    return 0
