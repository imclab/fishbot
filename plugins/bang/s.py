#!/usr/bin/python
"""!s - Regular expression substitution. Options available are:
The python standard re ones, some perl (g,i), and a number for
number of lines to scan (0-9).
Usage: !s/<select>/<replace>/<options>"""
import re,sys,os,string,difflib
import fishapi

def bang(pipein, arguments, event):
    # This regexp is to split correctly on only unescaped / slashes like
    # 'asjdf/as[ad/c]df/as\/df' needs.
    # Returns ['asjdf', 'as[ad/c]df', 'as\\/df']
    unescaped_slash = re.compile(r"(?<!\\)(?<!\[)/(?!.?\])")
    if len(unescaped_slash.split(arguments)) == 4:
        # Assumed to start with s/
        (pattern, repl, options) = unescaped_slash.split(arguments)[1:]
        # Number of lines to search
        if re.search('([1-9])', options):
            lines = int(re.search('([1-9])', options).group(0)) + 1
        else:
            lines = 2
        # Search globally, or just the user executing the command
        if 'g' in options or 'M' in options:
            search_domain = fishapi.backend.last(event.target(), lines)[1:]
        else:
            search_domain = fishapi.backend.last(event.source(), lines)[1:]
            for each in search_domain:
                each[4] = re.sub('^ACTION', fishapi.getnick(each[1]), each[4])
        try:
            option_values = {'I':re.I, 'L':re.L, 'M':re.M, 'S':re.S, 'U':re.U, 'X':re.X,
                             'i':re.I,           'g':re.M}
            # eval, be careful changing this as to not allow arbitrary
            # python to be executed
            compiled = re.compile(pattern, options and eval('|'.join(options), None, option_values) or 0)
            returned = []
            for each in search_domain:
                if compiled.search(each[4]):
                    returned.append("%s meant to say: %s" % (fishapi.getnick(each[1]), compiled.sub(repl, each[4]).replace("\/", "/")))
            return (returned, None)
        except:
            raise
    else:
        return ("Invalid regular expression (check for missing /'s)", None)
