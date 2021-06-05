import dbtest
import base64, io
import aipost

db = dbtest.Database()

sql = 'SELECT * FROM pomail_mail'
row = db.executeAll(sql)

id = row[0]['id']
b_image = row[0]['attach_file']

## To.상연 : b_image에 파싱된 이미지 값을 넣으면 됩니다. tag UPDATE 할 때 PK인 id 값 필요한거 참고하시구요!!!!
buf_decode = base64.b64decode(b_image)
#print(id)
#print(buf_decode)
im = io.BytesIO(buf_decode)
#print(im)


client = aipost.AIServerBackend('124.50.4.138', 'TEST_TOKEN', 5000)
images = {
    'test.png': im
}
result = client.test(images)
#print(result)
print(result['result'])

sql2 = 'UPDATE pomail_mail SET tag = %s WHERE id = %s;'
db.execute(sql2, (result['result'], id))
db.commit()
