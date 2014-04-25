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
import os, glob, shutil
from html.parser import HTMLParser
from string import Template

#file directories
minified_files_dir  = "bin/"
source_files_dir    = "src/"

#List of ile to be minified
css_files = ["style.css", "BlenderController.min.css"]
js_files = ["controller.js"]
html_files = ["index.html"]
py_files = ["customButtons.py", "handler.py", "server_test.py", "startServers.py", "endServers.py", "server.py", "WebControllerAddon.py"]

#List of files to move once built
output_files = ["WebControllerAddon.py"]


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
            return "<"+tag+">" + FileBuilder.replacements["_"+file.replace(".", "_").upper()].strip('"""').replace("\\\\d", "\\d").replace("\\.", "\.") +"</"+tag+">"
        else:
            return None
        
class FileBuilder:
    replacements = dict()
    def __init__(self, files, minify_func, in_folder, out_folder ):
        self.in_dir = in_folder
        self.out_dir = out_folder
        self.files = files
        self.func_subsitute = None
        self.func_minify = minify_func
        
    def minify(self):
        for file in self.files:
            print("Minifying: ", file, "   ...")
            content = open(self.in_dir + file).read()
            content = Template( content).safe_substitute(FileBuilder.replacements)
            min_content = self.func_minify(content)
            output = open(self.out_dir + file, "w").write(min_content)
            # all cap filename and replace dot wioth underscorse to get the replace string name, add double slashes
            FileBuilder.replacements["_"+file.replace(".", "_").upper()] = '"""' + min_content.replace("\\n", "\\\\n").replace("\\r", "\\\\r").replace("\\d", "\\\\d").replace("\\'", "\\\\'") + '"""'
            print("Done!")

def miniy_js(content):
    return slimit.minify(content, mangle=True, mangle_toplevel=True)
    
def miniy_css(content):
    return cssmin.cssmin(content)
    
def miniy_html(content):
    content = content.split("\n")
    new_content = ""
    p = HTMLBuilder()
    for line in content:
        line = line.strip()
        if line:
            p.feed(line)
            replacement = p.replacement()
            if replacement:
                line = replacement
            new_content += line
    return htmlmin.minify(new_content, remove_comments=True, remove_empty_space=True, )

def miniy_py(content):
    minifier = mnfy.SourceCode()
    minifier.visit(ast.parse(content))
    return str(minifier)


def main():
    # Makes the output dir
    if not os.path.exists(minified_files_dir):
        os.makedirs(minified_files_dir)
    else:
        for file in glob.glob(minified_files_dir+"*"):
            if os.path.isfile(file):
                os.remove(file)
    
    builders = []
    builders.append( FileBuilder( css_files,  miniy_css, source_files_dir+"web/",   minified_files_dir) )
    builders.append( FileBuilder( js_files,   miniy_js,  source_files_dir+"web/",   minified_files_dir) )
    builders.append( FileBuilder( html_files, miniy_html,source_files_dir+"web/",   minified_files_dir) )
    builders.append( FileBuilder( py_files,   miniy_py,  source_files_dir,          minified_files_dir) )
    
    for b in builders:
        b.minify()
                
    for file in output_files:
        shutil.copyfile(minified_files_dir+file, "./"+file)
    
if __name__ == '__main__':
    main()