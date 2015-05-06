#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import sys
import pprint as pp
import re


def parseXml(xmlfile):
    ppty = pp.PrettyPrinter(indent=4,depth=10,width=40)
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    mybigdict = {}
    if root.tag == "pise":
        print("#"*20+" Wrapper Pise "+"#"*20)
        mybigdict = getPiseElement(tree)
        endtext = "#"*20+" [ End Wrapper Pise ] "+"#"*20
    elif root.tag == "tool":
        print("#"*20+" Wrapper Galaxy "+"#"*20)
        mybigdict = getGalaxyElement(tree,root)
        endtext = "#"*20+" [ End Wrapper Galaxy ]"+"#"*20
    else:
        sys.exit(" Unknown Xml file ")
    # initialize some key in the big dict to avoid some key exceptions.
    if not mybigdict.has_key("vprog"):
        mybigdict["vprog"] = "0"
    if not mybigdict.has_key("vtool"):
        mybigdict["vtool"] = "0"
    #ppty.pprint(mybigdict)
    #print(endtext)
    return mybigdict



def getGalaxyElement(tree,root):
    mybigdict = {}
    mybigdict["short_args"] = []
    mybigdict["long_args"] = []
    mybigdict["descrips_args"] = []
    mybigdict["general_descrip"] = []
    mybigdict["value"] = []
    mybigdict["output_files"] = []

    sub_elems = {}
    sub_elems['inputs'] = []
    sub_elems['outputs'] = []
    mybigdict['sub_elems'] = {}
    for elem in tree.iter():
        if elem.tag == "tool":
            if "version" in elem.attrib:
                mybigdict["vtool"] = elem.attrib["version"]
            if "name" in elem.attrib:
                mybigdict["progfullname"] = elem.attrib["name"]
            if "id" in elem.attrib:
                mybigdict["progshortname"] = elem.attrib["id"]
        elif elem.tag == "description":
            mybigdict["general_descrip"].append(elem.text)
        elif elem.tag == "command":
            mybigdict["exactcommand"] = elem.text
            if "interpreter" in elem.attrib:
                mybigdict["interpreter"] = elem.attrib["interpreter"]
        elif elem.tag == "help":
            mybigdict["general_descrip"].append(elem.text)
        elif elem.tag == "inputs":
            sub_elems["inputs"].append(parse_galaxy_sub_elem(elem))
            ## debug
            #print("elem" + str(ET.dump(elem)))
        elif elem.tag == "outputs":
            sub_elems["outputs"].append(parse_galaxy_sub_elem(elem))
        #mybigdict["progshortname"] = baseprog
    mybigdict['sub_elems'] = sub_elems
    # debug
    #print(type(mybigdict['sub_elems']["inputs"][0]))
    #pp.pprint(mybigdict['sub_elems']["inputs"][0])
    #print(type(mybigdict['sub_elems']["outputs"][0]))
    #pp.pprint(mybigdict['sub_elems']["outputs"][0])
    return mybigdict



def getPiseElement(tree):
    mybigdict = {}
    mybigdict["long_args"] = []
    mybigdict["descrips_args"] = []
    mybigdict["general_descrip"] = []
    sub_elems = {}
    sub_elems['others'] = []
    sub_elems['paragraph'] = []
    # inputs
    sub_elems['infile'] = []
    sub_elems['integer'] = []
    sub_elems['float'] = []
    sub_elems['sequence'] = []
    sub_elems['string'] = []
    # outputs
    sub_elems['outfile'] = []
    # could be both (input/output)...
    sub_elems['excl'] = []
    # unknown
    sub_elems['others'] = []
    mybigdict['sub_elems'] = {}
    for elem in tree.iter():
        if elem.tag == "versiontool":
            mybigdict["vtool"] = elem.text
        if elem.tag == "title":
            mybigdict["progshortname"] = elem.text
        elif elem.tag == "versionprog":
            mybigdict["vprog"] = elem.text
        elif elem.tag == "category":
            mybigdict["category"] = elem.text
        elif elem.tag == "command":
            mybigdict["progfullname"] = elem.text
        elif elem.tag == "description":
            mybigdict["general_descrip"].append(elem.text)
        elif elem.tag == "parameter":
            if elem.attrib["type"] == "Results" or \
            elem.attrib["type"] == "OutFile":
                sub_elems['outfile'].append(parse_pise_sub_elem(elem, \
                False))
            elif elem.attrib["type"] == "Sequence":
                sub_elems['sequence'].append(parse_pise_sub_elem(elem, \
                False))
            elif elem.attrib["type"] == "InFile":
                sub_elems['infile'].append(parse_pise_sub_elem(elem, \
                False))
            elif elem.attrib["type"] == "Integer":
                sub_elems['integer'].append(parse_pise_sub_elem(elem, \
                False))
            elif elem.attrib["type"] == "Float":
                sub_elems['float'].append(parse_pise_sub_elem(elem, \
                False))
            elif elem.attrib["type"] == "String":
                sub_elems['string'].append(parse_pise_sub_elem(elem, \
                False))
            elif elem.attrib["type"] == "Excl":
                sub_elems['excl'].append(parse_pise_sub_elem(elem, \
                False))
            elif elem.attrib["type"] == "Paragraph":
                sub_elems['paragraph'].append(parse_pise_sub_elem(elem,\
                True))
            else:
                sub_elems['others'].append(parse_pise_sub_elem(elem,\
                False))
        #mybigdict["progshortname"] = baseprog
    mybigdict["exactcommand"] = mybigdict["progfullname"] + " "
    #mybigdict["exactcommand"] = mybigdict["progfullname"] + " " + \
    #" ".join(mybigdict["short_args"])
    mybigdict['sub_elems'] = sub_elems
    return mybigdict



def parse_galaxy_sub_elem(elem):
    mydict = {}
    if elem.tag == "inputs":
        mydict[elem.tag] = {}
        mydict[elem.tag]["input_files"] = []
        mydict[elem.tag]["sequence"] = []
        mydict[elem.tag]["integer"] = []
        mydict[elem.tag]["float"] = []
        mydict[elem.tag]["text"] = []
        mydict[elem.tag]["boolean"] = []
        mydict[elem.tag]["long_args"] = []
        mydict[elem.tag]["integer"] = []
        # inputs in galaxy could be input file or any other input value
        # like input textbox...
        for subelem in elem.iter():
            if subelem.tag == "param":
                if "name" in subelem.attrib:
                    name = subelem.attrib["name"]
                    mydict[elem.tag][name] = {}
                    mydict[elem.tag][name]["long_args"] = name
                else:
                    # Is that possible ?
                    print("An input sub element has no name " + \
                    str(ET.dump(subelem)))
                    continue
                if "help" in subelem.attrib:
                    mydict[elem.tag][name]["descrips_args"] = subelem.\
                    attrib["help"]
                if "label" in subelem.attrib:
                    mydict[elem.tag][name]["prompt"] = subelem.\
                    attrib["label"]
                if "value" in subelem.attrib:
                    # value galaxy <=> vdef pise
                    mydict[elem.tag][name]["value"] = subelem.\
                    attrib["value"]
                if subelem.attrib["type"] == "select":
                    mydict[elem.tag][name]["vlist"] = {}
                    mydict[elem.tag][name]["vlist"]["value"] = []
                    mydict[elem.tag][name]["vlist"]["text"] = []
                    for elemval in subelem.findall("option"):
                        if "selected" in elemval.attrib:
                            mydict[elem.tag][name]["value"] = elemval.\
                            attrib["value"]
                        mydict[elem.tag][name]["vlist"]["value"].append(\
                        elemval.attrib["value"])
                        mydict[elem.tag][name]["vlist"]["text"].append(\
                        elemval.text)
                elif subelem.attrib["type"] == "data" or \
                subelem.attrib["type"] == "file" or \
                subelem.attrib["type"] == "ftpfile" :
                    if subelem.attrib["format"] == "fasta":
                        mydict[elem.tag][name]["sequence"] = True
                    else:
                        mydict[elem.tag][name]["input_files"] = True
                elif subelem.attrib["type"] == "integer":
                    mydict[elem.tag][name]["integer"] = True
                elif subelem.attrib["type"] == "float":
                    mydict[elem.tag][name]["float"] = True
                elif subelem.attrib["type"] == "text":
                    mydict[elem.tag][name]["string"] = True
                elif subelem.attrib["type"] == "boolean":
                    mydict[elem.tag][name]["boolean"] = True
            elif subelem.tag == "conditional" or subelem.tag == "when":
                print("A conditional/when tag has been detected! "+\
                "There is no equivalent in Pise!")

    elif elem.tag == "outputs":
        mydict[elem.tag] = {}
        mydict[elem.tag]["long_args"] = []
        for subelem in elem.iter():
            if subelem.tag == "data":
                if "name" in subelem.attrib:
                    name = subelem.attrib["name"]
                    mydict[elem.tag][name] = {}
                    mydict[elem.tag][name]["long_args"] = name
                else:
                    print("An output sub element has no name " + \
                    str(ET.dump(subelem)))
                    continue
            if "format" in subelem.attrib:
                # format is text or exotic type from datatypes_conf.xml
                # file (sam, bam, maf, acedb, qual...)
                # Anyway it is often text... Except some binaries :(
                # So I will consider it is text
                mydict[elem.tag][name]["format"] = subelem.\
                attrib["format"]
            if "from_work_dir" in subelem.attrib:
                mydict[elem.tag][name]["from_work_dir"] = subelem.\
                attrib["from_work_dir"]
            if "label" in subelem.attrib:
                mydict[elem.tag][name]["descrips_args"] = subelem.\
                attrib["label"]
            if "metadata_source" in subelem.attrib:
                mydict[elem.tag][name]["metadata_source"] = subelem.\
                attrib["metadata_source"]

    return mydict



def parse_pise_sub_elem(elem, paragraph):
    mydict = {}
    mydict[elem.tag] = {}
    try:
        name = elem.find("name").text
        mydict[elem.tag]["long_args"] = name
    except:
        pass
    for subelem in elem.iter():
        if subelem.tag == "comment":
            if subelem.find("value") is not None:
                for elemval in subelem.findall("value"):
                    mydict[elem.tag]["general_descrip"] = elemval.text
        elif subelem.tag == "prompt":
            mydict[elem.tag]["descrips_args"] = subelem.text
        if paragraph is False:
            if subelem.tag == "vdef":
                value = subelem.find("value").text
                mydict[elem.tag]["value"] = value
            if subelem.tag == "filenames":
                mydict[elem.tag]["outfile"] = subelem.text
            elif subelem.tag == "format":
                if subelem.find("code") is not None:
                    code = subelem.find("code").text.replace('=',' ')
                    code = code.split()
                    for the_arg in code:
                        if the_arg.startswith("-"):
                            mydict[elem.tag]["short_args"] = the_arg
            elif subelem.tag == "vlist":
                mydict[elem.tag]["vlist"] = {}
                mydict[elem.tag]["vlist"]["value"] = []
                mydict[elem.tag]["vlist"]["text"] = []
                for vlistelem in subelem.iter():
                    if vlistelem.tag == "value":
                        mydict[elem.tag]["vlist"]["value"].\
                        append(vlistelem.text)
                    elif vlistelem.tag == "label":
                        mydict[elem.tag]["vlist"]["text"].\
                        append(vlistelem.text)
    return mydict
