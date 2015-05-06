#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

class JsonData():
    """
    Class for json objects
    """
    def __init__(self,wn,ann,step_id,tname,ttool_id,ttype,ttool_version, \
    tinput_name, toutput_name, tuser_output_name, ttool_state, \
    ttool_errors):
        """
        Constructor
        """
        self.wn = wn
        self.ann = ann
        self.step_id = step_id
        self.tname = tname
        self.ttool_id = ttool_id
        self.ttype = ttype
        self.ttool_version = ttool_version
        self.tinput_name = tinput_name
        self.toutput_name = toutput_name
        self.tuser_output_name = tuser_output_name
        self.ttool_state = ttool_state
        self.ttool_errors = ttool_errors



    def display(self, text):
        """
        display data
        """
        for line in text:
            print(line+"\n")



    def ParseInOutVal(self, InOutput, InOutType, aff):
        """
        Parse In/Out values in json
        """
        text = []
        InOut = []
        for j in iter(InOutput):
            if(InOutput[0] is not None):
                if(j['name']):
                    text.append("\t Name : "+j['name'])
                    InOut.append(["name", j, j['name']])
                if(InOutType == "input"):
                    text.append("\t Description : "+j['description'])
                    InOut.append(["description", j, j['description']])
                if(InOutType == "output"):
                    text.append("\t Type : "+j['type'])
                    InOut.append(["type", j, j['type']])
        if(aff == True):
            self.display(text)
        return InOut



    def ParseParams(self, params_tools, aff):
        """
        Parse tool_state in json
        """
        pattern = re.compile('advanced')
        text = []
        opts = {}
        try:
            if(params_tools['adv_opts']):
                match = re.search(pattern, \
                params_tools['adv_opts'])
                if(match is not None):
                    opts["advanced"] = params_tools['adv_opts']
                    text.append("\t - Advanced option found")
                    text.append("\t" + params_tools['adv_opts'])
                else:
                    opts["basic"] = params_tools['adv_opts']
                    text.append("\t - Basic option found")
                    text.append("\t" + params_tools['adv_opts'])
        except:
            text.append("\t - No option available for this tool : "+ \
            self.tname)
            text.append("\t" + self.ttool_state)
            opts["other"] = self.ttool_state
        if(aff == True):
            self.display(text)
        return opts



    def __str__(self):
        str_return = "From str method of JsonData: name is %s" \
        % (self.wn)
        str_return += "\nannotation is %s" % (self.ann)
        str_return += "\nstep_id is %s" % (self.step_id)
        str_return += "\ntool name is %s" % (self.tname)
        str_return += "\nid is %s" % (self.ttool_id)
        str_return += "\nTool type is %s" % (self.ttype)
        str_return += "\nTool version is %s" % (self.ttool_version)
        str_return += "\nTool input name is %s" % (self.tinput_name)
        str_return += "\nTool output name is %s" % (self.toutput_name)
        str_return += "\nTool user output name is %s" \
        % (self.tuser_output_name)
        str_return += "\nTool state is %s" % (self.ttool_state)
        str_return += "\nTool errors are %s" % (self.ttool_errors)
        return str_return
