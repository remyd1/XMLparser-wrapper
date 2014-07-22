XMLparser-wrapper
=================

Create Galaxy/Pise wrapper from XML or StdOut (myprog --help), or just display options from a galaxy workflow...


What is the goal of this project ?
==================================

Main goal is to provide a simple tool to create simple skeleton XML wrappers file for [Galaxy](https://wiki.galaxyproject.org/) or even Pise (a very old framework from Pasteur institute (now replaced by [Mobyle](http://mobyle.pasteur.fr/cgi-bin/portal.py#welcome) ) )

*   Yes, but how ?

That is quite easy:


    git clone https://github.com/remyd1/XMLparser-wrapper.git
    cd XMLparser-wrapper
    python ParserConverterXML.py --help
    python ParserConverterXML.py h2gw -c "ls --help" -o ../ls.gw.xml


*   Now, it is full of questions... ?!

Relax, it is just to help the program to parse the output. Otherwise, answer "A", to have an automatic parsing process. However, if you want to get all options exactly, you will have to parse it manually with the program.

Answer 'S' for short options (those with just a single dash).

Answer 'L' for long options (those with two dash e.g. : "--help").

Answer 'D' for a block of descriptions.

*   Could I enter specific delimiters to parse my output ?

Of course, just add '-d "your delimiter regexp"'.


*   What are other options (disp, ga2p, p2ga) ?


It is just for display content of a galawy workflow (disp) or for Pise users who would like to convert a Galaxy Workflow into a Pise wrapper (not working for the moment).



License Apache V2
=================

Copyright 2014 Dernat Rémy

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

