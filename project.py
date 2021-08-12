# Cristina Bautista 161260
# Proyecto 1 - Redes
# Para MongooseIM https://mongooseim.readthedocs.io/en/2.1.1/user-guide/Getting-started/
# Para slixmpp https://slixmpp.readthedocs.io/en/latest/getting_started/echobot.html

import slixmpp
import logging
from getpass import getpass
from argparse import ArgumentParser
from slixmpp.exceptions import IqError, IqTimeout

# Muestra en consola e DEBUG
logging.basicConfig(level=logging.DEBUG, format="%(levelname)-8s %(message)s")

class Client(slixmpp.ClientXMPP):
  # Empieza lo bueno
  def __init__(self, userid, password):
    slixmpp.ClientXMPP.__init__(self, userid, password)
    self.userid = userid
    self.password = password

    self.add_event_handler("session_start", self.sessionStart)
    self.add_event_handler("register", self.registrar)

  async def sessionStart(self, e):
    self.send_presence()
    await self.get_roster()

    # Mostrar contactos
    # referencia de la libreria sleekmpp https://github.com/jplevyak/xmppbroadcast/blob/master/xmppbroadcast.py
    def mostrarContactos():
      print("\n")
      contacts = self.client_roster.groups()
      # print(contacts)
      for contact in contacts:
        print('***************Listado********************')
        for jid in contacts[contact]:
          user = self.client_roster[jid]['name']
          if self.client_roster[jid]['name']:
            print('\n', user, ' (',jid,')')
          else:
            print('\n', jid)

          connecciones = self.client_roster.presence(jid)
          for res, pres in connecciones.items():
            show = 'available'
            if pres['show']:
              show = pres['show']
            print('   - ',res, '(',show,')')
            if pres['status']:
              print('       ', pres['status'])
      print("")
      print('*************Fin Listado******************')
      print("Done!")

    # Agregar un nuevo contacto
    def nuevoContacto():
      nuevoContacto = input("Ingrese userid: ")
      self.send_presence_subscription(pto=nuevoContacto)
      mensaje="Buenas buenas!!! Hoy amanecimos..."
      self.send_message(mto=nuevoContacto, mbody=mensaje, mtype="chat", mfrom=self.boundjid.bare)

    # Mostrar detalles del contacto
    # referencia de la libreria sleekmpp https://github.com/jplevyak/xmppbroadcast/blob/master/xmppbroadcast.py
    def detallesContacto():
      self.get_roster()
      usedidContact = input("Ingrese userid: ")
      user = self.client_roster[usedidContact]['name']
      print('\n %s (%s)' % (user, usedidContact))

      connecciones = self.client_roster.presence(usedidContact)
      if connecciones == {}:
        print('       Away')
      for res, pres in connecciones.items():
        show = 'available'
        if pres['show']:
          show = pres['show']
        print('   - ', res, ' - ', show)
        print('       ',  pres['status'])




    print("session_start")
    loginStart = True
    while loginStart:
      print("""
      
      Submenu

      1.  Mostrar usuarios
      2.  Agregar a un usuario
      3.  Mostrar detalles de usuario
      4.  Mandar un DM
      5.  Chat grupal
      6.  Cambiar mensaje de presencia
      7.  Enviar archivo
      8.  Enviar notificaciones
      9.  Eliminar la cuenta
      10. Salir de la sesion
      
      
      """)
      loginOption = int(input("Que opcion desea realizar? "))
      if loginOption == 1:
        mostrarContactos()
      elif loginOption == 2:
        nuevoContacto()
      elif loginOption == 3:
        detallesContacto()
      elif loginOption == 4:
        pass
      elif loginOption == 5:
        pass
      elif loginOption == 6:
        pass
      elif loginOption == 7:
        pass
      elif loginOption == 8:
        pass
      elif loginOption == 9:
        self.register_plugin('xep_0030') 
        self.register_plugin('xep_0004')
        self.register_plugin('xep_0077')
        self.register_plugin('xep_0199')
        self.register_plugin('xep_0066')

        eliminar = self.Iq()
        eliminar['type'] = 'set'
        eliminar['from'] = self.boundjid.user
        eliminar['register']['remove'] = True
        print('*************Eliminado******************')
        eliminar.send()
        
        self.disconnect()

      elif loginOption == 10:
        self.disconnect()
        loginStart = False

      else:
        print("Por favor escoje una opcion del menu")


  async def registrar(self, iq):
    self.send_presence()
    self.get_roster()

    resp = self.Iq()
    resp['type'] = 'set'
    resp['register']['username'] = self.boundjid.user
    resp['register']['password'] = self.password

    try:
      await resp.send()
      logging.info("Account created for %s!" % self.boundjid)
    except IqError as e:
      logging.error("Could not register account: %s" % e.iq['error']['text'])
      self.disconnect()
    except IqTimeout:
      logging.error("No response from server.")
      self.disconnect()


def registrar(userid, password):
  cliente = Client(userid, password)
  cliente.register_plugin("xep_0030")
  cliente.register_plugin("xep_0004")
  cliente.register_plugin("xep_0077")
  cliente.register_plugin("xep_0199")
  cliente.register_plugin("xep_0066")

  cliente["xep_0077"].force_registration = True

  cliente.connect()
  cliente.process(forever=False)

  print("Registro exitoso!")
  
def iniciarSesion(userid, password):
  cliente = Client(userid, password)
  cliente.register_plugin("xep_0030")
  cliente.register_plugin("xep_0199")

  cliente.connect()
  cliente.process(forever=False)

  # print("\nInicio de sesion exitoso!")



start = True

while start:
  print("""
  Bienvenido!

  1. Registrar
  2. Iniciar Sesion
  3. Salir del proyecto
  
  """)
  firstOption = int(input("Que opcion desea realizar? "))
  if firstOption == 1:

    userid = input("Ingrese userid con @alumchat.xyz: ")
    password = input("Ingrese una password: ")

    registrar(userid, password)
    


  elif firstOption == 2:

    userid = input("Ingrese userid con @alumchat.xyz: ")
    password = input("Ingrese una password: ")
    iniciarSesion(userid, password)

    



  elif firstOption == 3:
    print("Hasta pronto!")
    start = False


  else:
    print("Por favor escoje una opcion del menu")