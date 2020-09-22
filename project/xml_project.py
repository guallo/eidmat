import amara
import os

class XML_Project:
    """ 
        Clase mediante la cual se realizan los procesos de lectura y escritura
        del xml que representa un proyecto.
    """
    def __init__(self): 
        """
            Constructor de la clase XML_Project.
        """        
        self.__doc = None
        
    def save_project(self, p_name, p_localization, p_m_list, p_date):
        """
            p_name: cadena de texto que representa el nombre del proyecto.
            p_localization: cadena de texto que representa el camino completo 
                            hasta la ubicacion del proyecto.
            p_m_list: lista que contiene el nombre de todos los archivos m 
                      incluidos en el proyecto.
            p_date: cadena de texto que representa la fecha en que fue creado 
                    el proyecto.            

            Metodo mediante el cual se guardan los datos del proyecto en 
            formato xml.
        """  
        self.__doc = amara.create_document()
        self.__doc.xml_append(self.__doc.xml_create_element(u'project'))
        self.__doc.project.xml_append(
            self.__doc.xml_create_element(u"name_project"))        
        self.__doc.project.name_project = u"%s"% (p_name)
        
        self.__doc.project.xml_append(
            self.__doc.xml_create_element(u"date_project"))        
        self.__doc.project.date_project = u"%s"% (p_date)
        
        self.__doc.project.xml_append(
            self.__doc.xml_create_element(u"VAR"))
        self.__doc.project.VAR = u"vars.var"
        
        self.__doc.project.xml_append(
            self.__doc.xml_create_element(u"HIST"))
        self.__doc.project.HIST = u"hist.txt"        
        
        self.__doc.project.xml_append(
            self.__doc.xml_create_element(u"SRC"))
        
        it = 0
        for i in p_m_list:
            self.__doc.project.SRC.xml_append(
                self.__doc.xml_create_element(u"m_file"))
            self.__doc.project.SRC.m_file[it] = u'%s' %(i)
            it += 1
            
        dir_ = os.path.join(p_localization, "build" + '.xml')
        f = open(dir_, 'w')        
        f.write(self.__doc.xml())
        f.close()        
        
    def open_project(self, p_localization):
        """
            p_localization: cadena de texto que representa el camino completo 
                            hasta la ubicacion del proyecto.

            Retorna: tres cadenas de texto (nombre del proyecto, fecha y hora 
                     de creacion del proyecto, lista de cadenas de texto con el
                     nombre de los archivos m).
           
            Metodo mediante el cual se leen los datos de un proyecto a partir 
            de su fichero xml asociado.
        """  
        xml = os.path.join(p_localization, "build.xml")
        self.__doc = amara.parse(xml)        
        name = str(self.__doc.project.name_project)
        date = str(self.__doc.project.date_project)
        aux = self.__doc.project.SRC.xml_xpath(u'm_file')        
        m_list = []
        for i in aux:
            m_list.append(str(i))
        return [name, date, m_list]