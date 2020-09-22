import gtk
import os
import time
import datetime
from distutils import file_util

from project.xml_project import XML_Project
from util.confirm import Confirm


class Project:
    """ 
        Representa un proyecto con sus atributos:  nombre del proyecto, 
        localizacion, fecha, hora, lista de archivos m.
    """    
    def __init__(self):
        """
            Crea un nuevo 'Project'.
        """ 
        self.__project_name = None
        self.__localization = None
        self.__date = None        
        self.__cant_m_files = 0
        self.__m_file_list = []
        self.__xml_proje = XML_Project()

    def get_m_file_list(self):        
        """            
            Retorna: una lista con los nombres de todos los archivos m 
                     anadidos al proyecto.

            Metodo mediante el cual se tiene acceso a la lista de nombres de
            los archivos m anadidos al proyecto.
        """
        return self.__m_file_list

    def new_project(self, p_name, p_localization):
        """
            p_name: cadena de texto que representa el nombre del proyecto.
            p_localization: cadena de texto que representa el camino completo 
                            hasta la ubicacion del proyecto.
            
            Metodo mediante el cual se crea un nuevo proyecto.
        """
        
        self.__project_name = p_name
        self.__localization = p_localization
        self.__date = "%--" + str(time.localtime()[2]) + "/" + \
            str(time.localtime()[1]) + "/" + str(time.localtime()[0]) + "--%"        
        
        #crear la estructura de directorio
        dire = os.path.join(p_localization)
        os.system('mkdir %s' %dire)
        
        file_ = os.path.join(dire, p_name + ".eidmat")
        f = open(file_, "w")
        f.write("")
        f.close()
        
        dire = os.path.join(p_localization, 'VAR')
        os.system('mkdir %s' %dire)
        
        file_ = os.path.join(dire, "vars.var")
        f = open(file_, "w")
        f.write("")
        f.close()
        
        dire = os.path.join(p_localization, 'HIST')
        os.system('mkdir %s' %dire)
        file_ = os.path.join(dire, ".hist.txt~")
        f = open(file_, "w")
        f.write("")
        f.close()
        
        dire = os.path.join(p_localization, 'SRC')
        os.system('mkdir %s' %dire)
        
    def add_m_file(self, p_m_file):
        """
            p_m_file: cadena de texto que representa el nombre del archivo m
                      que se anade al proyecto.

            Metodo mediante el cual se adiciona el nombre de un archivo m a 
            la lista <self.__m_file_list>. Responde a la funcionalidad de 
            importar un archivo m al proyecto.
        """
        if not p_m_file in self.__m_file_list:
            self.__m_file_list.append(p_m_file)
        
    def save_project(self):
        """
            Metodo mediante el cual se guardan los datos del proyecto. Este 
            proceso incluye el paso del historial de ser un archivo temporal a
            ser un archivo fijo del proyecto
        """        
        path = os.path.join(self.__localization, "HIST",  
                            ".hist.txt~")
        f = open(path, "r")
        hist = f.read()
        f.close()
        path = os.path.join(self.__localization, "HIST",
                            "hist.txt")
        f = open(path, "w")
        f.write(hist)
        f.close()
        self.__xml_proje.save_project(self.__project_name, self.__localization, 
                                     self.__m_file_list, 
                                     self.__date)
        
    def open_project(self, p_localization):
        """
            p_localization: cadena de texto que representa el camino completo 
                            hasta la ubicacion del proyecto.

            Metodo mediante el cual se abre un proyecto existente.
        """        
        self.__localization = p_localization
        self.__project_name, self.__date , self.__m_file_list = \
            self.__xml_proje.open_project(self.__localization)        
    
    def delete_m_file(self, p_m_file):
        """
            p_m_file: cadena de texto que representa el nombre del archivo m
                      que se desea eliminar del proyecto.

            Metodo mediante el cual se elimina un archivo m del proyecto.
        """ 
        self.__m_file_list.remove(p_m_file)
        path_m_file = os.path.join(self.__localization, "SRC", p_m_file)
        os.system("rm %s" %(path_m_file))
        self.__xml_proje.save_project(self.__project_name, self.__localization, 
                                     self.__m_file_list, 
                                     self.__date)
    
    def import_m_file(self, p_path):
        """
            p_m_file: cadena de texto que representa el camino hasta el archivo
                      m que se desea importar.

            Metodo mediante el cual se importa un archivo m al proyecto dado 
            su localizacion a traves de la variable <p_path>.
        """
        name = os.path.split(p_path)[1]
        path = os.path.join(self.__localization, "SRC")        
        if not os.access(os.path.join(path, name), os.F_OK):
            file_util.copy_file(p_path, path)
            self.add_m_file(name)
            self.__xml_proje.save_project(self.__project_name,  
                                          self.__localization, 
                                          self.__m_file_list, 
                                          self.__date)
        else:
            msg = os.path.join(path, name) + \
                " already exists.\n Do you want to replace it?"
            resp = Confirm(gtk.STOCK_DIALOG_QUESTION, msg, 
                               "Import File ", None,
                               None).run()
            if resp:                
                file_util.copy_file(p_path, path)
                self.add_m_file(name)
                self.__xml_proje.save_project(self.__project_name, 
                                              self.__localization,
                                              self.__m_file_list, 
                                              self.__date)
    
    def get_name_project(self):
        """
            Retorna: una cadena de texto que representa el nombre del proyecto.

            Metodo mediante el cual se retorna el nombre de proyecto.
        """
        return self.__project_name
    
    def get_localization(self):    
        """
            Retorna: una cadena de texto que representa la localizaion del 
                     proyecto.

            Metodo mediante el cual se retorna la localizacion del proyecto.
        """    
        return self.__localization
    
    def get_date_project(self):
        """
            Retorna: una cadena de texto que representa la fecha en que fue
                     creado el proyecto.

            Metodo mediante el cual se retorna la fecha de creacion del 
            proyecto.
        """
        return self.__date
        
    def save_as_project(self, p_name, p_localization):
        """
            p_name: cadena de texto que representa el nuevo nombre con que se
                    desea guardar el proyecto.
            p_localization: cadena de texto que representa el camino completo 
                            hasta la ubicacion del nuevo proyecto.

            Metodo mediante el cual se salva la informacion del proyecto actual
            como otro proyecto. Esencialmente, se copian los datos del proyecto 
            hacia la estructura del nuevo proyecto tras la ejecucion de la 
            opcion <Save As...> del menu proyecto.
        """       
        old_loc = self.__localization
        path = os.path.join(p_localization, p_name)
        self.new_project(p_name, path)
        
        old_path = os.path.join(old_loc, "HIST", "hist.txt")
        new_path = os.path.join(path, "HIST", "hist.txt")        
        file_util.copy_file(old_path, new_path)
        
        old_path = os.path.join(old_loc, "HIST", ".hist.txt~")
        new_path = os.path.join(path, "HIST", ".hist.txt~")        
        file_util.copy_file(old_path, new_path)        
        
        old_path = os.path.join(old_loc, "VAR", "vars.var")
        new_path = os.path.join(path, "VAR", "vars.var")        
        file_util.copy_file(old_path, new_path)
        
        old_path = os.path.join(old_loc, "SRC")
        new_path = os.path.join(path, "SRC")
        
        for i in self.__m_file_list:
            if os.access(os.path.join(old_path, i), os.F_OK):
                file_util.copy_file(os.path.join(old_path, i), new_path)
                            
            else:
                self.__m_file_list.remove(i)
                