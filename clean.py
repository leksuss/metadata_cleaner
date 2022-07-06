import os

from libmat2 import parser_factory

filepath = 'upload/1.pdf'

parser, mime = parser_factory.get_parser(filepath)

parser.lightweight_cleaning = True
parser.inplace = True

res = parser.remove_all()

if res and parser.inplace:
    os.rename(parser.output_filename, filepath)
