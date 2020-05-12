import Hangman
import ReverseGam
import TicTacToeModificado
from pathlib import Path
import PySimpleGUI as sg

# Se decidió usar pickle ya que es un tipo de dato de difícil acceso para el usuario, lo cual dificulta su manipulación; por el momento no se trabaja con ningún tipo de información 'sensible' (puntajes, datos personales valiosos), pero podría desearse implementar en futuras versiones. A pesar de sus problemas de seguridad, sabemos que en esta ocasión sólo el programa manipula el archivo.
import pickle

def cargarJugadores():
	jugadores = {}
	# Se decidió emplear un diccionario con la siguiente estructura:
	# 		{nombre de usuario: {nombre: dato, apellido: dato, cantidad de veces que jugó a juego: dato}
	# El principal motivo para esta elección es la facilidad de búsquedas directas en el archivo general, y la posibilidad de referenciar datos a partir de las estructuras provistas por PySimpleGUI, con especial énfasis en la legibilidad del código y la capacidad de modificar la ubicación de elementos sin temor a perder la referencia.
	if Path('jugadres.P').exists():
		with open('jugadores.P', 'rb') as f:
			jugadores = pickle.load(f)
	return jugadores

def guardarJugadores(jugadores):
	if Path('jugadres.P').exists():
		with open('jugadores.P', 'wb') as f:
			pickle.dump(jugadores,f)
	else:
		with open('jugadores.P', 'ab') as f:
			pickle.dump(jugadores,f)

def cargarNuevo():
	#Defino el diseño
	diseño = [
			  [sg.Txt('Nombre'), sg.In(size=(15,1), key='nombre'), sg.Txt('Apellido'), sg.In(size=(15,1), key='apellido')],
			  [sg.Txt('Nombre de usuario'), sg.In(size=(15,1), key='usuario')],
			  [sg.Submit('Crear'), sg.Cancel('Cancelar')]
			 ]

    # Creo la ventana
	form_1 = sg.Window('Cargar nuevo jugador').Layout(diseño)
	# Lectura de ventana
	evento, valores = form_1.Read()
	# Cierro la ventana
	form_1.Close()
	return valores

def cambioJugador(lista):
	#Defino el diseño
	diseño = [
			  [sg.Txt('Nombre de usuario'), sg.In(size=(15,1), key='usuario')],
			  [sg.Submit('OK')]
			 ]

    # Creo la ventana
	form_2 = sg.Window('Ingresar').Layout(diseño)
	# Lectura de ventana
	evento, valores = form_2.Read()
	# Cierro la ventana
	form_2.Close()
	return valores['usuario']

def main(args):

	def actualizarVentana(usuario, datos):
		nonlocal ventana
		nonlocal nombres_juegos

		ventana.FindElement('usuario').Update(usuario, visible=True)

		ap_nom = ', '.join([datos['apellido'], datos['nombre']])
		ventana.FindElement('ap_nom').Update(ap_nom, visible=True)

		ventana.FindElement('jugadas').Update(visible=True)

		for nombre in nombres_juegos:
			valor = 'cant_'+nombre
			ventana.FindElement(valor).Update(nombre+': '+str(datos[valor]), visible=True)

		ventana.FindElement('ingresar').Update(visible=False)
		ventana.FindElement('cambiar').Update(visible=True)

		for juego in nombres_juegos:
			ventana.FindElement(juego).Update(disabled=False)

	# Cargo los datos de jugadores
	jugadores = cargarJugadores()

	# Configuro valores for defecto y variables auxiliares
	sin_usuario = 'Ingresá con un usuario\nno creá uno nuevo para iniciar'
	usuario = sin_usuario
	ap_nom = ''
	datos = {}

	nombres_juegos = {'Ahorcado': Hangman.main, 'Ta-Te-Ti': TicTacToeModificado.main, 'Otello': ReverseGam.main}

    # Defino el diseño
	columna_1 = [
			  	 [sg.Txt('Jugador:')],
				 [sg.Txt(usuario, size=(25,1), key='usuario')],
				 [sg.Txt(ap_nom, size=(25,1), key='ap_nom', visible=False)],
				 [sg.Txt('')],
				 [sg.Txt('Partidas jugadas:', visible=False, key='jugadas')],
				 [sg.Txt('', size=(25,1), visible=False, key='cant_Ahorcado')],
				 [sg.Txt('', size=(25,1), visible=False, key='cant_Ta-Te-Ti')],
				 [sg.Txt('', size=(25,1), visible=False, key='cant_Otello')],
				 [sg.Txt('  '), sg.Button('Ingresar', key='ingresar'), sg.Button('Cambiar', visible=False, key='cambiar'), sg.Button('Nuevo')],
			  	 [sg.Txt('')]
			    ]

	columna_2 = [
				 [sg.Txt('')],
				 [sg.Txt('Seleccioná un juego')],
				 [sg.Button('Ahorcado', size=(10,1), disabled=True, key='Ahorcado')],
				 [sg.Button('Ta-Te-Ti', size=(10,1), disabled=True, key='Ta-Te-Ti')],
				 [sg.Button('Otello', size=(10,1), disabled=True, key='Otello')],
				 [sg.Txt('')],
				 [sg.Button('Salir')]
				]

	diseño = [
			  [sg.Column(columna_1), sg.Column(columna_2)]
			 ]

    # Creo la ventana
	ventana = sg.Window('Juegos').Layout(diseño)

	# Bucle de eventos
	while True:
		evento, valores = ventana.Read()

		if evento in (None, 'Salir'):
			#En cualquier caso de cierre de ventana guardo los datos
			guardarJugadores(jugadores)
			break

		elif evento == 'Nuevo':
			#En este caso se llama a una nueva ventana/formulario en la que el jugador ingresa sus datos
			nuevo = cargarNuevo()
			usuario = nuevo['usuario']
			for key in ('nombre', 'apellido'):
				datos[key] = nuevo[key]
			#La cantidad de veces que se jugó a cada juego se inicializa automáticamente en 0
			for nombre in nombres_juegos:
				valor = 'cant_'+nombre
				datos[valor] = 0

			actualizarVentana(usuario, datos)
			jugadores[usuario] = datos

		elif evento in ('ingresar', 'cambiar'):
			usuario = cambioJugador(list(jugadores.keys()))
			while usuario not in list(jugadores.keys()):
				sg.Popup('El usuario '+usuario+' no existe')
				usuario = cambioJugador(list(jugadores.keys()))

			actualizarVentana(usuario, datos)

		elif evento in nombres_juegos:
			# Esta línea llama al módulo correspondiente al botón presionado. Los juegos fueron modificados para, en caso de ser llamados por otro proceso, retornar la cantidad de veces que se ejecutó el bucle del juego en esa instancia.
			datos['cant_'+evento] = nombres_juegos[evento](datos['cant_'+evento])

			# Cada vez que la cantidad de veces que se jugó un juego es actualizada, se actualizan tanto la ventana como la estructura que contiene los datos de todos los jugadores.
			actualizarVentana(usuario, datos)
			jugadores[usuario] = datos


	# Cierro la ventana
	ventana.Close()

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
