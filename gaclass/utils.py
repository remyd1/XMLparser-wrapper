#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import subprocess
import os
#import traceback
import sys
import simplejson as json

from ga_parser_class import *


def ConstructMyGaParser(jsondata):
    """
    JsonData class called to construct my object
    < Take jsondata
    > Return a List of object JsonData
    """
    ListeJsonData = []
    annotation = jsondata['annotation']
    workflow_name = jsondata['name']
    nb_steps = len(jsondata['steps'])

    for i in range(nb_steps):
        step_id = jsondata['steps'][str(i)]['id']
        tname = jsondata['steps'][str(i)]['name']
        ttool_id = jsondata['steps'][str(i)]['tool_id']
        ttype = jsondata['steps'][str(i)]['type']
        ttool_version = jsondata['steps'][str(i)]['tool_version']
        tinput_name = jsondata['steps'][str(i)]['inputs']
        toutput_name = jsondata['steps'][str(i)]['outputs']
        tuser_output_name = jsondata['steps'][str(i)]['user_outputs']
        ttool_state = jsondata['steps'][str(i)]['tool_state']
        ttool_errors = jsondata['steps'][str(i)]['tool_errors']

        ListeJsonData.append(JsonData(workflow_name, annotation, step_id, \
        tname, ttool_id, ttype, ttool_version, tinput_name, toutput_name, \
        tuser_output_name, ttool_state, ttool_errors))

    return ListeJsonData



def getjson(infile):
    try:
        data = infile.read()
        infile.close()
        #if not limited to 4500 characters ?
        try:
            jsondata = json.loads(data)
            return jsondata
        except:
            sys.exit("Not a json file !! Bye bye...")
    #except Exception as e:
        #top = traceback.extract_stack()[-1]
        #print(', '.join([type(e).__name__, os.path.basename(top[0]), \
        #str(top[1])]))
    except:
        sys.exit("Your file is not a text file readable !! Bye "+\
        "bye...")



def getworkflowparams(ListeJsonData):
    """
    < Get workflow parameters if it is possible... (advanced edit option
    enable on workflow creation)
    """
    aff = True
    params_tools = []
    for JsonData in ListeJsonData:
        step_id = JsonData.step_id
        tname = JsonData.tname
        ttool_id = JsonData.ttool_id
        ttype = JsonData.ttype
        ttool_version = JsonData.ttool_version
        tinput_name = JsonData.tinput_name
        toutput_name = JsonData.toutput_name
        tuser_output_name = JsonData.tuser_output_name
        ttool_state = JsonData.ttool_state
        ttool_errors = JsonData.ttool_errors

        if ttool_errors is None:
            print("id : "+str(step_id))
            print("tool name : "+tname)
            if ttool_id is not None:
                print("tool_id : " +ttool_id)
            print("type : " +ttype)
            if ttool_version is not None:
                print("version : " +ttool_version)
            if tinput_name:
                print("Input : ")
                JsonData.ParseInOutVal(tinput_name, "input", aff)
            if toutput_name:
                print("Output : ")
                JsonData.ParseInOutVal(toutput_name, "output", aff)
            if ttype == "tool":
                print("#"*40)
                #params_tools = ttool_state.replace("\\","")
                #params_tools = eval(ttool_state)
                params_tools = json.loads(ttool_state)
                JsonData.ParseParams(params_tools, aff)
            print("\n\n")
        else:
            print("This tool is in error state" +tname)



def getinterpreter(filetype):
    """
    Try to get the interpreter from filetype
    < Get the content of the "file" linux command on a specific
    executable
    > Return the interpreter
    """
    if re.search("Bourne-Again shell", filetype, flags=re.I):
        interpreter = 'bash'
    elif re.search("python", filetype, flags=re.I):
        interpreter = 'python'
    elif re.search("perl", filetype, flags=re.I):
        interpreter = 'perl'
    elif re.search("Tenex C shell", filetype, flags=re.I):
        interpreter = 'tcsh'
    elif re.search("C shell", filetype, flags=re.I):
        interpreter = 'csh'
    elif re.search("Korn shell", filetype, flags=re.I):
        interpreter = 'ksh'
    elif re.search("zsh", filetype, flags=re.I):
        interpreter = 'zsh'
    elif re.search("PHP", filetype, flags=re.I):
        interpreter = 'php'
    else:
        interpreter = 'sh'
    return interpreter



def GetProgHelpParam(execline, record_separator, field_separator, fromfile):
    """
    Try to parse the Help section of a program stdout
    < Get a command line to execute [Help section of this program]
    < Get one or two delimiter (eventually a regexp) for RS and FS
    > Return the list of short/(eventually)long arguments
    > Return eventually a description of each argument and a general
    description of the program
    > Return the interpreter used
    > Return the program basename
    """
    short_args = []
    long_args = []
    descrips = []
    general_descrip = []
    interpreter = ""
    # initialize dialup with undefined option
    DIALS = "U"

    first_message = "\n   Try [A]utomatic search (ok for well "+\
    "formatted help). If there is short (e.g. -f) and long options "+\
    "available (e.g. --file), you will have to choose [M]anual, "+\
    "to check each output.\n If you have only [L]ong options, e.g. "+\
    "--myoption, choose [L]ong options.\n" +\
    " If you have only [S]hort options, choose 'S'.\n"+\
    " Please note that [A]utomatic search could overwrite your field "+\
    "separator.\n" +\
    " [M]anual choices also allow you to add general description.\n"+\
    "    [A]|L|S|M:"

    each_dial = "#"*12+"\n   Try [A]utomatic search (could overwrite"+\
    " your separator) ? Or, is it a [L]ong or a [S]hort Option (the "+\
    "important part is the beginning of the line) ? Or add this "+\
    "content to the general [D]escription ? Or [I]gnore ? \n"+\
    "    [A]|L|S|D|I:"

    sep_r = re.compile(record_separator, flags=re.U)
    sep_f = re.compile(field_separator, flags=re.U)
    fs = field_separator

    std_help_pattern = re.compile(r"^(?P<short>\w+,?" + fs + ")?"+\
    "(--?(?P<long>\w+([-=]?(\w+)?)*)" + fs + ")?(?P<descrip>((.+"+\
    "(\n|\r\n?)?)*))", re.M|re.U|re.I)

    if fromfile is False:
        print("Try to parse default help output from program '%s'" \
        % execline)
        # some problems with "<" or ">" because we need to generate a xml
        # content
        results = sanitize(sendcommand(execline))
    else:
        results = execline
    print("\n\n"+"#"*25+"\n")
    print("Output that should be parse : \n\n"+"#"*25+"\n %s" % results)
    print("\n"+"#"*25+"\n\n")

    generic_opt = raw_input(first_message)

    argsarray = re.split(sep_r, results)

    print("\n\n"+"#"*25+"\n\n")
    for arg in argsarray:
        #the_option = arg.split()
        the_option = re.split(sep_f, arg)
        """
        generic_opt is automatic -> Same as bellow without asking
        anything
        """
        if generic_opt == "A" or generic_opt == "":
            # for debug: some search are bad because of a wrong
            # field separator
            #print arg
            content_in_arg = std_help_pattern.search(arg)
            results = content_in_arg.groupdict()
            if results:
                if results['short']:
                    short_o = "-" + results['short'].strip(' ,;')
                    short_args.append(short_o)
                else:
                    short_args.append("")
                if results['long']:
                    long_o = "--" + results['long'].strip(' ,;')
                    long_args.append(long_o)
                else:
                    long_args.append("")
                if results['descrip']:
                    descrips.append(results['descrip'])
                else:
                    descrips.append("")
            continue
        if generic_opt == "M":
            print("\n\n"+"#"*12+"\n")
            print(arg)
            print("\n")
            DIALS = raw_input(each_dial)
            if DIALS == "A" or DIALS == "" or DIALS == "U":
                content_in_arg = std_help_pattern.search(arg)
                results = content_in_arg.groupdict()
                if results:
                    if results['short']:
                        short_o = "-" + results['short'].strip(' ,;')
                        short_args.append(short_o)
                    else:
                        short_args.append("")
                    if results['long']:
                        long_o = "--" + results['long'].strip(' ,;')
                        long_args.append(long_o)
                    else:
                        long_args.append("")
                    if results['descrip']:
                        descrips.append(results['descrip'])
                    else:
                        descrips.append("")
                continue
        if DIALS != "D" and DIALS != "I":
            try:
                first_opt = the_option[0]
                if len(the_option) >= 3:
                    short_args.append("-"+first_opt)
                    long_args.append(the_option[1])
                    descrips.append(" ".join(the_option[2:]))
                elif len(the_option) == 2:
                    if(generic_opt == "L") or (DIALS == "L"):
                        short_args.append("")
                        long_args.append(first_opt)
                        descrips.append(" ".join(the_option[1:]))
                    elif(generic_opt == "S") or (DIALS == "S"):
                        short_args.append("-"+first_opt)
                        long_args.append("")
                        descrips.append(" ".join(the_option[1:]))
                else:
                    descrips.append(" ".join(the_option[1:]))
                    long_args.append("")
                    short_args.append("")
            except:
                print("Warning: Bad field separator ?!!")
        elif DIALS == "D":
            general_descrip.append(arg)
        else:
            DIALS = "U" #undefined
    interpreter_list = ["bash", "csh", "ksh", "sh", "python", "php", \
    "perl", "tcsh", "zsh", "java"]
    progname = execline.split()[0]
    # check if progname is an iterpreter or the program itself (executable)
    for arg0 in interpreter_list:
        if progname == arg0:
            # check for dash in next args to see if it is option or
            # the program name itself
            for next_arg in execline.split()[1:]:
                if next_arg[0] != "-":
                    progname = next_arg
                    break
            interpreter = arg0
    if interpreter == "":
        filetype = sendcommand("file "+progname)
        interpreter = getinterpreter(filetype)
    progshortname = os.path.basename(progname)
    print(progshortname)
    print(interpreter)

    print("\n"+"#"*25+"\n")
    for value in short_args:
        print("\t"+value)
    print("\n"+"#"*25+"\n")
    for long_value in long_args:
        print("\t"+long_value)
    print("\n"+"#"*25+"\n")
    for descrip in descrips:
        print("\t"+descrip)
    print("\n"+"#"*25+"\n")
    for g_descrip in general_descrip:
        print("\t"+g_descrip)

    mybigdict = {}
    mybigdict["short_args"] = []
    mybigdict["short_args"] = short_args
    mybigdict["long_args"] = []
    mybigdict["long_args"] = long_args
    mybigdict["descrips_args"] = []
    mybigdict["descrips_args"] = descrips
    mybigdict["general_descrip"] = []
    mybigdict["general_descrip"] = general_descrip
    mybigdict["progfullname"] = progname
    mybigdict["progshortname"] = progshortname
    mybigdict["interpreter"] = interpreter
    ##for debug
    #print(mybigdict)

    return mybigdict



def GetVersion(progfullname):
    """
    Try to get version for the program
    and ask version for the tool to create
    """
    vprogoutput = sendcommand(progfullname+ \
    " --version")
    vprog = re.search(r"\d+(\.\d+)*\s", vprogoutput, \
    re.M|re.U)
    if vprog:
        print("Find version:"+vprog.group().encode('utf8'))
        vprog = vprog.group().encode('utf8')
    else:
        print("Could not retrieve version information for "+\
        "program "+progfullname)
        getvprog = raw_input("Please tell me your program "+\
        "version :")
        vprog = getvprog
    vtool = raw_input("Please tell me your OnlineTool "+\
    "version :")
    return (vprog, vtool)



def pisewrapper(ListeJsonData, fname):
    """
    Galaxy file transformer to pise wrapper (xml)
    < Take the content of the ga file (json/galaxy format)
    > Return an xml file (pise format) in the same directory of ga file
    file.
    """
    writewn = False
    if type(fname) is str:
        xmlfile = open(fname, "w")
    else:
        xmlfile = fname
    In = []
    Out = []
    aff = False
    param_tools = []
    headers = "<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>\n"+\
    "<!DOCTYPE pise SYSTEM \"PARSER/pise.dtd\">\n"

    for JsonData in ListeJsonData:
        #print(str(JsonData))
        wn = JsonData.wn
        ann = JsonData.ann
        step_id = JsonData.step_id
        tname = JsonData.tname
        ttool_id = JsonData.ttool_id
        ttype = JsonData.ttype
        ttool_version = JsonData.ttool_version
        tinput_name = JsonData.tinput_name
        toutput_name = JsonData.toutput_name
        tuser_output_name = JsonData.tuser_output_name
        ttool_state = JsonData.ttool_state
        ttool_errors = JsonData.ttool_errors

        if ttool_errors is None:
            if tinput_name:
                In = JsonData.ParseInOutVal(tinput_name, "input", aff)
            if toutput_name:
                Out = JsonData.ParseInOutVal(toutput_name, "output", aff)
        if ttype == "tool":
            params_tools = json.loads(ttool_state)
            opts = JsonData.ParseParams(params_tools, aff)

        #headers +
        #parameter type infile
        if writewn == False:
            headers += '<pise>\n'+\
            '<head>\n'+\
            ' '*2 +'<title>'+wn+'</title>\n'+\
            ' '*2 +'<description>'+ann+'</description>\n'+\
            ' '*2 +'<authors>ParserConverterXML</authors>\n'+\
            '</head>\n'+\
            ' '*2 +'<command>'+wn+'</command>\n'+\
            ' '*2 +'<parameters>\n'
            xmlfile.write(headers)
            writewn = True


        xmlfile.write(' '*10 +'<parameter type="InFile" ismandatory="'+\
        '1">\n')
        xmlfile.write(' '*12 +'<name>'+tname+'</name>\n')
        xmlfile.write(' '*10 +'</parameter>\n')

        xmlfile.write(' '*10 +'<parameter type="InFile" ismandatory="'+\
        '1">\n')
        xmlfile.write(' '*12 +'<name>'+str(tinput_name)+'</name>\n')
        xmlfile.write(' '*10 +'</parameter>\n')

    footers = ' '*2 +'</parameters>\n'+\
    '</pise>'
    xmlfile.write(footers)
    xmlfile.close()



def sanitize(string):
    charsdict = {
    '<': '&lt;',
    '>': '&gt;',
    '&': '&amp;',
    '"': '&quot;'
    }
    for k, v in charsdict.iteritems():
        string = string.replace(k, v)
    return string



def sendcommand(cmd):
    """
    Take a shell bash command
    Return the stdout value for a pipe subprocess
    """
    proc = subprocess.Popen("bash", shell=True, stdin=subprocess.PIPE, \
    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.communicate(cmd)[0]
