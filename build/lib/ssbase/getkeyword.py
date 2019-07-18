
import xlrd
import xlsxwriter
import redis

redis = redis.StrictRedis(host='127.0.0.1', port=6379, decode_responses=True)


ExcelFile=xlrd.open_workbook(r'C:\Users\Administrator\Desktop\first_result.xlsx') #打开目标处理xlsx
sheet=ExcelFile.sheet_by_index(0) #定位到索引为0的工作表，即第一个工作表
cols=sheet.col_values(1) #取第3列的数据
# print(redis.llen('provider'))
for i in range(1,len(cols)):
    redis.lpush('licenceCode1',cols[i])
    print(redis.llen('licenceCode1'),cols[i])


# for i in range(redis.llen('licenceCode')):
#     redis.lpop('licenceCode')
# print(redis.llen('licenceCode'))

# l = ['成都房江湖信息科技有限公司','成都昱超贸易有限公司','南宁市顺柏贸易有限公司','浙江力德节能科技有限公司','温岭市广源门窗幕墙工程有限公司','上海柏瑜实业有限公司','深圳市明源云客电子商务有限公司','广西金图工程咨询有限公司','辽宁同飞玺铭会计师事务所有限责任公司','重庆力瑞机械设备有限公司','云南卓立工程检测有限公司']
#
# for i in l :
#     redis.lpush('provider_law',i)

