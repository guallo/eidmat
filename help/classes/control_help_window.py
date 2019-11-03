import os
import sys

from util.terminal import Terminal


class ControlHelpWindow:
    """
        Clase controladora que permite realizar peticiones a Octave, leer las 
        respuestas y busca palabras en componentes Web.
    """    
    def __init__(self, p_help_w):
        """
            p_help_w: representa una instancia de HelpWindow.

            Constructor de la clase ControlHelpWindow.
        """       
        self.__term = Terminal()
        self.__term.feed_child("\n")

    def excec_command(self, p_command, p_method):
        """
            p_command: representa una cadena de texto.
            p_method: representa un metodo de la clase HelpWindow.

            Metodo que solicita la ayuda correspondiente a un comando propio 
            de Octave.
        """
        self.__term.feed_child(p_command, p_method)

    def destroy_terminal(self):
        """
            Metodo que destruye la instancia a Octave tras el cierre de la
            ventana Ayuda.
        """
        self.__term.feed_child("exit\n")

    def web_search(self, p_localization, p_texto, p_sal = None):
        """
            p_localization: representa una cadena de texto con la direccion 
                            de la pagina web solicitada.
            p_texto: representa una cadena de texto.
            p_sal: representa True o False en correspondencia con el tipo de 
                   busqueda.

            Retorna: el codigo de una pagina web con la frase contenida en 
                     <p_text> de color rojo o un mensaje dando a conocer que la
                     misma no se encontro. En caso de que <p_sal!=None> y se 
                     encuentre la frase al menos una vez, se retorna tambien 
                     una cadena de control.         
            
            Metodo que busca una palabra o frase en la documentacion de Octave
            retornando una pagina con la frase remarcada en color rojo si la 
            busqueda es local o una cadena de control si la palabra o frase fue
            encontrada al menos una vez durante una busqueda global.
        """        
        web_code = ""
        if not p_localization:
            return "No se busco"
        loc = p_localization.replace("file:///", "/")            
        if "#" in loc:
            aux = ""
            for i in loc:
                if i == "#":
                    break
                aux += i
            loc = aux
        f = open(loc, "r")
        for linea in f:            
            web_code += linea                 
        f.close()
        flag = False
        aux = ""
        cant_letters = len(p_texto)
        valid_word = ""
        iter1 = 0
        ampersan = False
        valid_flag = False
        if p_texto in web_code:
            for i in web_code:                
                if i == '>':
                    flag = True                    
                if i == '<' :
                    if len(valid_word) > 0:
                        aux += valid_word
                    flag = False
                if i == '&':
                    if len(valid_word) > 0:
                        aux += valid_word
                    flag = False
                    ampersan = True
                if i == ';' and ampersan:
                    flag = True 
                    ampersan = False    
                if flag == True:
                    valid_word += i
                    if p_texto[iter1].lower() == i.lower():
                        iter1 += 1
                    else:
                        aux += valid_word
                        valid_word = ""
                        iter1 = 0
                    if iter1 == cant_letters:
                        if p_sal:
                            return "si"
                        aux = aux + '<em style="color:red">' + valid_word \
                                                                + '</em>'                        
                        iter1 = 0
                        valid_word = ""
                        valid_flag = True
                else:
                    aux += i
                    valid_word = ""
                    iter1 = 0                        
            web_code = aux
            if valid_flag:                
                return web_code     
            else:
                return "No se encontro"
        else:
            return "No se encontro"

    def web_search_file(self, p_word, p_loc):     
        """
            p_word: representa la palabra a buscar. 
            p_loc: representa la localizacion o direccion de la pagina web.

            Retorna: localizacion de la pagina web o la cadena <no> en caso de 
                     no encontrarse la palabra o frase deseada en la pagina.

            Metodo que busca una palabra o frase deseada dentro de una pagina 
            web especificada. Solo se lee el fichero y se pregunta si esta o
            no la palabra sin diferenciar su estancia dentro de un tag.
        """
        dir_ = os.path.join(os.path.dirname(sys.argv[0]), "help", "octave_doc",
                            p_loc + ".html")
        f = open(dir_, "r")
        text = f.read()
        f.close()
        if p_word in text:
            return p_loc
        return "no"
