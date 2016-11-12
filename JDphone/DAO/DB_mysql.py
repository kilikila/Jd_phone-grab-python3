import pymysql.cursors

class DB_Mysql(object):
    def __init__(self,config):
        self.config=config
        self.config["cursorclass"]=pymysql.cursors.DictCursor
        try:
            self.con=pymysql.connect(**self.config)
        except:
            return None


    def creatTable(self,Name,fields):
        '''创建表  Num:int'''
        if not len(fields):return None


        temp_str=""
        for k,v in fields.items():
            temp_str+=k+" "+v+","

        temp_str=temp_str[:-1] #移除多余的逗号

        sqlStr="create table %s(TBid int primary key auto_increment,"%Name

        sqlStr+=temp_str+");"
        #self.con.cursor().execute(sqlStr)
        self.__executeSql(sqlStr)

    def insertData(self,table,data):
        '''插入数据 [{},{}]'''
        fieldStr=""
        valsStr = ""

        for k in data[0].keys():
            fieldStr+=k+","

        for s_v in data:
            valStr=""
            for v in s_v.values():
                valStr+="\""+v+"\""+","
            valsStr+="("+valStr[:-1]+"),"

        fieldStr="("+fieldStr[:-1]+")"
        valsStr=valsStr[:-1]


        sqlStr="insert into %s"%table+fieldStr+" values"+valsStr+";"

        self.__executeSql(sqlStr)

    def __executeSql(self,sqlStr):
        '''执行SQL语句'''
        result=None
        try:
            with self.con.cursor() as cur:
                result=cur.execute(sqlStr)
            self.con.commit()
        except:
            print("SQL执行失败")
            return  None
        else:
            return result

    def closeConnect(self):
        self.con.close()
        pass

if __name__ == '__main__':
    pass

'''
config = {
    'host':'localhost',
    'port': 3306,
    'user': 't1',
    'password': '123456',
    'db': 'test1',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor,
}

# Connect to the database
connection = pymysql.connect(**config)

# 执行sql语句
try:
    with connection.cursor() as cursor:
        # 执行sql语句，进行查询
        sql = 'SELECT * FROM student'
        cursor.execute(sql)
        # 获取查询结果
        result = cursor.fetchall()
        print(result)
    # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
    connection.commit()

finally:
    connection.close();
'''



