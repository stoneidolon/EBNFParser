
from Misakawa.ObjectRegex.Node import Ref, AstParser, SeqParser, LiteralParser, MetaInfo
from token import token 
import re
namespace     = globals()
recurSearcher = set()
字 = LiteralParser('[^\\[\]\(\),。由以有所列于作为]', name = '字')
字2 = LiteralParser('[^\]]', name = '字2')
分隔 = LiteralParser('\n', name = '分隔')
由义言物 = AstParser([LiteralParser.Eliteral('由', name = '\'由\''),Ref('概念'),Ref('具象')], name = '由义言物')
以义行物 = AstParser([LiteralParser.Eliteral('以', name = '\'以\''),Ref('概念'),Ref('具象')], name = '以义行物')
左标 = LiteralParser.Eliteral('[', name = '左标')
右标 = LiteralParser.Eliteral(']', name = '右标')
概念 = AstParser([Ref('字')],[Ref('左标'),SeqParser([Ref('字2')]),Ref('右标')], name = '概念')
具象 = AstParser([Ref('以义行物')],[Ref('由义言物')],[Ref('谓词倒装')], name = '具象')
作为 = AstParser([LiteralParser.Eliteral('作', name = '\'作\''),LiteralParser.Eliteral('为', name = '\'为\'')], name = '作为')
谓词倒装 = AstParser([Ref('位置倒装'),SeqParser([Ref('作为'),Ref('位置倒装')])], name = '谓词倒装')
所以于 = AstParser([LiteralParser.Eliteral('于', name = '\'于\'')],[LiteralParser.Eliteral('所', name = '\'所\'')], name = '所以于')
位置倒装 = AstParser([Ref('基本'),SeqParser([Ref('所以于'),Ref('基本')])], name = '位置倒装')
基本 = AstParser([Ref('元素'),SeqParser([Ref('基本')], atmost = 1)], name = '基本')
元素 = AstParser([Ref('字符串')],[Ref('数值')],[Ref('概念')],[Ref('列')],[LiteralParser.Eliteral('(', name = '\'(\''),Ref('具象'),LiteralParser.Eliteral(')', name = '\')\'')], name = '元素')
列 = AstParser([LiteralParser.Eliteral('有', name = '\'有\''),Ref('具象'),SeqParser([LiteralParser.Eliteral(',', name = '\',\''),Ref('具象')]),LiteralParser.Eliteral('列', name = '\'列\'')], name = '列')
逃逸 = AstParser([LiteralParser('\\\\', name = '\'\\\\\''),LiteralParser.Eliteral('"', name = '\'\"\'')], name = '逃逸')
字符串 = AstParser([LiteralParser.Eliteral('"', name = '\'\"\''),SeqParser([SeqParser([Ref('逃逸')],[Ref('一切')], atleast = 1, atmost = 1)]),LiteralParser.Eliteral('"', name = '\'\"\'')], name = '字符串')
数值 = AstParser([SeqParser([LiteralParser('\d', name = '\'\d\'')], atleast = 1),SeqParser([LiteralParser.Eliteral('.', name = '\'.\''),SeqParser([LiteralParser('\d', name = '\'\d\'')], atleast = 1)], atmost = 1)], name = '数值')
一切 = LiteralParser.Eliteral('[\w\W]', name = '一切')
语句 = AstParser([Ref('具象'),SeqParser([LiteralParser.Eliteral(';', name = '\';\''),Ref('具象')]),LiteralParser.Eliteral('。', name = '\'。\'')], name = '语句')
由义言物.compile(namespace, recurSearcher)
以义行物.compile(namespace, recurSearcher)
概念.compile(namespace, recurSearcher)
具象.compile(namespace, recurSearcher)
作为.compile(namespace, recurSearcher)
谓词倒装.compile(namespace, recurSearcher)
所以于.compile(namespace, recurSearcher)
位置倒装.compile(namespace, recurSearcher)
基本.compile(namespace, recurSearcher)
元素.compile(namespace, recurSearcher)
列.compile(namespace, recurSearcher)
逃逸.compile(namespace, recurSearcher)
字符串.compile(namespace, recurSearcher)
数值.compile(namespace, recurSearcher)
语句.compile(namespace, recurSearcher)
