import re, urllib, urllib2, wordnik
import wordnik

def generate_docs(params, response, summary, path):
    """This will generate the documentation for a function given some information
    about the params, the response (not currently used), the summary, and the path."""
    docstring   = "{0}\n".format(summary)
    docstring  += "{0}\n".format(path)
    
    pathParams  = [ p for p in params if p['paramType'] == "path" and p.get('name') != "format" ]
    if pathParams:
        docstring += "\nPath Parameters:\n"
    for param in pathParams:
        name      = param.get('name') or 'body'
        paramDoc  = "  {0}\n".format(name)
        docstring += paramDoc
 
    
    otherParams = [ p for p in params if p['paramType'] != "path" ]
    if otherParams:
        docstring += "\nOther Parameters:\n"
    for param in otherParams:
        name      = param.get('name') or 'body'
        paramDoc  = "  {0}\n".format(name)
        docstring += paramDoc

    return docstring

def create_method(name, doc, params, path):
    """The magic behind the dynamically generated methods in the Wordnik object"""
    def _method(self, *args, **kwargs):
        return self._run_command(name, *args, **kwargs)
    
    _method.__doc__  = str(doc)
    _method.__name__ = str(name)
    _method._path    = path
    _method._params  = params
    
    return _method

def process_args(path, params, args, kwargs):
    """This does all the path substitution and the population of the
    headers and/or body, based on positional and keyword arguments.
    """

    required_params = [ p for p in params if params[p]['required'] and p != 'format' and  params[p]['paramType'] != 'path' ]
    given_params = kwargs.keys()
    
    if not set(given_params).issuperset(set(required_params)):
        notsupplied = set(given_params).symmetric_difference(set(required_params)).intersection(set(required_params))
        raise wordnik.MissingParameters("Some required parameters are missing: {0}".format(notsupplied))
        
    
    
    positional_args_re  = re.compile('{([\w]+)}')
    headers             = {}
    body                = None
    
    ## get "{format} of of the way first"
    format = kwargs.get('format') or wordnik.DEFAULT_FORMAT
    path = path.replace('{format}', format) + "?"

    ## substiture the positional arguments, left-to-right
    for arg in args:
        path = positional_args_re.sub(arg, path, count=1)

    ## now look through the keyword args and do path substitution
    for arg,value in kwargs.items():
        if arg not in path:
            continue
        bracketedString = "{" + arg + "}"
        pathPattern = re.compile(bracketedString)
        path = pathPattern.sub(value, path)
        ## we want to remove this item from kwargs (we already used it!)
        kwargs.pop(arg)

    ## if we need to set the HTTP body, we do it in kwargs
    if 'body' in kwargs:
        body = urllib.urlencode(kwargs.pop('body'))
    
    ## handle additional query and header args
    for arg in kwargs:
        if arg in params and params[arg]['paramType'] == 'query':
            path += "{0}={1}&".format(arg, kwargs[arg])
        else:
            headers[arg] = kwargs[arg]

    ## If we still have any unsubstituted params in the path, we need to 
    ## raise an exception.
    
    if positional_args_re.search(path):
        raise wordnik.MissingParameters("Some required parameters are missing: {0}".format(path))
    
    ## similarly, raise and exception if we're missing a keyword arg.
    for param in params.keys():
        if params[param]['paramType'] == 'body' and body == None:
            raise wordnik.MissingParameters("Some required parameters are missing: {0}".format(param))
    
    ## return a 3-tuple of (<URI path>, <headers>, <body>)
    return (path, headers, body)


def uncamel(string):
    """unCamels cameledStrings"""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def remove_params(path):
    """Gets rid of all {params} in a URL"""
    param_re = re.compile('{[\w]+}')
    return param_re.subn('', path)[0]
    
def componentize(path):
    """Splits a path on underscores and returns the components"""
    return re.split('[_]+', path)
    
def normalize(path, method):
    """Makes a crazy path + HTTP method look like a sane method name"""
    under_re = re.compile('(^[_]+|[_]+$)')
    repeat_under_re = re.compile('[_]+')
    
    p = remove_params(path)
    p = p.replace('/', '_').replace('.', '_').strip('_')
    components = componentize(p)
    m = [ components[0], method ]
    m.extend(components[1:])
    return uncamel("_".join(m))

def dictify(params):
    p = {}
    for param in params:
        if 'name' in param:
            p[param['name']] = param
        else:
            p['body'] = param

    return p

def find_missing_path_params(self, path):
    """This will check to make sure there are no un-substituted params
    e.g. /word.json/{word}
    """
    if self.positional_args_re.search(path):
        matches = self.positional_args_re.findall(path)
        missingParams = ", ".join(matches)
        raise MissingParameters("Could not substitute some parameters: {0}".format(missingParams))


