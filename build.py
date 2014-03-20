#! /usr/bin/env python3

# Copyright (C) <2014> <Joseph Liveccchi, joewashear007@gmail.com>
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



#needed libraries
# https://github.com/mankyd/htmlmin
# https://github.com/brettcannon/mnfy
# https://github.com/zacharyvoase/cssmin
# https://github.com/rspivak/slimit

import slimit
import cssmin
import htmlmin
import mnfy
import ast
import os
import shutil
from html.parser import HTMLParser
from string import Template

#output directory
output = "built_files/"
temp = "tmp/"
output_files = ["WebControllerAddon.py"]
#List of ile to be minified
css_files = ["style.css", "BlenderController.min.css"]
js_files = ["controller.js"]
html_files = ["index.html"]
py_files = ["handler.py", "server_test.py", "startServers.py", "endServers.py"]
py_files_with_web_subs = ["server.py"]
py_files_with_py_subs = ["WebControllerAddon.py"]



#Replacements in python files
web_replacements = {"_WEBSITE": "index.html"} 
py_replacements = {"_START_SERVER":"startServers.py", "_END_SERVER":"endServers.py", "_HANDLER":"handler.py", "_SERVER":"server.py"} 


class HTMLBuilder(HTMLParser):
    def __init__(self):
        super( HTMLBuilder, self ).__init__()
        self._replace = ""
        
    def handle_starttag(self, tag, attrs):
        self._replace = None
        for attr in attrs:
            key, value = attr
            if tag == "link" and "href" in key:
                if value in css_files:
                    self._replace = "style", value
            if tag == "script" and "src" in key:
                if value in js_files:
                    self._replace = "script", value

    def replacement(self):
        #Returns what should be replaced
        if self._replace:
            tag, file = self._replace 
            return "<"+tag+">" + open(temp + file).read() +"</"+tag+">"
        else:
            return None



def main():
    # Makes the output dir
    if os.path.exists(output):
        shutil.rmtree(output) 
    os.makedirs(output)
    
    if os.path.exists(temp):
        shutil.rmtree(temp) 
    os.makedirs(temp)
    
    #minify the CSS files
    for file in css_files:
        with open(temp + file, "w") as f:
            f.write( cssmin.cssmin(open("web/" + file).read()) )
    #Minify the Javascript files
    for file in js_files:      
        with open( temp + file, "w") as f:
            f.write( slimit.minify(open("web/"+file).read(), mangle=True, mangle_toplevel=True) )
    #Adds the minify CSS & JS file in HTML, minfy the HTML
    for file in html_files:  
        content = open("web/"+ file).readlines()
        new_content = ""
        p = HTMLBuilder()
        for line in content:
            line = line.strip()
            if line :
                p.feed(line)
                replacement = p.replacement()
                if replacement:
                    line = replacement
                new_content += line
        f = open(temp + file, "w")
        f.write( htmlmin.minify(new_content, remove_comments=True, remove_empty_space=True, ))
        
    #Preforms minify python files
    for file in py_files:
        content = open("python/" + file).read()
        minifier = mnfy.SourceCode()
        minifier.visit(ast.parse(content))
        with open(temp + file, "w") as f:
            f.write(  str(minifier) ) 
    
    #Build the website subsitute dictionary
    subs_web= dict()
    for i in web_replacements:
        subs_web[i] = '"""' + open(temp  + web_replacements[i]).read() + '"""'
    #Preforms Website Subsitutes on Pythons files, Minify them
    for file in py_files_with_web_subs:
        content = open("python/" + file).read()
        new_content = Template(content).safe_substitute(subs_web)
        minifier = mnfy.SourceCode()
        minifier.visit(ast.parse(new_content))
        with open(temp + file, "w") as f:
            f.write(  str(minifier) ) 
    
    #Build subsitute dictionary
    subs_py = dict()
    for i in py_replacements:
        s = open(temp  + py_replacements[i] ).read()
        s = s.replace("\\n", "\\\\n").replace("\\d", "\\\\d").replace("\\'", "\\\\'")
        subs_py[i] = """'''""" + s + """'''"""
    #Preforms Subsitutes on Pythons files, Minify them
    for file in py_files_with_py_subs:
        content = open("python/" + file).read()
        new_content = Template(content).safe_substitute(subs_py)
        minifier = mnfy.SourceCode()
        minifier.visit(ast.parse(new_content))
        with open(temp + file, "w") as f:
            f.write(  str(minifier) ) 
            
    #Copy the final output
    for i in output_files:
        shutil.copyfile(temp + i, output + i)
    
if __name__ == '__main__':
    main()