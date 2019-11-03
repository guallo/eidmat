import gtk
import os
import sys

from util.confirm import Confirm
from util.message import Message
from util.terminal import Terminal


class GenerateComands:
    """
        Clase que genera los  comandos de Octave necesarios
        para el correcto funcionamiento del la ayuda en la seccion Index.
    """
    def __init__(self, p_help_window):
        """
            p_help_window: representa una instancia de HelpWindow.

            Constructor de la clase GenerateComands.
        """  
        self.__help = p_help_window
        self.__list_letters=["a", "b", "c", "d", "e", "f", "g", "h", "i", 
                             "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
                             "t",  "u", "v", "w", "x", "y", "z", "_"]
        self.__letter = "a"
        self.__list_keys = {}
        l = self.__list_letters
        for i in xrange(len(l)):
            self.__list_keys[l[i]] = []
        self.__term = Terminal()
        self.__term.feed_child("\n", self._ready)

    def _ready(self, p_texto):
        """
            p_texto: representa una cadena de texto.
    
            Metodo auxiliar que verifica el momento en que Octave esta listo 
            para recibir comandos de la peticion.
        """
        self.excec_help()

    def excec_help(self):
        """
            Metodo que solicita a Octave la relacion de todos los comandos
            propios.    
        """
        command = "help\n"
        self.__term.feed_child(command, self.show_help)

    def show_help(self, p_text):
        """
            p_text: representa una cadena de texto con la respuesta de la 
                    peticion de ayuda a octave de un comando.
        
            Metodo que procesa la respuesta de Octave una vez enviado el 
            comando help. Adicionalmente, este metodo es el encargado de llenar
            las listas asociadas a cada letra del abecedario.
        """
        aux = p_text.split("mailing list.")
        aux = aux[1].split("\n")
        aux = aux[1:]
        for i in range(len(aux)):
            if aux[i] != "":
                if not "***" in aux[i] and aux[i][0].lower() in \
                   self.__list_letters:
                    aux2 = aux[i].split(" ")           
                    for i in range(len(aux2)):
                        if aux2[i] != "":
                            if not ".m" in aux2[i] and not ".oct" in aux2[i]:
                                self._situate(aux2[i])
                            elif ".m" in aux2[i] or ".oct" in aux2[i]:
                                aux3 = aux2[i].split(".")
                                self._situate(aux3[0])                                
        self.__term.feed_child("exit\n")
        self.__list_keys["_"].pop()
        self.__help.write_comand("a")

    def _situate(self, p_command):
        """
            p_command: representa una cadena de texto (comando de octave).

            Metodo que situa un comando en su lista correspondiente de acuerdo
            con la letra con que comienza.
        """
        text = p_command[0].lower()
        if text == "_":
            pass
        if text in self.__list_letters:
            if not p_command in self.__list_keys[text]:
                self.__list_keys[text].append(p_command)
            else:
                return

    def get_list(self, p_letter):
        """
            p_letter: representa una letra del abecedario.

            Retorna: lista con las palabras que comienzan con la letra que 
                     representa p_letter.
    
            Metodo que dado un caracter devuelve la lista de los comandos
            que comienzan con este caracter. Adicionalmente se controla la 
            letra activa en el Index.
        """        
        self.__letter = p_letter
        return self.__list_keys[p_letter]        

    def get_letter(self):        
        """
            Retorna: una letra del abecedario.
            
            Metodo que retorna la letra activa en el Index.
        """
        return self.__letter

