import json, re, urllib, urllib2, wordnik
import wordnik

def generate_docs(params, response, summary, path):
    """This will generate the documentation for a function given some information
    about the params, the response (not currently used), the summary, and the path."""
    docstring   = "{0}\n".format(summary)
    docstring  += "{0}\n".format(path)
    
    path_params  = get_path_params(params)
    other_params = get_other_params(params)
   
    if path_params:
        docstring += "\nPath Parameters:\n"
        for param in path_params:
            param_doc  = "  {0}\n".format(param.get('name'))
            docstring += param_doc
 
    if other_params:
        docstring += "\nOther Parameters:\n"
        for param in other_params:
            param_doc  = "  {0}\n".format(param.get('name'))
            docstring += param_doc

    return docstring

def get_path_params(params):
    path_params = []
    for param in [ p for p in params if p['paramType'] == 'path' ]:
        p = {}
        p['name']        = param.get('name') or 'body'
        p['description'] = param.get('description')
        p['paramType']   = param.get('paramType')
        p['required']    = param.get('required')
        path_params.append(p)
    return path_params

def get_query_params(params):
    query_params = []
    for param in [ p for p in params if p['paramType'] == 'query' ]:
        p = {}
        p['name']        = param.get('name') or 'body'
        p['description'] = param.get('description')
        p['paramType']   = param.get('paramType')
        p['required']    = param.get('required')
        query_params.append(p)
    return query_params

def get_other_params(params):
    other_params = []
    for param in [ p for p in params if p['paramType'] != 'path' ]:
        p = {}
        p['name']        = param.get('name') or 'body'
        p['description'] = param.get('description')
        p['paramType']   = param.get('paramType')
        p['required']    = param.get('required')
        other_params.append(p)
    return other_params

def get_required_params(params):
    required_params = []
    for param in [ p for p in params if p['paramType'] != 'path' and p['required'] == True ]:
        p = {}
        p['name']        = param.get('name') or 'body'
        p['description'] = param.get('description')
        p['paramType']   = param.get('paramType')
        p['required']    = param.get('required')
        required_params.append(p['name'])
    return required_params
      
def create_method(name, doc, params, path, httpmethod):
    """The magic behind the dynamically generated methods in the Wordnik object"""
    def _method(self, *args, **kwargs):
        return self._run_command(name, *args, **kwargs)
    
    _method.__doc__  = str(doc)
    _method.__name__ = str(name)
    _method._path    = path
    _method._params  = params
    _method._http    = httpmethod
    
    return _method

def process_args(path, params, args, kwargs):
    """This does all the path substitution and the population of the
    headers and/or body, based on positional and keyword arguments.
    """
    required_params = get_required_params(params)
    given_params    = kwargs.keys()
    query_params    = get_query_params(params)
    
    if not set(given_params).issuperset(set(required_params)):
        notsupplied = set(given_params).symmetric_difference(set(required_params)).intersection(set(required_params))
        raise wordnik.MissingParameters("Some required parameters are missing: {0}".format(notsupplied))
    
    ## get "{format} of of the way first"
    format = kwargs.get('format') or wordnik.DEFAULT_FORMAT
    path   = path.replace('{format}', format) + "?"    
    
    positional_args_re  = re.compile('{([\w]+)}')
    headers             = {}
    body                = None
    
    ## substiture the positional arguments, left-to-right
    for arg in args:
        path = positional_args_re.sub(urllib.quote(arg), path, count=1)

    ## now look through the keyword args and do path substitution
    for arg,value in kwargs.items():
        if arg not in path:
            continue
        bracketedString = "{" + arg + "}"
        pathPattern = re.compile(bracketedString)
        path = pathPattern.sub(urllib.quote(value), path)
        ## we want to remove this item from kwargs (we already used it!)
        kwargs.pop(arg)

    ## if we need to set the HTTP body, we do it in kwargs
    if 'body' in kwargs:
        body = json.dumps(kwargs.pop('body'))
    
    ## handle additional query args
    for param in query_params:
        name = param.get('name')
        if name in kwargs:
            path += "{0}={1}&".format(name, urllib.quote(kwargs.pop(name).__str__()))

    
    ## put all remaining kwargs in the headers
    for arg in kwargs:    
        headers[arg] = urllib.quote(kwargs[arg])

    ## If we still have any unsubstituted params in the path, we need to 
    ## raise an exception.
    
    if positional_args_re.search(path):
        raise wordnik.MissingParameters("Some required parameters are missing: {0}".format(path))
    
    ## similarly, raise and exception if we're missing a keyword arg.
    for param in params:
        if param['paramType'] == 'body' and body == None:
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
