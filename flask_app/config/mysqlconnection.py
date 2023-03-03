import pymysql.cursors
import pymysql


class SqlConnection:
    def __init__(self, db='hashapp_schema'):
        host = 'localhost'
        port = 3306
        user = 'root'
        passwd = 'root'
        db = db
        self.db_conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
        self.cursor = self.db_conn.cursor()
        """
        dr run -d -p 3306:3306 --name hashapp_schema --mount src=hashapp_schema,dst=/var/lib/mysql  -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=hashapp_schema mariadb
        
        dr exec -ti hashapp_schema bash
        """

        self.cursor.execute("select @@version")
        output = self.cursor.fetchall()
        print(output)

    
    def consulta(self, query, params=None):
        self.query = query
        self.parametros = params
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def ejecutar_funcion(self, funcion, parametros = None):
        self.query = funcion
        self.parametros = parametros
        try:
            self.cursor.callproc(funcion, parametros)
            return True
        except Exception as e:
            # ex = Exception(f'''\n\n\nerror:\n{str(e)}\n\n\n\n\n\nquery:\n{str(self.query)}\n\n\n\n\n\nparams:\n{str(self.parametros)}\n\n\n''')
            # print(str(ex))
            # show_error(ex, send_email = True)
            print(e)
            self.db_conn.rollback()
            return False

    def consulta_asociativa(self, query, params=None):
        self.query = query
        self.parametros = params
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        descripcion = [d[0].lower() for d in self.cursor.description]
        # print(descripcion)
        resultado = [dict(zip(descripcion, linea)) for linea in self.cursor]
        # print(resultado)
        return resultado

    def ejecutar(self, query, parametros = None):
        self.parametros = parametros
        self.query = query
        try:
            if not parametros:
                self.cursor.execute(query)
                # print(self.cursor.bindvars)
                return True
            else:
                if isinstance(parametros, dict):
                    self.cursor.execute(None, parametros)
                    # print(self.cursor.bindvars)
                elif isinstance(parametros, list):
                    self.cursor.executemany(None, parametros)
                    # print(self.cursor.bindvars)
                else:
                    raise Exception('Parametros: tipo no valido')
                return True
        except Exception as e:
            # ex = Exception(f'''\n\n\nerror:\n{str(e)}\n\n\n\n\n\nquery:\n{str(self.query)}\n\n\n\n\n\nparams:\n{str(self.parametros)}\n\n\n''')
            # print(str(ex))
            # show_error(ex, send_email = True)
            print(e)
            self.db_conn.rollback()
            return False

    def commit(self):
        try:
            self.db_conn.commit()
            return True
        except Exception as e:
            # ex = Exception(f'''\n\n\nerror:\n{str(e)}\n\n\n\n\n\nquery:\n{str(self.query)}\n\n\n\n\n\nparams:\n{str(self.parametros)}\n\n\n''')
            # print(str(ex))
            # show_error(ex, send_email = True)
            print(e)
            self.db_conn.rollback()
            return False

    def rollback(self):
        self.db_conn.rollback()
        return True
    
    def close(self):
        self.db_conn.close()
        return True

    def paginador(self, query, registros_pagina = 10, pagina = 1, params = None):
        try:
            # print(query)
            if params:
                num_registros = len(self.consulta_asociativa(query, params))
            else:
                num_registros = len(self.consulta_asociativa(query))
            paginas = math.ceil(num_registros/registros_pagina)
            if paginas < pagina: pagina = paginas
            limite_superior = registros_pagina * pagina
            limite_inferior = limite_superior - registros_pagina + 1

            query = ''' SELECT *
                        FROM (SELECT a.*, ROWNUM rnum
                                FROM ({0}) A)
                        WHERE rnum BETWEEN {2} AND {1}
                    '''.format(query,
                            limite_superior,
                            limite_inferior)
            self.query = query
            self.parametros = params
            if params:
                registros = self.consulta_asociativa(query, params)
            else:
                registros = self.consulta_asociativa(query)

            if num_registros < registros_pagina:
                pagina = 1
            return {
                'registros': registros,
                'num_registros': num_registros,
                'paginas': paginas,
                'pagina': pagina,
            }
        except Exception as e:
            # ex = Exception(f'''\n\n\nerror:\n{str(e)}\n\n\n\n\n\nquery:\n{str(self.query)}\n\n\n\n\n\nparams:\n{str(self.parametros)}\n\n\n''')
            # print(str(ex))
            # show_error(ex, send_email = True)
            print(e)
            return False
