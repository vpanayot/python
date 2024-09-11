import datetime
import json
import random
import sqlite3
from typing import Optional, Any, Self

class Message:
    '''
    A class to represent a message with key, value and timestamp.

    Attributes
    ----------
    key : str
        An identifier for the message.
    value : float
        A float value representing the content of the message.
    ts : datetime
        The timestamp at which the message was created.
    '''

    def __init__(
            self, 
            key: str,
            value: float,
            ts: datetime.datetime,
        ) -> None:

        self.key = key
        self.value = value
        self.ts = ts

    def __repr__(self) -> str:
        class_name = type(self).__name__     
        return '{}({!r}, {!r}, {!r})'.format(class_name, self.key, self.value, self.ts)
    
    def __str__(self):
        return f'Key: {self.key}, Value: {self.value}, Timestamp: {self.ts}'

class Source:
    '''
    A class to represent a source that reads a message.

    The class is meant to be used as a base class and not used directly.
    
    Attributes
    ----------
    name : str
        A name used to identify the source.
    infinite_flag : bool
        Shows whether source is infinite or not.

    Methods
    -------
    read_message(self) -> Message:
        Returns a message read from the source.
    has_message(self) -> bool:
        Returns True if there are still messages left.
    '''

    def __init__(self, name) -> None:
        self.name = name
        self.infinite_flag = False

    def __repr__(self) -> str:
        return f'{type(self).__name__}({self.name})'

    def read_message(self) -> Message:
        pass

    def has_message(self) -> bool:
        pass


class SimulationSource(Source):
    '''
    A class that simulates a source and generates a random message.
    
    Attributes
    ----------
    name : str
        A name used to identify the source.
    infinite_flag : bool
        Shows whether source is infinite or not.

    Methods
    -------
    read_message(self) -> Message:
        Generates and returns a random message.
    
    generate_key(self) -> str:

    generate_value(self) -> float:

    generate_timestamp(self) -> datetime.datetime:

    has_message(self) -> bool:
        Source is infinite so it always returns True.
    '''

    def __init__(self, name) -> None:
        super().__init__(name)
        self.infinite_flag = True

    def read_message(self) -> Message:
        '''Generates and returns a random message.'''

        # Use internal methods to generate the messsage atrributes
        key = self.generate_key()
        value = self.generate_value()
        curr_ts = self.generate_timestamp()

        return Message(key, value, curr_ts)

    def generate_key(self) -> str:
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        numbers = '0123456789'
        return random.choice(letters) + ''.join(random.choices(numbers, k=3))
    
    def generate_value(self) -> float:
        return round(random.uniform(0, 100), 1)
    
    def generate_timestamp(self) -> datetime.datetime:
        return datetime.datetime.now().astimezone()

    def has_message(self) -> bool:
        return True

class FileSource(Source):
    '''
    A class that reads from a file source.
    
    Attributes
    ----------
    name : str
        A name used to identify the source.
    data : Any
        Data returned from file
    index : int
        An indicator of the position to which data has been read

    Methods
    -------
    read_message(self) -> Message:
        Reads and returns a message object from a text file. Returns None if no data left to read.

    has_message(self) -> bool:
        Returns true if there are still messages left in the file.

    parse_record(
        self, 
        record: dict[str, str], 
        ts_fmt: str = '%Y-%m-%d %H:%M:%S.%f%z'
    ) -> Message:
        Parses the record read from source and returns it as a Message object.
    '''

    def __init__(self, name, file_path) -> None:
        super().__init__(name)
        self.file_path = file_path
        # Load all data from the file
        with open(self.file_path, 'r') as file:
            self.data = json.load(file)
        self.index = 0
    
    def parse_record(
            self, 
            record: dict[str, str], 
            ts_fmt: str = '%Y-%m-%d %H:%M:%S.%f%z'
        ) -> Message:

        '''
        Parses the record read from source and returns it as a Message object.
        Optionally a datetime format can be passed as an argument to indicate how to parse the timestamp.
        '''

        key = record['key']
        value = record['value']
        ts = datetime.datetime.strptime(record['ts'], ts_fmt)

        return Message(key, value, ts)

    def read_message(self) -> Optional[Message]:
        '''Reads and returns a Message object from a text file. Returns None if no data left to read.'''

        if self.index < len(self.data):
            record = self.data[self.index]
            self.index += 1
            return self.parse_record(record)
        else:
            return None
        
    def has_message(self) -> bool:
        '''Returns true if there are still messages left in the file.'''
        return self.index < len(self.data)
    
class SourceFactory:
    '''
    Factory class for creating Source objects.

    Methods
    -------
    def create_source(cls, name: str, type: str, *args) -> Source:
        Class method that accepts name, type and additional arguments and creates a Source concrete class object based on the type.
    '''
    @classmethod
    def create_source(cls, name: str, type: str, *args) -> Source:
        '''
        Class method that accepts name, type and additional arguments and creates a Source concrete class object based on the type.
        Possible type values are:
            - 'sim' - returns SimulationSource object
            - 'file' - returns FileSource object
        Other type values are invalid and raise a ValueError exception
        '''
        if type == 'sim':
            return SimulationSource(name)
        elif type == 'file':
            return FileSource(name, *args)
        else:
            raise ValueError('Invalid type')
        

class Sink:
    '''
    A class to represent a sink that writes a message.

    The class is meant to be used as a base class and not used directly.
    
    Attributes
    ----------
    name : str
        A name used to identify the sink.

    Methods
    -------
    write_message(self, msg: Message) -> None:
        Writes a message to a sink.
    '''
    def __init__(self, name) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f'{type(self).__name__}({self.name})'

    def write_message(self, msg: Message) -> None:
        pass 

class ConsoleSink(Sink):
    '''
    A class that prints a message to a console.
    
    Attributes
    ----------
    name : str
        A name used to identify the sink.

    Methods
    -------
    write_message(self, msg: Message) -> None:
        Prints a Message objects passed as argument to the console.
    '''
    
    def __init__(self, name) -> None:
        super().__init__(name)

    def write_message(self, msg: Message) -> None:
        '''Prints a Message objects passed as argument to the console.'''
        print(msg)

class SQLiteSink(Sink):
    '''
    A class that writes a message to a table in SQLite Database.
    
    Attributes
    ----------
    name : str
        A name used to identify the sink.
    db_name : str
        The name of the SQLite database
    table_name : str
        Name of the table to be loaded
    conn : Connection
        SQLite Connection object
    
    Methods
    -------
    write_message(self, msg: Message) -> None:
        Writes a Message objects passed as argument to the table.

    cleanup_table(self)-> None:
        Deletes all previously loaded data in the table.
    '''

    def __init__(
            self, 
            name: str,
            db_name: str,
            table_name: str
        ) -> None:
        super().__init__(name)
        self.db_name = db_name
        self.table_name = table_name
        self.conn = None

    def _open_conn(self) -> sqlite3.Cursor:
        '''Opens a connection to the database and returns a Cursor object.'''
        self.conn = sqlite3.connect(self.db_name)
        return self.conn.cursor()
    
    def _commit(self) -> None:
        '''Commits the SQL operation.'''
        self.conn.commit()

    def _close_conn(self) -> None:
        '''Closes the connection to the database.'''
        self.conn.close()

    def cleanup_table(self)-> None:
        '''Deletes all previously loaded data in the table.'''
        try:
            cursor = self._open_conn()
            cursor.execute(f'DELETE FROM {self.table_name}')
            self._commit()
        except sqlite3.Error as e:
            raise e
        finally:
            if self.conn:
                self._close_conn()

    def write_message(self, msg: Message) -> None:
        '''Writes a Message objects passed as argument to the table.'''
        try:
            cursor = self._open_conn()
            cursor.execute(f"INSERT INTO {self.table_name} (id, value, ts) VALUES ('{msg.key}', {msg.value}, '{msg.ts}')")
            self._commit()
        except sqlite3.Error as e:
            raise e
        finally:
            if self.conn:
                self._close_conn()

class SinkFactory:
    '''
    Factory class for creating Sink objects.

    Methods
    -------
    create_sink(cls, name: str, type: str, *args) -> Sink:
        Class method that accepts name, type and additional arguments and creates a Sink concrete class object based on the type.
    '''
    @classmethod
    def create_sink(cls, name: str, type: str, *args) -> Sink:
        '''
        Class method that accepts name, type and additional arguments and creates a Sink concrete class object based on the type.
        Possible type values are:
            - 'console' - returns ConsoleSink object
            - 'sqlite' - returns SQLiteSink object
        Other type values are invalid and raise a ValueError exception
        '''
        if type == 'console':
            return ConsoleSink(name)
        elif type == 'sqlite':
            return SQLiteSink(name, *args)
        else:
            raise ValueError('Invalid type')

class ETL():
    '''
    A class that executes extract, transform and load operations.

    Attributes
    ----------
    src : Source
        Source object from which the ETL process reads.
    tgt : Sink
        Sink object to which the ETL process writes.
    
    Methods
    -------
    source(self, name: str, type: str, *args: Any) -> Self:
        Creates a Source object from which the ETL process to read and returns a self reference.
    sink(self, name: str, type: str, *args: Any) -> Self:
        Creates a Sink object to which the ETL process to write and returns a self reference.
    run(self) -> None:
        Reads a message from the Source object and writes it to the Sink object.
    '''
    def __init__(self, src: Optional[Source] = None, tgt: Optional[Sink] = None) -> None:
        self.src = src
        self.tgt = tgt

    def source(self, name: str, type: str, *args: Any) -> Self:
        '''
        Creates a Source object from which the ETL process to read and returns a self reference.
        Possible type values are:
            - 'sim' - returns SimulationSource object
            - 'file' - returns FileSource object
        Other type values are invalid and raise a ValueError exception
        '''
        self.src = SourceFactory.create_source(name, type, *args)
        return self
    
    def sink(self, name: str, type: str, *args: Any) -> Self:
        '''
        Creates a Sink object to which the ETL process to write and returns a self reference.
        Possible type values are:
            - 'console' - returns ConsoleSink object
            - 'sqlite' - returns SQLiteSink object
        Other type values are invalid and raise a ValueError exception
        '''
        self.tgt = SinkFactory.create_sink(name, type, *args)
        return self
    
    def run(self) -> None:
        '''Reads a message from the Source object and writes it to the Sink object.'''

        if self.src is None:
            raise ValueError('No source specified')
        
        if self.tgt is None:
            raise ValueError('No sink specified')

        print(f'Reading from source {self.src} and writing to sink {self.tgt}...')
        
        if self.src.infinite_flag:
            self.tgt.write_message(self.src.read_message())
        else:
            while self.src.has_message():
                self.tgt.write_message(self.src.read_message())
