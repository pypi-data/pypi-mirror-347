from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from typing import Literal, Optional

from .exceptions_db import DatabaseConnectionError, DatabaseTypeError, SessionError


class DBConnection:
    def __init__(
        self,
        connection_string: str = None,
        username: str = None,
        password: str = None,
        hostname: str = None,
        port: int = None,
        database_name: str = None,
        dialect: Literal["pyodbc", "psycopg2"] = None,
        db_type: Literal["sql_server", "mysql", "postgres", "sqlite"] = "sqlite"
    ):
        self.username = username
        self.password = password
        self.hostname = hostname
        self.port = port
        self.database_name = database_name
        self.dialect = dialect
        self.db_type = db_type
        self.connection_string = connection_string
        self.engine = None
        self.session: Optional[Session] = None

        if not self.connection_string and self._can_build_connection_string():
            self.connection_string = self._build_connection_string()

        self._build_connection()

    def _can_build_connection_string(self) -> bool:
        return all([self.username, self.password, self.hostname, self.port, self.database_name])

    def _build_connection_string(self) -> str:
        if self.db_type == "sql_server":
            port_part = f":{self.port}" if self.port else ""
            driver = "pyodbc" if self.dialect == "pyodbc" else "pymssql"
            return f"mssql+{driver}://{self.username}:{self.password}@{self.hostname}{port_part}/{self.database_name}"
        elif self.db_type == "mysql":
            return f"mysql+pymysql://{self.username}:{self.password}@{self.hostname}:{self.port}/{self.database_name}"
        elif self.db_type == "postgres":
            driver = "+psycopg2" if self.dialect == "psycopg2" else ""
            return f"postgresql{driver}://{self.username}:{self.password}@{self.hostname}:{self.port}/{self.database_name}"
        elif self.db_type == "sqlite":
            return f"sqlite:///{self.database_name}.sqlite3"
        else:
            raise DatabaseTypeError("Tipo de banco de dados não suportado.")

    def _build_connection(self):
        try:
            if self.db_type == "sql_server":
                self._handle_sql_server_connection()
            else:
                self._create_and_validate_engine(self.connection_string)
        except Exception as e:
            self._handle_connection_error(e)

    def _handle_sql_server_connection(self):
        drivers = [
            "?driver=ODBC+Driver+17+for+SQL+Server",
            "?driver=ODBC+Driver+13+for+SQL+Server",
            "?driver=SQL+Server"
        ]
        for driver in drivers:
            try:
                self._create_and_validate_engine(self.connection_string + driver)
                break
            except Exception as e:
                if "No module named" in str(e):
                    raise DatabaseConnectionError(f"Driver não encontrado: {driver}")
                continue

    def _create_and_validate_engine(self, connection_string):
        self.engine = create_engine(connection_string, echo=False)
        with self.engine.connect() as conn:
            conn.execute(text("SELECT 1"))

    def _handle_connection_error(self, e: Exception):
        error_msg = str(e).lower()
        if "login failed" in error_msg or "authentication failed" in error_msg:
            raise DatabaseConnectionError("Autenticação falhou. Verifique suas credenciais.")
        elif "timeout" in error_msg:
            raise DatabaseConnectionError("Tempo de conexão esgotado. Verifique o alcance do servidor.")
        elif "database" in error_msg and "not exist" in error_msg:
            raise DatabaseConnectionError("O banco de dados não existe.")
        else:
            raise DatabaseConnectionError(f"Falha ao conectar ao banco de dados: {str(e)}")

    def get_engine(self):
        return self.engine

    def __enter__(self):
        try:
            local_session = sessionmaker(bind=self.engine)
            self.session = local_session()
            return self
        except Exception as e:
            raise SessionError(f"Failed to create session: {str(e)}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            self.session.close()


if __name__ == "__main__":
    db = DBConnection(
        username="your_username",
        password="your_password",
        hostname="localhost",
        port=1433,
        database_name="teste"
    )
    with db as connection:
        engine = connection.get_engine()
        print("Connection established successfully.")
