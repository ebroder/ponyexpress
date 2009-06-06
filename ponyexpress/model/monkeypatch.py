"""
PonyExpress model monkeypatches.

Sometimes upstream code isn't perfect, and requiring a bleeding edge
release is too annoying, so we'll monkeypatch in code changes.

So far, we change SQLite to fix SQLAlchemy ticket #1016. Unless you
explicitly specify a column as being PRIMARY KEY AUTOINCREMENT, it's
possible for primary key values to be repeated. Unfortunately, because
of how IMAP expects the UID and UIDVALIDITY and other fields to
change, that's not acceptable for PonyExpress.
"""

import sqlalchemy
from sqlalchemy.databases import sqlite
import sqlalchemy.types as sqltypes

# Unfortunately, everything changed names between SA 0.5 and 0.6,
# although very little changed functionality. This is why people
# shouldn't actually monkeypatch
from pkg_resources import parse_version
sa05 = (parse_version(sqlalchemy.__version__) < parse_version('0.6a'))

if sa05:
    DefaultDDLCompiler = sqlite.SQLiteSchemaGenerator
else:
    DefaultDDLCompiler = sqlite.SQLiteDDLCompiler

# I'm monkey patching the sqlite dialect to always set AUTOINCREMENT
# on single-column primary key fields, because I need the semantics of
# a ROWID never being reused
class PonySQLiteDDLCompile(DefaultDDLCompiler):
    def get_column_specification(self, column, **kwargs):
        colspec = [self.preparer.format_column(column)]

        if sa05:
            colspec.append(column.type.dialect_impl(self.dialect).get_col_spec())
        else:
            colspec.append(self.dialect.type_compiler.process(column.type))

        default = self.get_column_default_string(column)
        if default is not None:
            colspec.append('DEFAULT ' + default)

        if not column.nullable:
            colspec.append('NOT NULL')

        if column.primary_key and column.autoincrement and \
                len(column.table.primary_key.columns) == 1 and \
                isinstance(column.type, sqltypes.Integer) and \
                not column.foreign_keys:
            colspec.append('PRIMARY KEY AUTOINCREMENT')

        return ' '.join(colspec)

    def visit_primary_key_constraint(self, constraint):
        if len(constraint.columns) == 1:
            c = list(constraint).pop(0)
            if c.primary_key and c.autoincrement and \
                    isinstance(c.type, sqltypes.Integer) and \
                    not c.foreign_keys:
                return ''
        return super(PonySQLiteDDLCompile, self).visit_primary_key_constraint(constraint)

if sa05:
    sqlite.dialect.schemagenerator = PonySQLiteDDLCompile
else:
    sqlite.dialect.ddl_compiler = PonySQLiteDDLCompile
