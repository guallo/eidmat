import os


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
        self.__letter = "a"
        self.__list_keys = {}
        for l in [chr(n) for n in xrange(ord("a"), ord("z") + 1)] + ["_"]:
            self.__list_keys[l] = []

    def show_help(self):
        """
            Este metodo es el encargado de llenar las listas
            asociadas a cada letra del abecedario.
        """
        path = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir,
                                "edebugger", "completion", "octave_symbols.db")
        file_ = open(path)
        get = False
        for line in file_:
            if line.startswith("#") or get:
                if get:
                    self._situate(line.strip())
                get = not get
        file_.close()
        self.__list_keys["_"].pop()
        self.__help.write_comand("a")

    def _situate(self, p_command):
        """
            p_command: representa una cadena de texto (comando de octave).

            Metodo que situa un comando en su lista correspondiente de acuerdo
            con la letra con que comienza.
        """
        text = p_command[0].lower()
        if text.isalpha() or text == "_":
            self.__list_keys[text].append(p_command)

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

