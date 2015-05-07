#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from xml.dom import minidom
# -> elementTree ?
import re

class XmlGW():
    """
    Class for xml objects
    . you want to create a xml wrapper for galaxy from any program help
    """
    def __init__(self, mybigdict, vprog, vtool):
        if "short_args" in mybigdict:
            self.short_args = mybigdict["short_args"]
        if "long_args" in mybigdict:
            self.long_args = mybigdict["long_args"]
        self.descrips = mybigdict["descrips_args"]
        self.general_descrip = mybigdict["general_descrip"]
        self.progfullname = mybigdict["progfullname"]
        self.progshortname = mybigdict["progshortname"]
        self.interpreter = mybigdict["interpreter"]
        if "vlist" in mybigdict:
            self.vlist = mybigdict["vlist"]
        else:
            self.vlist = None
        if "value" in mybigdict:
            self.value = mybigdict["value"]
        else:
            self.value = None
        if "output_files" in mybigdict:
            self.output_files = mybigdict["output_files"]
        else:
            self.output_files = None
        if "input_files" in mybigdict:
            self.input_files = mybigdict["input_files"]
        else:
            self.input_files = None
        if "exactcommand" in mybigdict:
            self.exactcommand = mybigdict["exactcommand"]
        else:
            self.exactcommand = None
        if "sub_elems" in mybigdict:
            self.sub_elems = mybigdict["sub_elems"]
        else:
            self.sub_elems = None
        self.vprog = vprog
        self.vtool = vtool




    def GenGalaxWrapper(self, fromwrapper):
        """
        Generate a galaxy wrapper from mybigdict, an extraction of the
        program help standard output.
        < Take a filename to write into [xml wrapper] for galaxy
        < Take the list of arguments informations extracted
        > Write to file given
        """
        j = []
        content = "<tool id=\""+self.progshortname+ "\" name=\""+ \
        self.progfullname+"\" version=\""+self.vtool+"\">"
        try:
            content += "\n"+" "*4+"<description>"+\
            self.general_descrip[0].strip()+"</description>"
        except:
            content += "\n"+" "*4+"<description></description>"
        content += "\n\n"+" "*4+"<requirements>\n"+" "*8+\
        "<requirement type=\"\">"+"</requirement>\n"+" "*4+\
        "</requirements>"
        content += "\n\n"+" "*4+"<command interpreter=\""+\
        self.interpreter+"\">"
        if self.exactcommand is not None:
            content += "\n"+" "*8+self.exactcommand
        else:
            content += "\n"+" "*8+self.progshortname
        content += "\n"+" "*4+"</command>"

        if fromwrapper is True:
            content += self.GenGalaxWrapperFromPise()
        else:
            content += "\n\n"+" "*4+"<inputs>"
            for i in range(len(self.short_args)):
                if self.input_files is not None:
                    content += "\n"+" "*8+"<param name=\""+\
                    self.input_files[i]+"\" type=\"data\" label=\""+\
                    self.input_files[i]+"\">"
                if self.vlist is not None:
                    if self.long_args[i] in self.vlist:
                        selectname = self.long_args[i]
                        content += "\n"+" "*8+"<param name=\""+\
                        selectname+"\" type=\"select\" label=\""+\
                        self.descrips[i]+"\">"
                        for idx in range(len(self.\
                        vlist[selectname]["value"])):
                            content += "\n"+" "*12+"<option value=\""+\
                            self.vlist[selectname]["value"][idx]+\
                            "\" >"+self.vlist[selectname]["text"][idx]+\
                            "</option>"
                if not re.search("output", self.descrips[i], re.I):
                    if self.long_args[i] != "":
                        name = re.sub('[!@#$-=]', '', self.long_args[i])
                        content += "\n"+" "*8+"<param name=\""+\
                        name+"\" type=\"\" label=\""+self.long_args[i]+\
                        "\" help=\""+self.descrips[i]+"\" />"
                    else:
                        name = re.sub('[!@#$-=]', '', self.short_args[i])
                        content += "\n"+" "*8+"<param name=\""+name+\
                        "\" type=\"\" label=\""+self.short_args[i]+\
                        "\" help=\""+self.descrips[i]+"\" />"
                else:
                    j.append(i)
            content += "\n"+" "*4+"</inputs>"
            content += "\n\n"+" "*4+"<outputs>"
            if self.output_files is not None:
                for i in range(len(self.output_files)):
                    content += "\n"+" "*8+"<data name=\""+\
                    self.output_files[i]+"\" label=\""+\
                    self.output_files[i]+"\" format=\"\" />"
            else:
                if len(j) == 0:
                    content += "\n"+" "*8+"<data name=\""+\
                    self.progshortname+"_out\" label=\"\" format=\""+\
                    "\"></data>"
                else:
                    for k in j:
                        if self.long_args[k] != "":
                            content += "\n"+" "*8+"<data name=\""+\
                            self.long_args[k]+"_out\" label=\""+\
                            self.descrips[k]+"\" help=\""+\
                            self.descrips[k]+"\" format=\"\"></data>"
                        else:
                            content += "\n"+" "*8+"<data name=\""+\
                            self.short_args[k]+"_out\" label=\""+\
                            self.descrips[k]+"\" help=\""+\
                            self.descrips[k]+"\" format=\"\"></data>"

            content += "\n"+" "*4+"</outputs>"
        content += "\n\n"+" "*4+"<help>"
        for gdescrip in self.general_descrip:
            if gdescrip is not None:
                # argparse.Filetype open files in binary mode.
                # need python 3 to open files with utf-8 codecs
                # directly from argparse
                try:
                    content += '\n'+gdescrip.encode('ascii', 'replace').\
                    strip()
                except:
                    content += '\n'+gdescrip.strip()
        content += "\n"+" "*4+"</help>"
        content += "\n</tool>"
        return content



    def GenGalaxWrapperFromPise(self):
        """
        When parsing argument from wrapper, the sub-elements are more
        precise. So the method is different from the help stdout parsing
        """
        subelems_content = ""
        if self.sub_elems is not None:
            # sub_elem is a dict containing lists
            if (len(self.sub_elems["infile"]) > 0) or \
            (len(self.sub_elems["sequence"]) > 0) or \
            (len(self.sub_elems["others"]) > 0):
                subelems_content += "\n"+" "*4+"<inputs>\n"
                for infile in self.sub_elems["infile"]:
                    subelems_content += " "*8+"<param format='txt' "+\
                    "name='"+infile["parameter"]["long_args"]+"' type"+\
                    "='data' label='"
                    if infile["parameter"].has_key("general_descrip"):
                        subelems_content += infile["parameter"]\
                        ["general_descrip"]
                    elif infile["parameter"].has_key("descrips_args"):
                        subelems_content += infile["parameter"]\
                        ["descrips_args"]
                    subelems_content += "' />\n"
                for sequence in self.sub_elems["sequence"]:
                    subelems_content += " "*8+"<param format='fasta' "+\
                    "name='"+sequence["parameter"]["long_args"]+"' "+\
                    "type='data' label='"
                    if sequence["parameter"].has_key("general_descrip"):
                        subelems_content += sequence["parameter"]\
                        ["general_descrip"]
                    elif sequence["parameter"].has_key("descrips_args"):
                        subelems_content += sequence["parameter"]\
                        ["descrips_args"]
                    subelems_content += "' />\n"
                for integer in self.sub_elems["integer"]:
                    subelems_content += " "*8+"<param "+\
                    "name='"+integer["parameter"]["long_args"]+"' "+\
                    "type='integer' label='"
                    if integer["parameter"].has_key("general_descrip"):
                        subelems_content += integer["parameter"]\
                        ["general_descrip"]
                    elif integer["parameter"].has_key("descrips_args"):
                        subelems_content += integer["parameter"]\
                        ["descrips_args"]
                    subelems_content += "' value='"
                    if integer["parameter"].has_key("value"):
                        if integer["parameter"]["value"] is not None:
                            subelems_content += integer["parameter"]\
                            ["value"]
                    subelems_content += "' />\n"
                for floatval in self.sub_elems["float"]:
                    subelems_content += " "*8+"<param "+\
                    "name='"+floatval["parameter"]["long_args"]+"' "+\
                    "type='float' label='"
                    if floatval["parameter"].has_key("general_descrip"):
                        subelems_content += floatval["parameter"]\
                        ["general_descrip"]
                    elif floatval["parameter"].has_key("descrips_args"):
                        subelems_content += floatval["parameter"]\
                        ["descrips_args"]
                    subelems_content += "' value='"
                    if floatval["parameter"].has_key("value"):
                        if floatval["parameter"]["value"] is not None:
                            subelems_content += floatval["parameter"]\
                            ["value"]
                    subelems_content += "' />\n"
                for string in self.sub_elems["string"]:
                    subelems_content += " "*8+"<param "+\
                    "name='"+string["parameter"]["long_args"]+"' "+\
                    "type='text' label='"
                    if string["parameter"].has_key("general_descrip"):
                        subelems_content += string["parameter"]\
                        ["general_descrip"]
                    elif string["parameter"].has_key("descrips_args"):
                        subelems_content += string["parameter"]\
                        ["descrips_args"]
                    subelems_content += "' value='"
                    if string["parameter"].has_key("value"):
                        if string["parameter"]["value"] is not None:
                            subelems_content += string["parameter"]\
                            ["value"]
                    subelems_content += "' />\n"
                    #'long_args','value'
                for others in self.sub_elems["others"]:
                    # other <=> unknown. I will consider that is a string
                    subelems_content += " "*8+"<param name='"+\
                    others["parameter"]["long_args"]+"' type='text' "
                    subelems_content += " value='"
                    if others["parameter"].has_key("value"):
                        subelems_content += others["parameter"]\
                        ["value"]
                    subelems_content += "' label='"
                    if others["parameter"].has_key("general_descrip"):
                        subelems_content += others["parameter"]\
                        ["general_descrip"]
                    elif others["parameter"].has_key("descrips_args"):
                        subelems_content += others["parameter"]\
                        ["descrips_args"]
                    subelems_content += "' size='30' />\n"
                subelems_content += " "*4+"</inputs>\n"
            for excl in self.sub_elems["excl"]:
                if excl["parameter"].has_key("value"):
                    if excl["parameter"]["value"] is not None:
                        vdef = excl["parameter"]["value"]
                    else:
                        vdef = ""
                else:
                    vdef = ""
                if excl["parameter"].has_key("vlist"):
                    subelems_content += "\n"+" "*4+"<param name='"+\
                    excl["parameter"]["long_args"]+"' type"+\
                    "='select' label='"
                    if excl["parameter"].has_key("descrips_args"):
                        subelems_content += excl["parameter"]["descrips_args"]
                    elif excl["parameter"].has_key("general_descrip"):
                        subelems_content += excl["parameter"]["general_descrip"]
                    subelems_content += "'>\n"
                    for key, option_val in enumerate(excl["parameter"]\
                    ["vlist"]["value"]):
                        subelems_content += " "*8
                        if option_val is not None:
                            subelems_content += "<option value='"+\
                            option_val+"'"
                            if option_val == vdef:
                                subelems_content += " selected='true'"
                            subelems_content += ">"
                            if excl["parameter"]["vlist"].has_key("text"):
                                if excl["parameter"]["vlist"]["text"]\
                                [key] is not None:
                                    subelems_content += excl["parameter"]\
                                    ["vlist"]["text"][key]
                            subelems_content += "</option>\n"
                    subelems_content += " "*4+"</param>\n"
            if len(self.sub_elems["outfile"]) > 0:
                subelems_content += "\n"+" "*4+"<outputs>\n"
                for outfile in self.sub_elems["outfile"]:
                    subelems_content += " "*8+"<data format='' "+\
                    "name='"+outfile["parameter"]["long_args"]+"'"+\
                    " type='data' label='"
                    if outfile["parameter"].has_key("general_descrip"):
                        subelems_content += outfile["parameter"]\
                        ["general_descrip"]
                    elif outfile["parameter"].has_key("descrips_args"):
                        subelems_content += outfile["parameter"]\
                        ["descrips_args"]
                    subelems_content += "' />\n"
                subelems_content += " "*4+"</outputs>\n"
                #'long_args','value'
            for paragraph in self.sub_elems["paragraph"]:
                subelems_content += "\n"+" "*4+"<!-- "
                if paragraph["parameter"].has_key("descrips_args"):
                    subelems_content += "Pise paragraph: "+\
                    paragraph["parameter"]["descrips_args"]+" \n"
                if paragraph["parameter"].has_key("general_descrip"):
                    subelems_content += "\n"+" "*4+\
                    paragraph["parameter"]["general_descrip"]+" \n"
                subelems_content += " -->\n"
        return subelems_content


