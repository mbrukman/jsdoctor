import scanner

class Source(object):
  def __init__(self, script, path=None):
    self.script = script
    self.path = path
    
    self.provides = set()
    self.requires = set()
    self.symbols = set()
    self.filecomment = None

  def __str__(self):
    source_string = super(Source, self).__str__()

    if self.path:
      source_string += ' ' + self.path

    return source_string

class Symbol(object):
  def __init__(self, identifier, start, end):
    self.identifier = identifier
    self.start = start
    self.end = end
    self.source = None
    self.comment = None

  def __str__(self):
    symbol_string = super(Symbol, self).__str__()

    symbol_string += ' ' + self.identifier

    if self.source:
      symbol_string += ' ' + str(self.source)

    return symbol_string

class Comment(object):
  def __init__(self, text, start, end):
    self.text = text
    self.start = start
    self.end = end

def ScanScript(script, path=None):

  source = Source(script, path)
  source.provides.update(set(scanner.YieldProvides(script)))
  source.requires.update(set(scanner.YieldRequires(script)))

  pairs = scanner.ExtractDocumentedSymbols(script)

  for comment_match, identifier_match in pairs:
    comment_text = scanner.ExtractTextFromJsDocComment(comment_match.group())
    comment = Comment(comment_text, comment_match.start(), comment_match.end())
    
    if identifier_match:
      # TODO(nanaze): Identify scoped variables and expand identifiers.
      identifier = scanner.StripWhitespace(identifier_match.group())
      symbol = Symbol(identifier, identifier_match.start(), identifier_match.end())

      symbol.source = source
      symbol.comment = comment
      source.symbols.add(symbol)
    else:
      assert not source.filecomment, '@fileoverview comment made more than once' 
      source.filecomment = comment

  return source


    
    
