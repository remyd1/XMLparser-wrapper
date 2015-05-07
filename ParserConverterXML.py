#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Pise[xml]/galaxy[json,xml] ga parser wrapper/workflow tool
examples:
- To convert ls option to a Pise XML wrapper:
python ParserConverterXML.py h2p -o ls.xml -c "ls --help"
- To convert ls option to a Galaxy XML wrapper:
python ParserConverterXML.py h2gw -o ls.xml -c "ls --help"
- To display the content of a Galaxy workflow:
python ParserConverterXML.py disp -i galaxy_workflow.ga
- To convert the content of a Galaxy workflow to a Pise XML file:
python ParserConverterXML.py ga2p -i galaxy_workflow.ga
- To convert a Pise XML file to a Galaxy Xml file:
python ParserConverterXML.py p2gw -i PiseWrapper.xml -o GalaxyWrapper.xml
- To convert a Galaxy XML file to a Pise Xml file:
python ParserConverterXML.py gw2p -i GalaxyWrapper.xml -o PiseWrapper.xml
"""

import argparse
import sys

from gaclass.wrapper_galaxy_class import *
from gaclass.pise_parser_class import *
from gaclass.utils import *
from gaclass.xmlparser import *



if __name__ == "__main__":
    """
    Main program for galaxy parser
    < It takes arguments from command line
    see usage :
        <disp || ga2p || p2ga || h2gw || h2p || p2gw || gw2p>
            (required)
        -i --filename [/path/to/filename]
        -o --filename [/path/to/filename]
        -c/-d for h2gw action
        -help
    > Return a xml file or the content of the ga file with nice display
    in the console.
    """
    usage = "usage :\n\
        disp || ga2p || p2ga || h2gw || h2p || p2gw || gw2p \n\
            (required)\n\
        -i --filename [/path/to/filename]\n\
        -o --filename [/path/to/filename]\n\
        -c/-d for h2gw | h2p action\n\
        -help\n\
        ParserConverterXML.py <disp|ga2p|p2ga|h2gw|h2p|p2gw|gw2p>"
    epilog = "ParserConverterXML is under Apache license. A beta"\
    + " release from Remy Dernat, Evolution Science Institute -"\
    + " Montpellier, France."

    parser = argparse.ArgumentParser(description=usage, epilog=epilog)
    parser.add_argument('--version', action='version', \
    version='%(prog)s 0.2')

    subparsers = parser.add_subparsers(help='command', dest='command')

    disp = subparsers.add_parser("disp", help="Display galaxy "\
    + "workflow parameters (.ga / json file).")
    disp.add_argument('-i', '--input', type=argparse.FileType('r'), \
    help="Galaxy workflow (.ga) filename to parse")
    disp.set_defaults(command='disp')

    ga2p = subparsers.add_parser('ga2p', help="Convert galaxy workflow"\
    +" to XML-Pise (.ga / json file).")
    ga2p.add_argument('-o', '--output', \
    type=argparse.FileType('wb', 0), help="Pise "+\
    "filename to create")
    ga2p.add_argument('-i', '--input', type=argparse.FileType('r'), \
    help="Galaxy workflow (.ga / json file) filename to parse")
    ga2p.set_defaults(command='ga2p')

    p2ga = subparsers.add_parser('p2ga', help="Convert pise wrapper to"\
    " galaxy workflow (.ga / json file).")
    p2ga.add_argument('-o', '--output', \
    type=argparse.FileType('wb', 0), help="Galaxy "+\
    "filename to create")
    p2ga.add_argument('-i', '--input', type=argparse.FileType('r'), \
    help="Galaxy workflow (.ga / json file) filename to parse")
    p2ga.set_defaults(command='p2ga')

    p2gw = subparsers.add_parser('p2gw', help="Convert pise wrapper to"\
    " galaxy wrapper (.xml).")
    p2gw.add_argument('-o', '--output', \
    type=argparse.FileType('wb', 0), help="Galaxy "+\
    "filename to create")
    p2gw.add_argument('-i', '--input', type=argparse.FileType('r'), \
    help="Pise wrapper (.xml) filename to parse")
    p2gw.set_defaults(command='p2gw')

    gw2p = subparsers.add_parser('gw2p', help="Convert galaxy wrapper "\
    "to pise wrapper (.xml).")
    gw2p.add_argument('-o', '--output', \
    type=argparse.FileType('wb', 0), help="Pise "\
    "filename to create")
    gw2p.add_argument('-i', '--input', type=argparse.FileType('r'), \
    help="Galaxy wrapper (.xml) filename to parse")
    gw2p.set_defaults(command='gw2p')

    h2gw = subparsers.add_parser('h2gw', help="retrieve arguments "\
    +"options from an help program output and convert it to a galaxy "\
    +"wrapper.")
    h2gw.add_argument('-o', '--output', required=True, \
    type=argparse.FileType('wb', 0), help="Galaxy "+\
    "filename to create")
    fileorcmdgw = h2gw.add_mutually_exclusive_group(required=True)
    fileorcmdgw.add_argument("-i", "--input", type=argparse.FileType('r'), \
    help="A help file "\
    +"to parse; Usually 'yourbinaryprogram --help' or '-h'. "+\
    "Can not be used with -c")
    fileorcmdgw.add_argument("-c", "--commandline", \
    help="Your command line "+\
    "to parse; Usually 'yourbinaryprogram --help' or '-h'. "+\
    "Can not be used with -i")
    h2gw.add_argument("-rs", "--record_separator", \
    help="Record separator is a string that seperate each line of "+\
    "arguments. It could be a regular expression. Default value is "+\
    "a regexp: '\\n\\s+-'.", default="\n\s+-")
    h2gw.add_argument("-fs", "--field_separator", \
    help="Field separator is a string that seperate each option and"+\
    " description within a line of help. It could be a regular "+\
    "expression. Default value is a regexp: '\\s+'.", default="\s+")
    h2gw.set_defaults(command='h2gw')

    h2p = subparsers.add_parser('h2p', help="retrieve arguments "\
    +"options from an help program output and convert it to a Pise "\
    +"wrapper.")
    h2p.add_argument('-o', '--output', required=True, \
    type=argparse.FileType('wb', 0), help="Pise "+\
    "filename to create")
    fileorcmdp = h2p.add_mutually_exclusive_group(required=True)
    fileorcmdp.add_argument("-i", "--input", type=argparse.FileType('r'), \
    help="A help file "\
    +"to parse; Usually 'yourbinaryprogram --help' or '-h'. "+\
    "Can not be used with -c")
    fileorcmdp.add_argument("-c", "--commandline", \
    help="Your command line "\
    +"to parse; Usually 'yourbinaryprogram --help' or '-h'. "+\
    "Can not be used with -i")
    h2p.add_argument("-rs", "--record_separator", \
    help="Record separator is a string that seperate each line of "+\
    "arguments. It could be a regular expression. Default value is "+\
    "a regexp: '\\n\\s+-'.", default="\n\s+-")
    h2p.add_argument("-fs", "--field_separator", \
    help="Field separator is a string that seperate each option and"+\
    " description within a line of help. It could be a regular "+\
    "expression. Default value is a regexp: '\\s+'.", default="\s+")
    h2p.set_defaults(command='h2p')

    args = parser.parse_args()

    ListeJsonData = []
    jsondata = False
    fromwrapper = False

    infile = False
    try:
        if args.input:
            infile = args.input
            fname = infile.name.rpartition(".")
            fname = fname[0]
    except:
        infile = False
        if args.command != "disp" and args.command != "h2p" and \
        args.command != "h2gw":
            sys.exit("Could not execute this command without an input"+\
            " file!")

    outfile = False
    try:
        if args.output:
            outfile = args.output
    except:
        outfile = False


    if args.command == "disp":
        jsondata = getjson(infile)
        print("Processing workflow params...")
        if jsondata:
            ListeJsonData = ConstructMyGaParser(jsondata)
            getworkflowparams(ListeJsonData)
        else:
            print("jsondata is not defined")
    elif args.command == "ga2p":
        jsondata = getjson(infile)
        print("Converting to Pise XML...")
        if jsondata:
            ListeJsonData = ConstructMyGaParser(jsondata)
            if outfile is False:
                pisewrapper(ListeJsonData, fname+".xml")
                print("The XML file is located in the same directory "\
                +"as your original ga file, with the same name.")
            else:
                pisewrapper(ListeJsonData, outfile)
        else:
            print("jsondata is not defined")

    elif args.command == "p2gw":
        fromwrapper = True
        print("Converting Pise XML to galaxy XML...")
        mybigdict = parseXml(infile)
        vprog = mybigdict["vprog"]
        vtool = mybigdict["vtool"]
        if not 'progshortname' in mybigdict:
            mybigdict["progshortname"] = mybigdict["progfullname"]
        if not 'interpreter' in mybigdict:
            mybigdict["interpreter"] = raw_input("Interpreter not "+\
            "found. Please, give me one (otherwise, it will be "+\
            "'bash'):")
            if mybigdict["interpreter"] == "":
                mybigdict["interpreter"] = 'bash'
        GalaxWrapperObj = XmlGW(mybigdict, vprog, vtool)
        GalaxWrapper = GalaxWrapperObj.GenGalaxWrapper(fromwrapper)
        if outfile:
            outfile.write(GalaxWrapper)
            outfile.close()
            print("The Galaxy XML wrapper has been generated. Edit that "+\
            "file to check if everything is ok, especially options that "+\
            "require specific or conditionnaly constraints (when tags / "+\
            "select / data_ref) ")
        else:
            sys.exit("No output file found!")

    elif args.command == "gw2p":
        fromwrapper = True
        print("Converting Galaxy XML to Pise XML...")
        mybigdict = parseXml(infile)
        vtool = mybigdict["vtool"]
        vprog = raw_input("Please give me the program version:")
        catname = raw_input("In what category would you like to "+\
        "include this Tool[[NGS]|Phylogenomics|Population "+\
        "Genetics|Population Dynamics|Ecological Modelling] :")
        if not catname:
            catname = "NGS"
        while 1:
            nb_paraph = raw_input("How many paragraph do you need"+\
            " for your Web Form ?:")
            try:
                nb_paraph = int(nb_paraph)
                break
            except:
                print("Sorry, not a number. Try again...\n")
        if not 'progshortname' in mybigdict:
            mybigdict["progshortname"] = mybigdict["progfullname"]
        PiseWrapper = XmlPise(mybigdict, vprog, vtool, catname, \
        nb_paraph)
        PiseWrapperFormat = PiseWrapper.createXml(fromwrapper)
        if outfile:
            outfile.write(PiseWrapperFormat)
            outfile.close()
        else:
            sys.exit("No output file found!")

    elif args.command == "p2ga":
        print("Converting Pise XML to galaxy file...")

    elif args.command == "h2gw":
        """
        Help to Galaxy Wrapper
        """
        if not outfile:
            sys.exit("No output file found!")
        else:
            outfile = args.output
        if args.commandline:
            execline = args.commandline
        elif infile:
            content = infile.read()
            infile.close()
        else:
            sys.exit("No command line or help file given... Bye bye...")
        try:
            if args.record_separator:
                record_separator = args.record_separator
        except:
            record_separator = "\n\s+-"
        try:
            if args.field_separator:
                field_separator = args.field_separator
        except:
            field_separator = "\s+"
        if infile:
            mybigdict = GetProgHelpParam(content, record_separator, \
            field_separator, True)
        else:
            mybigdict = GetProgHelpParam(execline, record_separator, \
            field_separator, False)
        vprog, vtool = GetVersion(mybigdict["progfullname"])
        GalaxWrapperObj = XmlGW(mybigdict, vprog, vtool)
        GalaxWrapper = GalaxWrapperObj.GenGalaxWrapper(fromwrapper)
        outfile.write(GalaxWrapper)
        outfile.close()

    elif args.command == "h2p":
        if args.commandline:
            execline = args.commandline
            outfile = args.output
            try:
                if args.record_separator:
                    record_separator = args.record_separator
            except:
                record_separator = "\n\s+-"
            try:
                if args.field_separator:
                    field_separator = args.field_separator
            except:
                field_separator = "\s+"
            mybigdict = GetProgHelpParam(execline, record_separator, \
            field_separator, False)
            vprog, vtool = GetVersion(mybigdict["progfullname"])
            catname = raw_input("In what category would you like to "+\
            "include this Tool[[NGS]|Phylogenomics|Population "+\
            "Genetics|Population Dynamics|Ecological Modelling] :")
            if not catname:
                catname = "NGS"
            while 1:
                nb_paraph = raw_input("How many paragraph do you need"+\
                " for your Web Form ?:")
                try:
                    nb_paraph = int(nb_paraph)
                    break
                except:
                    print("Sorry, not a number. Try again...\n")

            PiseWrapper = XmlPise(mybigdict, vprog, vtool, catname, \
            nb_paraph)
            PiseWrapperFormat = PiseWrapper.createXml(fromwrapper)
            outfile.write(PiseWrapperFormat)
            outfile.close()
        else:
            sys.exit("No command line given... Bye bye...")
    else:
        sys.exit("There is no valid action... Bye, bye...\n"+usage)
