from xml.dom import minidom

import symboltypes

def GenerateDocs(namespace_map):
  for namespace, symbols in namespace_map.iteritems():
    filepath = '%s.html' % namespace
    doc = _GenerateDocument(namespace, symbols)
    content = doc.documentElement.toprettyxml(indent='  ')
    yield filepath, content

def _MakeTextNode(content):
  text = minidom.Text()
  text.data = content
  return text

def _MakeHeader(content=None):
  return _MakeElement('h2', content)

def _MakeElement(tagname, content=None):
  element = minidom.Element(tagname)

  if content:
    element.appendChild(_MakeTextNode(content))
  
  return element

def _IsStatic(symbol):
  return bool(symbol.static)

def _IsNotStatic(symbol):
  return not _IsStatic(symbol)

def _GetSymbolsOfType(symbols, type):
  return [symbol for symbol in symbols if symbol.type == type]

def _GenerateDocument(namespace, symbols):
  doc = minidom.getDOMImplementation().createDocument(None, 'html', None)

  body =  doc.createElement('body')
  doc.documentElement.appendChild(body)
  
  for elem in _GenerateContent(namespace, symbols):
   body.appendChild(elem)
    
  return doc

def _AddSymbolDescriptions(node_list, symbols):
  for symbol in symbols:
    node_list.append(_MakeElement('h3', symbol.identifier))
    for section in symbol.comment.description_sections:
      node_list.append(_MakeElement('p', section))  

def _GenerateContent(namespace, symbols):

  node_list = minidom.NodeList()

  sorted_symbols = sorted(symbols, key= lambda symbol: symbol.identifier)

  # Constructor
  constructor_symbols = _GetSymbolsOfType(
    sorted_symbols, symboltypes.CONSTRUCTOR)

  if constructor_symbols:
    node_list.append(_MakeElement('h2', 'Constructor'))
    _AddSymbolDescriptions(node_list, constructor_symbols)

  # Interface
  interface_symbols = _GetSymbolsOfType(
    sorted_symbols, symboltypes.INTERFACE)
        
  if interface_symbols:
    node_list.append(_MakeElement('h2', 'Interface'))
    _AddSymbolDescriptions(node_list, interface_symbols)

  # Enumerations
  enum_symbols = _GetSymbolsOfType(
     sorted_symbols, symboltypes.ENUM)
  if enum_symbols:
    node_list.append(_MakeElement('h2', 'Enumerations'))
    _AddSymbolDescriptions(node_list, enum_symbols)

  instance_methods = filter(_IsNotStatic,
      _GetSymbolsOfType(sorted_symbols, symboltypes.FUNCTION))
  if instance_methods:
    node_list.append(_MakeElement('h2', 'Instance methods'))
    _AddSymbolDescriptions(node_list, instance_methods)

  instance_properties = filter(_IsNotStatic,
      _GetSymbolsOfType(sorted_symbols, symboltypes.PROPERTY))
  if instance_properties:
    node_list.append(_MakeElement('h2', 'Instance properties'))
    _AddSymbolDescriptions(node_list, instance_properties)      

  static_functions = filter(_IsStatic,
      _GetSymbolsOfType(sorted_symbols, symboltypes.FUNCTION))
  if static_functions:
    node_list.append(_MakeElement('h2', 'Static methods'))
    _AddSymbolDescriptions(node_list, static_functions)  

  static_properties = filter(_IsStatic,
      _GetSymbolsOfType(sorted_symbols, symboltypes.PROPERTY))
  if static_properties:
    node_list.append(_MakeElement('h2', 'Static properties'))
    _AddSymbolDescriptions(node_list, static_properties)      
    
  

  return node_list


                       
    
  

  

  
