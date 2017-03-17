import pymysql.cursors

class DB_Mysql(object):
    def __init__(self,config):
        self.config=config
        self.config["cursorclass"]=pymysql.cursors.DictCursor
        try:
            self.con = pymysql.connect(**self.config)
        except Exception as e:
            print("类初始化错误--"+repr(e))
            #创建数据库
            self.con = pymysql.connect(host=self.config["host"], user=self.config["user"], password=self.config["password"],charset=self.config["charset"])
            sqlStr = "create database %s" %  self.config["db"]
            if not self.__executeSql(sqlStr):
                return None
            else:
                self.con = pymysql.connect(**self.config)

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
        #print(sqlStr)
        self.__executeSql(sqlStr)

    def insertData(self,table,data):
        '''插入数据 [{k1:v1,k2:v2},{k1:v1,k2:v2}]'''
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

    def getData(self,table,*fields):  #--------------需修改----------- 符合field-生成器？------
        '''获取某表数据'''
        fieldstr=""
        for f in fields:
            fieldstr+=f+","
            pass
        fieldstr=fieldstr[0:-1]

        sqlStr="SELECT %s"%fieldstr+" FROM common %s"%table

        return self.__executeSql(sqlStr,False)

    def __executeSql(self,sqlStr,changeTag=True):
        '''执行SQL语句  Tag默认True是会对数据库修改的行为'''
        result=None
        try:
            with self.con.cursor() as cur:
                result=cur.execute(sqlStr)
                if not changeTag:result=cur.fetchall()
            self.con.commit()
        except Exception as e:
            print("SQL执行失败--"+repr(e))
            return  None
        else:
            return result or True

    def closeConnect(self):
        self.con.close()
        pass

if __name__ == '__main__':
    '''
    config = {
        'host': '192.168.1.116',
        'port': 3306,
        'user': 'newPC',
        'password': '123456',
        'db': 'liulimusic',
        'charset': 'utf8'
    }
'''
    config = {
        'host': 'localhost',  # '192.168.1.116',
        'port': 3306,
        'user': 'musicUser',  # 'newPC',
        'password': '123456',
        'db': 'liulimusic',
        'charset': 'utf8'
    }
    connection = pymysql.connect(**config)
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



