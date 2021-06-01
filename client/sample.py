import dbtest
import base64

db = dbtest.Database()

sql = 'SELECT * FROM pomail_mail'
row = db.executeAll(sql)

id = row[-3]['id']
b_image = row[-3]['attach_file']
buf_decode = base64.b64decode(b_image)
print(id)
print(buf_decode)

'''
# 모델 결과에 따라 tag 바꾸기
# 이미지 가지고 있는 행의 id
id = row[-2]['id']

# AI 서버 호출
b_image = row[-2]['attach_file']
result = 1
sql2 = f'UPDATE pomail_mail SET tag = %d WHERE id = %d' %(result, id)
db.execute(sql2)
db.commit()
'''
'''
client = test.AIServerBackend('localhost', 'TEST_TOKEN', 5000)
images = {
    id: buf_decode
}
print(client.test(images))
'''