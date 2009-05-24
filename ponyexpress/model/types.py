from sqlalchemy import types
import zlib

class GzipBinary(types.TypeDecorator):
    """
    A type that compresses everything with zlib before storing it in
    the database, and decompresses everything on its way out.

    Since compression and decompression are relatively expensive
    operations, this type is best used with a deferred column.
    """

    impl = types.Binary

    def __init__(self, compresslevel=9, *args, **kwargs):
        self.compresslevel = compresslevel
        super(GzipBinary, self).__init__(*args, **kwargs)

    def process_bind_param(self, value, engine):
        return zlib.compress(value, self.compresslevel)

    def convert_result_value(self, value, engine):
        return zlib.decompress(value)

    def copy(self):
        return GzipBinary(self.compresslevel)
