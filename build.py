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
from html.parser import HTMLParser
from string import Template

output = "bin"
css_files = ["style.css", "BlenderController.min.css"]
js_files = ["controller.js"]
html_files = ["index.html"]
py_files = ["handler.py", "main.py", "server.py", "startServers.py"]
replacements = {"WEBSITE": "index.html"} 


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
            return "<"+tag+">" + open(output + "/"+ file).read() +"</"+tag+">"
        else:
            return None



def main():
    
    if not os.path.exists(output):
        os.makedirs(output)
    
    for file in css_files:
        with open("bin/" + file, "w") as f:
            f.write( cssmin.cssmin(open("web/" + file).read()) )
            
    for file in js_files:      
        with open("bin/"+ file, "w") as f:
            f.write( slimit.minify(open("web/"+file).read(), mangle=True, mangle_toplevel=True) )
           
    for file in html_files:  
        with open("bin/" + file, "w") as f:
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
            f.write( htmlmin.minify(new_content, remove_comments=True, remove_empty_space=True, ))
    
    #Build sub dictionary
    subs = dict()
    for i in replacements:
        subs[i] = '"""' + open(output + "/" + replacements[i]).read() + '"""'
    
    for file in py_files:
        content = open("python/" + file).read()
        new_content = Template(content).safe_substitute(subs)
        minifier = mnfy.SourceCode()
        minifier.visit(ast.parse(new_content))
        with open("bin/" + file, "w") as f:
            f.write(  str(minifier) ) 
    
if __name__ == '__main__':
    main()