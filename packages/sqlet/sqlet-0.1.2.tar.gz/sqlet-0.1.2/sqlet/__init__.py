import sqlite3
import psycopg

class db:
    def __init__(self, SUBD:str, connection:str):
        '''
        for sqlite  -> 'sqlite',  'path/name'\n
        for postgre -> 'postgre', 'host+port+username+password+dbname'
        '''
        
        if SUBD.lower() == 'sqlite':
            self._SUBD = 'sqlite'
            self._db = connection
            self.tables = []
            con = sqlite3.connect(self._db)
            cus = con.cursor()
            cus.execute("SELECT name FROM sqlite_master where type='table'")
            for table in cus.fetchall():
                self.tables.append(table[0])
                setattr(self,table[0],_db_table(table[0], SUBD, connection))

        elif SUBD.lower() == 'postgre':
            self._SUBD = 'postgre'
            self.tables = []
            connection = connection.split('+')
            self._db = {'host':connection[0], 'port':connection[1], 'user':connection[2], 'password':connection[3], 'dbname':connection[4]}
            conn = psycopg.connect(dbname=self._db['dbname'],user=self._db['user'],password=self._db['password'],host=self._db['host'],port=self._db['port'])
            cus = conn.cursor()
            cus.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            for table in cus.fetchall():
                self.tables.append(table[0])
                setattr(self,table[0],_db_table(table[0], SUBD, self._db))
            conn.commit()
            cus.close()
            conn.close()

    def __str__(self):
        outp = ''
        for table in self.tables:
            if not outp: outp += f"tables: '{table}'"
            else: outp += f", '{table}'"
        outp += f"; DBMS: {self._SUBD} "
        return f"<data base ({outp})>"
    def __repr__(self):
        outp = ''
        for table in self.tables:
            if not outp: outp += f"tables: '{table}'"
            else: outp += f", '{table}'"
        outp += f"; DBMS: {self._SUBD} "
        return f"<data base ({outp})>"

    def sql(self,q:str):
        if self._SUBD == 'sqlite':
            con = sqlite3.connect(self._db)
            cus = con.cursor()
            cus.execute(q)
            outp = cus.fetchall()
            con.commit()
            cus.close()
            con.close()
            
            return outp
        elif self._SUBD == 'postgre':
            conn = psycopg.connect(dbname=self._db['dbname'],user=self._db['user'],password=self._db['password'],host=self._db['host'],port=self._db['port'])
            cus = conn.cursor()
            cus.execute(q)
            outp = cus.fetchall()
            conn.commit()
            cus.close()
            conn.close()
            return outp

    def selectf(self, table:str, columns:list=[], filter:str=None):
        '''
        select('tablename', columns=['column1', 'column2', ... ,], filter='sql filter')\n
        select('tablename', filter='sql filter') - all columns\n\n
        db_obj.tablename.selectf(filter='sql filter')
        '''
        if self._SUBD == 'sqlite':
            con = sqlite3.connect(self._db)
            cus = con.cursor()
            if not columns:
                cus.execute(f"select name from PRAGMA_TABLE_INFO('{table}')")
                for name in cus.fetchall():
                    columns.append(name[0])
            cols = ''
            for c in columns:
                if not cols: cols += c
                else: cols += ',' + c
            cus.execute(f"select {cols} from {table} {f'where {filter}' if filter else ''}")
            res = cus.fetchall()
            output = []
            for r in res:
                one = {}
                for i in range(0,len(columns)):
                    one[columns[i]] = r[i]
                output.append(_db_output(one, table, self._SUBD, self._db))
            con.commit()
            cus.close()
            con.close()
            
            return output
        
        elif self._SUBD == 'postgre':
            con = psycopg.connect(dbname=self._db['dbname'],user=self._db['user'],password=self._db['password'],host=self._db['host'],port=self._db['port'])
            cus = con.cursor()
            if not columns:
                cus.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}'")
                for name in cus.fetchall():
                    columns.append(name[0])
            cols = ''
            for c in columns:
                if not cols: cols += c
                else: cols += ',' + c
            cus.execute(f"select {cols} from {table} {f'where {filter}' if filter else ''}")
            res = cus.fetchall()
            output = []
            for r in res:
                one = {}
                for i in range(0,len(columns)):
                    one[columns[i]] = r[i]
                output.append(_db_output(one, table, self._SUBD, self._db))
            con.commit()
            cus.close()
            con.close()
            
            return output

    def select(self, table:str, *columns, **filter):
        '''
        select('tablename', 'column1', 'column2', ... , column=value, column2=value, ...)\n
        select('tablename', column=value, column1=value1, ...) - all columns\n\n
        db_obj.tablename.select(column=value, column1=value1, ...)
        '''
        if self._SUBD == 'sqlite':
            con = sqlite3.connect(self._db)
            cus = con.cursor()
            if not columns:
                cus.execute(f"select name from PRAGMA_TABLE_INFO('{table}')")
                for name in cus.fetchall():
                    columns += (name[0],)
                
            cols = ''
            for c in columns:
                if not cols: cols += c
                else: cols += ',' + c

            filtr = ''
            for col, val in filter.items():
                if not filtr: 
                    if not val: filtr = f" ({col} = '' or {col} is NULL) "
                    else : filtr += f" {col} = '{val}' "
                else:
                    if not val: filtr = f" and ({col} = '' or {col} is NULL) "
                    else : filtr += f" and {col} = '{val}' "

            cus.execute(f"select {cols} from {table} {f'where {filtr}' if filtr else ''}")
            res = cus.fetchall()
            output = []
            for r in res:
                one = {}
                for i in range(0,len(columns)):
                    one[columns[i]] = r[i]
                output.append(_db_output(one, table, self._SUBD, self._db))
            con.commit()
            cus.close()
            con.close()
            
            return output
        
        elif self._SUBD == 'postgre':
            con = psycopg.connect(dbname=self._db['dbname'],user=self._db['user'],password=self._db['password'],host=self._db['host'],port=self._db['port'])
            cus = con.cursor()
            if not columns:
                cus.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}'")
                for name in cus.fetchall():
                    columns += (name[0],)
                
            cols = ''
            for c in columns:
                if not cols: cols += c
                else: cols += ',' + c

            filtr = ''
            for col, val in filter.items():
                if not filtr: 
                    if not val: filtr = f" ({col} = '' or {col} is NULL) "
                    else : filtr += f" {col} = '{val}' "
                else:
                    if not val: filtr = f" and ({col} = '' or {col} is NULL) "
                    else : filtr += f" and {col} = '{val}' "

            cus.execute(f"select {cols} from {table} {f'where {filtr}' if filtr else ''}")
            res = cus.fetchall()
            output = []
            for r in res:
                one = {}
                for i in range(0,len(columns)):
                    one[columns[i]] = r[i]
                output.append(_db_output(one, table, self._SUBD, self._db))
            con.commit()
            cus.close()
            con.close()
            
            return output
    
    def select1(self, table:str, *columns, **filter):
        '''
        same as select() but returns only first value
        '''
        if self._SUBD == 'sqlite':
            con = sqlite3.connect(self._db)
            cus = con.cursor()
            if not columns:
                cus.execute(f"select name from PRAGMA_TABLE_INFO('{table}')")
                for name in cus.fetchall():
                    columns += (name[0],)
                
            cols = ''
            for c in columns:
                if not cols: cols += c
                else: cols += ',' + c

            filtr = ''
            for col, val in filter.items():
                if not filtr: filtr += f" {col} = '{val}' "
                else:      filtr += f" and {col} = '{val}' "

            cus.execute(f"select {cols} from {table} {f'where {filtr}' if filtr else ''}")
            res = cus.fetchall()
            output = []
            for r in res:
                one = {}
                for i in range(0,len(columns)):
                    one[columns[i]] = r[i]
                output.append(_db_output(one, table, self._SUBD, self._db))
            con.commit()
            cus.close()
            con.close()
            
            return output[0] if output else None

        elif self._SUBD == 'postgre':
            con = psycopg.connect(dbname=self._db['dbname'],user=self._db['user'],password=self._db['password'],host=self._db['host'],port=self._db['port'])
            cus = con.cursor()
            if not columns:
                cus.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}'")
                for name in cus.fetchall():
                    columns += (name[0],)
                
            cols = ''
            for c in columns:
                if not cols: cols += c
                else: cols += ',' + c

            filtr = ''
            for col, val in filter.items():
                if not filtr: filtr += f" {col} = '{val}' "
                else:      filtr += f" and {col} = '{val}' "

            cus.execute(f"select {cols} from {table} {f'where {filtr}' if filtr else ''}")
            res = cus.fetchall()
            output = []
            for r in res:
                one = {}
                for i in range(0,len(columns)):
                    one[columns[i]] = r[i]
                output.append(_db_output(one, table, self._SUBD, self._db))
            con.commit()
            cus.close()
            con.close()
            
            return output[0] if output else None

    def insertf(self, table:str, columns:list=[], values:list=[]):
        '''
        incert2('table_name', columns=['column','column2', ...], values=['value1','value2',...])\n
        incert2('table_name', values=['value1','value2',...]) - all columns\n
        '''
        if self._SUBD == 'sqlite':
            con = sqlite3.connect(self._db)
            cus = con.cursor()
            cols = ''
            for c in columns:
                if not cols: cols += c
                else: cols += ',' + c
            vals = ''
            for v in values:
                if not vals: vals += v
                else: vals += ',' + v
            cus.execute(f"insert into {table} {cols} values ({vals})")
            output = ''
            con.commit()
            cus.close()
            con.close()
            
            return output
        
        elif self._SUBD == 'postgre':
            con = psycopg.connect(dbname=self._db['dbname'],user=self._db['user'],password=self._db['password'],host=self._db['host'],port=self._db['port'])
            cus = con.cursor()
            cols = ''
            for c in columns:
                if not cols: cols += c
                else: cols += ',' + c
            vals = ''
            for v in values:
                if not vals: vals += v
                else: vals += ',' + v
            cus.execute(f"insert into {table} {cols} values ({vals})")
            output = ''
            con.commit()
            cus.close()
            con.close()
            
            return output

    def insert(self, table:str, **colvals):
        '''
        incert('table_name', column=value, column_2=value_2, ...)\n
        db_obj.tablename.insert(column=value, column_2=value_2, ...)
        '''
        if self._SUBD == 'sqlite':
            con = sqlite3.connect(self._db)
            cus = con.cursor()
            cols = ''
            vals = ''
            for key, value in colvals.items():
                if not cols: cols += str(key)
                else: cols += ',' + str(key)
                if not vals: vals += f"'{value}'"
                else: vals += ',' + f"'{value}'"
            cus.execute(f"insert into {table} ({cols}) values ({vals})")
            output = ''
            con.commit()
            cus.close()
            con.close()
            
            return output
        
        elif self._SUBD == 'postgre':
            con = psycopg.connect(dbname=self._db['dbname'],user=self._db['user'],password=self._db['password'],host=self._db['host'],port=self._db['port'])
            cus = con.cursor()
            cols = ''
            vals = ''
            for key, value in colvals.items():
                if not cols: cols += str(key)
                else: cols += ',' + str(key)
                if not vals: vals += f"'{value}'"
                else: vals += ',' + f"'{value}'"
            cus.execute(f"insert into {table} ({cols}) values ({vals})")
            output = ''
            con.commit()
            cus.close()
            con.close()
            
            return output
    
    def update(self, table:str, filter:str, values:dict):
        '''
        update('tablename', filter='sql filter', values={'column': 'new_value', 'column2': 'new_value2', ...})\n
        or can be used as method of "select()" output - select(...).update(column=new_value, column2=new_value2, ...)
        '''
        if self._SUBD == 'sqlite':
            con = sqlite3.connect(self._db)
            cus = con.cursor()

            vals = ''
            for col, val in values.items():
                if not vals: vals += f" {col} = '{val}' "
                else:      vals += f" , {col} = '{val}' "

            cus.execute(f"update {table} set {vals} where {filter}")
            output = cus.fetchall()
            con.commit()
            cus.close()
            con.close()
            
            return output
        
        elif self._SUBD == 'postgre':
            con = psycopg.connect(dbname=self._db['dbname'],user=self._db['user'],password=self._db['password'],host=self._db['host'],port=self._db['port'])
            cus = con.cursor()

            vals = ''
            for col, val in values.items():
                if not vals: vals += f" {col} = '{val}' "
                else:      vals += f" , {col} = '{val}' "

            cus.execute(f"update {table} set {vals} where {filter}")
            output = cus.fetchall()
            con.commit()
            cus.close()
            con.close()
            
            return output

    def deletef(self, table:str, filter:str):
        '''
        deletef('tablename', filter='sql_filter')
        '''
        if self._SUBD == 'sqlite':
            con = sqlite3.connect(self._db)
            cus = con.cursor()
            cus.execute(f"delete from {table} {f"where {filter}" if filter else ''}")
            output = cus.fetchall()
            con.commit()
            cus.close()
            con.close()
            
            return output
        elif self._SUBD == 'postgre':
            con = psycopg.connect(dbname=self._db['dbname'],user=self._db['user'],password=self._db['password'],host=self._db['host'],port=self._db['port'])
            cus = con.cursor()
            cus.execute(f"delete from {table} {f"where {filter}" if filter else ''}")
            output = cus.fetchall()
            con.commit()
            cus.close()
            con.close()
            
            return output
        
    def delete(self, table:str, **filter):
        '''
        delete('tablename', column=value, column2=value2, ...)\n
        or can be used as method of "select()" output - select(...).delete()
        '''
        if self._SUBD == 'sqlite':
            con = sqlite3.connect(self._db)
            cus = con.cursor()

            filtr = ''
            for col, val in filter.items():
                if not filtr: filtr += f"{col} = {val}"
                else:      filtr += f"and {col} = {val}"

            cus.execute(f"delete from {table} {f"where {filtr}" if filtr else ''}")
            output = cus.fetchall()
            con.commit()
            cus.close()
            con.close()
            
            return output
        
        elif self._SUBD == 'postgre':
            con = psycopg.connect(dbname=self._db['dbname'],user=self._db['user'],password=self._db['password'],host=self._db['host'],port=self._db['port'])
            cus = con.cursor()

            filtr = ''
            for col, val in filter.items():
                if not filtr: filtr += f"{col} = {val}"
                else:      filtr += f"and {col} = {val}"

            cus.execute(f"delete from {table} {f"where {filtr}" if filtr else ''}")
            output = cus.fetchall()
            con.commit()
            cus.close()
            con.close()
            
            return output



class _db_table:
    def __init__(self, table_name:str, SUBD:str, connection:str):
        self._SUBD = SUBD
        if SUBD.lower() == 'sqlite':
            self._SUBD = 'sqlite'
            self._db = connection
            self._columns = []
            con = sqlite3.connect(self._db)
            cus = con.cursor()
            cus.execute(f"select name from PRAGMA_TABLE_INFO('{table_name}')")
            for name in cus.fetchall():
                self._columns.append(name[0])
        elif SUBD.lower() == 'postgre':
            self._SUBD = 'postgre'
            self._db = connection
            self._columns = []
            conn = psycopg.connect(dbname=self._db['dbname'],user=self._db['user'],password=self._db['password'],host=self._db['host'],port=self._db['port'])
            cus = conn.cursor()
            cus.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
            for name in cus.fetchall():
                self._columns.append(name[0])
            conn.commit()
            cus.close()
            conn.close()
            
        self._table_name = table_name

    def __str__(self):
        outp = f'{self._columns}'
        return f"<{outp}>"
    
    def __repr__(self):
        outp = f'{self._columns}'
        return f"<db table (columns: {outp})>"


    def selectf(self, columns:list=[], filter:str=None):
        '''
        select(columns=['column1', 'column2', ... ,], filter='sql filter')\n
        select(filter='sql filter') - all columns\n\n
        '''
        table = self._table_name
        if self._SUBD == 'sqlite':
            con = sqlite3.connect(self._db)
            cus = con.cursor()
            if not columns:
                columns = self._columns
            cols = ''
            for c in columns:
                if not cols: cols += c
                else: cols += ',' + c
            cus.execute(f"select {cols} from {table} {f'where {filter}' if filter else ''}")
            res = cus.fetchall()
            output = []
            for r in res:
                one = {}
                for i in range(0,len(columns)):
                    one[columns[i]] = r[i]
                output.append(_db_output(one, table, self._SUBD, self._db))
            con.commit()
            cus.close()
            con.close()
            
            return output
    
    def select(self, *columns, **filter):
        '''
        select('column1', 'column2', ... , column=value, column2=value, ...)\n
        select(column=value, column1=value1, ...) - all columns\n\n
        '''
        table = self._table_name
        if self._SUBD == 'sqlite':
            con = sqlite3.connect(self._db)
            cus = con.cursor()

            if not columns:
                columns = tuple(self._columns)
                
            cols = ''
            for c in columns:
                if not cols: cols += c
                else: cols += ',' + c

            filtr = ''
            for col, val in filter.items():
                if not filtr: 
                    if not val: filtr = f" ({col} = '' or {col} is NULL) "
                    else : filtr += f" {col} = '{val}' "
                else:
                    if not val: filtr = f" and ({col} = '' or {col} is NULL) "
                    else : filtr += f" and {col} = '{val}' "

            cus.execute(f"select {cols} from {table} {f'where {filtr}' if filtr else ''}")
            res = cus.fetchall()
            output = []
            for r in res:
                one = {}
                for i in range(0,len(columns)):
                    one[columns[i]] = r[i]
                output.append(_db_output(one, table, self._SUBD, self._db))
            con.commit()
            cus.close()
            con.close()
            
            return output

    def select1(self, *columns, **filter):
        '''
        same as select() but returns only first value
        '''
        table = self._table_name
        if self._SUBD == 'sqlite':
            con = sqlite3.connect(self._db)
            cus = con.cursor()

            if not columns:
                columns = tuple(self._columns)
                
            cols = ''
            for c in columns:
                if not cols: cols += c
                else: cols += ',' + c

            filtr = ''
            for col, val in filter.items():
                if not filtr: filtr += f" {col} = '{val}' "
                else:      filtr += f" and {col} = '{val}' "

            cus.execute(f"select {cols} from {table} {f'where {filtr}' if filtr else ''}")
            res = cus.fetchall()
            output = []
            for r in res:
                one = {}
                for i in range(0,len(columns)):
                    one[columns[i]] = r[i]
                output.append(_db_output(one, table, self._SUBD, self._db))
            con.commit()
            cus.close()
            con.close()
            
            return output[0] if output else None

    def update(self, filter:str, values:dict):
        '''
        update(filter='sql filter', values={'column': 'new_value', 'column2': 'new_value2', ...})\n
        !!!or can be used as method of "select()" output - select(...).update(column=new_value, column2=new_value2, ...)
        '''
        table = self._table_name
        if self._SUBD == 'sqlite':
            con = sqlite3.connect(self._db)
            cus = con.cursor()

            vals = ''
            for col, val in values.items():
                if not vals: vals += f" {col} = '{val}' "
                else:      vals += f" , {col} = '{val}' "

            cus.execute(f"update {table} set {vals} where {filter}")
            output = cus.fetchall()
            con.commit()
            cus.close()
            con.close()
            
            return output

    def insertf(self, columns:list=[], values:list=[]):
        '''
        incertf('columns=['column','column2', ...], values=['value1','value2',...])\n
        incertf(values=['value1','value2',...]) - all columns\n
        '''
        table = self._table_name
        if self._SUBD == 'sqlite':
            con = sqlite3.connect(self._db)
            cus = con.cursor()
            cols = ''
            for c in columns:
                if not cols: cols += c
                else: cols += ',' + c
            vals = ''
            for v in values:
                if not vals: vals += v
                else: vals += ',' + v
            cus.execute(f"insert into {table} {cols} values ({vals})")
            output = cus.fetchall()
            con.commit()
            cus.close()
            con.close()
            
            return output

    def insert(self, **colvals):
        '''
        incert(column=value, column_2=value_2, ...)\n
        '''
        table = self._table_name
        if self._SUBD == 'sqlite':
            con = sqlite3.connect(self._db)
            cus = con.cursor()
            cols = ''
            vals = ''
            for key, value in colvals.items():
                if not cols: cols += str(key)
                else: cols += ',' + str(key)
                if not vals: vals += f"'{value}'"
                else: vals += ',' + f"'{value}'"
            cus.execute(f"insert into {table} ({cols}) values ({vals})")
            output = cus.fetchall()
            con.commit()
            cus.close()
            con.close()
            
            return output

    def deletef(self, filter:str):
        '''
        deletef(filter='sql_filter')
        '''
        table = self._table_name
        if self._SUBD == 'sqlite':
            con = sqlite3.connect(self._db)
            cus = con.cursor()
            cus.execute(f"delete from {table} {f"where {filter}" if filter else ''}")
            output = cus.fetchall()
            con.commit()
            cus.close()
            con.close()
            
            return output
        
    def delete(self, **filter):
        '''
        delete(column=value, column2=value2, ...)\n
        or can be used as method of "select()" output - select(...).delete()
        '''
        table = self._table_name
        if self._SUBD == 'sqlite':
            con = sqlite3.connect(self._db)
            cus = con.cursor()

            filtr = ''
            for col, val in filter.items():
                if not filtr: filtr += f"{col} = {val}"
                else:      filtr += f"and {col} = {val}"

            cus.execute(f"delete from {table} {f"where {filtr}" if filtr else ''}")
            output = cus.fetchall()
            con.commit()
            cus.close()
            con.close()
            
            return output

class _db_output:
    def __init__(self, vals:dict, table_name:str, SUBD:str, connection:str ):
        if SUBD.lower() == 'sqlite':
            self._SUBD = 'sqlite'
            self._db = connection
            self._table_name = table_name
        elif SUBD.lower() == 'postgre':
            self._SUBD = 'postgre'
            self._db = connection
            self._table_name = table_name
        
        for key, value in vals.items():
            setattr(self,key,value)

    def __str__(self):
        outp = vars(self)
        if '_SUBD' in outp: del outp['_SUBD']
        if '_db' in outp: del outp['_db']
        if '_table_name' in outp: del outp['_table_name']
        return str(outp)
    def __repr__(self):
        outp = vars(self)
        if '_SUBD' in outp: del outp['_SUBD']
        if '_db' in outp: del outp['_db']
        if '_table_name' in outp: del outp['_table_name']
        return f"<sqlet {outp}>"
    def dict(self):
        outp = vars(self)
        if '_SUBD' in outp: del outp['_SUBD']
        if '_db' in outp: del outp['_db']
        if '_table_name' in outp: del outp['_table_name']
        return outp
    def _as_filter(self):
        dict = self.dict()
        filtr = ''
        for key, val in dict.items():
            one = ''
            if not val: one = f"({key} = '' or {key} is NULL)"
            else: one = f"{key} = '{val}'"
            if not filtr: filtr += f" {one} "
            else:       filtr += f" and {one} "
        return filtr

    def update(self,**values):
        if self._SUBD == 'sqlite':
            con = sqlite3.connect(self._db)
            cus = con.cursor()

            table = self._table_name

            vals = ''
            for col, val in values.items():
                if not vals: vals += f" {col} = '{val}' "
                else:      vals += f" , {col} = '{val}' "

            filtr = self._as_filter()

            cus.execute(f"update {table} set {vals} where {filtr}")
            output = ''
            con.commit()
            cus.close()
            con.close()
            
            return output
        
        elif self._SUBD == 'postgre':
            con = psycopg.connect(dbname=self._db['dbname'],user=self._db['user'],password=self._db['password'],host=self._db['host'],port=self._db['port'])
            cus = con.cursor()

            table = self._table_name

            vals = ''
            for col, val in values.items():
                if not vals: vals += f" {col} = '{val}' "
                else:      vals += f" , {col} = '{val}' "

            filtr = self._as_filter()

            cus.execute(f"update {table} set {vals} where {filtr}")
            output = ''
            con.commit()
            cus.close()
            con.close()
            
            return output

    def delete(self):
        if self._SUBD == 'sqlite':
            con = sqlite3.connect(self._db)
            cus = con.cursor()
            table = self._table_name
            filtr = self._as_filter()
            cus.execute(f"delete from {table} where {filtr}")
            output = cus.fetchall()
            con.commit()
            cus.close()
            con.close()
            
            return output
        
        elif self._SUBD == 'postgre':
            con = psycopg.connect(dbname=self._db['dbname'],user=self._db['user'],password=self._db['password'],host=self._db['host'],port=self._db['port'])
            cus = con.cursor()
            table = self._table_name
            filtr = self._as_filter()
            cus.execute(f"delete from {table} where {filtr}")
            output = cus.fetchall()
            con.commit()
            cus.close()
            con.close()
            
            return output