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
    print("session_start")
    loginStart = True
    while loginStart:
      print("""
      
      Submenu

      1.  Eliminar la cuenta
      2.  Mostrar usuarios
      3.  Agregar a un usuario
      4.  Mostrar detalles de contacto de un usuario
      5.  Mandar un DM
      6.  Chat grupal
      7.  Cambiar mensaje de presencia
      8.  Enviar archivo
      9.  Enviar notificaciones
      10. Salir de la sesion
      
      
      """)
      loginOption = int(input("Que opcion desea realizar? "))
      if loginOption == 1:
        pass
      elif loginOption == 2:
        pass
      elif loginOption == 3:
        pass
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
        pass
      elif loginOption == 10:
        loginStart = False
      else:
        print("Por favor escoje una opcion del menu")


  async def registrar(self, iq):
    self.send_presence()
    await self.get_roster()

    resp = self.Iq()
    resp['type'] = 'set'
    resp['register']['userid'] = self.boundjid.user
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
  cliente.register_plugin("xep_0199")
  cliente.register_plugin("xep_0066")
  cliente.register_plugin("xep_0077")

  cliente["xep_0077"].force_registration = True

  cliente.connect()
  cliente.process()

  print("Registro exitoso!")
  
def iniciarSesion(userid, password):
  cliente = Client(userid, password)
  cliente.register_plugin("xep_0030")
  cliente.register_plugin("xep_0199")

  cliente.connect()
  cliente.process(forever=False)

  print("\nInicio de sesion exitoso!")



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