from django.db import connection
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import SqlLexer
from sqlparse import format


def print_queries():
    queries = connection.queries
    for query in queries:
        sql_formatted = format(str(query['sql']), reindent=True)
        print(highlight(sql_formatted, SqlLexer(), TerminalFormatter()))
