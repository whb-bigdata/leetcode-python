import os

from typing import Any, Optional, Sequence, Tuple

try:
    import psycopg2
    from psycopg2 import sql
except ModuleNotFoundError:
    psycopg2 = None
    sql = None


def pgconnect():
    """建立与 PostgreSQL 的连接"""
    if psycopg2 is None:
        print('缺少 psycopg2 驱动。请先执行: python3 -m pip install psycopg2-binary')
        return None

    conn = None
    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(
            host=os.getenv('PGHOST', 'localhost'),
            database=os.getenv('PGDATABASE', 'postgres'),
            user=os.getenv('PGUSER', 'postgres'),
            password=os.getenv('PGPASSWORD'),
            port=os.getenv('PGPORT', '5432'),
        )
        print('Connected successfully!')
    except Exception as e:
        print('Unable to connect to the database')
        print(e)
    return conn


def get_data_directory():
    """连接数据库并获取数据存储目录 (data_directory)"""
    conn = pgconnect()

    if not conn:
        print('数据库连接失败，无法查询路径。')
        return

    try:
        # 使用 with 语句，离开作用域时会自动关闭 cursor
        with conn.cursor() as cur:
            # 1. 执行 SQL 语句
            cur.execute('SHOW data_directory;')

            # 2. 获取单行结果 (SHOW 命令只返回一行结果)
            result = cur.fetchone()

            # result 是一个元组，例如: ('/opt/homebrew/var/postgresql@15',)
            if result:
                data_dir = result[0]
                print('\n====================================')
                print(f'PostgreSQL 数据目录为:\n{data_dir}')
                print('====================================\n')
                print(f'后续在终端停止数据库可直接使用命令:\npg_ctl stop -D {data_dir} -m fast')
                return data_dir

    except Exception as e:
        print('执行 SQL 查询出错:', e)

    finally:
        # 3. 始终确保关闭数据库连接
        conn.close()
        print('Database connection closed.')


def display_query_results(columns: Sequence[str], rows: Sequence[Sequence[Any]]) -> None:
    """以简单表格形式展示查询结果。"""
    if not columns:
        print('查询没有返回列。')
        return
    if not rows:
        print('查询成功，但没有返回记录。')
        return

    text_rows = [["NULL" if value is None else str(value) for value in row] for row in rows]
    widths = [len(column) for column in columns]
    for row in text_rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(value))

    separator = '+-' + '-+-'.join('-' * width for width in widths) + '-+'
    header = '| ' + ' | '.join(
        column.ljust(width) for column, width in zip(columns, widths)
    ) + ' |'
    print(separator)
    print(header)
    print(separator)
    for row in text_rows:
        print('| ' + ' | '.join(value.ljust(width) for value, width in zip(row, widths)) + ' |')
    print(separator)
    print(f'共 {len(rows)} 条记录。')


def run_select_query(
    query: Any, params: Optional[Sequence[Any]] = None
) -> Optional[Tuple[list[str], list[tuple[Any, ...]]]]:
    """执行只读查询，展示并返回 (列名, 记录)。

    参数必须通过 ``params`` 传入，而不是使用字符串拼接，防止 SQL 注入。
    连接失败或查询失败时返回 None。
    """
    conn = pgconnect()
    if not conn:
        return None

    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            if cur.description is None:
                print('该 SQL 没有返回结果集。请使用 run_select_query 执行 SELECT/SHOW 查询。')
                return [], []

            columns = [description[0] for description in cur.description]
            rows = cur.fetchall()
            display_query_results(columns, rows)
            return columns, rows
    except Exception as error:
        print('执行查询出错:', error)
        return None
    finally:
        conn.close()
        print('Database connection closed.')


def get_all_table_names(schema: str = 'public') -> list[str]:
    """查询并返回指定 schema 中的所有普通表名。"""
    result = run_select_query(
        """
        SELECT tablename
        FROM pg_catalog.pg_tables
        WHERE schemaname = %s
        ORDER BY tablename;
        """,
        (schema,),
    )
    if result is None:
        return []
    _, rows = result
    return [row[0] for row in rows]


def display_table(table_name: str, schema: str = 'public', limit: int = 20) -> None:
    """查询并展示一张表的前 ``limit`` 条记录。

    schema 与 table_name 是 SQL 标识符，不能作为普通 %s 参数传入；因此使用
    psycopg2.sql.Identifier 安全地引用它们。limit 仍使用参数化查询。
    """
    if limit < 0:
        raise ValueError('limit 必须大于或等于 0')
    if sql is None:
        print('缺少 psycopg2 驱动，无法执行 PostgreSQL 查询。')
        return

    query = sql.SQL('SELECT * FROM {}.{} LIMIT %s').format(
        sql.Identifier(schema), sql.Identifier(table_name)
    )
    run_select_query(query, (limit,))


# 执行函数
if __name__ == '__main__':
    get_data_directory()
    tables = get_all_table_names()
    if tables:
        print(f'发现的表: {tables}')
        print(f'展示表 {tables[0]} 的前 20 条记录:')
        display_table(tables[0])
