
from Misakawa.ObjectRegex.Node import Ref, AstParser, SeqParser, LiteralParser, MetaInfo
import re
namespace     = globals()
recurSearcher = set()
token = re.compile('|'.join(['module','import','\}','\{','\`','\]','\[','\=\>','\=','\:','\/\*','\.','\-\>','\,','\*\/','\)','\(','/\*[\W\w]*?/\*','//[^\n]*','[a-z]*"[\w|\W]*"','0[XxOoBb][\da-fA-F]+','\d+(?:\.\d+|)(?:E\-{0,1}\d+|)','\n',';','[a-zA-Z_][a-z0-9A-Z_]*','\/\/|\/|\|\||\||\>\>|\<\<|\>\=|\<\=|\<\-|\>|\<|\=\>|\-\-|\+\+|\*\*|\+|\-|\*|\=\=|\=|\%|\^','\?|\!|\&|\$|\@|\+|\-|\~']))
multilineComment = AstParser([LiteralParser.Eliteral('/*', name = '\'/*\''),Ref('multilineComment'),LiteralParser.Eliteral('*/', name = '\'*/\'')],[LiteralParser('/\*[\W\w]*?/\*', name = '\'/\*[\W\w]*?/\*\'')], name = 'multilineComment')
Comment = LiteralParser('//[^\n]*', name = 'Comment')
String = LiteralParser('[a-z]*"[\w|\W]*"', name = 'String')
numberLiteral = LiteralParser('0[XxOoBb][\da-fA-F]+', name = 'numberLiteral')
Decimal = LiteralParser('\d+(?:\.\d+|)(?:E\-{0,1}\d+|)', name = 'Decimal')
Constant = LiteralParser('null|false|true', name = 'Constant')
NEWLINE = LiteralParser('\n', name = 'NEWLINE')
EOL = LiteralParser(';', name = 'EOL')
Insertable = AstParser([Ref('EOL')],[Ref('NEWLINE')],[Ref('Comment')],[Ref('multilineComment')], name = 'Insertable')
simpleName = LiteralParser('[a-zA-Z_][a-z0-9A-Z_]*', name = 'simpleName')
Identifier = AstParser([Ref('simpleName')],[LiteralParser.Eliteral('`', name = '\'`\''),Ref('simpleName'),LiteralParser.Eliteral('`', name = '\'`\'')], name = 'Identifier')
labelDeclaration = AstParser([LiteralParser.Eliteral(':', name = '\':\''),Ref('Identifier')], name = 'labelDeclaration')
block = AstParser([LiteralParser.Eliteral('{', name = '\'{\''),Ref('statements'),LiteralParser.Eliteral('}', name = '\'}\'')], name = 'block')
body = AstParser([Ref('block')],[Ref('statement')],[SeqParser([Ref('Insertable')]),Ref('body'),SeqParser([Ref('Insertable')])], name = 'body')
module = AstParser([Ref('simpleName'),SeqParser([LiteralParser.Eliteral(',', name = '\',\''),Ref('simpleName')])], name = 'module')
moduleDeclaration = AstParser([LiteralParser.Eliteral('module', name = '\'module\''),Ref('module')], name = 'moduleDeclaration')
Import = AstParser([LiteralParser.Eliteral('import', name = '\'import\''),Ref('module')], name = 'Import')
statement = AstParser([Ref('flowControl')],[Ref('declaration')],[Ref('flowControlSign'),SeqParser([Ref('Identifier')], atmost = 1)],[Ref('expression')], name = 'statement')
flowControlSign = LiteralParser('break|return|continue', name = 'flowControlSign')
flowControl = AstParser([Ref('If')],[Ref('While')], name = 'flowControl')
If = AstParser([LiteralParser('if', name = '\'if\''),LiteralParser.Eliteral('(', name = '\'(\''),Ref('expression'),LiteralParser.Eliteral(')', name = '\')\''),Ref('body'),SeqParser([LiteralParser('else', name = '\'else\''),Ref('body')], atmost = 1)], name = 'If')
While = AstParser([SeqParser([Ref('labelDeclaration')], atmost = 1),LiteralParser('while', name = '\'while\''),LiteralParser.Eliteral('(', name = '\'(\''),Ref('expression'),LiteralParser.Eliteral(')', name = '\')\''),Ref('body')], name = 'While')
declaration = AstParser([Ref('structDeclaration')],[Ref('variableDeclaration')], name = 'declaration')
structDeclaration = AstParser([LiteralParser('struct', name = '\'struct\''),Ref('Identifier'),LiteralParser.Eliteral('{', name = '\'{\''),SeqParser([SeqParser([Ref('Insertable')]),Ref('variableDeclarationEntry'),SeqParser([Ref('Insertable')])]),LiteralParser.Eliteral('}', name = '\'}\'')], name = 'structDeclaration', toIgnore={'Insertable'})
variableDeclarationEntry = AstParser([Ref('Identifier'),SeqParser([LiteralParser.Eliteral(':', name = '\':\''),Ref('Type')], atmost = 1)], name = 'variableDeclarationEntry')
variableDeclarationEntryList = AstParser([Ref('variableDeclarationEntry'),SeqParser([LiteralParser.Eliteral(',', name = '\',\''),Ref('variableDeclarationEntry')])], name = 'variableDeclarationEntryList')
variableDeclaration = AstParser([SeqParser([LiteralParser('let', name = '\'let\'')],[LiteralParser('var', name = '\'var\'')], atleast = 1, atmost = 1),Ref('variableDeclarationEntry'),SeqParser([LiteralParser.Eliteral('=', name = '\'=\''),Ref('expression')], atmost = 1)], name = 'variableDeclaration')
Type = AstParser([LiteralParser.Eliteral('[', name = '\'[\''),Ref('TypeList'),LiteralParser.Eliteral('=>', name = '\'=>\''),Ref('Type'),LiteralParser.Eliteral(']', name = '\']\'')],[Ref('Identifier')], name = 'Type')
TypeList = AstParser([Ref('Type'),SeqParser([LiteralParser.Eliteral(',', name = '\',\''),Ref('Type')])], name = 'TypeList')
genericParameters = AstParser([LiteralParser('<', name = '\'<\''),Ref('Identifier'),SeqParser([LiteralParser.Eliteral(',', name = '\',\''),Ref('Identifier')]),LiteralParser('>', name = '\'>\'')], name = 'genericParameters')
BinaryOperator = LiteralParser('\/\/|\/|\|\||\||\>\>|\<\<|\>\=|\<\=|\<\-|\>|\<|\=\>|\-\-|\+\+|\*\*|\+|\-|\*|\=\=|\=|\%|\^', name = 'BinaryOperator')
UnaryOperator = LiteralParser('\?|\!|\&|\$|\@|\+|\-|\~', name = 'UnaryOperator')
expression = AstParser([Ref('LambdaDef')],[Ref('BinaryOperation')], name = 'expression')
LambdaDef = AstParser([Ref('variableDeclarationEntry'),LiteralParser.Eliteral('->', name = '\'->\''),Ref('body')],[LiteralParser.Eliteral('(', name = '\'(\''),Ref('variableDeclarationEntryList'),LiteralParser.Eliteral(')', name = '\')\''),LiteralParser.Eliteral('->', name = '\'->\''),Ref('body')],[LiteralParser.Eliteral('{', name = '\'{\''),SeqParser([Ref('Insertable')]),SeqParser([Ref('variableDeclarationEntryList'),LiteralParser.Eliteral('->', name = '\'->\'')], atmost = 1),Ref('statements'),LiteralParser.Eliteral('}', name = '\'}\'')],[SeqParser([Ref('genericParameters')], atmost = 1),SeqParser([Ref('Type')], atmost = 1),Ref('LambdaDef')], name = 'LambdaDef', toIgnore={'Insertable'})
BinaryOperation = AstParser([Ref('UnaryOperation'),SeqParser([Ref('BinaryOperator'),Ref('UnaryOperation')])], name = 'BinaryOperation')
UnaryOperation = AstParser([Ref('AtomExpr')],[Ref('UnaryOperator'),Ref('UnaryOperation')], name = 'UnaryOperation')
AtomExpr = AstParser([Ref('Atom'),SeqParser([Ref('Trailer')])], name = 'AtomExpr')
expressionList = AstParser([Ref('expression'),SeqParser([LiteralParser.Eliteral(',', name = '\',\''),Ref('expression')])], name = 'expressionList')
Trailer = AstParser([LiteralParser.Eliteral('(', name = '\'(\''),SeqParser([Ref('expressionList')], atmost = 1),LiteralParser.Eliteral(')', name = '\')\''),SeqParser([Ref('LambdaDef')], atmost = 1)],[LiteralParser.Eliteral('.', name = '\'.\''),Ref('Identifier')], name = 'Trailer')
Atom = AstParser([Ref('Constant')],[Ref('String')],[Ref('Identifier')],[Ref('numberLiteral')],[Ref('Decimal')],[LiteralParser.Eliteral('(', name = '\'(\''),Ref('expression'),LiteralParser.Eliteral(')', name = '\')\'')], name = 'Atom')
statements = AstParser([SeqParser([SeqParser([Ref('Insertable')]),SeqParser([Ref('statement')]),SeqParser([Ref('Insertable')])])], name = 'statements', toIgnore={'Insertable'})
multilineComment.compile(namespace, recurSearcher)
Insertable.compile(namespace, recurSearcher)
Identifier.compile(namespace, recurSearcher)
labelDeclaration.compile(namespace, recurSearcher)
block.compile(namespace, recurSearcher)
body.compile(namespace, recurSearcher)
module.compile(namespace, recurSearcher)
moduleDeclaration.compile(namespace, recurSearcher)
Import.compile(namespace, recurSearcher)
statement.compile(namespace, recurSearcher)
flowControl.compile(namespace, recurSearcher)
If.compile(namespace, recurSearcher)
While.compile(namespace, recurSearcher)
declaration.compile(namespace, recurSearcher)
structDeclaration.compile(namespace, recurSearcher)
variableDeclarationEntry.compile(namespace, recurSearcher)
variableDeclarationEntryList.compile(namespace, recurSearcher)
variableDeclaration.compile(namespace, recurSearcher)
Type.compile(namespace, recurSearcher)
TypeList.compile(namespace, recurSearcher)
genericParameters.compile(namespace, recurSearcher)
expression.compile(namespace, recurSearcher)
LambdaDef.compile(namespace, recurSearcher)
BinaryOperation.compile(namespace, recurSearcher)
UnaryOperation.compile(namespace, recurSearcher)
AtomExpr.compile(namespace, recurSearcher)
expressionList.compile(namespace, recurSearcher)
Trailer.compile(namespace, recurSearcher)
Atom.compile(namespace, recurSearcher)
statements.compile(namespace, recurSearcher)