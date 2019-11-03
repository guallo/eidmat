import gtk
import gtk.glade
import gtkmozembed
import pango
import os
import sys
import gobject

from help.classes.web import Web
from help.classes.control_help_window import ControlHelpWindow
from help.classes.generate_comands import GenerateComands
from util.message import Message


class HelpWindow:
    """
        Clase para el control de los eventos y metodos referidos a la Ayuda
        del sistema.
    """    
    def __init__(self, p_mwindow):
        """
            p_mwindow: representa el MainWindow.

            Constructor de la clase HelpWindow.
        """ 
        self.__searching_stop = False
        self.__searching_ocupate = False
        self.__wait = False
        self.__update = False
        self.__buscar = False

        self.__window_search = None
        self.__xml4 = None

        self.__letras_alfabeto = []
        self.__lista_labels = []

        self.__comando_actual = ""
        self.__page_select_search_result = ""
        self.__command = ""

        self.path2 = os.path.join(os.getcwd(), os.path.dirname(sys.argv[0]),\
                                  "images", 'guiHelp.glade')        
        self.__xml2 = gtk.glade.XML(self.path2, 'window2')
        self.__xml2.signal_autoconnect(self)

        self.__window2 = self.__xml2.get_widget('window2')
        self.__window2.maximize()

        self.__hpaned2 = self.__xml2.get_widget('hpaned2')

        # Tener una referencia del mwindow
        self.__mwindow = p_mwindow

        # Boton reabrir panel de busqueda lateral izquierdo.
        self.__show_help_navigator = self.__xml2.get_widget('toolbutton31')

        # Boton Stop
        self.__stop_button = self.__xml2.get_widget('toolbutton3')
        self.__stop_button.set_sensitive(False)     

        self.__notebook_sections = self.__xml2.get_widget('notebook2')
        self.__notebook_view = self.__xml2.get_widget('notebook3')        

        # Ocultar tags del notebook3 que representa la derecha de la ventana.
        self.__notebook_view.set_show_tabs(False)

        # Campo donde se entra el comando a buscar.
        self.__entry_Index = self.__xml2.get_widget('entry1')               

        # Campo para buscar en el Search Result.
        self.__entry_Search = self.__xml2.get_widget('entry4')   

        # Respuesta del Search.
        self.__textview_index = self.__xml2.get_widget('textview1') 
        self.__textview_index.set_editable(False)
        self.__textview_index.modify_font(
            pango.FontDescription("monospace Expanded 10"))        
        color = gtk.gdk.color_parse("blue")
        self.__textview_index.get_buffer().create_tag("blue_foreground",
                                                      foreground_gdk = color)
        color = gtk.gdk.color_parse("red")
        self.__textview_index.get_buffer().create_tag("red_foreground",
                                                      foreground_gdk = color)
        self.__textview_index.get_buffer().create_tag("bold",
                                                  weight = pango.WEIGHT_BOLD)        

        # Combobox para poner el historial del Contents.
        self.__combo_history_list = gtk.ListStore(str, object)
        self.__combo_history = gtk.ComboBox(self.__combo_history_list)
        comboCell = gtk.CellRendererText()
        self.__combo_history.pack_start(comboCell, True)
        self.__combo_history.add_attribute(comboCell, 'text', 0)
        self.__combo_history.show_all()
        self.__combo_history.connect("changed", 
                                     self.on_comboboxentry2_changed)
        self.__xml2.get_widget("hbox1").pack_start(self.__combo_history, 
                                                   True, True, 0)

        # Verifica si se cambio de elemento en el combo_history.
        self.__combo_change = False

        # Representa el arbol en la seccion Search Result.
        self.__treeview_search = self.__xml2.get_widget('treeview6')
        self.__liststore_search = gtk.ListStore(str)
        self.__treeview_search.set_model(self.__liststore_search)
        column = gtk.TreeViewColumn("Title")
        cell = gtk.CellRendererText()
        column.pack_start(cell)
        column.set_attributes(cell, text = 0)
        column.set_sort_column_id(0)
        self.__treeview_search.append_column(column)        
        self.write_label()
        self.color_label(self.__lista_labels[0])
        self.__treeview_index = self.__xml2.get_widget('treeview5')
        self.__liststore_index = gtk.ListStore(str)
        self.__treeview_index.set_model(self.__liststore_index)
        column = gtk.TreeViewColumn("Title")
        cell = gtk.CellRendererText()
        column.pack_start(cell)
        column.set_attributes(cell, text = 0)
        column.set_sort_column_id(0) 
        self.__treeview_index.append_column(column)        
        self.__generate_command = GenerateComands(self)

        # Componente Web.
        gtkmozembed.push_startup() # Necesaria para que pinche el gtkmozembed.
        self.__web_contents = gtkmozembed.MozEmbed()
        self.__web_search = gtkmozembed.MozEmbed()

        self.__dire = os.path.join(os.getcwd(), os.path.dirname(sys.argv[0]))

        self.__pagina_seleccionada_contents = 'octave'
        self.dir_page()
        self.__web_contents.show()

        # Adicionar al hbox el componente Web del Contents y Search Result.
        self.__xml2.get_widget('hbox10').add(self.__web_contents)        
        self.__xml2.get_widget('hbox11').add(self.__web_search)

        self.__window2.show_all()

        self.__treeview_Contents = self.__xml2.get_widget('treeview4')        
        self.__model = gtk.TreeStore(str)
        self.__treeview_Contents.set_model(self.__model)        
        column = gtk.TreeViewColumn()
        self.__treeview_Contents.append_column(column)        
        self.cell = gtk.CellRendererText()
        column.pack_start(self.cell, True)
        column.add_attribute(self.cell, 'text', 0)

        # Instancia a la clase Web.
        self.__web = Web()
        self.__web.set_mode(self.__model)
        self.__model = self.__web.get_mode()
        self.__web.set_diccionary()

        # Instancia a la clase ControlHelpWindow.
        self.__control_helpw = ControlHelpWindow(self)

        iter_ = self.__model.get_iter_first()
        self.__treeview_Contents.set_cursor_on_cell(
            self.__model.get_path(iter_))
        self.__treeview_Contents.scroll_to_cell(self.__model.get_path(iter_))
        
        


##------------------------------------Eventos--------------------------------##

    def on_toolbutton30_clicked(self, p_widget):
        """
            p_widget: representa un GtkToolButton.

            Metodo que permite ocultar el navegador de la ayuda o 
            <Help Navigator>.
        """
        self.__xml2.get_widget("alignment4").hide()
        self.__hpaned2.set_position(0)    
        self.__show_help_navigator.set_visible_horizontal(True)
        self.__show_help_navigator.set_visible_vertical(True)

    def on_toolbutton31_clicked(self, p_widget): 
        """
            p_widget: representa un GtkToolButton.

            Metodo que permite visualizar el navegador de la ayuda o 
            <Help Navigator>.
        """
        self.__xml2.get_widget("alignment4").show()
        self.__hpaned2.set_position(350)
        self.__show_help_navigator.set_visible_horizontal(False)
        self.__show_help_navigator.set_visible_vertical(False)

    def on_toolbutton33_clicked(self, p_widget): 
        """
            p_widget: representa un GtkToolButton.

            Evento que posibilita la busqueda de una palabra o frase en la 
            documentacion de Octave a traves del metodo auxiliar 
            <buscar_palabra_search_result>.
        """
        text = self.__entry_Search.get_text()
        self.buscar_palabra_search_result(text)

    def on_toolbutton23_clicked(self, p_widget):
        """
            p_widget: representa un GtkToolButton.

            Metodo que permite ir a la pagina web anterior mientras se trabaja
            en las secciones <Contents> y <Search Result>.
        """
        if self.__notebook_sections.get_current_page() == 0:
            if self.__web_contents.can_go_back():
                self.__web_contents.go_back()
        elif self.__notebook_sections.get_current_page() == 2:
            if self.__web_search.can_go_back():
                self.__web_search.go_back()                

    def on_toolbutton24_clicked(self, p_widget):    
        """
            p_widget: representa un GtkToolButton.

            Metodo que permite ir a la pagina web siguiente mientras se trabaja
            en las secciones <Contents> y <Search Result>.
        """       
        if self.__notebook_sections.get_current_page() == 0:
            if self.__web_contents.can_go_forward:
                self.__web_contents.go_forward()
        elif self.__notebook_sections.get_current_page() == 2:
            if self.__web_search.can_go_forward():
                self.__web_search.go_forward()

    def on_toolbutton29_clicked(self, p_widget):
        """
            p_widget: representa un GtkToolButton.

            Metodo que permite buscar palabras o frases en cualquiera de las 
            secciones (Contents / Index / Search Result) al hacer click en el 
            item <Find>.
        """
        if self.__buscar == False:
            self.__xml4 = gtk.glade.XML(self.path2, 'dialog2')
            self.__xml4.signal_autoconnect(self)
            self.__window_search = self.__xml4.get_widget('dialog2')
            self.__buscar = True
        else:
            if self.__window_search:
                self.__window_search.present()

    def on_toolbutton1_clicked(self, p_widget):
        """
            p_widget: representa un GtkToolButton.

            Metodo que permite exportar la pagina web actual al navegador web 
            por defecto que se este empleando mientras se trabaja en las 
            secciones <Contents> o <Search Result>.
        """        
        if self.__notebook_sections.get_current_page() == 0:  
            p = self.__pagina_seleccionada_contents
            dire = "'file://%s/help/octave_doc/%s.html'" %(self.__dire, p)
        elif self.__page_select_search_result:

            p = self.__page_select_search_result
            dire = "'file://%s/help/octave_doc/%s.html'" %(self.__dire, p)
        else:
            return        
        os.system('firefox %s &' %dire)

    def on_toolbutton3_clicked(self, p_widget):
        """
            p_widget: representa un GtkToolButton.

            Metodo que detiene la busqueda activa en la sesion <Search Result>.
        """
        if self.__searching_ocupate:
            self.__searching_stop = True

    def on_notebook2_switch_page(self, p_widget, p_gpointer, p_page_number):		
        """
            p_widget: representa un GtkNotebook.
            p_gpointer: representa un gpointer.
            p_page_number: representa el numero de la pagina que esta el 
            notebook.

            Metodo que permite actualizar elementos visuales cuando se cambia 
            de seccion (Contents / Index / Searchs Result).        
        """
        self.__notebook_view.set_current_page(p_page_number)
        if p_page_number == 1:
            self.__web.destroy_diccionary()
            self.__xml2.get_widget('toolbutton23').hide()
            self.__xml2.get_widget('toolbutton24').hide()
            self.__xml2.get_widget('toolbutton1').hide()
            self.__xml2.get_widget('toolbutton2').hide()
        else:
            self.__web.set_diccionary()
            self.__xml2.get_widget('toolbutton23').show()
            self.__xml2.get_widget('toolbutton24').show()           
            self.__xml2.get_widget('toolbutton1').show()
            self.__xml2.get_widget('toolbutton2').show()
    def on_entry1_changed(self, p_widget):  
        """
            p_widget: representa un GtkEntry.

            Metodo que permite ejecutar la busqueda de un comando solicitado
            en el campo de entrada de texto de la seccion <Index> cada vez que 
            se modifica su contenido.
        """        
        aux = self.__entry_Index.get_text().strip()
        self.__comando_actual = aux
        letter = self.__generate_command.get_letter()
        if aux != "" and aux[0] != letter:
            self.rewrite_comand(aux[0])        
        self.move_scrool_index(aux)

    def on_entry2_key_press_event(self, p_widget, p_event):        
        """
            p_widget: representa un GtkEntry.
            p_event: representa un GdkEvent.

            Metodo que permite ejecutar la busqueda de un comando solicitado
            en el campo de entrada de texto de la seccion <Index> una vez que 
            se presiona la tecla <enter>.       
        """
        if p_event.keyval == gtk.keysyms.Return or \
           p_event.keyval == gtk.keysyms.KP_Enter:
            text = self.__entry_Search.get_text()
            self.buscar_palabra_search_result(text)

    def rewrite_comand(self, p_texto): 
        """
            p_texto: representa una cadena de texto.

            Metodo que permite actualizar la lista de comandos en la seccion
            <Index> una vez que es modificada la primera letra del campo 
            de entrada de texto de esta seccion o cuando se selecciona 
            directamente un caracter.
        """
        if p_texto == "_":
            self.write_comand(p_texto)
        for i in xrange(len(self.__lista_labels)):
            if self.__lista_labels[i].get_text() == p_texto.upper():
                self.gest_label(self.__lista_labels[i], \
                                self.__lista_labels[i].get_text().lower())
                break

    def gestionar_labels(self, p_label, p_event):        
        """
            p_label: representa una cadena de texto.
            p_event: representa un GdkEvent.

            Metodo que permite, mediante una llamada al metodo auxiliar 
            <gest_label>, listar la totalidad de los comandos cuya letra 
            inicial coincide con la etiqueta del boton seleccionado en la 
            seccion <Index>.
        """ 
        self.gest_label(p_label, p_label.get_text().lower())

    def on_treeview4_cursor_changed(self, p_widget):
        """
            p_widget: representa un GtkTreeView.

            Metodo que permite visualizar el contenido de la pagina 
            seleccionada en la sesion <Contents>.
        """
        selection = self.__treeview_Contents.get_selection()   
        model, iter_, = selection.get_selected()
        if iter_:
            text = model.get_value(iter_, 0)            
            self.__pagina_seleccionada_contents = self.__web.get_page(text)
            self.dir_page()
            for i in xrange(len(self.__combo_history_list)):
                if text == self.__combo_history_list[i][0]:
                    return
            self.__combo_history_list.append([text, model.get_path(iter_)])
            self.__combo_change = True
            self.__combo_history.set_active(len (self.__combo_history_list)-1)

    def on_treeview5_cursor_changed(self, p_widget):        
        """
            p_widget: representa un GtkTreeView.

            Metodo que permite visualizar el contenido de la ayuda de un
            comando al seleccionar un elemento de la lista de comandos 
            en la sesion <Index>.
        """
        selection = self.__treeview_index.get_selection()
        model, iter_, = selection.get_selected()
        if iter_:
            text = model.get_value(iter_, 0)
            self.__command = text
            self.mostrar_ayuda_index()

    def on_treeview6_cursor_changed(self, p_widget):
        """
            p_widget: representa un GtkTreeView.

            Metodo que permite visualizar el contenido de la pagina 
            seleccionada en la sesion <Search Result>.      
        """
        selection = self.__treeview_search.get_selection()   
        model, iter_, = selection.get_selected()
        if iter_:
            text = model.get_value(iter_, 0)            
            text = self.__web.get_page(text)
            self.__page_select_search_result = text
            self.__web_search.load_url('file://' + self.__dire 
                                       + '/help/octave_doc/' + text + ".html")

    def on_comboboxentry2_changed(self, p_widget):
        """
            p_widget: representa un GtkComboBox.

            Metodo que visualiza una pagina seleccionada dentro del historial
            de paginas visitadas.
        """
        if self.__combo_change:
            self.__combo_change = False
            return
        element = self.__combo_history_list[self.__combo_history.get_active()]
        aux = element[0]
        if aux[0] == '':
            return
        self.__notebook_view.set_current_page(0)
        self.__notebook_sections.set_current_page(0)
        self.__pagina_seleccionada_contents = self.__web.get_page(aux)
        self.__treeview_Contents.expand_to_path(element[1])
        self.__treeview_Contents.set_cursor_on_cell(element[1],
                        self.__treeview_Contents.get_column(2))
        self.__treeview_Contents.scroll_to_cell(element[1])
        self.dir_page()

    def on_dialog2_destroy(self, p_widget):
        """
            p_widget: representa un GtkDialog.

            Metodo que coloca en falso la variable <self.__buscar> una vez
            destruido el cuadro de dialogo <Search> de la Ayuda.
        """
        self.__buscar = False

    def on_cancelbutton1_clicked(self, p_widget):    
        """
            p_widget: representa un GtkButton.

            Metodo que cancela la accion de busqueda y cierra el cuadro de 
            dialogo <Search>.
        """
        self.__xml4.get_widget('dialog2').destroy()
        self.__window_search = None

    def event_buscar_palabra_boton(self, p_widget):    
        """
            p_widget: representa un GtkButton.
            
            Metodo que activa la busqueda de palabras o frases dentro de las 
            secciones <Contents>, <Index> y <Search Result>.       
        """
        self.buscar_palabra()

    def event_buscar_palabra_enter(self, p_widget, p_event):
        """
            p_widget: representa un GtkEntry
            p_event: representa un GdkEvent

            Metodo que activa la busqueda de palabras o frases dentro de las 
            secciones <Contents>, <Index> y <Search Result> una vez que se 
            pulse la tecla <enter> en el campo de entrada de texto. 
        """        
        if p_event.keyval == gtk.keysyms.Return \
           or p_event.keyval == gtk.keysyms.KP_Enter:
            self.buscar_palabra()

    def on_actualizar_button(self, p_widget):
        """
            p_widget: representa un GtkToolButton.

            Metodo que actualiza la pagina web seleccionada en los paneles 
            laterales de las secciones <Contents> o <Search Result>.
        """
        if self.__notebook_sections.get_current_page() == 1:
            self.__command = self.__comando_actual
            self.mostrar_ayuda_index()
        if self.__notebook_sections.get_current_page() == 0:
            self.dir_page()
        if self.__notebook_sections.get_current_page() == 2 \
           and self.__page_select_search_result != "":
            self.__web_search.load_url('file://' + self.__dire
                + '/help/octave_doc/' + self.__page_select_search_result
                + ".html")   

##-----------------------------------Metodos---------------------------------##

    def mostrar_ayuda_index(self):
        """
            Metodo que solicita el contenido de la ayuda correspondiente a un 
            comando de Octave listado en la seccion <Index> de la Ayuda.
        """
        if self.__wait:
            self.__update = True
            return
        comand = "help " + self.__command + "\n"        
        self.__control_helpw.excec_command(comand, 
                                           self.mostrar_ayuda_index2)
        self.__wait = True
        self.__comando_actual = self.__command

    def mostrar_ayuda_index2(self, p_texto):          
        """
            p_texto: representa una cadena de texto.

            Metodo que visualiza el texto de la ayuda correspondiente a un 
            comando de Octave listado en la seccion <Index>.
        """
        texto = p_texto
        if "sorry" in texto or "not found" in texto:
            self.__textview_index.get_buffer().set_text("Command not found")
            start, end = self.__textview_index.get_buffer().get_bounds()
            self.__textview_index.get_buffer().apply_tag_by_name(
                "red_foreground", start, end)
        else:   
            aux = texto.split("Additional help for built-in functions")
            texto = aux[0]
            texto = texto + "Help and information about Octave is also \
available on the WWW\nat http://www.octave.org and via the \
help@octave.org\nmailing list."
            self.__command = self.__command.replace(" ", "")
            texto = texto.replace("help " + self.__command, "")
            self.__textview_index.get_buffer().set_text(texto)                 
            self.buscar_palabra_comandos("blue_foreground", self.__command)            
            start, end = self.__textview_index.get_buffer().get_bounds()
            self.__textview_index.get_buffer().apply_tag_by_name("bold", start, 
                                                                 end)
        self.__wait = False
        if self.__update:
            self.mostrar_ayuda_index()
            self.__update = False

    def dir_page(self):
        """
            Metodo que visualiza una pagina web dada la ubicacion de la 
            misma.        
        """        
        self.__web_contents.load_url('file://' + self.__dire + 
                                     '/help/octave_doc/'\
                                     + self.__pagina_seleccionada_contents 
                                     + ".html")

    def write_comand(self, p_letra = None):
        """
            p_letra: representa una letra del alfabeto si no se pasa nada 
                     es None.

            Metodo que lista la totalidad de los comandos de Octave en la 
            sesion <Index> dada una letra del abecedario.
        """
        self.__letras_alfabeto = self.__generate_command.get_list(p_letra)
        if self.__letras_alfabeto == None:
            return
        self.__liststore_index.clear()
        self.__letras_alfabeto.sort()
        for i in xrange(len(self.__letras_alfabeto)):
            self.__liststore_index.append([self.__letras_alfabeto[i]])            

    def write_label(self):
        """
            Metodo que genera el listado de las etiquetas de los botones de la
            sesion <Index> de la Ayuda.
        """
        i = 16        
        while i < 54:
            if i == 29:
                i = 41            
            self.__lista_labels.append(self.__xml2.get_widget("label" 
                                                              + str(i)))
            i += 1   

    def gest_label(self, p_label, p_letra):    
        """
            p_label: representa un GtkLabel.
            p_letra: representa una letra del alfabeto.

            Metodo que cambia las propiedades de la etiqueta correspondiente al
            boton seleccionado mediante llamadas a los metodos auxiliares 
            <color_label> y <write_comand>.
        """
        self.color_label(p_label)
        self.write_comand(p_letra)

    def color_label(self, p_label):
        """
            p_label: representa un GtkLabel.
            
            Metodo que cambia la propiedad color de la etiqueta <p_label>.
        """
        for i in xrange(len(self.__lista_labels)):
            self.__lista_labels[i].set_markup('<span foreground="blue" >'\
                          + self.__lista_labels[i].get_text() + '</span>')
        p_label.set_markup('<span foreground="red" >' + p_label.get_text() + 
                           '</span>')

    def buscar_palabra_search_result(self, p_text):
        """
            p_text: representa una cadena de texto.

            Metodo que busca la palabra o frase <p_text> dentro de la 
            documentacion de Octave.
        """                     
        self.__web.set_diccionary()
        diccionario = self.__web.get_diccionario()        
        lista = []        
        if self.__entry_Search.get_text() == "": 
            pass
        else:  
            self.__stop_button.set_sensitive(True) 
            if self.__searching_ocupate:
                return
            self.__searching_ocupate = True
            self.__liststore_search.clear()   
            for a in xrange(len(diccionario.items())):
                if self.__searching_stop:
                    self.__searching_stop = False
                    self.__searching_ocupate = False
                    self.__stop_button.set_sensitive(False)     
                    #phrase = "Search finished by user"                
                    #Message(gtk.STOCK_DIALOG_INFO, phrase, 
                            #"Help", self.__window2).run()
                    return
                ver = self.__control_helpw.web_search_file(
                    p_text, diccionario.items()[a][1])
                if ver != "no":
                    dir_ = os.path.join(os.path.dirname(sys.argv[0]), 
                                        "help", "octave_doc",
                                        diccionario.items()[a][1] + ".html")
                    s = self.__control_helpw.web_search(
                        dir_, p_text, True)
                    if s != "No se encontro":
                        lista.append(diccionario.items()[a][0])
                        self.__liststore_search.append(
                            [diccionario.items()[a][0]])
                        while gtk.events_pending():
                            gtk.main_iteration(False)
            if len(lista) > 0:
                selection = self.__treeview_search.get_selection()   
                model, iter_, = selection.get_selected()
                self.__stop_button.set_sensitive(False)
                #phrase = "Search for << " + p_text + " >> finished"
                if iter_ or self.__notebook_sections.get_current_page() != 2:
                    self.__searching_ocupate = False
                    #Message(gtk.STOCK_DIALOG_INFO, phrase, #"Help", self.__window2).run()
                    return
                iter_ = self.__liststore_search.get_iter_first()
                text = self.__liststore_search.get_value(iter_, 0)
                text = self.__web.get_page(text)
                self.__web_search.load_url('file://' + self.__dire +
                                           '/help/octave_doc/' + text +
                                           ".html")
                self.__page_select_search_result = text
                self.__treeview_search.set_cursor_on_cell(
                    self.__liststore_search.get_path(iter_))
                self.__treeview_search.scroll_to_cell(
                    self.__liststore_search.get_path(iter_))                
                #Message(gtk.STOCK_DIALOG_INFO, phrase, "Help", self.__window2).run()
            else:
                self.__stop_button.set_sensitive(False)
                self.lansar_no_se_encontro("Phrase not found")
        self.__searching_ocupate = False

    def buscar_palabra_comandos(self, p_tag_name, p_texto):
        """
            p_tag_name: representa una cadena de texto.
            p_texto: representa una cadena de texto.

            Metodo que resalta en Azul o Rojo (segun el valor de <p_tag_name>) 
            el termino de busqueda <p_texto> en la seccion <Index>.
        """
        texto = p_texto
        start, end = self.__textview_index.get_buffer().get_bounds()
        if not (texto in self.__textview_index.get_buffer().get_text(start,
                                                                     end)):
            if self.__buscar:
                self.lansar_no_se_encontro("Phrase not found")
            return 
        if not start.forward_search(texto, gtk.TEXT_SEARCH_TEXT_ONLY):
            return 
        if self.__textview_index.get_buffer().get_tag_table(). \
           lookup(p_tag_name) \
           != None:
            self.__textview_index.get_buffer().remove_tag_by_name(p_tag_name,
                                                                  start, end)
        finished = False
        while finished == False:        
            res = start.forward_search(texto, gtk.TEXT_SEARCH_TEXT_ONLY)
            if not res:
                finished = True
            else:
                matchStart, matchEnd = res
                self.__textview_index.get_buffer().apply_tag_by_name(
                    p_tag_name, matchStart, matchEnd)
                start = matchEnd

    def buscar_palabra(self):
        """
            Metodo que busca una palabra o frase en una pagina web o en el 
            contenido de la ayuda de un comando de Octave indicandose el 
            resaltado en color Rojo del termino de busqueda, si este fue 
            encontrado.
        """        
        texto = self.__xml4.get_widget("entry3").get_text()
        if texto.strip(" ") == "":
            self.lansar_no_se_encontro("Empty Files")
            return
        if self.__notebook_sections.get_current_page() == 0:            
            localizacion = self.__web_contents.get_location()
            s = self.__control_helpw.web_search(localizacion, texto)
            if s != "No se encontro":
                self.__web_contents.render_data(s, len(s), 
                                                localizacion, 'text/html') 
            else:
                self.lansar_no_se_encontro(" Phrase not found ")            
        elif self.__notebook_sections.get_current_page() == 1:
            self.buscar_palabra_comandos("red_foreground", texto)
        else:
            localizacion = self.__web_search.get_location()
            s = self.__control_helpw.web_search(localizacion, texto)
            if s != "No se encontro" and s != "No se busco":                
                self.__web_search.render_data(s, len(s), 
                                              localizacion, 'text/html')
            elif s == "No se encontro":
                self.lansar_no_se_encontro("Phrase not found")
            else:
                self.lansar_no_se_encontro("Must perform a search")
        self.__xml4.get_widget('dialog2').destroy()

    def lansar_no_se_encontro(self, p_mensaje):
        """
            p_mensaje: representa una cadena de texto.

            Metodo que activa un mensaje de error de no encontrarse la palabra
            o frase de busqueda.
        """  
        Message(gtk.STOCK_DIALOG_ERROR, p_mensaje, "Sorry", self.__window2).run()

    def on_copiar1_activate (self, p_menu_item):
        """
            p_menu_item: representa un GtkImageMenuItem.

            Metodo que permite el copiado de texto a traves de las opciones del
            menu Edit o el acceso rapido <ctrl+c>.
        """
        if self.__entry_Index.is_focus():
            self.__entry_Index.emit("copy-clipboard")
        elif self.__textview_index.is_focus():
            self.__textview_index.emit("copy-clipboard")
        elif self.__entry_Search.is_focus():  
            self.__entry_Search.emit("copy-clipboard")

    def on_cortar1_activate(self, p_menu_item):
        """
            p_menu_item: representa un GtkImageMenuItem.

            Metodo que permite el cortado de texto a traves de las opciones del
            menu Edit o el acceso rapido <ctrl+x>.
        """
        if self.__entry_Index.is_focus():
            self.__entry_Index.emit("cut-clipboard")
        elif self.__textview_index.is_focus():
            self.__textview_index.emit("cut-clipboard")
        elif self.__entry_Search.is_focus(): 
            self.__entry_Search.emit("cut-clipboard")

    def on_pegar1_activate(self, p_menu_item):
        """
            p_menu_item: representa un GtkImageMenuItem.

            Metodo que permite el pegado de texto a traves de las opciones del
            menu Edit o el acceso rapido <ctrl+v>.
        """
        if self.__entry_Index.is_focus():
            self.__entry_Index.emit("paste-clipboard")
        elif self.__entry_Search.is_focus():            
            self.__entry_Search.emit("paste-clipboard")

    def move_scrool_index(self, p_text):
        """
            p_text: representa una cadena de texto.

            Metodo que posiciona el scroll de la sesion <Index> en el comando 
            cuyo texto coincide con el texto <p_text>.
        """
        if p_text == "":
            return
        for row in self.__liststore_index:
            if row[0].startswith(p_text):
                self.__treeview_index.set_cursor(row.path)
                gobject.timeout_add(0, lambda: 
                                    self.__treeview_index.scroll_to_cell(
                                        row.path, None, True, 0.0, 0.0))
                break    

    def on_menuitem11_popup_menu(self, p_widget):
        """
            p_widget: representa un GtkMenuItem.

            Metodo que habilita o desabilita los elementos del menu Edit 
            en correspondencia con elemento que tenga el foco.
        """
        self.__xml2.get_widget('cortar1').set_sensitive(False)
        self.__xml2.get_widget('copiar1').set_sensitive(False)
        self.__xml2.get_widget('pegar1').set_sensitive(False)            
        if self.__notebook_sections.get_current_page() == 1:
            if self.__entry_Index.is_focus():
                self.__xml2.get_widget('cortar1').set_sensitive(True)
                self.__xml2.get_widget('copiar1').set_sensitive(True)
                self.__xml2.get_widget('pegar1').set_sensitive(True)
            elif self.__textview_index.is_focus():
                self.__xml2.get_widget('copiar1').set_sensitive(True)
        if self.__notebook_sections.get_current_page() == 2:
            if self.__entry_Search.is_focus():
                self.__xml2.get_widget('cortar1').set_sensitive(True)
                self.__xml2.get_widget('copiar1').set_sensitive(True)
                self.__xml2.get_widget('pegar1').set_sensitive(True)

    def close(self, p_widget, p_event = None):
        """
            p_widget: representa un GtkImageMenuItem o un GtkWindow en
                      dependencia de quien llame el metodo.
            p_event: representa un GdkEvent.

            Metodo que permite la salida de la Ayuda una vez seleccionada la
            opcion <Quit> del menu <File> o el acceso rapido <ctrl+q>.
        """
        self.__control_helpw.destroy_terminal()
        self.__window2.destroy()
        self.__mwindow.help_closed()
        if self.__window_search:
            self.__window_search.destroy()

    def present(self):
        """
            Metodo que trae al frente la ventana de Ayuda.
        """
        self.__window2.present()

    def on_acerca_de1_activate(self, p_menu_item):
        """
            p_menu_item: representa un GtkImageMenuItem.

            Metodo que muestra la ventana <About> de la aplicacion.
        """
        self.__mwindow.show_about()
