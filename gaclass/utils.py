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

        ListeJsonData.append(JsonData(workflow_name,annotation,step_id,\
        tname,ttool_id,ttype,ttool_version,tinput_name,toutput_name, \
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
        #print ', '.join([type(e).__name__, os.path.basename(top[0]), str(top[1])])
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

        if(ttool_errors is None):
            print "id : "+str(step_id)
            print "tool name : "+tname
            if(ttool_id is not None):
                print "tool_id : " +ttool_id
            print "type : " +ttype
            if(ttool_version is not None):
                print "version : " +ttool_version
            if(tinput_name):
                print "Input : "
                JsonData.ParseInOutVal(tinput_name,"input",aff)
            if(toutput_name):
                print "Output : "
                JsonData.ParseInOutVal(toutput_name,"output",aff)
            if(ttype == "tool"):
                print "#"*40
                #params_tools = ttool_state.replace("\\","")
                #params_tools = eval(ttool_state)
                params_tools = json.loads(ttool_state)
                JsonData.ParseParams(params_tools, aff)
            print "\n\n"
        else:
            print "This tool is in error state" +tname



def getinterpreter(filetype):
    """
    Try to get the interpreter from filetype
    < Get the content of the "file" linux command on a specific
    executable
    > Return the interpreter
    """
    if re.search("Bourne-Again shell",filetype,flags=re.I):
        interpreter = 'bash'
    elif re.search("python",filetype,flags=re.I):
        interpreter = 'python'
    elif re.search("perl",filetype,flags=re.I):
        interpreter = 'perl'
    elif re.search("Tenex C shell",filetype,flags=re.I):
        interpreter = 'tcsh'
    elif re.search("C shell",filetype,flags=re.I):
        interpreter = 'csh'
    elif re.search("Korn shell",filetype,flags=re.I):
        interpreter = 'ksh'
    elif re.search("zsh",filetype,flags=re.I):
        interpreter = 'zsh'
    elif re.search("PHP",filetype,flags=re.I):
        interpreter = 'php'
    else:
        interpreter = 'sh'
    return interpreter



def GetProgHelpParam(execline,delimiter):
    """
    Try to parse the Help section of a program stdout
    < Get a command line to execute [Help section of this program]
    < Get a delimiter (eventually a regexp)
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
    DIALS = "U" #undefined option
    std_help_pattern = re.compile(r"^((?P<short>\w{1})?,?(\s)+"+\
    "(--?(?P<long>(\w)+)(\s)+)?)?(?P<descrip>((.+(\n|\r\n?)?)"+\
    "*))", re.M|re.U|re.I)

    print "Try to parse default help output from program '%s'" \
    % execline
    results = sendcommand(execline)
    print "Output that should be parse : \n\n %s" % results

    print "#"*25+"\n\n"+"#"*25
    generic_opt = raw_input("Try [A]utomatic search (ok for well "+\
    "formatted help stdout like 'ls --help'). If there is short"+\
    " and long options available, you will have to choose '[M]ixes' "+\
    "to check each output. Otherwise, if you have _only_ [-]short + "+\
    "[--]long options + description behind, choose 'L' (for [L]ong). "+\
    "If you have only [S]hort options, choose 'S'. [M]ixes choices "+\
    "allow also you to add general description.\n [A]|L|S|M:")
    sep = re.compile(delimiter,flags=re.U)
    argsarray = re.split(sep,results)
    for arg in argsarray:
        the_option = arg.split()
        """
        generic_opt is automatic -> Same as bellow without asking
        anything
        """
        if generic_opt == "A" or generic_opt == "":
            content_in_arg = std_help_pattern.search(arg)
            results = content_in_arg.groupdict()
            if results:
                if results['short']:
                    short_args.append("-"+results['short'])
                if results['long']:
                    long_args.append("--"+results['long'])
                else:
                    long_args.append("")
                if results['descrip']:
                    descrips.append(results['descrip'])
            continue
        if generic_opt == "M":
            print arg
            DIALS = raw_input("Try [[A]]utomatic search ? There is a "+\
            "[L]ong / [S]hort Option ? Or add this content to "\
            +"general [D]escription or [I]gnore ? [A]|L|S|D|I:")
            if DIALS == "A" or DIALS == "" or DIALS == "U":
                content_in_arg = std_help_pattern.search(arg)
                results = content_in_arg.groupdict()
                if results:
                    if results['short']:
                        short_args.append("-"+results['short'])
                    if results['long']:
                        long_args.append("--"+results['long'])
                    else:
                        long_args.append("")
                    if results['descrip']:
                        descrips.append(results['descrip'])
                continue
        if(DIALS != "D" and DIALS != "I"):
            try:
                short_args.append("-"+the_option[0])
                if(generic_opt == "L") or (DIALS == "L"):
                    long_args.append(the_option[1])
                    descrips.append(" ".join(the_option[2:]))
                else:
                    descrips.append(" ".join(the_option[1:]))
                    long_args.append("")
            except:
                print "bad delimiter... ?!!"
        elif(DIALS == "D"):
            general_descrip.append(arg)
        else:
            DIALS = "U" #undefined
    interpreter_list = ["bash", "csh", "ksh", "sh", "python", "php", \
    "perl", "tcsh", "zsh"]
    progname = execline.split()[0]
    for arg0 in interpreter_list:
        if(progname == arg0):
            progname = execline.split()[1]
            interpreter = arg0
    if interpreter == "":
        filetype = sendcommand("file "+progname)
        interpreter = getinterpreter(filetype)
    progshortname = os.path.basename(progname)
    print progshortname
    print interpreter

    print "\n"+"#"*25+"\n"
    for value in short_args:
        print "\t"+value
    print "\n"+"#"*25+"\n"
    for long_value in long_args:
        print "\t"+long_value
    print "\n"+"#"*25+"\n"
    for descrip in descrips:
        print "\t"+descrip
    print "\n"+"#"*25+"\n"
    for g_descrip in general_descrip:
        print "\t"+g_descrip

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

    return mybigdict



def GetVersion(progfullname):
    """
    Try to get version for the program
    and ask version for the tool to create
    """
    vprogoutput = sendcommand(progfullname+ \
    " --version")
    vprog = re.search(r"\d+(\.\d+)*\s",vprogoutput,\
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
        xmlfile = open(fname,"w")
    else:
        xmlfile = fname
    In = []
    Out = []
    aff = False
    param_tools = []
    headers = "<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>\n"+\
    "<!DOCTYPE pise SYSTEM \"PARSER/pise.dtd\">\n"

    for JsonData in ListeJsonData:
        #print str(JsonData)
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

        if(ttool_errors is None):
            if(tinput_name):
                In = JsonData.ParseInOutVal(tinput_name,"input",aff)
            if(toutput_name):
                Out = JsonData.ParseInOutVal(toutput_name,"output",aff)
        if(ttype == "tool"):
            params_tools = json.loads(ttool_state)
            opts = JsonData.ParseParams(params_tools,aff)

        #headers +
        #parameter type infile
        if(writewn == False):
            headers += '<pise>\n'+\
            '<head>\n'+\
            ' '*2 +'<title>'+wn+'</title>\n'+\
            ' '*2 +'<description>'+ann+'</description>\n'+\
            ' '*2 +'<authors>ParserConverterXML</authors>\n'+\
            '</head>\n'+\
            ' '*2 +'<command>'+wn+'</command>\n'+\
            ' '*2 +'<parameters>\n';
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

    footers=' '*2 +'</parameters>\n'+\
    '</pise>';
    xmlfile.write(footers)
    xmlfile.close()



def sendcommand(cmd):
    """
    Take a shell bash command
    Return the stdout value for a pipe subprocess
    """
    proc = subprocess.Popen("bash",shell=True,stdin=subprocess.PIPE, \
    stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return proc.communicate(cmd)[0]
