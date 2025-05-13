# coding:utf-8
from tools_hjh import DBConn, Tools, ProcessPool
from tools_hjh.Tools import locatdate, str_exception
from tools_hjh import Log
from tools_hjh import ThreadPool
from tools_hjh import OracleTools
import time
from math import ceil
import sys
from uuid import uuid4
from concurrent.futures import TimeoutError

help_mess = '''Version 2.11.14

使用方法
python3 ora2pg.py example.conf run_mode example.log
example.log会被清空重写

run_mode : ↓
copy_table 复制表结构，包括表、分区和注释，也包括列上的默认值和非空约束 
copy_data 复制数据，tables参数的对象必须是自己库的表、视图或同义词等，不能是引用其他库的dblink
copy_data 现在有限支持P2O、O2O和P2P的数据复制，P2O和P2P不支持分页，不支持检查点
copy_index 复制索引
copy_pk 复制主键
copy_fk 复制外键
copy_uk 复制唯一键
copy_sequence 复制序列
copy_from_sql 根据给入的SQL去Oracle查询，结果复制数据到PG
compare_data_number 统计每个表在Oracle和PG端的数据量是否一致，但是不会校对数据
compare_index 统计每个表在Oracle和PG端的索引量是否一致（不包含约束自带的索引），但是不会比较索引列
compare_constraint 统计每个表在Oracle和PG端的主键+外键+唯一键数量是否一致
get_table_ddl 得到copy_table的PG端的SQL到日志文件
get_table_oracle_ddl 得到copy_table的Oracle端的SQL到日志文件
drop_fk 删除PG端已存在的外键

注意事项：
copy_table，表名列名无论oracle中是大小写，转为pg中一律为小写
copy_table，is_clear=yes会提前drop table，如果表存在外键关联第一次可能删不掉，多执行几次copy_table即可
copy_table，rowid类型会转为varchar(18)，而不是oid，转为oid数据迁移不过去
copy_table：RAW(16)类型会转为PG的UUID类型，且数据rawtohex函数处理后写入PG。其他RAW长度转为bytea，作为二进制处理
copy_data，is_clear=yes会提前清空表
copy_data，O2P时，oracle中的chr(0)会被强行替换为chr(32)
copy_data，O2P时，oracle中date和timestamp类型中的0000年会被强行替换为0001年，00月替换为01月，00日替换为01日
copy_data，O2P时，收集元数据时，会count表，is_count_full=yes则强制走全表，避免索引与表不同步的情况，因此大表可能比较慢
copy_index，is_clear决定是否会先drop已存在索引
copy_index，如果索引名已被占用（被其他对象占用），且is_clear=yes会自动重命名
copy_index，对于分区表的唯一索引，会自动在末尾加入分区字段
copy_index，sys_op_c2c(cols)函数会被去掉，仅索引cols
copy_pk、copy_fk、copy_uk，使用命名模式，重名会失败
copy_pk、copy_fk、copy_uk，is_clear决定是否会先drop已存在约束
copy_pk、copy_uk，对于分区表的主键和唯一键，会自动在末尾加入分区字段
compare_data_number，只会比较两端每个表行数是否一致，而无法校对数据
compare_index、compare_constraint，只会比较两端每个表的索引数量、键数量是否一致，而不会去比较被索引或被键的字段
copy_from_sql，不支持并行
drop_fk，重建pk的时候如果有外键依赖则删除不了，所以设置删除外键的选项

目前已发现的容易出问题的情况有：
1.被索引字段含有函数
2.默认值含有函数
3.Oracle中存在大小写不同但是名字相同的表，于是出现多对一的情况
4.对于tables中的对象是视图的情况，可以同步表结构和数据，但是无法同步分区、注释、索引、约束等信息
5.如果tables中的源表是一个通过dblink同步过来的视图或同义词，copy_data会失败，但是却可以通过copy_from_sql抽取
6.在表名和用户名中慎用大小写混合，通常oracle全大写，pg全小写
'''

date = locatdate().replace('-', '')

try:
    run_mode = sys.argv[2]
except:
    run_mode = None
try:
    config_file = sys.argv[1]
except:
    config_file = None
try:
    log_file = sys.argv[3]
except:
    log_file = date + '.log'
    
if config_file == None or config_file == 'help':
    print(help_mess)
    sys.exit()

Tools.rm(log_file)
log = Log(log_file)

conf = Tools.cat(config_file)
conf_map = {}
for line in conf.split('\n'):
    if '=' in line and not line.startswith('#'):
        key = line.split('=', 1)[0].strip()
        val = line.split('=', 1)[1].strip()
        conf_map[key] = val

forever_number_to_numeric = conf_map['forever_number_to_numeric'].lower().replace('true', 'yes')
if forever_number_to_numeric == 'yes':
    forever_number_to_numeric = True
else:
    forever_number_to_numeric = False

is_auto_count = conf_map['is_auto_count'].lower().replace('true', 'yes')
is_count_full = conf_map['is_count_full'].lower().replace('true', 'yes')
smallest_object = conf_map['smallest_object'].lower()
is_only_insert = conf_map['is_only_insert'].lower().replace('true', 'yes')
is_clear = conf_map['is_clear'].lower().replace('true', 'yes')
is_only_scn = conf_map['is_only_scn'].lower().replace('true', 'yes')
# is_optimize_clob = conf_map['is_optimize_clob'].lower().replace('true', 'yes')

if conf_map['is_to_lower'].lower().replace('true', 'yes') == 'yes':
    is_to_lower = True
else:
    is_to_lower = False

compare_data_number_maximum_percentage_difference = float(conf_map['compare_data_number_maximum_percentage_difference'])
src_db_type = conf_map['src_db_type']
src_ip = conf_map['src_ip']
src_port = int(conf_map['src_port'])
src_database = conf_map['src_db']
src_read_username = conf_map['src_read_username']
src_read_password = conf_map['src_read_password']

tables = conf_map['tables']
exclude_tables = conf_map['exclude_tables']
sqls = conf_map['copy_from_sql']

dst_db_type = conf_map['dst_db_type']
dst_ip = conf_map['dst_ip']
dst_port = int(conf_map['dst_port'])
dst_database = conf_map['dst_db']
dst_username = conf_map['dst_username']
dst_password = conf_map['dst_password']

parallel_num = int(conf_map['parallel_num'])
if parallel_num < 1:
    parallel_num = 1
    
max_page_num = int(conf_map['page_num'])
if max_page_num < 1:
    max_page_num = 1
if max_page_num > parallel_num:
    max_page_num = parallel_num - 1

save_parallel = 3

once_mb = 20
once_num_normal = 50000
once_num_lob = 1000

input_global_scn = conf_map['scn']

tables_data_num = {}
tasks = []

scn_time = 0
get_matedata_over = False


# 主控制程序
def main():
    if run_mode == 'copy_data':
        if src_db_type == 'oracle' and dst_db_type == 'pgsql':
            copy_data_o2x()
        elif src_db_type == 'oracle' and dst_db_type == 'oracle':
            copy_data_o2x()
        elif src_db_type == 'pgsql' and dst_db_type == 'oracle':
            copy_data_p2x()
        elif src_db_type == 'pgsql' and dst_db_type == 'pgsql':
            copy_data_p2x()
        
    elif run_mode == 'copy_table':
        if src_db_type == 'oracle' and dst_db_type == 'pgsql':
            copy_table_o2p()
        elif src_db_type == 'oracle' and dst_db_type == 'oracle':
            copy_table_o2o()
        
    elif run_mode == 'copy_index':
        if src_db_type == 'oracle' and dst_db_type == 'pgsql':
            copy_index_o2p()
        elif src_db_type == 'oracle' and dst_db_type == 'oracle':
            copy_index_o2o()
        
    elif run_mode == 'copy_pk' or run_mode == 'copy_uk' or run_mode == 'copy_fk' or run_mode == 'drop_fk':
        if src_db_type == 'oracle' and dst_db_type == 'pgsql':
            copy_constraint_o2p(run_mode)
        elif src_db_type == 'oracle' and dst_db_type == 'oracle':
            copy_constraint_o2o(run_mode)
    
    elif run_mode == 'copy_check':
        if src_db_type == 'oracle' and dst_db_type == 'pgsql':
            copy_check_o2p()
        
    elif run_mode == 'copy_sequence' or run_mode == 'copy_seq':
        if src_db_type == 'oracle' and dst_db_type == 'pgsql':
            copy_sequence_o2p()
        elif src_db_type == 'oracle' and dst_db_type == 'oracle':
            copy_sequence_o2o()
        
    elif run_mode == 'compare_data_number':
        compare_data_number()
        
    elif run_mode == 'compare_index':
        if src_db_type == 'oracle' and dst_db_type == 'pgsql':
            compare_index_o2p()
        
    elif run_mode == 'compare_constraint':
        if src_db_type == 'oracle' and dst_db_type == 'pgsql':
            compare_constraint_o2p()
        
    elif run_mode == 'copy_from_sql':
        if src_db_type == 'oracle' and dst_db_type == 'pgsql':
            copy_from_sql_o2p()
    
    elif run_mode == 'get_table_oracle_ddl':
        get_table_oracle_ddl()
        
    elif run_mode == 'get_table_pg_ddl':
        get_table_pg_ddl()
    
    else:
        print(help_mess)

    
def print_error(e):
    log.error(str(e))


def get_table_map_list(src_db):
    # 解析出需要迁移的表以及映射关系
    table_map_list = []
    for table_mess in tables.split('[--split--]'):
        table_mess = table_mess.strip()
        src_where = '1=1'
        # 根据有没有-->分两类，再根据有没有where分两类，敲定src_schema，src_table，src_where，dst_schema，dst_table
        if '-->' in table_mess:
            if 'where' in table_mess:
                src_schema = table_mess.split('-->')[0].split('.')[0].strip()
                src_table = table_mess.split('-->')[0].split('.')[1].split('where')[0].strip()
                src_where = table_mess.split('-->')[0].split('.')[1].split('where')[1].strip()
            else:
                src_schema = table_mess.split('-->')[0].split('.')[0].strip()
                src_table = table_mess.split('-->')[0].split('.')[1].strip()
            dst_schema = table_mess.split('-->')[1].split('.')[0].strip()
            dst_table = table_mess.split('-->')[1].split('.')[1].strip()
        else:
            if 'where' in table_mess:
                src_schema = table_mess.split('.')[0].strip()
                src_table = table_mess.split('.')[1].split('where')[0].strip()
                src_where = table_mess.split('.')[1].split('where')[1].strip()
            else:
                src_schema = table_mess.split('.')[0].strip()
                src_table = table_mess.split('.')[1].strip()
            dst_schema = src_schema
            dst_table = src_table
            
        # 根据数据库类型，决定大小写，无论怎样，用户大小写需要规范化
        if is_to_lower:
            if src_db_type == 'oracle' and dst_db_type == 'pgsql':
                src_schema = src_schema.upper()
                if '-->' not in table_mess:
                    dst_schema = dst_schema.lower()
                    dst_table = dst_table.lower()
            elif src_db_type == 'pgsql' and dst_db_type == 'oracle':
                src_schema = src_schema.lower()
                if '-->' not in table_mess:
                    dst_schema = dst_schema.upper()
                    dst_table = dst_table.upper()
            elif src_db_type == 'pgsql' and dst_db_type == 'pgsql':
                src_schema = src_schema.lower()
                if '-->' not in table_mess:
                    dst_schema = dst_schema.lower()
                    dst_table = dst_table
            elif src_db_type == 'oracle' and dst_db_type == 'oracle':
                src_schema = src_schema.upper()
                if '-->' not in table_mess:
                    dst_schema = dst_schema.upper()
                    dst_table = dst_table
        else:
            if src_db_type == 'oracle' and dst_db_type == 'pgsql':
                src_schema = src_schema.upper()
                dst_schema = dst_schema.lower()
            elif src_db_type == 'pgsql' and dst_db_type == 'oracle':
                src_schema = src_schema.lower()
                dst_schema = dst_schema.upper()
            elif src_db_type == 'pgsql' and dst_db_type == 'pgsql':
                src_schema = src_schema.lower()
                dst_schema = dst_schema.lower()
            elif src_db_type == 'oracle' and dst_db_type == 'oracle':
                src_schema = src_schema.upper()
                dst_schema = dst_schema.upper()

        # 判断src_table是不是*，如果是，根据不同数据库类型判定src_table
        if src_table != '*':
            table_map = (src_schema, src_table, dst_schema, dst_table, src_where)
            if table_map not in table_map_list and table_map[0] + '.' + table_map[1] not in exclude_tables:
                table_map_list.append(table_map)
        elif src_table == '*' and src_db_type == 'oracle':
            select_tables_sql = "select table_name from dba_tables where table_name not like '%$%' and owner = '" + src_schema + "' order by 1"
            tables_from_sql = src_db.run(select_tables_sql).get_rows()
            for table_from_sql in tables_from_sql:
                if dst_db_type == 'pgsql' and is_to_lower:
                    table_map = (src_schema, table_from_sql[0], dst_schema, table_from_sql[0].lower(), src_where)
                else:
                    table_map = (src_schema, table_from_sql[0], dst_schema, table_from_sql[0], src_where)
                if table_map not in table_map_list and table_map[0] + '.' + table_map[1] not in exclude_tables:
                    table_map_list.append(table_map)
        elif src_table == '*' and src_db_type == 'pgsql':
            select_tables_sql = '''
                select c.relname from pg_class c
                join pg_namespace n on c.relnamespace = n.oid
                join pg_roles r on r.oid = c.relowner
                where n.nspname = ?
                and c.relkind in('r', 'p')
                and not c.relispartition
                and not exists(select 1 from pg_inherits where inhrelid = c.oid)
                order by 1
            '''
            tables_from_sql = src_db.run(select_tables_sql, (src_schema,)).get_rows()
            for table_from_sql in tables_from_sql:
                if dst_db_type == 'oracle':
                    table_map = (src_schema, table_from_sql[0], dst_schema, table_from_sql[0].upper(), src_where)
                elif dst_db_type == 'pgsql':
                    table_map = (src_schema, table_from_sql[0], dst_schema, table_from_sql[0], src_where)
                if table_map not in table_map_list and table_map[0] + '.' + table_map[1] not in exclude_tables:
                    table_map_list.append(table_map)
    return table_map_list

        
def copy_data_o2x():
        
    # 获取连接
    src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password, poolsize=parallel_num + 5)
    
    # 解析出需要迁移的表以及映射关系
    table_map_list = get_table_map_list(src_db)
    
    # 清理表
    if is_clear == 'yes':
        dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, poolsize=parallel_num + 5)
        tp = ThreadPool(parallel_num)
        for table_map in table_map_list:
            tp.run(truncate_table, (dst_db, table_map))
        tp.wait()
        dst_db.close()
            
    # 获取scn，如果需要
    if is_only_scn == 'yes' and len(input_global_scn) == 0:
        global scn_time
        global_scn, scn_time = src_db.run("select to_char(current_scn),to_char(SYSTIMESTAMP(6),'yyyy-mm-dd hh24:mi:ss.ff6') from v$database").get_rows()[0]
    elif is_only_scn == 'yes' and len(input_global_scn) > 0:
        global_scn = input_global_scn
    else:
        global_scn = None
    
    # 多线程启动表分析程序    
    def run_get_table_metadata(tp, src_db):
        try:
            global get_matedata_over
            for table_map in table_map_list:
                try:
                    qrs = src_db.run('select * from ' + table_map[0] + '."' + table_map[1] + '" where rownum = 1')
                except Exception as _:
                    log.error('获取元数据失败', table_map[0] + '.' + table_map[1], str_exception(_))
                    continue
                col_desc = qrs.get_cols_description()
                rows = qrs.get_rows()
                if len(rows) > 0:
                    tp.run(get_table_metadata, (src_db, table_map, global_scn, col_desc), name=table_map[0] + '.' + table_map[1])
            
            # 监控元数据获取未完成的表
            log.info('获取元数据任务全部分配完成。')
            while True:
                if tp.get_running_num() > 0 and tp.get_running_num() <= parallel_num:
                    log.info('获取元数据，正在执行的表：' + str(set(tp.get_running_name())))
                    
                if tp.get_running_num() > 0:
                    time.sleep(5)
                else:
                    break
            
            # 等待获取元数据完全完成
            tp.wait()
            src_db.close()
            get_matedata_over = True
            log.info('获取元数据任务全部执行完成。')
        except Exception as _:
            log.error('获取元数据失败', str_exception(_))
        
    tp = ThreadPool(parallel_num)
    ttp = ThreadPool(1)
    ttp.run(run_get_table_metadata, (tp, src_db,))
    # ttp.wait()
    
    # 多进程启动导数
    pp = ProcessPool(parallel_num)

    def callback(task):
        if task is not None:
            # get_data_from_oracle(*task)
            pp.run(get_data_from_oracle, task, name=task[1], callback=callback, error_callback=print_error)
    
    already_run_tasks = []
    while True:
        time.sleep(1)
        for task in tasks.copy():
            if task not in already_run_tasks:
                already_run_tasks.append(task)
                pp.run(get_data_from_oracle, task, name=task[1], callback=callback, error_callback=print_error)
    
        if len(tasks) == len(already_run_tasks) and get_matedata_over:
            log.info('导数任务全部分配完成。')
            break
    
    while True:
        if pp.get_running_num() > 0:
            if len(set(pp.get_running_name())) > 0 and len(set(pp.get_running_name())) <= parallel_num:
                log.info('导数任务，正在执行的任务：' + str(len(set(pp.get_running_name()))) + '个' + '，' + str(set(pp.get_running_name())))
            else:
                log.info('导数任务，正在执行的任务：' + str(len(set(pp.get_running_name()))) + '个')
            time.sleep(5)
        else:
            break
    
    log.info('导数任务全部执行完成。')
    
    # 获取输出报告
    if is_auto_count == 'yes':
        compare_data_number()


def truncate_table(dst_db, table_map):
    try:
        dst_schema = table_map[2]
        dst_table = table_map[3]
        dst_conn = dst_db.dbpool.connection()
        if dst_db_type == 'pgsql':
            truncate_table_sql = 'truncate table ' + dst_schema + '."' + dst_table + '" cascade'
        elif dst_db_type == 'oracle':
            truncate_table_sql = 'truncate table ' + dst_schema + '."' + dst_table + '"'
        dst_cur = dst_conn.cursor()
        dst_cur.execute(truncate_table_sql)
        dst_conn.commit()
        log.info(dst_db_type + '执行SQL成功', truncate_table_sql)
    except Exception as _:
        log.warning(dst_db_type + '执行SQL失败', truncate_table_sql, str_exception(_))
    finally:
        dst_cur.close()
        dst_conn.close()


# 表分析程序
def get_table_metadata(src_db, table_map, global_scn, col_desc):

    def fenye(table_map, mess, table_scn, table_metadata):
        my_once_num = once_num_normal
        for c in col_desc:
            if 'LOB' in str(c[1]) or 'RAW' in str(c[1]) or 'LONG' in str(c[1]):
                my_once_num = once_num_lob
                break
        
        if max_page_num == 1:
            if is_count_full == 'yes':
                count_sql = 'select /*+full(t) parallel(1)*/ count(1) from ' + mess + ' as of scn ' + table_scn + ' t where ' + src_where
            else:
                count_sql = 'select /*+parallel(1)*/ count(1) from ' + mess + ' as of scn ' + table_scn + ' t where ' + src_where
            src_num = src_db.run(count_sql).get_rows()[0][0]
            tasks.append((table_map, mess, table_scn, col_desc, table_metadata, None, None))
        else:
            # 分页
            if is_count_full == 'yes':
                count_sql = 'select /*+full(t) parallel(1)*/ count(1) from ' + mess + ' as of scn ' + table_scn + ' t where ' + src_where
            else:
                count_sql = 'select /*+parallel(1)*/ count(1) from ' + mess + ' as of scn ' + table_scn + ' t where ' + src_where
            src_num = src_db.run(count_sql).get_rows()[0][0]
            log.info('获取源端数据量成功', mess, str(src_num))
            if src_num < my_once_num * max_page_num:
                tasks.append((table_map, mess, table_scn, col_desc, table_metadata, None, None))
            else:
                page_rn = ceil(src_num / max_page_num)
                for page in range(1, max_page_num + 1):
                    tasks.append((table_map, mess, table_scn, col_desc, table_metadata, page, page_rn))
        return src_num
    
    try:
        src_schema = table_map[0]
        src_table = table_map[1]
        dst_schema = table_map[2]
        dst_table = table_map[3]
        src_where = table_map[4]

        # 如果没有scn，则此处获取
        if global_scn is None:
            table_scn = src_db.run('select to_char(current_scn) from v$database').get_rows()[0][0]
        else:
            table_scn = global_scn
            
        # 判定“表”是什么
        object_type = ''
        sql = 'select wm_concat(distinct object_type) from dba_objects where owner = ? and object_name = ?'
        rows = src_db.run(sql, (src_schema, src_table)).get_rows()
        if len(rows) == 0:
            object_type = 'other'
        elif 'TABLE' in str(rows[0]):
            object_type = 'table'
            table_metadata = OracleTools.get_table_metadata(src_db, src_schema, src_table, partition=True)
        elif 'VIEW' in str(rows[0]):
            object_type = 'view'
        elif 'SYNONYM' in str(rows[0]):
            object_type = 'synonym'
        else:
            object_type = 'other'
                
        report_table_id = src_schema + '.' + src_table + '-->' + dst_schema + '.' + dst_table
        # 如果是表，获取表元数据信息，遍历分区子分区，多进程分配查询任务及后续任务
        if object_type == 'table':
            src_num = 0
            partition_mess = table_metadata['partition']
            if partition_mess is not None and smallest_object != 'table':
                for partition in partition_mess['partitions']:
                    partition_name = partition['name']
                    subpartitions = partition['subpartitions']
                    # 子分区
                    if len(subpartitions) > 0 and smallest_object == 'subpartition':
                        for subpartition in subpartitions:
                            subpartition_name = subpartition['name']
                            mess = src_schema + '."' + src_table + '" subpartition(' + subpartition_name + ')'
                            src_num = src_num + fenye(table_map, mess, table_scn, table_metadata)
                    # 分区
                    else:
                        mess = src_schema + '."' + src_table + '" partition(' + partition_name + ')'
                        src_num = src_num + fenye(table_map, mess, table_scn, table_metadata)
            # 单表
            else:
                mess = src_schema + '."' + src_table + '"'
                src_num = fenye(table_map, mess, table_scn, table_metadata)
        # 其他类型
        else:
            table_metadata = None
            mess = src_schema + '."' + src_table + '"'
            src_num = fenye(table_map, mess, table_scn, table_metadata)
        tables_data_num[report_table_id] = [table_scn, src_num, None]
        log.info('获取表元数据成功', src_schema + '.' + src_table)
    except Exception as _:
        log.error('获取表元数据失败', src_schema + '.' + src_table, str_exception(_))


def get_data_from_oracle(table_map, mess, table_scn, col_desc, table_metadata=None, page=None, page_rn=None, retry_time=0):
    select_sql = ''
    
    def ready():
        try:
            nonlocal select_sql
            src_where = table_map[4]
            dst_schema = table_map[2]
            my_mess = mess + '(' + str(page) + ')'
        
            # 获取连接
            src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password, poolsize=max_page_num + 5)
            dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, poolsize=save_parallel + 5, options='-c search_path=' + dst_schema + ',public')
            
            # copy中转为csv要用
            cols_for_copy = col_desc
            # cols_for_copy = src_db.run('select * from ' + mess + ' where rownum = 1').get_cols_description()
            if table_metadata is not None:
                idx = 0
                for col in table_metadata['columns']:
                    virtual = col['virtual']
                    if virtual == 'YES':
                        cols_for_copy.pop(idx)
                    idx = idx + 1
            
            # 解析列，用于拼接cols_str和merge_col，处理char，拆分clob
            is_exists_blob = False
            once_num = once_num_normal
            cols_str = ''
            
            if dst_db_type == 'pgsql':
                for col in cols_for_copy:
                    if 'CHAR' in str(col[1]):
                        cols_str = cols_str + 'translate("' + col[0] + '",chr(0),chr(32)),' 
                    elif 'CLOB' in str(col[1]):
                        once_num = once_num_lob
                        cols_str = cols_str + 'replace("' + col[0] + '",chr(0),chr(32)),' 
                    elif 'DATE' in str(col[1]):
                        cols_str = cols_str + '''replace(replace(replace(to_char("''' + col[0] + '''",'yyyy-mm-dd hh24:mi:ss'),'0000-','0001-'),'-00-','-01-'),'-00','-01'),'''
                    elif 'TIMESTAMP' in str(col[1]):
                        cols_str = cols_str + '''replace(replace(replace(to_char("''' + col[0] + '''",'yyyy-mm-dd hh24:mi:ss.ff9'),'0000-','0001-'),'-00-','-01-'),'-00','-01'),'''
                    elif 'BLOB' in str(col[1]):
                        is_exists_blob = True
                        once_num = once_num_lob
                        cols_str = cols_str + '"' + col[0] + '",' 
                    elif 'RAW' in str(col[1]) and col[2] == 16:
                        once_num = once_num_lob
                        cols_str = cols_str + 'rawtohex("' + col[0] + '"),' 
                    elif 'NUMBER' in str(col[1]) or 'INT' in str(col[1]):
                        cols_str = cols_str + 'to_char("' + col[0] + '"),' 
                    else:
                        cols_str = cols_str + '"' + col[0] + '",' 
                    idx = idx + 1
                cols_str = cols_str[:-1]
                
            elif dst_db_type == 'oracle':
                cols_str_lob = ''
                cols_str_nomal = ''
                for col in cols_for_copy:
                    if 'LOB' in str(col[1]) or 'LONG' in str(col[1]):
                        cols_str_lob = cols_str_lob + '"' + col[0].strip() + '",'
                        once_num = once_num_lob
                    else:
                        cols_str_nomal = cols_str_nomal + '"' + col[0].strip() + '",'
                cols_str_nomal = cols_str_nomal.rstrip(',')
                cols_str_lob = cols_str_lob.rstrip(',')
                cols_str = cols_str_nomal + ',' + cols_str_lob
                cols_str = cols_str.strip(',')
                cols_str = Tools.merge_spaces(cols_str).replace(' ', '')
                
            # 组装抽数sql
            if page is None:
                select_sql = 'select /*+full(t)*/ ' + cols_str + '  from ' + mess + ' as of scn ' + table_scn + ' t where ' + src_where
            else:
                select_sql = '''
                    select ''' + cols_str + ''' from (
                        select /*+full(t)*/ t.*,rownum rn 
                        from ''' + mess + ''' 
                        as of scn ''' + str(table_scn) + ''' t
                        where rownum <= ''' + str(page) + ''' * ''' + str(page_rn) + '''
                        and ''' + src_where + '''
                    ) where rn <= ''' + str(page) + ''' * ''' + str(page_rn) + '''
                    and rn > ''' + str(page - 1) + ''' * ''' + str(page_rn) + '''
                '''
            # 获取抽数用的结果集
            rs = src_db.run(select_sql)
            return src_db, dst_db, once_num, rs, is_exists_blob, cols_for_copy
        except Exception as _:
            log.error('到' + src_db_type + '获取数据失败，准备阶段出错', my_mess, str_exception(_))
    
    try:
        tp = ThreadPool(1)
        tid = tp.run(ready)
        src_db, dst_db, once_num, rs, is_exists_blob, cols_for_copy = tp.get_result(tid, timeout=300)
    except TimeoutError as _:
        if retry_time < 20:
            retry_time = retry_time + 1
            select_sql = Tools.remove_leading_space(select_sql).replace('\n', ' ') + '-->' + table_map[2] + '.' + table_map[3]
            task = (table_map, mess, table_scn, col_desc, table_metadata, page, page_rn, retry_time)
            # log.error('到' + src_db_type + '获取数据失败', mess, '获取' + src_db_type + '连接超时60s，请使用后面SQL，使用copy_from_sql补数', select_sql, str_exception(_))
            log.warning('到' + src_db_type + '获取数据失败', mess + '(' + str(page) + ')', '获取' + src_db_type + '连接超时，自动重试，当前是第' + str(retry_time) + '次重试' , str_exception(_))
            tp.close()
            return task
        else:
            log.error('到' + src_db_type + '获取数据失败', mess + '(' + str(page) + ')', '获取' + src_db_type + '连接超时，不再重试', select_sql, str_exception(_))
            tp.close()
            return None
    except Exception as _:
        log.error('到' + src_db_type + '获取数据失败', mess + '(' + str(page) + ')', select_sql, str_exception(_))
        tp.close()
        return None
        
    try: 
        # 抽数阶段
        i = 1
        tp = ThreadPool(save_parallel)
        while True:
            if page is None:
                my_mess = mess + '(' + str(i) + ')'
            else:
                my_mess = mess + '(' + str(page) + '-' + str(i) + ')'
            time_start = time.time()
            rows = []
            rows_size = 0
            while True:
                rss = rs.get_rows(once_num)
                if len(rss) == 0:
                    break
                else:
                    rows.extend(rss)
                    rows_size = rows_size + len(str(rows).encode('utf-8')) / 1024 / 1024
                if rows_size >= once_mb:
                    break
            select_time = time.time() - time_start
            if len(rows) == 0:
                break
            else:
                if src_db_type == 'oracle' and dst_db_type == 'pgsql':
                    tp.run(save_to_pg, (dst_db, table_map, rows, rows_size, cols_for_copy, my_mess, select_time, table_scn, is_exists_blob))
                elif src_db_type == 'oracle' and dst_db_type == 'oracle':
                    tp.run(save_to_oracle, (dst_db, table_map, rows, rows_size, cols_for_copy, my_mess, select_time, table_scn))
            i = i + 1
        tp.wait()
        return None
    except Exception as _:
        log.error('到' + src_db_type + '获取数据失败，抽数阶段出错', mess + '(' + str(page) + ')', str_exception(_))
        return None
    finally:
        src_db.close()
        dst_db.close()

        
def get_data_from_sql(table_map): 
    dst_schema = table_map[2]
    dst_table = table_map[3]
    select_sql = table_map[1]
    mess = select_sql + '-->' + dst_schema + '.' + dst_table
    try:
        # 获取连接
        src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password, poolsize=8)
        dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, poolsize=save_parallel + 5, options='-c search_path=' + dst_schema + ',public')
                
        rs = src_db.run(select_sql)
        cols = rs.get_cols_description()
        is_exists_blob = False
        
        if 'LOB' in str(cols):
            once_num = once_num_lob
        else:
            once_num = once_num_normal
        
        i = 1
        tp = ThreadPool(save_parallel)
        while True:
            time_start = time.time()
            rows = []
            rows_size = 0
            while True:
                rss = rs.get_rows(once_num)
                if len(rss) == 0:
                    break
                else:
                    rows.extend(rss)
                    rows_size = rows_size + len(str(rss).encode('utf-8')) / 1024 / 1024
                if rows_size >= once_mb:
                    break
            select_time = time.time() - time_start
            if len(rows) == 0:
                break
            if src_db_type == 'oracle' and dst_db_type == 'pgsql':
                tp.run(save_to_pg, (dst_db, table_map, rows, rows_size, cols, mess, select_time, '', is_exists_blob))
            elif src_db_type == 'oracle' and dst_db_type == 'oracle':
                tp.run(save_to_oracle, (dst_db, table_map, rows, rows_size, cols, mess, select_time, ''))
            i = i + 1
        tp.wait()
    except Exception as _:
        log.error('通过SQL获取数据失败', dst_schema + '.' + dst_table, str_exception(_))
    finally:
        src_db.close()
        dst_db.close()

        
def save_to_pg(dst_db, table_map, rows, rows_size, cols, mess, select_time, table_scn, is_exists_blob):
    dst_owner = table_map[2]
    dst_table = table_map[3]
    src_where = table_map[4]
    time_start = time.time()
    
    wenhaos = ''
    for _ in cols:
        wenhaos = wenhaos + '?,'
    wenhaos = wenhaos[0:-1]
    
    cols_str = ''
    for col in cols:
        if is_to_lower:
            cols_str = cols_str + '"' + col[0].lower() + '",'
        else:
            cols_str = cols_str + '"' + col[0] + '",'
    cols_str = cols_str[0:-1]
    
    insert_sql = 'insert into ' + dst_owner + '."' + dst_table + '"(' + cols_str + ') values(' + wenhaos + ')'
    
    if is_only_insert == 'yes' or is_exists_blob:
        try:
            num = dst_db.run(insert_sql, rows)
            if num == -1:
                raise Exception('unknown error, num = -1')
            num = str(num) + '(insert)' 
        except Exception as _:
            log.error('写入' + dst_db_type + '失败', mess, str_exception(_))
            return
    else:
        try:
            num = dst_db.pg_copy_from(dst_table, rows, cols)
            num = str(num) + '(copy)'
        except Exception as _:
            log.warning('写入' + dst_db_type + '失败，改为insert重试', mess, str_exception(_))
            try:
                num = dst_db.run(insert_sql, rows)
                if num == -1:
                    raise Exception('unknown error, num = -1')
                num = str(num) + '(insert)' 
            except Exception as _:
                log.error('写入' + dst_db_type + '失败', mess, str_exception(_))
                return

    save_time = time.time() - time_start
    if src_where == '1=1':
        src_where = ''
    try:
        read_speed = str(round(rows_size / select_time, 2))
    except:
        read_speed = '∞'
    try:
        write_speed = str(round(rows_size / save_time, 2))
    except:
        write_speed = '∞'
    log.info('写入' + dst_db_type + '成功', mess, src_where, num, '大小=' + str(round(rows_size, 2)) + 'MB', '读速=' + read_speed + 'MB/s', '写速=' + write_speed + 'MB/s', 'scn=' + table_scn)


def save_to_oracle(dst_db, table_map, rows, rows_size, cols, mess, select_time, table_scn):
    dst_owner = table_map[2]
    dst_table = table_map[3]
    src_where = table_map[4]
    time_start = time.time()
    
    wenhaos = ''
    for _ in cols:
        wenhaos = wenhaos + '?,'
    wenhaos = wenhaos[0:-1]
    
    cols_str_lob = ''
    cols_str_nomal = ''
    for col in cols:
        if 'LOB' in str(col[1]) or 'LONG' in str(col[1]):
            cols_str_lob = cols_str_lob + '"' + col[0].strip() + '",'
        else:
            cols_str_nomal = cols_str_nomal + '"' + col[0].strip() + '",'
    cols_str_nomal = cols_str_nomal.rstrip(',')
    cols_str_lob = cols_str_lob.rstrip(',')
    cols_str = cols_str_nomal + ',' + cols_str_lob
    cols_str = cols_str.strip(',')
    cols_str = Tools.merge_spaces(cols_str).replace(' ', '')
    
    insert_sql = 'insert into ' + dst_owner + '."' + dst_table + '"(' + cols_str + ') values(' + wenhaos + ')'
    
    try:
        num = dst_db.run(insert_sql, rows)
        if num == -1:
            raise Exception('unknown error, num = -1')
        num = str(num) + '(insert)' 
    except Exception as _:
        log.error('写入' + dst_db_type + '失败', mess, str_exception(_))
        return
    
    save_time = time.time() - time_start
    if src_where == '1=1':
        src_where = ''
    try:
        read_speed = str(round(rows_size / select_time, 2))
    except:
        read_speed = '∞'
    try:
        write_speed = str(round(rows_size / save_time, 2))
    except:
        write_speed = '∞'
    log.info('写入' + dst_db_type + '成功', mess, src_where, num, '大小=' + str(round(rows_size, 2)) + 'MB', '读速=' + read_speed + 'MB/s', '写速=' + write_speed + 'MB/s', 'scn=' + table_scn)


def copy_from_sql_o2p():
    dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, poolsize=parallel_num + 5)
        
    table_map_list = []
    for table_mess in sqls.split('[--split--]'):
        dst_schema = table_mess.split('-->')[1].split('.')[0].lower()
        dst_table = table_mess.split('-->')[1].split('.')[1].lower()
        src_sql = table_mess.split('-->')[0]
        table_map_list.append((None, src_sql, dst_schema, dst_table, None))
        
    # 清理表
    if is_clear == 'yes':
        tp = ThreadPool(parallel_num)
        for table_map in table_map_list:
            tp.run(truncate_table, (dst_db, table_map,))
        tp.wait()
        
    # 多进程启动导数
    pp = ProcessPool(parallel_num)
    for table_map in table_map_list:
        pp.run(get_data_from_sql, (table_map,))
    pp.wait()
    
    dst_db.close()

    
def copy_index_o2p():

    def copy_one_index(table_map):
        src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password, poolsize=8)
        dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, poolsize=8)
        
        src_schema = table_map[0]
        src_table = table_map[1]
        dst_schema = table_map[2]
        dst_table = table_map[3]
        dst_conn = dst_db.dbpool.connection()
        dst_cur = dst_conn.cursor()
        
        # 删除此表已存在的索引
        if is_clear == 'yes':
            select_exists_index = "select indexname from pg_indexes t where not exists(select 1 from information_schema.constraint_table_usage t2 where t2.table_catalog = ? and t2.table_schema = t.schemaname and t2.table_name = t.tablename and t2.constraint_name = t.indexname) and t.schemaname = '" + dst_schema + "' and t.tablename = '" + dst_table + "'"
            rss = dst_db.run(select_exists_index, (dst_database,)).get_rows()
            for rs in rss:
                drop_index_sql = 'drop index ' + dst_schema + '."' + rs[0] + '"'
                try:
                    dst_cur.execute(drop_index_sql)
                    dst_conn.commit()
                    log.info(dst_db_type + '执行SQL成功', drop_index_sql)
                except Exception as _:
                    log.error(dst_db_type + '执行SQL失败', drop_index_sql, str_exception(_))
                
        sqls = OracleTools.get_table_ddl_pg(src_db, src_schema, src_table, forever_number_to_numeric=forever_number_to_numeric, to_lower=is_to_lower)
        for sql in sqls:
            if sql.startswith('create table '):
                pass
            elif sql.startswith('create index ') or sql.startswith('create UNIQUE index '):
                sql = sql.replace(' ' + src_schema + '.', ' ' + dst_schema + '.')
                sql = sql.replace('."' + src_table + '"', '."' + dst_table + '"')
                try:
                    dst_cur.execute(sql)
                    dst_conn.commit()
                    log.info(dst_db_type + '执行SQL成功', sql)
                except Exception as _:
                    if 'already exists' in str(_) and is_clear == 'yes':
                        log.warning(dst_db_type + '存在重名对象，自动改名重试', sql, str_exception(_))
                        index_name = sql.split(' on ')[0].split(' ')[-1].strip('"')
                        index_name_new = 'idx_' + str(uuid4()).replace('-', '')
                        sql = sql.replace(' index "' + index_name, ' index "' + index_name_new)
                        try:
                            dst_cur.execute(sql)
                            dst_conn.commit()
                            log.info(dst_db_type + '执行SQL成功', sql)
                        except Exception as _:
                            log.error(dst_db_type + '执行SQL失败', sql, str_exception(_))
                    else:
                        log.error(dst_db_type + '执行SQL失败', sql, str_exception(_))
            elif sql.startswith('comment on '):
                pass
            elif sql.startswith('alter table ') and ' foreign key (' in sql:
                pass
            else:
                pass
        
        src_db.close()
        dst_cur.close()
        dst_conn.close()
        dst_db.close()
    
    src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password, poolsize=8)
    dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, poolsize=8)
    dst_conn = dst_db.dbpool.connection()
    dst_cur = dst_conn.cursor()
    
    table_map_list = get_table_map_list(src_db)
    
    for table_map in table_map_list:
        dst_schema = table_map[2]
        dst_cur.execute('create schema if not exists ' + dst_schema)
        dst_conn.commit()
    
    tp = ThreadPool(parallel_num)
    for table_map in table_map_list:
        tp.run(copy_one_index, (table_map,))
    tp.wait()
        
    src_db.close()
    dst_cur.close()
    dst_conn.close()
    dst_db.close()

    
def copy_index_o2o():

    def copy_one_index(table_map):
        src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password, poolsize=8)
        dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, poolsize=8)
        
        src_schema = table_map[0]
        src_table = table_map[1]
        dst_schema = table_map[2]
        dst_table = table_map[3]
        dst_conn = dst_db.dbpool.connection()
        dst_cur = dst_conn.cursor()
                        
        sqls = OracleTools.get_table_ddl(src_db, src_schema, src_table)
        for sql in sqls:
            if sql.startswith('create table '):
                pass
            elif sql.startswith('create index ') or sql.startswith('create UNIQUE index '):
                sql = sql.replace(' ' + src_schema + '.', ' ' + dst_schema + '.')
                sql = sql.replace('."' + src_table + '"', '."' + dst_table + '"')
                try:
                    dst_cur.execute(sql)
                    dst_conn.commit()
                    log.info(dst_db_type + '执行SQL成功', sql)
                except Exception as _:
                    if 'already exists' in str(_) and is_clear == 'yes':
                        log.warning(dst_db_type + '存在重名对象，自动改名重试', sql, str_exception(_))
                        index_name = sql.split(' on ')[0].split(' ')[-1].strip('"')
                        index_name_new = 'idx_' + str(uuid4()).replace('-', '')
                        sql = sql.replace(' index "' + index_name, ' index "' + index_name_new)
                        try:
                            dst_cur.execute(sql)
                            dst_conn.commit()
                            log.info(dst_db_type + '执行SQL成功', sql)
                        except Exception as _:
                            log.error(dst_db_type + '执行SQL失败', sql, str_exception(_))
                    else:
                        log.error(dst_db_type + '执行SQL失败', sql, str_exception(_))
            elif sql.startswith('comment on '):
                pass
            elif sql.startswith('alter table ') and ' foreign key (' in sql:
                pass
            else:
                pass
        
        src_db.close()
        dst_cur.close()
        dst_conn.close()
        dst_db.close()
    
    src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password, poolsize=8)
    dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, poolsize=8)
    dst_conn = dst_db.dbpool.connection()
    dst_cur = dst_conn.cursor()
    
    table_map_list = get_table_map_list(src_db)
    
    tp = ThreadPool(parallel_num)
    for table_map in table_map_list:
        tp.run(copy_one_index, (table_map,))
    tp.wait()
        
    src_db.close()
    dst_cur.close()
    dst_conn.close()
    dst_db.close()


def copy_check_o2p():

    def copy_one_check(table_map):
        src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password, poolsize=8)
        dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, poolsize=8)
        
        src_schema = table_map[0]
        src_table = table_map[1]
        dst_schema = table_map[2]
        dst_table = table_map[3]
        dst_conn = dst_db.dbpool.connection()
        dst_cur = dst_conn.cursor()
        
        # 删除此表已存在的索引
        # if is_clear == 'yes':
            # select_exists_index = "select indexname from pg_indexes t where not exists(select 1 from information_schema.constraint_table_usage t2 where t2.table_catalog = ? and t2.table_schema = t.schemaname and t2.table_name = t.tablename and t2.constraint_name = t.indexname) and t.schemaname = '" + dst_schema + "' and t.tablename = '" + dst_table + "'"
            # rss = dst_db.run(select_exists_index, (dst_database,)).get_rows()
            # for rs in rss:
                # drop_index_sql = 'drop index ' + dst_schema + '."' + rs[0] + '"'
                # try:
                    # dst_cur.execute(drop_index_sql)
                    # dst_conn.commit()
                    # log.info(dst_db_type + '执行SQL成功', drop_index_sql)
                # except Exception as _:
                    # log.error(dst_db_type + '执行SQL失败', drop_index_sql, str_exception(_))
                
        ora_check_sql = "select owner, table_name, constraint_name, search_condition from dba_constraints where constraint_type = 'C' and owner = ? and table_name = ? and status = 'ENABLED'"

        rows = src_db.run(ora_check_sql, (src_schema, src_table)).get_rows()
        for row in rows:
            if not row[3].endswith('IS NOT NULL'):
                try: 
                    sql = "alter table " + dst_schema + '."' + dst_table + '" add constraint "' + row[2].lower() + '" check (' + row[3].replace('"', '') + ')'
                    # dst_cur.execute(sql)
                    # dst_conn.commit()
                    log.info(dst_db_type + '执行SQL成功(测试中，仅输出，未执行)', sql)
                except Exception as _:
                    log.error(dst_db_type + '执行SQL失败', sql, str_exception(_))
        
        src_db.close()
        dst_cur.close()
        dst_conn.close()
        dst_db.close()
    
    src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password, poolsize=8)
    dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, poolsize=8)
    dst_conn = dst_db.dbpool.connection()
    dst_cur = dst_conn.cursor()
    
    table_map_list = get_table_map_list(src_db)
    
    for table_map in table_map_list:
        dst_schema = table_map[2]
        dst_cur.execute('create schema if not exists ' + dst_schema)
        dst_conn.commit()
    
    tp = ThreadPool(parallel_num)
    for table_map in table_map_list:
        tp.run(copy_one_check, (table_map,))
    tp.wait()
        
    src_db.close()
    dst_cur.close()
    dst_conn.close()
    dst_db.close()

    
def copy_table_o2p():

    def copy_one_table(src_db, dst_db, table_map):
        src_schema = table_map[0].strip()
        src_table = table_map[1].strip()
        dst_schema = table_map[2].strip()
        dst_table = table_map[3].strip()
        dst_conn = dst_db.dbpool.connection()
        dst_cur = dst_conn.cursor()
        # is_suc = True
    
        if is_clear == 'yes':
            drop_sql = 'drop table if exists ' + dst_schema + '."' + dst_table + '"'
            try:
                dst_cur.execute(drop_sql)
                dst_conn.commit()
                log.info(dst_db_type + '执行SQL成功', drop_sql)
            except Exception as _:
                log.error(dst_db_type + '执行SQL失败', drop_sql, str_exception(_))
        
        try:
            sqls = OracleTools.get_table_ddl_pg(src_db, src_schema, src_table, forever_number_to_numeric=forever_number_to_numeric, to_lower=is_to_lower)
        except Exception as _:
            log.error('元数据获取失败', src_schema + '.' + src_table, str_exception(_))
            return
        
        if len(sqls) == 0:
            log.error('元数据获取失败', src_schema + '.' + src_table, '表不存在')
            return
        
        for sql in sqls:
            if sql.startswith('alter table') and ' foreign key (' in sql:
                pass
            elif sql.startswith('alter table') and ' primary key (' in sql:
                pass
            elif sql.startswith('alter table') and ' unique (' in sql:
                pass
            elif sql.startswith('create index ') or sql.startswith('create UNIQUE index '):
                pass
            else:
                sql = sql.replace(' ' + src_schema + '.', ' ' + dst_schema + '.')
                sql = sql.replace('."' + src_table + '"', '."' + dst_table + '"')
                try:
                    dst_cur.execute(sql)
                    dst_conn.commit()
                    log.info(dst_db_type + '执行SQL成功', sql)
                except Exception as _:
                    if 'relation' in str(_) and 'already exists' in str(_):
                        log.warning(dst_db_type + '执行SQL失败', sql, str_exception(_))
                    # is_suc = False
                    # if sql.startswith('create table ') and 'partition of' not in sql:
                        # log.error(dst_db_type + '创建表失败', sql, str_exception(_))
                        # break
                    else:
                        log.error(dst_db_type + '执行SQL失败', sql, str_exception(_))
                    
        # if is_suc: 
            # log.info(dst_db_type + '创建表成功', src_schema + '.' + src_table + '-->' + dst_schema + '.' + dst_table)
        
        dst_cur.close()
        dst_conn.close()
            
    src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password, poolsize=parallel_num + 5)
    dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, poolsize=parallel_num + 5)
    dst_conn = dst_db.dbpool.connection()
    dst_cur = dst_conn.cursor()
    
    table_map_list = get_table_map_list(src_db)
    
    for table_map in table_map_list:
        dst_schema = table_map[2]
        dst_cur.execute('create schema if not exists ' + dst_schema)
        dst_conn.commit()

    tp = ThreadPool(parallel_num)
        
    for table_map in table_map_list:
        tp.run(copy_one_table, (src_db, dst_db, table_map))
    tp.wait()
    
    src_db.close()
    dst_cur.close()
    dst_conn.close()
    dst_db.close()


def copy_table_o2o():

    def copy_one_table(src_db, dst_db, table_map):
        src_schema = table_map[0].strip()
        src_table = table_map[1].strip()
        dst_schema = table_map[2].strip()
        dst_table = table_map[3].strip()
        dst_conn = dst_db.dbpool.connection()
        dst_cur = dst_conn.cursor()
        is_suc = True
    
        if is_clear == 'yes':
            drop_sql = 'drop table ' + dst_schema + '."' + dst_table + '"'
            try:
                dst_cur.execute(drop_sql)
                dst_conn.commit()
                log.info('' + dst_db_type + '执行SQL成功', drop_sql)
            except Exception as _:
                if 'table or view does not exist' in str(_):
                    log.info('' + dst_db_type + '执行SQL失败', drop_sql, str_exception(_))
                else:
                    log.error('' + dst_db_type + '执行SQL失败', drop_sql, str_exception(_))
            
        try:
            sqls = OracleTools.get_table_ddl(src_db, src_schema, src_table)
        except Exception as _:
            log.error('元数据获取失败', src_schema + '.' + src_table, str_exception(_))
            return
        
        if len(sqls) == 0:
            log.error('元数据获取失败', src_schema + '.' + src_table, '表不存在')
            return
        
        for sql in sqls:
            if sql.startswith('alter table') and ' foreign key (' in sql:
                pass
            elif sql.startswith('alter table') and ' primary key (' in sql:
                pass
            elif sql.startswith('alter table') and ' unique (' in sql:
                pass
            elif sql.startswith('create index ') or sql.startswith('create UNIQUE index '):
                pass
            else:
                sql = sql.replace(' ' + src_schema + '.', ' ' + dst_schema + '.')
                sql = sql.replace('."' + src_table + '"', '."' + dst_table + '"')
                try:
                    dst_cur.execute(sql)
                    dst_conn.commit()
                except Exception as _:
                    is_suc = False
                    if sql.startswith('create table '):
                        log.error('' + dst_db_type + '创建表失败', sql, str_exception(_))
                        break
                    log.error('' + dst_db_type + '执行SQL失败', sql, str_exception(_))
                    
        if is_suc: 
            log.info(dst_db_type + '创建表成功', src_schema + '.' + src_table + '-->' + dst_schema + '.' + dst_table)
        
        dst_cur.close()
        dst_conn.close()
            
    src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password, poolsize=parallel_num + 5)
    dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, poolsize=parallel_num + 5)
    dst_conn = dst_db.dbpool.connection()
    dst_cur = dst_conn.cursor()
    
    table_map_list = get_table_map_list(src_db)
    
    tp = ThreadPool(parallel_num)
        
    for table_map in table_map_list:
        tp.run(copy_one_table, (src_db, dst_db, table_map))
    tp.wait()
    
    src_db.close()
    dst_cur.close()
    dst_conn.close()
    dst_db.close()


def copy_constraint_o2p(run_mode):
    
    def clear_k(table_map, run_mode):
        dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, poolsize=8)
        dst_conn = dst_db.dbpool.connection()
        dst_cur = dst_conn.cursor()
        
        dst_schema = table_map[2]
        dst_table = table_map[3]
        
        sql = '''
            select con.conname
            from pg_catalog.pg_constraint con
            inner join pg_catalog.pg_class rel on rel.oid = con.conrelid
            inner join pg_catalog.pg_namespace nsp on nsp.oid = connamespace
            where nsp.nspname = ?
            and rel.relname = ?
            and contype = ?
        '''
        
        if run_mode == 'copy_pk':
            rss = dst_db.run(sql, (dst_schema, dst_table, 'p')).get_rows()
        if run_mode == 'copy_uk':
            rss = dst_db.run(sql, (dst_schema, dst_table, 'u')).get_rows()
        if run_mode == 'copy_fk' or run_mode == 'drop_fk':
            rss = dst_db.run(sql, (dst_schema, dst_table, 'f')).get_rows()
        
        for rs in rss:
            try:
                drop_sql = 'alter table ' + dst_schema + '."' + dst_table + '" drop constraint "' + rs[0] + '"'
                dst_cur.execute(drop_sql)
                dst_conn.commit()
                log.info(dst_db_type + '执行SQL成功', drop_sql)
            except Exception as _:
                log.error(dst_db_type + '执行SQL失败', drop_sql, str_exception(_))
        
        dst_cur.close()
        dst_conn.close()
        dst_db.close()

    def copy_k(table_map, run_mode):
        src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password, poolsize=8)
        dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, poolsize=8)
    
        src_schema = table_map[0]
        src_table = table_map[1]
        dst_schema = table_map[2]
        dst_table = table_map[3]
        dst_conn = dst_db.dbpool.connection()
        dst_cur = dst_conn.cursor()
        sqls = OracleTools.get_table_ddl_pg(src_db, src_schema, src_table, forever_number_to_numeric=forever_number_to_numeric, to_lower=is_to_lower)
        for sql in sqls:
            if sql.startswith('create table '):
                pass
            elif sql.startswith('create index ') or sql.startswith('create UNIQUE index '):
                pass
            elif sql.startswith('comment on '):
                pass
            elif sql.startswith('alter table ') and ' add constraint ' in sql and ' foreign key (' in sql and run_mode == 'copy_fk':
                sql = sql.replace(' ' + src_schema + '.', ' ' + dst_schema + '.')
                sql = sql.replace(' ' + src_schema.lower() + '.', ' ' + dst_schema + '.')
                sql = sql.replace('."' + src_table + '"', '."' + dst_table + '"')
                try:
                    dst_cur.execute(sql)
                    dst_conn.commit()
                    log.info(dst_db_type + '执行SQL成功', sql)
                except Exception as _:
                    if 'already exists' in str(_) and is_clear == 'yes':
                        log.warning(dst_db_type + '存在重名对象，自动改名重试', sql, str_exception(_))
                        k_name = sql.split(' add constraint ')[1].split(' ')[0]
                        k_name_new = 'fk_' + str(uuid4()).replace('-', '')
                        sql = sql.replace(' constraint ' + k_name, ' constraint ' + k_name_new)
                        try:
                            dst_cur.execute(sql)
                            dst_conn.commit()
                            log.info(dst_db_type + '执行SQL成功', sql)
                        except Exception as _:
                            log.error(dst_db_type + '执行SQL失败', sql, str_exception(_))
                    else:
                        log.error(dst_db_type + '执行SQL失败', sql, str_exception(_))
            elif sql.startswith('alter table ') and ' add constraint ' in sql and ' unique (' in sql and run_mode == 'copy_uk':
                sql = sql.replace(' ' + src_schema + '.', ' ' + dst_schema + '.')
                sql = sql.replace('."' + src_table + '"', '."' + dst_table + '"')
                try:
                    dst_cur.execute(sql)
                    dst_conn.commit()
                    log.info(dst_db_type + '执行SQL成功', sql)
                except Exception as _:
                    if 'already exists' in str(_) and is_clear == 'yes':
                        log.warning(dst_db_type + '存在重名对象，自动改名重试', sql, str_exception(_))
                        k_name = sql.split(' add constraint ')[1].split(' ')[0]
                        k_name_new = 'uk_' + str(uuid4()).replace('-', '')
                        sql = sql.replace(' constraint ' + k_name, ' constraint ' + k_name_new)
                        try:
                            dst_cur.execute(sql)
                            dst_conn.commit()
                            log.info(dst_db_type + '执行SQL成功', sql)
                        except Exception as _:
                            log.error(dst_db_type + '执行SQL失败', sql, str_exception(_))
                    else:
                        log.error(dst_db_type + '执行SQL失败', sql, str_exception(_))
            elif sql.startswith('alter table ') and ' add constraint ' in sql and ' primary key (' in sql and run_mode == 'copy_pk':
                sql = sql.replace(' ' + src_schema + '.', ' ' + dst_schema + '.')
                sql = sql.replace('."' + src_table + '"', '."' + dst_table + '"')
                try:
                    dst_cur.execute(sql)
                    dst_conn.commit()
                    log.info(dst_db_type + '执行SQL成功', sql)
                except Exception as _:
                    if 'already exists' in str(_) and is_clear == 'yes':
                        log.warning(dst_db_type + '存在重名对象，自动改名重试', sql, str_exception(_))
                        k_name = sql.split(' add constraint ')[1].split(' ')[0]
                        k_name_new = 'pk_' + str(uuid4()).replace('-', '')
                        sql = sql.replace(' constraint ' + k_name, ' constraint ' + k_name_new)
                        try:
                            dst_cur.execute(sql)
                            dst_conn.commit()
                            log.info(dst_db_type + '执行SQL成功', sql)
                        except Exception as _:
                            log.error(dst_db_type + '执行SQL失败', sql, str_exception(_))
                    else:
                        log.error(dst_db_type + '执行SQL失败', sql, str_exception(_))
                    
        src_db.close()
        dst_cur.close()
        dst_conn.close()
        dst_db.close()
    
    src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password, poolsize=8)
    dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, poolsize=8)
    dst_conn = dst_db.dbpool.connection()
    dst_cur = dst_conn.cursor()
    
    table_map_list = get_table_map_list(src_db)
    
    for table_map in table_map_list:
        dst_schema = table_map[2]
        dst_cur.execute('create schema if not exists ' + dst_schema)
        dst_conn.commit()
    
    tp = ThreadPool(parallel_num)
    
    if is_clear == 'yes' or run_mode == 'drop_fk':
        for table_map in table_map_list:
            tp.run(clear_k, (table_map, run_mode))
        tp.wait()
    
    if run_mode != 'drop_fk':
        for table_map in table_map_list:
            tp.run(copy_k, (table_map, run_mode))
        tp.wait()
        
    src_db.close()
    dst_cur.close()
    dst_conn.close()
    dst_db.close()


def copy_constraint_o2o(run_mode):

    def copy_k(table_map, run_mode):
        src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password, poolsize=8)
        dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, poolsize=8)
    
        src_schema = table_map[0]
        src_table = table_map[1]
        dst_schema = table_map[2]
        dst_table = table_map[3]
        dst_conn = dst_db.dbpool.connection()
        dst_cur = dst_conn.cursor()
        sqls = OracleTools.get_table_ddl(src_db, src_schema, src_table)
        for sql in sqls:
            if sql.startswith('create table '):
                pass
            elif sql.startswith('create index ') or sql.startswith('create UNIQUE index '):
                pass
            elif sql.startswith('comment on '):
                pass
            elif sql.startswith('alter table ') and ' add constraint ' in sql and ' foreign key (' in sql and run_mode == 'copy_fk':
                sql = sql.replace(' ' + src_schema + '.', ' ' + dst_schema + '.')
                sql = sql.replace('."' + src_table + '"', '."' + dst_table + '"')
                try:
                    dst_cur.execute(sql)
                    dst_conn.commit()
                    log.info(dst_db_type + '执行SQL成功', sql)
                except Exception as _:
                    if 'already exists' in str(_) and is_clear == 'yes':
                        log.warning(dst_db_type + '存在重名对象，自动改名重试', sql, str_exception(_))
                        k_name = sql.split(' add constraint ')[1].split(' ')[0]
                        k_name_new = 'fk_' + str(uuid4()).replace('-', '')
                        sql = sql.replace(' constraint ' + k_name, ' constraint ' + k_name_new)
                        try:
                            dst_cur.execute(sql)
                            dst_conn.commit()
                            log.info(dst_db_type + '执行SQL成功', sql)
                        except Exception as _:
                            log.error(dst_db_type + '执行SQL失败', sql, str_exception(_))
                    else:
                        log.error(dst_db_type + '执行SQL失败', sql, str_exception(_))
            elif sql.startswith('alter table ') and ' add constraint ' in sql and ' unique (' in sql and run_mode == 'copy_uk':
                sql = sql.replace(' ' + src_schema + '.', ' ' + dst_schema + '.')
                sql = sql.replace('."' + src_table + '"', '."' + dst_table + '"')
                try:
                    dst_cur.execute(sql)
                    dst_conn.commit()
                    log.info(dst_db_type + '执行SQL成功', sql)
                except Exception as _:
                    if 'already exists' in str(_) and is_clear == 'yes':
                        log.warning(dst_db_type + '存在重名对象，自动改名重试', sql, str_exception(_))
                        k_name = sql.split(' add constraint ')[1].split(' ')[0]
                        k_name_new = 'uk_' + str(uuid4()).replace('-', '')
                        sql = sql.replace(' constraint ' + k_name, ' constraint ' + k_name_new)
                        try:
                            dst_cur.execute(sql)
                            dst_conn.commit()
                            log.info(dst_db_type + '执行SQL成功', sql)
                        except Exception as _:
                            log.error(dst_db_type + '执行SQL失败', sql, str_exception(_))
                    else:
                        log.error(dst_db_type + '执行SQL失败', sql, str_exception(_))
            elif sql.startswith('alter table ') and ' add constraint ' in sql and ' primary key (' in sql and run_mode == 'copy_pk':
                sql = sql.replace(' ' + src_schema + '.', ' ' + dst_schema + '.')
                sql = sql.replace('."' + src_table + '"', '."' + dst_table + '"')
                try:
                    dst_cur.execute(sql)
                    dst_conn.commit()
                    log.info(dst_db_type + '执行SQL成功', sql)
                except Exception as _:
                    if 'already exists' in str(_) and is_clear == 'yes':
                        log.warning(dst_db_type + '存在重名对象，自动改名重试', sql, str_exception(_))
                        k_name = sql.split(' add constraint ')[1].split(' ')[0]
                        k_name_new = 'pk_' + str(uuid4()).replace('-', '')
                        sql = sql.replace(' constraint ' + k_name, ' constraint ' + k_name_new)
                        try:
                            dst_cur.execute(sql)
                            dst_conn.commit()
                            log.info(dst_db_type + '执行SQL成功', sql)
                        except Exception as _:
                            log.error(dst_db_type + '执行SQL失败', sql, str_exception(_))
                    else:
                        log.error(dst_db_type + '执行SQL失败', sql, str_exception(_))
                    
        src_db.close()
        dst_cur.close()
        dst_conn.close()
        dst_db.close()
    
    src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password, poolsize=8)
    dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, poolsize=8)
    dst_conn = dst_db.dbpool.connection()
    dst_cur = dst_conn.cursor()
    
    table_map_list = get_table_map_list(src_db)
    
    tp = ThreadPool(parallel_num)

    for table_map in table_map_list:
        tp.run(copy_k, (table_map, run_mode))
    tp.wait()
    
    src_db.close()
    dst_cur.close()
    dst_conn.close()
    dst_db.close()

    
def copy_sequence_o2p():
    src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password, poolsize=8)
    dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, poolsize=8)
    dst_conn = dst_db.dbpool.connection()
    dst_cur = dst_conn.cursor()
    table_map_list = get_table_map_list(src_db)
    sql = 'select * from dba_sequences where sequence_owner = ?'
    
    schemas = []
    for table_map in table_map_list:
        if (table_map[0], table_map[2]) not in schemas:
            schemas.append((table_map[0], table_map[2]))
            
    for schema in schemas:
        src_schema = schema[0]
        dst_schema = schema[1]        
        rows = src_db.run(sql, (src_schema,)).get_rows()
        for row in rows:
            # sequence_owner = row[0]
            sequence_name = row[1]
            min_value = row[2]
            max_value = row[3]
            increment_by = row[4]
            cycle_flag = row[5]
            # order_flag = row[6]
            cache_size = row[7]
            last_number = row[8]
            if max_value > 9223372036854775807:
                max_str = 'no maxvalue'
            else:
                max_str = 'maxvalue ' + str(max_value)
            if cache_size == 0:
                cache_str = ''
            else:
                cache_str = 'cache ' + str(cache_size)
            if cycle_flag == 'N':
                cycle_str = ''
            else:
                cycle_str = 'cycle'
            drop_sql = 'drop sequence if exists ' + dst_schema + '.' + sequence_name.lower()
            try:
                dst_cur.execute(drop_sql)
                dst_conn.commit()
                log.info(dst_db_type + '执行SQL成功', drop_sql)
            except Exception as _:
                log.warning(drop_sql, str_exception(_))
            create_sql = 'create sequence ' + dst_schema + '.' + sequence_name.lower() + ' increment ' + str(increment_by) + ' minvalue ' + str(min_value) + ' ' + max_str + ' start ' + str(last_number) + ' ' + cache_str + ' ' + cycle_str 
            create_sql = Tools.merge_spaces(create_sql).strip()
            try:
                dst_cur.execute(create_sql)
                dst_conn.commit()
                log.info(dst_db_type + '执行SQL成功', create_sql)
            except Exception as _:
                log.error(dst_db_type + '执行SQL失败', create_sql, str_exception(_))
            
    src_db.close()
    dst_cur.close()
    dst_conn.close()
    dst_db.close()

    
def copy_sequence_o2o():
    src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password, poolsize=8)
    dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, poolsize=8)
    dst_conn = dst_db.dbpool.connection()
    dst_cur = dst_conn.cursor()
    table_map_list = get_table_map_list(src_db)
    sql = 'select * from dba_sequences where sequence_owner = ?'
    
    schemas = []
    for table_map in table_map_list:
        if (table_map[0], table_map[2]) not in schemas:
            schemas.append((table_map[0], table_map[2]))
            
    for schema in schemas:
        src_schema = schema[0]
        dst_schema = schema[1]        
        rows = src_db.run(sql, (src_schema,)).get_rows()
        for row in rows:
            # sequence_owner = row[0]
            sequence_name = row[1]
            min_value = row[2]
            max_value = row[3]
            increment_by = row[4]
            cycle_flag = row[5]
            order_flag = row[6]
            cache_size = row[7]
            last_number = row[8] + 100
                
            if cache_size == 0:
                cache_str = ''
            else:
                cache_str = 'cache ' + str(cache_size)
                
            if cycle_flag == 'N':
                cycle_str = 'nocycle'
            else:
                cycle_str = 'cycle'
                
            if order_flag == 'N':
                order_str = 'noorder'
            else:
                order_str = 'order'
                
            drop_sql = 'drop sequence ' + dst_schema + '."' + sequence_name + '"'
            try:
                dst_cur.execute(drop_sql)
                dst_conn.commit()
                log.info(dst_db_type + '执行SQL成功', drop_sql)
            except Exception as _:
                log.warning(drop_sql, str_exception(_))
            create_sql = 'create sequence ' + dst_schema + '."' + sequence_name + '" minvalue ' + str(min_value) + ' maxvalue ' + str(max_value) + ' increment by ' + str(increment_by) + ' start with ' + str(last_number) + ' ' + cache_str + ' ' + order_str + ' ' + cycle_str
            create_sql = Tools.merge_spaces(create_sql).strip()
            try:
                dst_cur.execute(create_sql)
                dst_conn.commit()
                log.info(dst_db_type + '执行SQL成功', create_sql)
            except Exception as _:
                log.error(dst_db_type + '执行SQL失败', create_sql, str_exception(_))
            
    src_db.close()
    dst_cur.close()
    dst_conn.close()
    dst_db.close()


def compare_data_number():
    tp = ThreadPool(parallel_num)

    def count(table_map, src_db, dst_db, global_scn):
        try:
            src_schema = table_map[0]
            src_table = table_map[1]
            dst_schema = table_map[2]
            dst_table = table_map[3]
            src_where = table_map[4]
            
            report_table_id = src_schema + '.' + src_table + '-->' + dst_schema + '.' + dst_table
            if report_table_id in tables_data_num:
                table_scn = tables_data_num[report_table_id][0]
            else:
                table_scn = global_scn
            table_scn = str(table_scn)
            
            if src_db_type == 'oracle' and is_count_full == 'yes':
                src_sql = 'select /*+full(t) parallel(1)*/ count(1) from ' + src_schema + '."' + src_table + '" as of scn ' + table_scn + ' t where ' + src_where
            elif src_db_type == 'oracle' and is_count_full != 'yes':
                src_sql = 'select /*+parallel(1)*/ count(1) from ' + src_schema + '."' + src_table + '" as of scn ' + table_scn + ' t where ' + src_where
            elif src_db_type == 'pgsql':
                src_sql = 'select count(1) from ' + src_schema + '."' + src_table + '" t where ' + src_where
            
            dst_sql = 'select count(1) from ' + dst_schema + '."' + dst_table + '"'
                
            e1 = ''
            e2 = ''
            try:
                src_num = None
                if report_table_id in tables_data_num:
                    src_num = tables_data_num[report_table_id][1]
                if src_num is None:
                    src_num = int(src_db.run(src_sql).get_rows()[0][0])
            except Exception as _:
                src_num = -1
                e1 = str(_)
            try:
                dst_num = int(dst_db.run(dst_sql).get_rows()[0][0])
            except Exception as _:
                dst_num = -2
                e2 = str(_)
                        
            tables_data_num[report_table_id] = [table_scn, src_num, dst_num]
            rs = 'Yes' if (tables_data_num[report_table_id][1] == tables_data_num[report_table_id][2]) else 'No'
            if tables_data_num[report_table_id][1] == 0 and tables_data_num[report_table_id][1] > 0:
                rs2 = '0.0'
            elif tables_data_num[report_table_id][1] == 0 and tables_data_num[report_table_id][1] == 0:
                rs2 = '100.0'
            elif tables_data_num[report_table_id][1] == -1:
                rs2 = '0.0'
            else:
                rs2 = str(round(tables_data_num[report_table_id][2] / tables_data_num[report_table_id][1] * 100, 2))
            log.info('表数据量是否一致：' + rs, rs2 + '%', report_table_id, 'src=' + str(tables_data_num[report_table_id][1]), 'dst=' + str(tables_data_num[report_table_id][2]), 'scn=' + table_scn, str(e1), str(e2))
        except Exception as _:
            log.error('对数失败', report_table_id, str_exception(_))

    try:
        src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password, poolsize=parallel_num + 5)
        dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, poolsize=parallel_num + 5)
    except Exception as _:
        log.error('连接数据库失败', str_exception(_))
        
    # 如果没有scn，则此处获取
    if len(input_global_scn) == 0:
        if src_db_type == 'oracle' and dst_db_type == 'pgsql':
            global_scn = src_db.run('select to_char(current_scn) from v$database').get_rows()[0][0]
        elif src_db_type == 'pgsql' and dst_db_type == 'oracle':
            global_scn = dst_db.run('select to_char(current_scn) from v$database').get_rows()[0][0]
        elif src_db_type == 'pgsql' and dst_db_type == 'pgsql':
            global_scn = None
        elif src_db_type == 'oracle' and dst_db_type == 'oracle':
            global_scn = src_db.run('select to_char(current_scn) from v$database').get_rows()[0][0]
    else:
        global_scn = input_global_scn
    
    # 解析出需要迁移的表以及映射关系
    table_map_list = get_table_map_list(src_db)
    
    error_table = ''
    for table_map in table_map_list:
        tp.run(count, (table_map, src_db, dst_db, global_scn))
    tp.wait()
        
    for k in tables_data_num:
        if tables_data_num[k][1] != tables_data_num[k][2]:
            if tables_data_num[k][1] == -1:
                error_table = error_table + k + '[--split--]'
            elif tables_data_num[k][1] != 0:
                rs2 = tables_data_num[k][2] / tables_data_num[k][1] * 100
                if rs2 < compare_data_number_maximum_percentage_difference:
                    error_table = error_table + k + '[--split--]'
            elif tables_data_num[k][1] == 0:
                if tables_data_num[k][2] != 0:
                    error_table = error_table + k + '[--split--]'
                
    error_table = error_table[:-11]
            
    log.info('数据量不一致的表：' + error_table)
    
    if scn_time != 0 and is_only_scn == 'yes' and run_mode == 'copy_data':
        log.info('数据版本时间：' + str(scn_time))
        
    src_db.close()
    dst_db.close()

        
def compare_index_o2p():

    def compare_index_one(src_db, dst_db, table_map):
        src_schema = table_map[0]
        src_table = table_map[1]
        dst_schema = table_map[2]
        dst_table = table_map[3]
        
        e1 = ''
        e2 = ''
        src_sql = "select count(distinct t.index_name) from dba_indexes t where not exists(select 1 from dba_constraints t2 where t2.owner = t.table_owner and t2.table_name = t.table_name and t2.constraint_name = t.index_name) and t.index_type not in('LOB') and t.table_owner = '" + src_schema + "' and t.table_name = '" + src_table + "'"
        dst_sql = "select count(distinct t.indexname) from pg_indexes t where not exists(select 1 from information_schema.constraint_table_usage t2 where t2.table_catalog = ? and t2.table_schema = t.schemaname and t2.table_name = t.tablename and t2.constraint_name = t.indexname) and t.schemaname = '" + dst_schema + "' and t.tablename = '" + dst_table + "'"
        try:
            src_num = src_db.run(src_sql).get_rows()[0][0]
        except Exception as _: 
            src_num = -1
            e1 = str(_)
        try:
            dst_num = dst_db.run(dst_sql, (dst_database,)).get_rows()[0][0]
        except Exception as _:
            dst_num = -2
            e2 = str(_)
        rs = 'Yes' if (src_num == dst_num) else 'No'
        log.info('表索引数量是否一致：' + rs, src_schema + '.' + src_table, 'src=' + str(src_num), 'dst=' + str(dst_num), str(e1), str(e2))
    
    try:
        src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password, poolsize=parallel_num + 5)
        dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, poolsize=parallel_num + 5)
    except Exception as _:
        log.error('比较索引数量时，' + src_db_type + '连接失败', str_exception(_))
    
    # 解析出需要迁移的表以及映射关系
    table_map_list = get_table_map_list(src_db)
    
    tp = ThreadPool(parallel_num)
    for table_map in table_map_list:
        tp.run(compare_index_one, (src_db, dst_db, table_map))
    tp.wait()

    src_db.close()
    dst_db.close()

    
def compare_constraint_o2p():

    def compare_constraint_one(src_db, table_map):
        src_schema = table_map[0]
        src_table = table_map[1]
        dst_schema = table_map[2]
        dst_table = table_map[3]
        dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, options='-c search_path=' + dst_schema + ',public', poolsize=8)
        e1 = ''
        e2 = ''
        src_sql = "select count(distinct constraint_name) from dba_constraints where constraint_type in('P','U','R') and owner = ? and table_name = ?"
        dst_sql = "select count(distinct constraint_name) from information_schema.table_constraints where constraint_type != 'CHECK' and table_catalog = '" + dst_database + "' and table_schema = '" + dst_schema + "' and table_name = '" + dst_table + "'"
        try:
            src_num = src_db.run(src_sql, (src_schema, src_table)).get_rows()[0][0]
        except Exception as _: 
            src_num = -1
            e1 = str(_)
        try:
            dst_num = dst_db.run(dst_sql).get_rows()[0][0]
        except Exception as _:
            dst_num = -2
            e2 = str(_)
        rs = 'Yes' if (src_num == dst_num) else 'No'
        log.info('表键数量是否一致：' + rs, src_schema + '.' + src_table, 'src=' + str(src_num), 'dst=' + str(dst_num), str(e1), str(e2))
        dst_db.close()
    
    try:
        src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password, poolsize=parallel_num + 5)
    except Exception as _:
        log.error('比较键数量时，' + src_db_type + '连接失败', str_exception(_))
    
    # 解析出需要迁移的表以及映射关系
    table_map_list = get_table_map_list(src_db)
    
    tp = ThreadPool(parallel_num)
    for table_map in table_map_list:
        tp.run(compare_constraint_one, (src_db, table_map,))
    tp.wait()

    src_db.close()


def get_table_oracle_ddl():
    src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password, poolsize=8)
    table_map_list = get_table_map_list(src_db)
    for table_map in table_map_list:
        src_schema = table_map[0]
        src_table = table_map[1]
        sqls = OracleTools.get_table_ddl(src_db, src_schema, src_table)
        for sql in sqls:
            log.out(sql + ';')
        log.out()

        
def get_table_pg_ddl():
    src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password, poolsize=8)
    table_map_list = get_table_map_list(src_db)
    for table_map in table_map_list:
        src_schema = table_map[0]
        src_table = table_map[1]
        sqls = OracleTools.get_table_ddl_pg(src_db, src_schema, src_table, to_lower=is_to_lower)
        for sql in sqls:
            log.out(sql + ';')
        log.out()


def copy_data_p2x():
    # 获取连接
    src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password, poolsize=8)
    table_map_list = get_table_map_list(src_db)
    
    pp = ProcessPool(parallel_num)
    for table_map in table_map_list:
        pp.run(copy_data_p2x_one, (table_map,), name=table_map[0] + '.' + table_map[1], error_callback=print_error)
    
    while True:
        if pp.get_running_num() > 0:
            if len(set(pp.get_running_name())) > 0 and len(set(pp.get_running_name())) <= parallel_num:
                log.info('导数任务，正在执行的任务：' + str(len(set(pp.get_running_name()))) + '个' + '，' + str(set(pp.get_running_name())))
            else:
                log.info('导数任务，正在执行的任务：' + str(len(set(pp.get_running_name()))) + '个')
            time.sleep(5)
        else:
            break
    pp.wait()
    log.info('导数任务全部执行完成。')

    src_db.close()
    
    # 获取输出报告
    if is_auto_count == 'yes':
        compare_data_number()


def copy_data_p2x_one(table_map):
    src_db = DBConn(src_db_type, src_ip, src_port, src_database, src_read_username, src_read_password, poolsize=8)
    dst_db = DBConn(dst_db_type, dst_ip, dst_port, dst_database, dst_username, dst_password, poolsize=8)
    src_schema = table_map[0]
    src_table = table_map[1]
    dst_schema = table_map[2]
    dst_table = table_map[3]
    src_where = table_map[4]
    try:
        if is_clear == 'yes':
            truncate_table_sql = 'truncate table ' + dst_schema + '."' + dst_table + '"'
            dst_db.run(truncate_table_sql)
            log.info(dst_db_type + '执行SQL成功', truncate_table_sql)
                    
        qrs = dst_db.run('select * from ' + dst_schema + '."' + dst_table + '" where 1=2')
        col_desc = qrs.get_cols_description()
        wenhaos = ''
        cols_str_nomal = ''
        cols_str_lob = ''
        once_num = once_num_normal
        for col in col_desc:
            if 'LOB' in str(col[1]) or 'LONG' in str(col[1]):
                cols_str_lob = cols_str_lob + col[0].strip() + ','
                once_num = once_num_lob
            else:
                cols_str_nomal = cols_str_nomal + col[0].strip() + ','
            wenhaos = wenhaos + '?,'
        wenhaos = wenhaos[0:-1]
        cols_str_nomal = cols_str_nomal.rstrip(',')
        cols_str_lob = cols_str_lob.rstrip(',')
        cols_str = cols_str_nomal + ',' + cols_str_lob
        cols_str = cols_str.strip(',')
        cols_str = Tools.merge_spaces(cols_str).replace(' ', '')
        
        if src_db_type == 'pgsql':
            select_sql = 'select "' + cols_str.lower().replace(',', '","') + '" from ' + src_schema + '."' + src_table + '" where ' + src_where
        elif src_db_type == 'oracle':
            select_sql = 'select "' + cols_str.replace(',', '","') + '" from ' + src_schema + '."' + src_table + '" where ' + src_where
        insert_sql = 'insert into ' + dst_schema + '."' + dst_table + '"("' + cols_str.replace(',', '","') + '") values(' + wenhaos + ')'
        
        qrs.close()
        
        if src_where == '1=1':
            src_where = ''

        rs = src_db.run(select_sql)
        i = 1
        while True:
            mess = src_schema + '.' + src_table + '-->' + dst_schema + '.' + dst_table + '(' + str(i) + ')'
            time_start = time.time()
            rows_size = 0
            rows = []
            while True:
                rss = rs.get_rows(once_num)
                if len(rss) == 0:
                    break
                else:
                    rss_new = []
                    for row in rss:
                        row_new = []
                        for cell in row:
                            if type(cell) == memoryview:
                                cell = cell.tobytes()
                            row_new.append(cell)
                        rss_new.append(row_new)
                    rows_size = rows_size + len(str(rss_new).encode('utf-8')) / 1024 / 1024 
                    rows.extend(rss_new)
                if rows_size >= once_mb:
                    break
            select_time = time.time() - time_start
            try:
                read_speed = str(round(rows_size / select_time, 2))
            except:
                read_speed = '∞'
                
            if len(rows) == 0:
                break
            else:
                time_start = time.time()
                num = dst_db.run(insert_sql, rows)
                save_time = time.time() - time_start
                try:
                    write_speed = str(round(rows_size / save_time, 2))
                except:
                    write_speed = '∞'
                log.info('写入' + dst_db_type + '成功', mess, src_where, num, '大小=' + str(round(rows_size, 2)) + 'MB', '读速=' + read_speed + 'MB/s', '写速=' + write_speed + 'MB/s')

            if len(rows) > 0 and len(rows) < once_num_lob:
                break
            
            i = i + 1
    except Exception as _:
        log.error(src_db_type + '到' + dst_db_type + '的导数失败', src_schema + '.' + src_table + '-->' + dst_schema + '.' + dst_table, str_exception(_))
    finally:
        src_db.close()
        dst_db.close()

    
if __name__ == '__main__': 
    main()
