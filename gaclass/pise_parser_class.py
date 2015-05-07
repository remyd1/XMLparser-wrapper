#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from xml.dom import minidom
# -> elementTree ?

import pprint as pp
#from utils import sanitize


class XmlPise():
    """
    Class for xml objects
    There is two possibilities :
    . you want to parse a pise xml wrapper
    . you want to create a xml tool for galaxy from xml pise wrapper
    """
    def __init__(self, mybigdict, vprog, vtool, catname, nb_paraph):
        if "short_args" in mybigdict:
            self.short_args = mybigdict["short_args"]
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
        self.catname = catname
        self.nb_paraph = nb_paraph



    def GenParams(self, short_args, long_args, descrips):
        """
        Generate some parapragh for Pise Xml wrapper
        """
        param = ''
        for key, s_o in enumerate(short_args):
            """
            s_o is for 'short_options'
            """
            param += '\n'+' '*10+'<parameter '
            param += 'type="Integer|Excl|Switch|Float|String|Results'
            param += '|InFile" ismandatory="1" iscommand="1" '
            param += 'issimple="1" ishidden="1"'
            param += '>\n'
            param += ' '*12+'<name>'+long_args[key]+'</name>\n'
            param += ' '*12+'<attributes>\n'
            param += ' '*14+'<prompt>'+long_args[key]+'</prompt>\n'
            param += ' '*14+'<format>\n'
            param += ' '*16+'<language>perl</language>\n'
            param += ' '*16+'<code>(defined $value)? " '+s_o+\
            ' $value":""</code>\n'
            param += ' '*14+'</format>\n'
            param += ' '*14+'<comment>\n'
            #param += ' '*16+'<value>'+descrips[key].decode('utf-8').\
            #encode('ascii', 'replace').strip()+'</value>\n'
            param += ' '*16+'<value>'+descrips[key].strip()+'</value>\n'
            param += ' '*14+'</comment>\n'
            param += ' '*14+'</comment>\n'
            param += ' '*14+'<vdef><value></value></vdef>\n'

            """
            Select / radiobox
            """
            param += ' '*14+'<!--vlist>\n'
            param += ' '*16+'<value></value><label></label>\n'
            param += ' '*16+'<value></value><label></label>\n'
            param += ' '*14+'</vlist-->\n'
            """
            Filenames are used by Results type to display the results
            files after processing
            """
            param += ' '*14+'<!--filenames></filenames-->\n'
            param += ' '*14+'<group>'+str(key)+'</group>\n'
            param += ' '*12+'</attributes>\n'
            param += ' '*10+'</parameter>\n\n'

        return param



    def GenParaph(self):
        the_paraph = 1
        paraphs = ""
        while the_paraph <= self.nb_paraph:
            paraph_group = str(the_paraph)
            paraph_txt = '\n\n'
            paraph_txt += ' '*4 +'<parameter type="Paragraph">\n'
            paraph_txt += ' '*6 +'<paragraph>\n'
            paraph_txt += ' '*8 +'<name>Your Paragraph Name</name>\n'
            paraph_txt += ' '*8 +'<prompt>Your Paragraph Prompt'\
            +'</prompt>\n'
            paraph_txt += ' '*8 +'<group>'+paraph_group+'</group>\n'
            paraph_txt += ' '*8 +'<parameters>\n'
            """
            Specific things go here
            """

            paraph_txt += '\n<!--... Paste parameter here ...-->\n\n'

            """
            close parapragh
            """
            paraph_txt += ' '*8 +'</parameters>\n'
            paraph_txt += ' '*6 +'</paragraph>\n'
            paraph_txt += ' '*4 +'</parameter>\n\n'

            paraphs += paraph_txt
            the_paraph += 1

        return paraphs



    def GenPiseWrapperFromGW(self):
        """
        When parsing argument from wrapper, the sub-elements are more
        precise. So the method is different from the help stdout parsing
        """
        subelems_content = ""
        group = 0
        #pp.pprint(self.sub_elems)
        if self.sub_elems is not None:
            # sub_elem is a dict containing lists
            if len(self.sub_elems["inputs"]) > 0:
                #print(type(self.sub_elems["inputs"]))
                for inputs in self.sub_elems["inputs"]:
                    if not inputs.has_key("inputs"):
                        continue
                    for the_input in inputs["inputs"].itervalues():
                        #print(type(the_input))
                        #pp.pprint(the_input)
                        if the_input:
                            group = group + 1
                            # check the type of input
                            subelems_content += ' '*4
                            if the_input.has_key("sequence"):
                                subelems_content += "<parameter type='"+\
                                "Sequence'>\n"
                            elif the_input.has_key("input_files"):
                                subelems_content += "<parameter type='"+\
                                "InFile'>\n"
                            elif the_input.has_key("integer") or \
                            the_input.has_key("boolean"):
                                subelems_content += "<parameter type='"+\
                                "Integer'>\n"
                            elif the_input.has_key("float"):
                                subelems_content += "<parameter type='"+\
                                "Float'>\n"
                            else:
                                subelems_content += "<parameter type='"+\
                                "String'>\n"
                            subelems_content += ' '*6
                            try:
                                subelems_content += "<name>"+\
                                the_input["long_args"]+"</name>\n"
                            except:
                                print("An input has no name! ")
                                pp.pprint(the_input)
                                continue
                            subelems_content += ' '*6
                            subelems_content += "<attributes>\n"
                            subelems_content += ' '*8
                            subelems_content += "<group>"+str(group)+\
                            "</group>\n"
                            if the_input.has_key("prompt"):
                                subelems_content += ' '*8
                                subelems_content += "<prompt>"+\
                                the_input["prompt"]+"</prompt>\n"
                            subelems_content += ' '*8+"<format>\n"
                            subelems_content += ' '*10+"<language>perl"+\
                            "</language>\n"
                            subelems_content += ' '*10+"<code> $value "+\
                            "</code>\n"
                            subelems_content += ' '*8+"</format>\n"
                            if the_input.has_key("descrips_args"):
                                subelems_content += ' '*8
                                subelems_content += "<comment>\n"
                                subelems_content += ' '*10+"<value>"+\
                                the_input["descrips_args"]+"</value>\n"
                                subelems_content += ' '*8+"</comment>\n"
                            if the_input.has_key("vlist"):
                                subelems_content += ' '*8
                                subelems_content += "<vlist>\n"
                                for key, vlist_value in \
                                enumerate(the_input["vlist"]["value"]):
                                    subelems_content += ' '*10+"<value>"+\
                                    vlist_value+"</value>\n"
                                    try:
                                        vlist_label = the_input["vlist"]\
                                        ["text"][key]
                                        subelems_content += ' '*10+\
                                        "<label>"+vlist_label+"</label>\n"
                                    except:
                                        print("No label for vlist value: "+\
                                        vlist_value)
                                subelems_content += ' '*8+"</vlist>\n"
                            if the_input.has_key("value"):
                                subelems_content += ' '*8
                                subelems_content += "<vdef>\n"
                                subelems_content += ' '*10+"<value>"+\
                                the_input["value"]+"</value>\n"
                                subelems_content += ' '*8+"</vdef>\n"
                            subelems_content += ' '*6+"</attributes>\n"
                            subelems_content += ' '*4
                            subelems_content += "</parameter>\n\n"
            if len(self.sub_elems["outputs"]) > 0:
                for outputs in self.sub_elems["outputs"]:
                    if not outputs.has_key("outputs"):
                        continue
                    for the_output in outputs["outputs"].itervalues():
                        if the_output is not None:
                            group = group + 10
                            subelems_content += ' '*4
                            subelems_content += "<parameter type='"+\
                            "Results'>\n"
                            subelems_content += ' '*6
                            try:
                                subelems_content += "<name>"+\
                                the_output["long_args"]+"</name>\n"
                            except:
                                print("An output has no name! ")
                                pp.pprint(the_output)
                                continue
                            subelems_content += ' '*4
                            subelems_content += ' '*6+"<attributes>\n"
                            subelems_content += ' '*8+"<filenames>*."+\
                            the_output["format"].strip(".")+\
                            "</filenames>\n"
                            subelems_content += ' '*8+"<group>"+\
                            str(group)+"</group>\n"
                            if the_output.has_key("descrips_args"):
                                subelems_content += ' '*8+"<prompt>"+\
                                the_output["descrips_args"]+"</prompt>\n"
                            subelems_content += ' '*6+"</attributes>\n"
                            subelems_content += ' '*4+"</parameter>\n\n"

                return subelems_content






    def createXml(self, fromwrapper):
        """
        Generate the Pise XML file
        """
        content = ""
        begin = '<?xml version="1.0" encoding="ISO-8859-1"?>\n'
        begin += '<!DOCTYPE pise SYSTEM "PARSER/pise.dtd">\n'
        begin += '<pise>\n'
        begin += ' '*2 +'<head>\n'
        begin += ' '*4 +'<title>'+self.progfullname+'</title>\n'
        description = ' '*4 +'<description>'
        for descrip in self.general_descrip:
            description += descrip
        description += '</description>\n'
        endheader = ' '*4 +'<category>'+self.catname+'</category>\n'+\
        ' '*4 +'<versionprog>'+self.vprog.strip()+'</versionprog>\n'+\
        ' '*4 +'<versiontool>'+self.vtool+'</versiontool>\n'+\
        ' '*2 +'</head>\n'
        beginbody = ' '*2+'<command>'+self.progshortname+'</command>\n'
        beginbody += ' '*2+'<parameters>\n'

        footer = ' '*2+'</parameters>\n'
        footer += '</pise>\n'
        content = self.GenParaph()
        if self.exactcommand is not None:
            content += "<!-- Here you have a list of arguments for the"+\
            "Unix exact command line (you could try to put these "+\
            "values into <code> ...  </code>):\n"
            exactcommand_args = self.exactcommand.split()
            for exactcommand_arg in exactcommand_args:
                content += " "*4+exactcommand_arg+"\n"
            content += "-->\n\n"
        if fromwrapper is True:
            content += self.GenPiseWrapperFromGW()
        else:
            param = self.GenParams(self.short_args,\
            self.long_args, self.descrips)
            content += param

        return_content = begin + description + endheader + beginbody

        return_content += '\n<!-- Put following parameters in the'+\
        ' paragraph you want (at the end of this file) -->\n'

        return_content += '<!-- Some explanations about parameters:'+\
        '\n - "ishidden"=1 means that it will not appear in '+\
        '{tool}-simple.html'+\
        '\n - "ismandatory"=1 means that this option is required'+\
        '\n - "issimple"=1 means ...'+\
        '\n - "iscommand"=1 means it is concatenated to the main '+\
        'command'+\
        '\n - type="Switch" is for checkbox'+\
        '\n - type="Excl" is for radio/select (one choice)'+\
        '\n - type="InFile" is to submit a file or paste a sequence'+\
        '\n - <vlist> could be used for select box or radio button'+\
        '\n - <vdef> is the default value for your option'+\
        '\n - <filenames> are used by Results type '+\
        'to display the results files after processing'+\
        'For other options, take a look at the Pise.dtd file -->\n\n'

        return_content += content
        return_content += footer
        return return_content
