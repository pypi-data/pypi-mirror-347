from typing import Dict
from datetime import datetime
from pathlib import Path
import os
import psutil


class FactoryDinamic:
    @staticmethod
    def create_entity_file(entity_name: str, columns: Dict[str, str], output_path: str = "./") -> str:
        type_mapping = {
            str: 'String',
            int: 'Integer',
            datetime: 'DateTime',
            bool: 'Boolean',
            float: 'Float'
        }

        if 'id' not in columns:
            columns = {'id': int, **columns}

        content = (
            'from datetime import datetime\n'
            'from typing import Optional\n'
            'from sqlalchemy import String, Integer, DateTime, Boolean, Float\n'
            'from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column\n\n'
            'class Base(DeclarativeBase):\n'
            '    pass\n\n'
            f'class {entity_name.capitalize()}(Base):\n'
            f'    __tablename__ = "{entity_name.lower()}"\n\n'
        )

        for col_name, col_type in columns.items():
            is_primary = col_name == 'id'
            nullable = not is_primary
            content += (
                f"    {col_name}: Mapped[{'Optional[' if nullable else ''}"
                f"{col_type.__name__}{']' if nullable else ''}] = "
                f"mapped_column({type_mapping[col_type]}"
                f"{'' if col_type != str else '(255)'}, "
                f"{'primary_key=True, ' if is_primary else ''}"
                f"nullable={str(nullable)})\n"
            )

        file_path = Path(output_path) / f"{entity_name.lower()}.py"
        with open(file_path, 'w') as f:
            f.write(content)

        return file_path

    @staticmethod
    def check_and_manage_execution(etapa: str = 'inicio', pid_file: str = 'execution.pid') -> bool:
        """
        Gerencia a execução única do script através de arquivo PID
        
        Args:
            etapa: 'inicio' para verificar/criar PID ou 'fim' para remover
            pid_file: nome do arquivo para armazenar o PID
        Returns:
            bool: True se pode executar, False se já está em execução
        """
        pid_path = Path(pid_file)

        if etapa == 'inicio':
            if pid_path.exists():
                try:
                    with open(pid_path, 'r') as f:
                        old_pid = int(f.read().strip())

                    if psutil.pid_exists(old_pid):
                        print(f"Processo já está em execução (PID: {old_pid})")
                        return False
                    else:
                        pid_path.unlink()
                except (ValueError, IOError) as e:
                    print(f"Erro ao ler arquivo PID: {e}")
                    pid_path.unlink(missing_ok=True)

            try:
                with open(pid_path, 'w') as f:
                    f.write(str(os.getpid()))
                return True
            except IOError as e:
                print(f"Erro ao criar arquivo PID: {e}")
                return False

        elif etapa == 'fim':
            # Remove arquivo PID
            pid_path.unlink(missing_ok=True)
            return True

        return False

    @staticmethod
    def run_with_pid_control(func):
        def wrapper(*args, **kwargs):
            if FactoryDinamic.check_and_manage_execution(etapa='inicio'):
                try:
                    result = func(*args, **kwargs)
                    FactoryDinamic.check_and_manage_execution(etapa='fim')
                    return result
                except Exception as e:
                    FactoryDinamic.check_and_manage_execution(etapa='fim')
                    raise e
            return None
        return wrapper


if __name__ == "__main__":
    # Example usage
    @FactoryDinamic.run_with_pid_control
    def create_entity_file_example():
        """
        Exemplo de uso da função create_entity_file
        """
        columns = {
            'nome': str,
            'idade': int,
            'data_criacao': datetime
        }

        file_path = FactoryDinamic.create_entity_file('usuario', columns)
        print(f"Entity file created at: {file_path}")

