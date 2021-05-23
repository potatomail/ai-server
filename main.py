from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
import numpy as np
import cv2
from tensorflow import keras

app = Flask(__name__)
api = Api(app)

cnn_id = keras.models.load_model('./models/cnn_id.h5')
cnn_driver = keras.models.load_model('./models/cnn_driver.h5')
cnn_student = keras.models.load_model('./models/cnn_student.h5')

models = [cnn_id, cnn_driver, cnn_student]

#image = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xdb\x00\x84\x00\t\x06\x07\x13\x13\x12\x15\x13\x13\x13\x15\x16\x15\x17\x19\x17\x18\x19\x18\x18\x18\x18\x18\x18\x19 \x1a\x17\x16\x1a\x18\x1a\x17\x18\x18\x1d( \x18 %\x1d\x15\x17!1!%)+...\x17\x1f383-7(-.+\x01\n\n\n\x0e\r\x0e\x1b\x10\x10\x1a-\x1f %---------------------------------------------+--++\xff\xc0\x00\x11\x08\x00\xb7\x01\x13\x03\x01"\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x1c\x00\x00\x02\x03\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x05\x02\x03\x06\x00\x01\x07\x08\xff\xc4\x009\x10\x00\x01\x02\x04\x04\x03\x06\x04\x06\x02\x03\x00\x03\x00\x00\x00\x01\x02\x11\x00\x03\x04!\x05\x121AQaq\x06\x13"\x81\x91\xa12\xb1\xc1\xd1\x07#BR\xe1\xf0\x14\x15br\xf1\x163\xa2\xff\xc4\x00\x18\x01\x00\x03\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x00\x04\xff\xc4\x00"\x11\x00\x02\x02\x02\x03\x01\x00\x03\x01\x01\x00\x00\x00\x00\x00\x00\x00\x01\x02\x11\x12!\x031AQ"aq2\x13\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00?\x00\xc3T\xa8)@&\x07)i\x8e8\xc7\x93\x15\x90\xb0\xd6,\xa7.\xa6:\xef\rD\xda\x18\x93\xf9\x89#HeWHf\x06N\xc32\xb9\x08IAJfM\x08v\x0f\xac5\xc4f\x94\x15"Z\xaf\xf0\x9e\x82\')?\xf0+E+\x94\xd4\x13\x0b3\xaa2\x8a\xa7))c\xa8x\xd3\x8a\x92i\x95\'[\xbb\xc6y2\xdagH\xc9\xee\x90\xc9\xd9l\x8f\x13\x83\xac{-\x04(\x8d\xf6\x8b\xe6\xa0#\xc5\xc6\x0c\x9bFU,ML\x14\xcdC\xbe\xca\xd7d\xca\x0e\xaf\x05v\xc3\x15\xce\xb0\x9d[_\xb0\x8c\xce\x15"\xa1k\x01\tS\xec[\xde4\x15\xf8Ww\x90*\xea\x17=c\xa2\t\xa8\xd17V_\x83R\x82\x02\xd6<[C\xa9\x93\x822\xa1\r\x99Z\xf2\x85tU9\x01}v\x82\xb0je.fuo\x15\x8e\xb4\x85f\x92b<)\xcd\x15\xccS\xc7\x98\x8a\xc8\x0114\xa4\x00\xc7\x84Y*\x10\xcd\xe2\xf2\xe6L\x99\x94\x0br\x84\xd5)\x12\xc9\n\x0cLkQ4\x99\xa4\xb5\x84g;FRf\x8d\xc4G\x969+\x1e/e\x14s\xca\x96R,\r\xa0J\xf9\n\x94\xa0x|\xa0\xc4\xd3\x04\xac)?\x0b<\x11R\xa4\xcf9\x05\x94\xde\x1e|DA-\xe2U\xbdX\xae\xa2\x80\xab\xf3\x13\xa4U\x86\xd5%\x132\xacxUb\xf0N\t_\xdc\xcc2\xa6\x8f\t\xe3\xb42\xc7\xb0 \x10f\xcb\xbaM\xfaC\xe2\xff\x00\xd2&\xdf\x8cC\x8eakB\xc1\x17\x96n\x1a\x17-a\x88\x8d\x0e\x0f\x8b:{\x89\xe2\xc7\xe1&\x01\x9f\xd9\xb9\x8a\xa9L\x94_9\xb1\xd8\r\xc9\xe8"S^\xa0\xaf\x83\x8f\xc3\xac\x1f9\xff\x00%c\xc2\x82\xd2\xdf\x8e\x85^Zz\xc6\xb3\x13\xc42\x92@\xd0|\xf6\xf4\x8b\xd5!2%\t2\xf4D\xb1\x97\xa8\xe3\xcc\xc6@\xe3\x00\xcb!g\xc6K1\xe2"g\\V\x81\xf1\xb9\xc1\xefc\xf2\x8c\xb5|\xe7:\xbc\x15W<\xa9J%D\x93\xc6\x15\xd4*\x08\xa0\xd3W\x14\xbcMf<@\x85\x19\x12B`\xb9sr\x86vx\xa1"\x06\x98\xac\xca\x82\t3\xe9\x9d\x8a\x9aL\xb3\xbc4\xc4\x02\x8d\x8e\x90\xab\xb1\x95i\xee\x82R. \xfcz\xb8\x8b\x01\x1c\xf2\xec\xa4z<\xc2\xaa\xc23\x03\x0b)jRf\xac\x9d/\nfT\xac\x93\n\xa6\xd4)$\xb6\xf0\xd1@\x93\xa3\xb1%\x0e\xf5}c\xc8\x04\x92nc\xa1\x89X}5.i\x80\xbd\xfe"\xfaZ/\xae\xa5i\x99\xc2\x83\xa9\x8b\r\xba\xc1x\xa4\xb9i\x03&\xa7s\xf4\x80\xe8)\x93\xdd\xe6s\xde\x1br\xd6\x06m\x93\xb6\x1f\x992\xc2V\x94\x97:\xc5\x14\x8a\x0b\x98\xb5\xab}\x04\x11\xdee\x19T\x1d\xb5\x1d"\xc4K\x05i!9\x12o\r\x16\xbd1T\xe9yP\x10\x05\xc9u\x1e\x1c\x04(\xc5$\x99L\xe3Xu[5\xa5\xb8\xd4\xa8\xdf\xce*\xc6\x10\x95\xa1\x1b\x90\xd0\xf1J\x80\x85\xa9\xc3\n\xd4\x9b\xec\xf1\xb0\xc0i\xd1\x94\xcbV\x82\xed\xc6\x15P\xcf\x00X9f~\x10\xd2\x82B\xa5\xab\xbc7q\xb4UU \xde\xcd\x9d\x0fu*QS\x00Z2\x8b\xa8\x0b+\x9a\xbd\x03\xb4y\x88T-HP\na\xbc\x05L\xa4\xa8%$\xd8\x1d8\xc5g\xcc\x92%\x81\xe5b\x1b*\xd6[5\xdb\xe5\x1a\x9e\xca\xcb+I\'\xca3\x98\xc2s,=\x92\x91h\xd0v~\xb3"\x06R\tm"\\Rw\x93\xf4i/\x81u\x81\xe6\x81\xc2<\xafw\x1c50$\x9cO\xbcY\xcc\x19B#\x8a\xcf\x98\xa0{\xb9k;X\x18\xec\xcdQ*\x16V\xd7\x10\xe4\x1d#2\xba\x82TJ\x8e\xc6\x18M\xc3\xe7\x04\xdd$jH \x83\x01\xd6a\xaaO\xd6!\'&QR\x18\xcb\xaaH\x92\xe7V#\xda\x13\xd0LWE>d\x9e|<\xe1\xa8\xa2iNt\xd6\x17\xad@\\m\x11\x9b\xa9YE\xd0\xce\xb6\x9d5\t\xef\x91\xf1\x00\xd3\x13\xb8<[q\x0c\xbb9XP;\x99\xa7\xc2\xad\x1e\x11\xd0V\x9c\xf9\xc7\x84\xef\xc0\xf1\x89b\x15\xa1J\rf1H\xf2[\xb2m^\x89\xf6\x9f\x08(\x99\x98|\x1a\x88\xd9v>\x8dI\x90\'L\xf8\xd4\x0eN!?\xcb@\xb8H\x15R\xc2T\x1f+9\xe4\xfa\x18c\x8e\xd7)\x19r\xd9<\xb4\xb6\x909ROE8\xd7\xd1\x1a*\xd7\x9eng\xb2\x8eW\xe1\xca1\x9d\xa1A\x04\x94\x86\x04\xbbs\x8d6%P\xe7\x86\xf1\x96\xc4&\xb91\x16Z\xc5\x02a"\xfa\xc5S\x15\x16\xcfT\x0eohV\xc2\x91\x10"`G\xaa1\xd2\xe4\xadwJI\x1c@\xb7\xacc6\x15K4 \x85\x10\xe0k\x17U\xd3\xc9_\x8eZ\x98\xee u\xe1\x8b\xca\xf7}[\xe6\xd0\x19\x92G(4#\x925\xfd\x8c\x9f\x91\xc1\xd5\xfeq\xa3\xab_xc\t\x81\xd4\x10\x15\x1a\x8e\xc8U\x19\x99\x8a\xb6\x89N#\xc2^\x14\xe2(\xca\x0c \n\x0fx\xd1\xf6\x89c)\x8c\xb5D\xa0\xb9a`\xdcX\x88\x11@\x98\xd94\xd2Hw\x11\xd1\x9b\x1dc\xc84&C*\xda\x90\xb5\x95\x07`\xe3\xff\x00"XZ\x0c\xc5\x04!\xee[\xa4/\x9f<\x06H\xda48UB$J\xef\xc8y\x8a\x07\xbaI\xd0lf+\x8f!\xc8\x98\x15@H\xb9t\x80\x14\x85\xb8R\x8b0\xd5\x87\xea<\x04\x12H\xee\xdd\xdf\xc6%\xa7\x91b~\xd1\x9c\x93Z\xbe\xf0\xccQ%E\xcb\x98\xd4\xa9HE\x1c\xa4\x0f\x8ad\xd5L\xe6.\xdfHF\x07\x1d\x14\xe1\xf4hZR\xa5\x9f\tuz\x12\x08\xf5\x80\xa7\xd3)\xc9k\x17n\x91]l\xd5\xcaZ\xa5\xbd\x82\x88\xe8\xec\xf0\xe5\x14aR\xc4\xd34)\x85\xd3\xb8\x82\x9f\xc1{Z\x03ER2\x04\xa6\xc1\xaex\xc5t\xb8\x9d\xc0.\xc2=\xa5\xa9M\xbc#*Ix\x8d2\xf3\xcc\x05\t\xb7\x08g90\x0ejFd\x85|)\xb5\xb71Je\xa7\xbc\x16\xf0\x8d\xf8Ex\x85J\xb2\xe6\xca\xe3F\xe1\xe5\r;-E6i\'((,\t\x8aFI\xe8\xcdYL\xb1\xde\xbb\xe8\x1d\xce\xc0\r\\\xc0\xd8_j0\xe93\nf-g\xc4\xce\x84\x92\x80:\xea|\xb8\xc3O\xc5")hD\xa9L\x935a*"\xce\x00$\xfd#\xe2\x80\x12@H\xb9\xb4U=\x14\xc2\x8f\xd4x\x04\xea9\xc8\xcfNP\xb4\xf1\x1a\xf9\xef\x0e\xe5\xa5-\xa0\x1eQ\xf3/\xc2l-t\xf4\xe5K\x0c\xa9\x871\x1c6\x00\xc7\xd1\xa4\x92bn[,\xa3\xa3\xda\xa9)"\xe8\n\xe4c\x1d\xda\xac\x05\x08\x96\xa9\xb2\x819|E\x02\xef\xd26\xaa\xff\x00\xc8\x1a\xa5\x10\xd1\x9b@\x94\x13>\x03S\xda\xd2\xa1\x94\xcb\x01>\xf0\xe3\x07\xa9\x92%LR\x83\x92\x9f\x0f\xa4\x01\xf8\xa5\xd9\xd3"\x7f|\x80\x04\xb9\x85\x98[\xc5\xbd\xb9\xc4\xa8\xa9\xd1.\x99\x05E\xca\x85\xc0\xdb\x80\x837d\x9f\xe2\x0b4\x97\xb0\xb4z\x89\x05J\r\r\xa8\x13-L\x02O\x9ch\xfb7\x84\xa0\xce\xef\x1b\xc3.\xfco\xfaG\xd7\xca4X*\xc7\x18.\x1e)\xa43x\xd5\xe2_+i\xe5\nqi\xe5L\x06\x82\xe7\xe9\x05c\xb8\x8c\xc0\xa4\x8bePc\xc4\x1e\xb1\x9b\xc4*\x1b3\x13s\x01\xb2\xb5B\x9cF\xb0\x93\xe7\x08\xe7\xce\xb9\x82\xea\xe7\xb80\xa6t\xcd`Y\xa8\x84\xc59\xb4E\xdb\xacrtx\x8auxP\x85PQ\x99\xab\t\x1a\x9e:q\x8f\xa2+\x0bE-*\x1e\xe1[\xf31\x88\xc0\x82\x8a\xc1H\xe2\x1f\x80k\x9fx\xdfU\t\x95(D\x9b\x00\x8d9\xb4O\x95\xa4\x95\x93\x93]\x08\x14\xecJn\x91v\x85U\x13\xe5Lt\x94\xf8\xb60\xe2l\x89\xb2\x94\xa4\x84\xf2#\xed\x0b\x06@\xe3-\xe2\x9cq\xf4\x9cR\x03\x91K\x91*0\xeb\xb1\xe3\xc0\xb6\xd6\xf1R\xa6\xa0\xa3"\xec\xfa\x18k\xd9\nb;\xc0n5\x7f-\xe1\xe7\x1dX\xf1{\x13\xe3\x00\x92A\xd22\xf3\x8b\x12\x06\x91\xa2\xc7\xd6\xf3JA\x85r$\x05\xaf(\x84\xe9\x19\xdbb\xd1(\xc7C\x99\x94`\x16\x8f`d\x11r(J\x9ajB\x9a\xc1A\x8d\x9fw\xda\x0f\xae\xa4R\x87\x85\xd4\x10\x18\xb6\xc3o(>M|\xdc\x9d\xda\x8a\x8a@\x01\x89k>\x96\x8eZ\x96JD\xb4\x10R\x96\x01?\xaa\xe6\xea\xe3\xacO+\x05\xae\x84\x8a*a\xc5\xec#I\x89,\xe4\x92\x9d\n\x12\xa0y\x97\xff\x00\xd8\xb6\x8b\x0eT\xc9\xe2d\xd4\x80\x00+P\x7f\xda\t\xf2\xb8\x10\xdb\xb5\xd4r\xd0\xab\x1beL\xc0y(}\xde\x13+\x06\xc4\x98\xb8\x96\xb5\xe7J\x89R\xceb8\x1e\x0f\x13\xa4\xc3T\xbay\x99l\xbc\xeeF\xe4B\xb4\xa7\xc5}\x85\x9b\xda4\xd3\xab\xfb\x84#Bf\xa5\x9ckah-k@J\xc5\xd4\xb8@|\x9d\xeaR\xe3MI\x8a\xe8\xe4\xa6J\xc8\x13B\x85\xc5\xbe\xf0E\x04\x81"\x9d3\xa6\x17T\xe3\x95<@\xbb\x98\n\x96L\xb38!\x0f\x95\xc9\'\xe6\xf0\x1d\xa1\x9ci\x0c\xa8%\xab2B\x96\xe9Q\xf3h\xfa\x86\x13L\x99R\xc2R\x1b\xa4|s\x12\xc5\xc0Vp\x08b\xc3\xa0\xfb\xc6\xcb\xb3\xbd\xba\x950\x04(\xe4"\xd7\xd0\xf9\xfd\xe2\xdcq\xfcl<i\x10\xfcY\xc2&\xd4\xc9B\xe5\x872\x89%;\x90\x7foH\xca\xf67\xb2KI\x13\'\x00\tb\x12v\xeb\xce>\xa1>xP\xb5\xc1\xd1\xb7\x80P|\\=\xe1\xb2tt\xa8&\xecm@\xc9\x16\x1aCy5\x0c!"Hg\xb9\xf2\x85]\xab\xed\x0f\xf8r;\xcc\xb9\x94\xa3\x95\t\xe2`G`\x96\x8d\xc2f<W<\x80/\xac|\xfb\xf0\xff\x00\xb6\xf3j&\x19\x13\xd0\x12\xb6\xce\x92,\x14:>\xce=ca\xda\n\xa5K\xa7\x9b1!\xd4\x94)C\xa8\x04\xc3\xd3\'fg\xb6\x98zj%\x80@d\xa8\x1d\x016\xf9Fb\xa7\x0bW\xe8e0\xd24\x98MW}M\xde\x0b\xf7\x88\x05\x8e\x80\xb3(?Q\xed\n\xf1j\xce\xe2RJC\x95\x1d~\xf1\x1e[M\x13\xe4\xecKB\x8f\x11\n\x04(m\xc67t\xf2\x84\x89\x05 ^\xea;\xf8\xb7\xf4\x00\x08U\xd9\xc5\xf7\xa7:\xb2\xb2.y\x9b\xe5\x0f\xe4\xfeQ}UjAR\x1d\xb57\xe7\xaf\xbcR\x1d\r\x15\xe8\x9f\x15\xc4Nb\xe2\xc7\xc49\x06\xd23UUN\x1c\xea`\xbc^r\x89\t%\xc7\x1d\xec\xfa\xc2J\xa9\xba\xfbC\x0c\xc1j\xa6\xbe\x9a@f\xf6\x89\xcd/\x15*\x14\')Q\x14#1m\xa3\x80\x89,=\x840\x0f\xa3\xf6_\x00\x95\xdd\x85\x05\x12n\x14m}>\x1e\x11\xae\x93\x85\x00\x12P\xb0\x96\xd1\xc1\'\xce\xe2>u\xd9\xecbd\xb4\xe5\xcc\x19\x9b\xc5\xd7n\x97\x8d\x15^8\xa9r\xc2\x89|\x9f\x171\xb9\r\xa3\x0f\x94$\xa0\x9fa\xc5\x05v\x8b\x0b\x9d\x9b\xbcA\x0b\xe3\x97_1\x19\xfa\x9a\x10\xbf\xf8\xacj"\xa4\xfe&\x84\xa8\xa7))\xb0\no[Au\x0b\x95P{\xd9J)$9\xe0Y\xae=b\x90j\x1f\xc2\x1c\x90\xf5\x02\xcd\xc1\x9d\x00\xadZj\xc2\xe2\x1cvs"d\xcc)$\x8b\x871F\x1fR\xb4\xb8l\xc3{<6\x97!\x06I\x08\xb1/\xa78^I\xaf\x18 \xcc\x9d^\x1aJs\xb3\x12KGa82BV\xb5|[F\x8a\xbe\x84\xa9H@P\x0c\x970\x99).A.\x01kDT\xf5\xb1\x96\xbb2\xd52&f7\xde:72\xfb?\x9cf\x041\xe2c\xa1\xb3\x88\x0c\xea\x10\x99\x92\xc1\x13\x1dd\x16\x00X\xf3}\xbaE\xa8\x993\'\x842\xf4${E\x18BV\x9f\ne\x84\x9d\x8d\x8fXq)(\xc8\x10\xe1+*\xf1>\xba\xb5\xa2-*6\x9fE8t\xe1*R\xfb\xc7+\x98\x95\'\x9d\xc8\x1fx&\xb2\xbf\xbf\x95\x95e\x8b%"\xda\x84\x9b\x0f\'0\x06,\x999\xc6G 2E\xed\xcfH&\x82JN|\xc4\x00\x12E\x8d\xeeG\xd2\x1a)\xd1\x92\xdd\x12\xa2\xa1\x96e\xcdXP9r\xdf\x840\xc6h\xa5\x8ays\x89\xbc\xbc\xc1]x\xb78CQRP\x85\xa2^\x8aP*\xe2@\xd3\xde\t\x93\x88\x0e\xe8\x85\x0c\xe9Z\x9b!\xd7`\xe26\x0e\xc7H\xa2@\\\xe9(Y\x0c\x948H:k\x15\xe1\xd2P&\xa8)\xd3\xe17\x1a^\x1ab\x12\xc2d\xa5\x00\xd9!>d\xeb\t\xa4\xc9\n!\x0es\x153\xe9c\xb4\x14\x9b\xd3\x16\xa9\xecI\xdaP\x94\xcc\xca\x82JF\x84\xef\x08\xf3\x90a\xe7led\x9eP\xcd\x94\x01\xbf\xd6\x10\xae:\xfaT\x13\xe8\xfd\x92\xed\x86|\xb2\xa6YvJ_B\x00\xb9\'m#p\x8a\x94\xb6`A\xe6\xe1\xbdL~|L\xd2\x0b\x87\x07\x88\x8d\xdfg1\xf9jBe\xac\xb1\x1a\x95\\ra\xf30\xad\x14\x8c\xcf\xa7\xca\x9c\xf7v\x1b}\xf9\xc7\xcb;\x7f\x88M\x99P\x12T\xc1\x1f\x08\x16\x00\xf1\xe7\x1a\xd4b\xa9$\x04)\x04\x8d\xc2\x92H\xf2&\x1b\xe14\xd2\xa7\xcc\xfc\xc4!KM\xc1)\x04\x8e\x06\xef\xeb\x1a:\x1a{B\x9f\xc2\x9e\xc8\xce3?\xca\x9e\x9c\x88o\x03\xbee\x12\x08%\x89\xb2X\xf9\xdba\x1fM\xae\xc3S6Z\xe5.\xe8XRH\xe4\xa0\xc6)\x9bW\xdd&\xe6\xdc\x7f\x88\x06ok)\x03\x8e\xf9\x04\x8b+\xc4,t \xdfc\xb45\xd9:\xa3\xe7\x98%4\xcaAYK7I@\x94\xaa\xccA\x16!\xce\xed\xa6\xc5\xe0\x8a\\D*BS\xdd\xe7\x0576\xf9E\x1f\x89X\xe2\x0c\xb1\xdd\x10\xa18\x14\xbd\xbfI\xb8\xf7\xd6;\xb0r\xfb\xc9h\x98\xa1\xe0\x97\xff\x00\xe9[\x0e\x80_\xd2\'\xc8\xb2\xa0X\xfe\x8e\x892)\xf2\x07I.\xa5u\xb5\xbc\xb4\xf2\x848\xadH\xb9\xb3\xff\x00t\xf3\x86\x18\xf5j\xb2\xa5\x8f\x84\x90T7`\xda\x1fBc1:fb\xeeJ\xb8z\xde\x1a\x86Z\x17V\xcc\xdd\xeem\xff\x00\x90\xa2\xa2g8k<\xa4\x9c\x89$\x9bX\x01\xf7\x84\x95E\x89\x1c\x0bt\x80\x14TVb9\x8cx\xa3\x10\x80bemh\x82\x17\xa9h\x8a\x91\xbe\x91\xc1~\x107\xbf\xa4\x10X\xd2\x86\xb070C\xf41\xa6\x9e\x916J\xc2\xc1#\xbbR\x85\xf9\x16\xde\xfd#\x13NX\xc6\xaf\x0b\x92f\xa1\xc1\xbav:A\nf\x12j\xf3,\x90\x18l#Y\xd9\xb0\xac\xaa\xd6\xc0${\x98]W\x87\xb2\xcaJ@\t>j~~p\xfb\x01\x97\x96W\x84\x81\xe3{\xf0\x01\x9a\x12OBMhu\x85\xd7)#-\xc5\x99\xf8\xc3l:b\x9b2@-{\xc2,D\xa9\nJ\x91t\x9e\x17c\re\xa9h\xa7\xcc\xc6\xf7\xf7\x88\x93\x8d\xae\xcfjjRB\x96\xab\xac\xfbD\xa8\xe4\xa7\xbb\x07\xab\xc6zd\xd0\\\x8c\xdd!\xf5\rNZE\xcc\xcb\xa1oxI+CZe]\xfbZ\xf1\xd1\x05(*\xecox\xe8[Dm\x89\xeb\xcc\xc4\xa1KK\x06P\x04\xb8\x7f\x13\xed\xb6\x86(\x9934\xa4\xbd\xce\x85GW\xd9\xe0\x9a\x9a`d\x82K\x95\xe5>\xaf\xaf8\x01J\xc8\x97S\x9c\x873z\xb7\xbbGElxt\x17$\x04\x19j\x9a\x91\x97\xc4\x1bGkz\xdf\xda\x0f\xa3\xa6\x94B\x95"j_\xf6.\xca\xf2<an;-]\xdc\x80\xa2\xe7"\x94yfYP\xf6#\xd6\x15S\xd0\x92\x9c\xd7H\xe2\xad\xf9\x01\x00\xa2t2\xa9\xa0\x9c\x12f\x92\xe0\x92\x01\xf9\x8f(\nj\x14\x03\x87{A\xd4\x86aG\xf8\xe9X9\xd4\x14\xc4\xee7\x1c\x0b\x16\x8a\'a\x93\x02\xf2\\u>\xf0l\xcfkE3&L \x00]\xafx\xd4\xf6\x1e\x90N\xa8J\x8d\xf2:\x89\xd9\xc4*V\x1aX\'0\xcex_\xce7]\x80\xc0\xe6S\xcbZ\xa6\xb6eX1\xdb\x8bA\x8e\xd8\xabf\x07\xf1.\x8f-N\x7f\xdc8\xbcbV\x88\xfa\xa7\xe2|\x87@X\xd8\xde>a0\x88\xe8[C\xbe\xcaQ-\xe2i\x96\xe0\x91p\x9b\xa9\xb6\x16\xbfK\xc4\xe4\x90\x02\x89\xe8 uObrxB\x92R\xa6:\xbb\xbf\x91\rnQ\x9e\x803Mq\x94\x1aJ\x88Sx\x8aT\x14\x85\x82\x01\x1e\x16\xd49\x05%\xf4\x8d\x97g\xbbF\x89Y<NH\xf1\x00Ig\xb0=c\xe7\x12\xaa\nK\x8d\x85\xb9Er\xd6S\x0ba\xb3\xeeS\xfbB\xa2.B\xd3vRT\x01\xe8A\xe5\xbc`\xf1*I}\xea\xa7+\xf2\xd2n\xa6 9\'\x807=#$+\xe75\x8a\x80\xe3\xb72\xf1\xaf\xec\x9fa\'\xd5\xb4\xfa\xa5)\x12\x7fH/\xdeL\xff\x00\xa8?\x02\x7f\xe5\xbe\xdc`\x06\xc6x_g\xff\x00\xd9)\x0bs*\x92P(\x96\x12\xd9\xd6_\xc4\xcf`\xe4\x17Q\xe1\xbd\xe3gR\x99R%\xa6\\\x91\x95(\x05!!\xf7\xbf\x8b\x89\xdc\x93\x06\xaaZ%K\xee\xe5$$%,\x02G/\n@\xf4\x8c\xbe!\x8b%L\x9b\x12\x10\x01;\xf3\x17\xb8k\xdfx!\x01\xc5\x14\x151\'31;\x96k\r:Fn\xb6ws1\xc1\x07\x87\x03\xaf\xa8\x831\t\xeeK\xeda\xc3[\xfd!\x05Z\x1c\xbd\xe1X\x08\xcd\xae)\xb8H\xbf+\x0f\xfa\xbf\x94\x0c\xb5\x12\xa2\xa3\xa9\x89\xccV\xdb\x0f\xacP\xb5@\t\xcb\x89$\xda=\x92\xa7\x7f\xef\xa4Jaaw\xbf_x\xc1EsA#h\xa9&-\x98\x93\xa4A0@\xcb$\xa0\xbb\xe9\r\xa8\xebL\xa2\x08\xf8N\xa2\x15\x85r\xe9\x1e.f\xd0\x02\x87uk\xefr\x90\x1c\x9bj\x05\xb5\xf5\x17\x8b%\xac\x04$(e\x19\xaf\xd3\x8c\x17\x86`\'\xbbD\xf5\x10\x12~\x14\xef}\xcf\x0e\x91*\xfc5y< \xa9\xef\xd0BJI\xba\x16O\xc0I\x15\x7f\x98r,\x84\xa7\x8d\xf3F\xd6\xa7\x10J\xe9\xd2\x90C\x98\xf9\xed\x150J\x94X\xb0\x8d.\x14\x8b\xa4\x9b}`4\x84\x93\xd0\xb9\n)\x98\xa4\xeb\xb8\x8d\r\x1dr\x8d\x1c\xe9e\x83\x97I\x8c\xca\xe7<\xe5\x03\xfb\xed\x13\xaaS8K\xb2O\xce\x00\xb1\xb5\xb1\xdd\x05B\x04\xb4\xe6\x98\x1d\xaf\x1d\x19\xc1L\xa3\xa2\x83yGB\x7f\xcd\x1a\xbfCiU\x882\x00\x17Y\t\x00p\x03Uy@\xe9\x01@\xa4\xdd\xc1\xeb\xa8\x84\x88\xa6Vp\xcaq\xc3\x85\xb8\xc3Y\xb3\xb2\xa8\xb3\xb8\x16a\xd3\xed\x0e\xcc\xd7\x83\x19\xd5*J\xa5\xb0I\xf0\xa5,\xde_h\xb2\xa4\x85\x8b\xcb\x19\x80\xcc\x06\xca\x1b\x8e\xb60\xb2~"\xb9\xb3\x82\xc2@$\x0b\x8b\x00F\xfe\xa2,Ez\xd2\xac\xdb^\xcd\xad\xdf\xeb\x18-}\x03\x9b)\t"zI.t?\xa7\xce\x0c\xa1\x9cJ\xcc\xc5\x17\x1e\xbeQI)[\x02\x9b3\xe5>v1\xa2\xec^\x19,\x8c\xd3.\x9c\xd6O\x1e\xbc\xa0\xd5\x8dC\xde\xc7vd\x05\x1a\x99\xa71W\xc0\x0e\x8d\xa8-\x1a\xc9\xd3u\x102\xeb\xd2\x19!\x85\xb4\xfe e\xd5\x03w\x87Z*\xa2\x923\x9d\xba\xa33d(\rE\xc4|jq\xbfH\xfb\xcdi\x0c^\xf6\xf9\xc7\xca;Y\x83\x10\xb31"\xc4\x92\xd1D\xc5\x922\xdd\xe6\xd1QW/8\x92\xd0_H\x88Da\x0fP\x9bC,\x17\x03\x9bR\xb0\x10\x92\xdb\xabD\x8f8\xb3\t\xc2\xf3\xa8f\x04\x87\xd0G\xd20\n\x84\xcbI@\x96\x90%\x96s\xaem\x81k5\xc1\xf4\xde0R\xb1\x9fg\xfb\'&HJ\x94\x04\xc5\xda\xea\x1e\x04\x80\xce\xc0\xeay\x9d#AUZ?M\xfeC\xa9\xfbB\xf9\xb5\xb9\x83\x83\xe1c~\xadn\x7fHKGR\x99R\xca\x1c\x90\x1c\x8d\xcd\xcb\x8f\x9byF\x08\xc2\xa6\xbc\xe6\x05,T\x977\xdc\x90E\xbc\x89\xd7\x88\x8f\x9fWV$\xccV@]\x80/\xaf\x85\x85\xf5\x11\xa0\xc51>\xeeR\x8b<\xd5|?\xb5\xc8\xd2\xfc2\xfb\x18\xca\xce\nR\x89%\xad\xa7\xf3\xbc\x00\x903\x99-\xb8\xd7\xef\x02\xa9{\xc4\xe7(\x0eqHM\xa0\x18\xa5w\xb4TS\x04\xa8\x01\xcf\xce"z@1\\\xb4\xc7\xab%\xe2\xd6\x83(\xb0\x89\x93X\x84\xb2O\xeaU\x93\xe4w\xf2\x81a\x00l\xcc7\xd8\xfd\x0cx\x8aE\x1f\xd2y\x16\xd7\xce4\x120\xd4K\x98\x87u\x80Fg\x0c9\xdbx#\x13\x9a\xa9\x93\x16\xbd\x13\xa2y\x01\xc25\x81\xb4#\xa0\xc2\xd6\xb2I\x05(O\xc4w\xe8>\xf0\xdaE,\x94\x10\xf2R\xbe\xaeH\xf5\x8b\xfb6\x7f1\x96l\xa0\xa1~\x96\x89\x8a\x81\x94\xa4\x87!\xc1;\xc2\xf6\r\x95\xce\xac@$ \xa8\'\xf6\xbd\x87Hm#\x1b(JJ@6b#<\x9a\x16J\x94\xee\x0e\x8d\xaf\x9c\r(-D\xb3\xd83\x0b\x98\x18\x98\x7f\x8aKBH\x98\x8f\x81w j\x0e\xf1L\x9a\x82\x00Q\xf8\x12`z,\x0e\xadLB\x14\xdc\xed\x05\x8e\xcb\xd5\x1b)#/\x0c\xd0q\x15\xab\x14\xadC:\x96\x0e\xa4\xb1\x81\xe6\xe2\x05\x89k\xe8a\x8dWf\xea\x9c\xfeY#f!\xa1=F\x19=%\x95)c\xc9\xc7\xb4\x1a2\x8d\x06Q,\x14\x03}\xfef:\x04\x93\xdf$\x00%\xa9\x87\xfcLt\x1cMA\xa8\x9af$\xa1\t\x01l\xe4\r\xdbR\x9e|\xa2\xc9\x18D\xc0\x8c\xd3T\x12Ud\x85(?,\xc3T\xbcWL\x8c\xa9\xcd\x98\x95\x07\xda\xfb\xb1\x07b\xf1\x19\xae\xa4\xb9.\xb2\xa0\t\xe3r\xc4\xf3\x89\xbf\xa8\x1a=\xa7&Z\x8a\n\xb4:j-\xc3\x8c\\J\x89v 9>\x86\x16\xcf\nJ\x81$\xde\x19N\xa9"Nd\x8dC\x1eF\x1d!}\x04\xac\xad\xf18\xb1:\x98+\x0b\xc6\x15-\xc0\xdf\xda3\xaa\\G\xbem"\xb4\x96\x8a-\x1a\xc9\xbd\xa7\x98\x16\x14\xfaZ6\xb8F$\x95 (\x86,\xfc\xe3\xe3k\x9a\xfb\xc3,?\x1dZ\x10P\xe7\x90\xfa\x93\x01\xa1\x94\x8f\xaaUV\x02\xc70\x0f\xa0\x8c\xf6-T\x8b\xb9\x1fa\xfc\xc6n~?\x99IJ\x01!\x0c\x07\x15\x1e1\xa0\xc20\x82\xb1\x9ep\xe1gw6w\xf3>\xd0\x03b\tXI\x9c3\x0b\x0c\xda\xb6\x83W/\xacBN\x04\x1c\x13`N\xbdO\xf3\x1b9\x14\xa5\tY\x076e\x82\x90\x033\xb0\xb7G&\x01[)V\x0e\x99j\x19\x80wf\xf6\xda\xd0\xc2\x9eRQ\t$2J\x83\x00Xh\xe5\x9f1\xb3\xb9E\x85\xfcP\xd6\x92M\x89W\x17\xb6\x8f\xf5\x8c\xf2\xb1E\x90P\x10\x02V\xa0s\x15\\\x00\xa0E\x9b\x80\xd3\x9c3M^f\xb1-\xfa\x8f\xc2\x0b0a\xbf\xf6\xf1\x8c\x1d[[`\x9b\x13\xb0\xf5\xf6xRjZ\xef\xd7\x87 =\xe2\x89\xf5A.\x94\x9c\xc4\x9b\xfa\xdd\xce\xda\xc2\xc9\xcb\x7f\x88\xbd\x9d\xb6~|c\x18\x9dMVgHf\xdc\x9d<\xb9\xc2\x9a\xc9\x87+]\xdd\xfa_o(\xbad\xde\r\xf6\x81f/\x8f\xf0!LA3\x1fX\x91[\xc5@\xbcN\x03\n9\xb6\x82h(W5Ye\xa4\xa8\xfc\xb9\x93\xb0\x82p\xfc!S\x02\x96\xa3\x95!\x872N\x80F\xd7\x08\xc3\x11I(\xba\xb3(\xf8\x94Y\x99\xc5\x93\xe5\xf5\x89\xcaih\x12\x9d\x08i;!5*J\xd6\xa9e#\xf4\x87$\x9d\x9d\xc0\r\xbf\x94jfK\x03*\n\\\x8fOX\xe0\x7f\'2\x94\xd9\xb4?\xf6\xd3\xda\x02\xa5XJ\x89*\x07a\xca\x17/\xa2\xa7aUr\xa5\rr\x82\x00$m\xd2&\x9c/:B\x82\x03\x1d\x1e\xd0U%2{\x85\xac\x84\x96 \xa8\xea\xef\x14\x9cI`\x80\x00a\xa3\xfd\xa3);\r%\xd9\xe4\xbc\x01$\x83`F\xc2\n\x95\x81\xca{\xa4\x13\xcfx\xf1\x15J\xf8\x84w\xf935kr\x86\xb1\x94\xa2{\xff\x00\xc7\xe4\xa5\xedc\xed\x05\xd1\xd3IG\x852\xd2\x15\xc5\x85\xf9\xc4eU$\xeao\xce\xdf8\x94\xdab\xee\x0bn d7\xf0(\x16\x8fA\x17\x8f$K+\x1e+\x11\xa8\x8b\x17H\x1a3a"\x85\x86\xd2 R\x95\\\x80\xd1\xefq\xc0\xc5*\xa7<`d\xc0xL\xa1\xba}\xa3\xa2\x8f\xf5\xe3\x84{\x1b)\x00\xf95"\xf4I$$j|\xed\x06\x19\x96)H`<M\xb9m\xccWSL\xa4\x16)\xf0\x86=~\xf1\tk\xcc\x95\xabr\x1b\xec!\xda\x13\xc0\xb9\x92\x12e\x85,k\xa1\x1a\xee\xee<\xa254\x084\xeb(Y*\x1a\xa5\xbdX\xbf\xd2%8~Z\x10u)s\xe7\x13\xec\xac\xb5N\x9ce\xa4xR\x92\xe7n\x0eO\x0b\x18n\xa8\x921\x8a\\R\xb9\x90\xef\xb4\xd8Wr\xb3\x95\x94\x82K\x11\xf2\x84I\x96\xe6\xf1R\x84L\xc8\xf6ZT\xa2\x02A$\xc4\xfb\x9b\xb2nLn\xbb=!\x12Y\x19\x01[\x02\xb5\x107\xd8>\x8d\xf7\x80\xc2\x91gd{2Q\xf9\x93\x00\xcc\xce\xc7a\xfc\xc6\xb5,\x13\xd2\xed\xc1\x8f\xf3\x03\xca\xaa$\x9c\xa9\xb3\x06\'N\x1da}L\xd0\xd9Vs\x1b\xdbArv\xf2\xde\x00\xff\x00\xa2\xe9\xf5\xeeHH\xcd\xfb\x8e\x89\x1c\x9c\xda\x17"\x94#3\x1dHt\xa6\xc1\xfak\xf6\x8e\x9dP[(d\xa7O\xbe\x90)\x9c\x94\xfc"\xec\xdcO\xf1\x18\x01\x0b\x00\x1f\n\x1b\x9b\x06\xe5\xc6(\xa8\xa9;\xab-\xdf(,\xdc\x9f\xfb\xac\x0f>\xb5CR\xcf\xe7\x02N\x9a5rO8\xc6\'>\xa3\xf6\xfd\x87\xf5\xe0)\x93w7\xfe\xf0\x8a\xe6O\x81\xe6*\x01\x8ffM&!x\x8b\xc4L\xc8\x06.@r\x00\xdc\xb7\xfe\xc3ita\t:\x15\x8b\xbf\xd8E8,\x89e\xcc\xc7,\xcc\x01\xdc\x91\xaf\xbd\xa2\xfa\xb5\x94\xcd,\x05\xf8\xc2\xc8\x9c\x9f\x81\xdd\x91\x19\xe6\x12\xa2r\xa4\xe7 \xf1\x1aC\xce\xd0V\x92\xa1.\xcc\xa6~\xa4\xc6~\x9b,\xa2\xa9\x84\x96ku\'H&t\xde\xf2b\x144t\x8b\xf27\x89c\xb2c\xfe\xd1bI\x95)2\xed`\xed\xc0\xb3\x08IM0\xa9\x06bn4<\x8f8\x0b\x17O{9Nl\tnm\xa4^$M\x93(\xa81B\x8d\xda\xe4\x7f\x10\x14J!\xfc\xaa\xc3.\x9cn\x95\xeb\xd4EH\x9c\x95:\x8a\x886a\x19\xaaJ\xd9\x85%\x048\x06\xc3x.\\\xd1m\x8bo\x06\x80\xec\xda&\xb2XM\x98\xbc\x15.\x9f\xc3\x9d\xfd4\x1eQ\x93@,<A\xb5q\xa7H\xf4\xd7)),\xb3~\x7fH\xc1\xc8\xdcIK\x8f\x10J\xc7\x90\x8ag\xca\x96\x9b\xa5JA\xe1\xb7\xa6\x91\x99\xa0\xc4\xb2\xa6\xe5W\xd0\x83\xf3\x82\xa5\xd7\x9c\xccT\xf0P\xf9\x0e*\x955,\xac\xc9)\x1a\x90r\x92 i\x13\xe5N6\xef\x0f\x12\xa2\xa0\x07\xa4\x01\xfe\xc0\xa8eX\x04\x03\x06\n\xe1\x94\x14j\x18\x1d\xa0vk\x0b\xff\x00V\x84\x97\xcc\xdd?\x98\xe9r\x9d^\x1c\xc7\x9a\x89oH\x8a*Tu\x00\xc5\x92\xeb\xd0\x94\xde\xc7\xda3A\xd2\x0b2\xd3\xbb\xfa\xc7B\xc3\x8asH\xe4c\xa0\xd1\xb2F\n\x91vR\x17p\x1c\xff\x00\xd4m~q\\\xaa \x13\x99\n\nB\x88 \xbf\x02\x97\x04lo\x16V\x1c\x88fb\xb25\xdc9s\xed\xe8\xd1L\x94\x19I\x96\xa4\x90RT\xa2\xfa\x80S\xb3t\x11Y2I]\xb2U\ty\xaa!\xacr\xb7 \x97\x8d\x17fHM2\x88\x95\x94\xaf\xc2\xff\x00\xb9\x89\x07\x9b\x17\xf6\x8c\xde\x158\x99\xae\xac\xaa\xcctm\x05\xdd\xf8F\xb9ujH\x03+\x8b\x00\xd6\x01\xa3-\xf6<#@X\x86\x1e&\xa3.@\xc1\xff\x00\x9bFN\xaf\xb2d\x1f\n\xacv1\xb5\x15\x8e\x0b\xbb\xdbF>\x8cz\x8f(\x06\xa6\xa8k\x97]\xcf\x9e\xcf\x15\x1a\x858?f\xc4\x92\x14\xa2\n\x83\xb3\x82@\xfe\xf1\x8b&\x01\x9b2\x95\xa5\xdbM86\xb1}Ej\x8d\x89\x006\x83\x9c-\x9bP\x90\xe6\xcf\xc9\x89\xfe\xff\x00\x10\x19\x90\xd8\xd7(\xff\x00\xc7\xd2\xf0\xbe\xa2\xad \x9d\xc9\x17;\xc2\xd9\x95D\xb3\x9b6\x904\xfa\x98S\x07L\xab}\xc8\x1b\x01\xf5\x8aWW\xc3HV\xa9\x86 fF\x00t\xfa\xb7\xfe\xfc\xe2\xa3P\xf0:\x12TX9\'ax{\x86\xf6p\x92\x0c\xe2@\xe0\x08\xf9\xfd\xa1[H"5\xce\xbc\x17&\x8dd\x15\x11\x94\x06{^\xfc\xa3K#\r\x94\x85\x05&Xp\xecH{\x8e#G\xe7\x04N\x96\n\x14B\x00*!\xcf\xf1\x0b\x98\xb6d\xe9\xf0\xf9\x8aX\n $\xefof\x89\xcf\xc1\x94\x89\x8cT\n\x1f]\xe1\xe8\xa7d\x8d<\xb5\x89NV\x7f\x85 \xb1\xb8\xe9\x1b&\x1b\xfa\x06)\xe5\xa6`\x01\x86\x85\x84\x0b\x8d\xca%i\xd9\xf7\xf3\x86\x8b\xa5\x1f\xfd\x8c\xc4\xd8\xeeD\x15.R\x14\x90M\xf2\xb9\x06\n\x12}\xd8\x82j\x9c\x19g\xe1\xb3\x1e\x04o\x05\xc8A\x0c7\x7f\xa4UQ\x94\x11\xcd\xcc_p\x87{\xa8\xb0<\x04k&\xd3&\xe1\xbcO\xa9h\xd4aj\x96e\x89G\xf5\xa0\xa4\xf2;F9\x8f\x937\xf3\rd\xadc O#\xce\x12\x8bAP4\xd9\tD\xc2\x0b\x82,^<X\x0f\xa8-\x06\xe2)\xcc\xb7?\x11\xe3\xbc\r\xfe\x19\xe0_\x8e\xd1\x8d(\xec\xb6Z\x82\x03\xb9\xe9\x17!9\x80)>QT\xa9;]\x83\x00vx:\x9a\x94 \x94\xa8\xb01\x80\x91\x01\'+\rF\xb7\x86\xb4\xebJ\xd9\xd3\xcbV\xbc_*\x9d+\xd8x\x06\xb0\x04\x95\xf8\xb3\x16)\xbe\x90\x03T\x11?\n\x01\xf5\x05\xf5\x1a@\x82\x8a|\xb69NRlD\x1c\'\xa9B\xce\xdf(\xf2n3\xdc\xe5\x96N\xba\x87p \xe8\xda\xa2\xda"\xb0K\xe8\xdb\xc4\xa6\xca\x0cJ\x89<\x86\x9eF#C3\xbeQ\x00\x80\x03\x92\\\x00:\xbc\t^\xb4\xe7\xb0U\x83\\\xeb\xd0p\x80\xc5\xbbG\x19\xada%-\xcc9\xf31\xd1\xec\xa5K\x00\x02K\xf2\x8e\x80\nf.\xa6\xaad\xd2\x9c\xc4|6\'\xf6\x8e<\xecc\xcay\xfe\x03-D1\x19\x87#\xb1\xf3\x16\x82\xa9\xf0\xe5,\x89rS\x99L\x1c\x9d\x00/\xa8\xfe\xeb\x12\xa8\xc0U.r%\x90<A\xf3\x13\xe1`nGF\x8avZ\xbd\x0b\xec\xfd0R\xfb\xe4\x82\xccE\xf4{\x1b\x1f\xee\xb0}L\xd0\xa2\xf9\x83\x1fo\xa4um\\\xa9\x00I\x96\x90BFf\xe2Kj\xf6.\x0b\xf1\xb0\x85\xf3qt\xdc\xb0r|\x9bkE\x11\xb4\x16g\xa1\x00\xd8\xdf~\x9f\xde0\xae\xae\xb0\x96p\xc2\xfa\x9f\xe9\x81j\xb1A\xb3<(\xaa\xaa}\xe0\xd8\x1d\x05\xd5W\x13\xc3\x9bB\xf9\xb5m\xa6\xf0,\xc5\x9d\xe2\t\xbcf\x00\x95N\x88\x99\xb1A\x8bi\xe4)j\x08BJ\x94l\x00\xb90\x0cy\x9a\x1cax\x04\xe9\xa3>\\\xa8\xfd\xc7~\x83x\xd1\xe0}\x912\xbcs\xd0\n\xac\xc1\xc1Jy\x9f\xdc}\xa3L\xb5\xdbb\x19\x8d\xb8hbr\x9dt6&r\x87\x0bD\xb0B\x01* m\xf5"\xd0o\xf8\xcc\xc9R\x92\x0b\xb8b\xe7\xabm\rf,\xbb\x11{]\xc1\x00q\x11t\x8a\x10H$\xe5+{\xfe\xee\x17\x89[`qb$\xaf!\xd1\xc6\xea\xe7\x16\xe6\x19\x9c\x00\xcd\xe2\x86U\x98b\x10\xd2\xf3:\x8d\xcb\x9d\x03\xea\xd0\x0f\xf8i\xcaH\xcd\x94\x16\r\xbc\x07h\x93\x8c\xba\x04\x9bN\x14|)f;}\xa0\x8aywJf%\x82\x8b;1<\xa2t4\xc1y\x80VEm{\x98\xb6J2,\x15\xe5;*\xfb\xf2\x8dld\x9f\xa0\xb30\xd5\x99\x84\xa7D\x86\xda\xfc\xdbx\xf0\xca\x12\xe5(\x90\xea\xcc[\xa6\xa5\xc45_v\xce\x80\xbd\t\x0c\xf6>P\xadr\x94\xa5\x8c\xab\xccZ\xefn\xa2\xf0\xe9\xb1\xe5\x1aB)\xc5\x0b.\xafox\xbdXyYK\x1f\r\x9b\xf9\xe1\x0e\x97\x81\xa4\\h5}\xb9A\t\xa6\xc8\x1bB\x08) [\xa1\x8d\x90\xb5ob\xf9}\x9fQr\x1dDh\x91\xa7\xacO\xfdL\xd4\\\xa4>\xecn=!\xac\xd5,\xab)\x9a\xa4\x0bffk\xf01<?\x08D\xa5\xe6\xefT\xb0\xfb\x9b\xfao\x196\xca\xd4E\xb3h\x98:\x95\x9f\x80vna\xe2\x85\xca*\x1a\x10?\xb71\xad\xa9\xa6\x96u\xcb\xc5\xf40%F\x1a\x9dB\xcaz\xdcB\xb6\x07\x16\xcc\xf5V\x1d\x91L\x1dA\x85\xda\xd1T\xb4\xa9[ihu?\x0fU\xd0&\x95\rK\x0fNf#"\x90\x82\x08u8\x0c\x90\x93\xaf24\x82#\x83(\xa7IJ5\xbe\x84_H\x9c\xb5\xa1,\x01c\xc0\x80<\xef\x133\x96\x95\xe4P\xee\xce\xba\x9b\xf9\x88i\xfe\xb13\x91\x99*%@ht=8B\xb0\xa86f\xe9\xc2\xc2\xad\xf0\xdc\x9e\'\x98\xe3\x15\xd5Pw\xd3?,8\x179\xacCp\x82\xa6\xf7\xa89\no\xb1"\xc0}a\xbfgi\x94\xa5\xb2\xcaBR\n\x94G\xb0\x80\xaf\xc1TX4\xfa4\xc8\x97.P\xf8\x94\xebY\xe8-\xf3\x81\xb1b\xd4\xf2\xe6\x0b)\'"\xad\xae\xe9\'\xca\'\xdaz\xc7\x9c\x19\xd8\xa4\x01\xe6L\x11:Jf\xd3\x80\x14\xc9`I#t\x12.9\x82!\xd7[\x15G\xf2t,\xa7IRB\x80\x00\x18\xe8>\x96H\xca\x19h\x03\x83GB\xdb\rK\xe1\x8aT\xe2\x95\xe6\x94\xb5\x050\x0b\x1a?\xf1\x05\xd4UN\xa8\xca\xa2\xa0\x9c\x89\xcb`\x08Q\xb7\xa6\x91\xd1\xd1Z\xa6^\xdbB\xea\xe9J\x9e\x8c\xc1\xb3\x86 \xe8\xf6\x01\x8f\xa4g\xe7)I7/\xb1\xea5\x8e\x8e\x8a\x92!6\xa8\x1d\xcf\xa4Q\xdeG\xb1\xd1\x80D\x18\xe1\x1d\x1d\x18\xc4\xe5\xa0\x92\x00\xd4\xda6xN\x056\x99d\x99\x85\n`\x1d9H6r/p#\xa3\xa1d\xc7\x8a4\xd4\xd3\xa6\x95e\x98\xa0X8\x00|\xc9\xe4bS\xa6\xa9>&\xe0\xed\xa7\xa4y\x1d\x13\x1f\xc3\xcc\xd9\x92TP\xc4hA\xbb?X\x86-\x8b(\x81\x94\x00\xa4\x17\xe5m6\x8fc\xa0\x01\xbaEs\xbbENBV\xd9\x97\xff\x00[\x8eY\x8e\xd1m:\x9c0pM\xc8\x1bGGC4f\xec.E\x11)Q\xfd\xbb\xbb\x1e\xa0\x88\xf2t\x94\x91\xe2\x1a\x07.\xc5\xfd#\xc8\xe8V\xa8\xd4AH\xfc\xb0\x12\xa2\x03\x8d\xcb\xb7\x00b\xb9t\xdc\x9f\x85\xd8\xc7\x91\xd0\x06I\x0c\xe9\xab\xc8GrP\xef\xaa\x8a\x9c\xf9D\x94\x13\xf0\xabt\xe8\xdc9\xc7G@3VV\xac<,\xe7J\x98j\xc4;\xb4Nk\xcb\xca\xc4s\xb6\x9e\x91\xd1\xd0|\x16I#\xa7L[$\xa2\xfc\xce\xdeF\x08\x97X_*\xf2\xae\xda\xe8|\xf6\x8e\x8e\x822#\x9dJ\x99\xe09\x02u-s\xe7\xb4MBiS%dY\x9c(\xa6\xe3\x90\r\x1d\x1d\x04\x00\x15r\xa6\xa9@\xa9N\xe5\xb6\x85\xb5US\xa4\xac\x04\x92\x97w\xf18\xeb\x1e\xc7B4NZ\xd9M>)5d\x89\x84)\xcf\xca\x0b\x9f]\x92Q\x94-\x9c\xf8\x88\xe0\r\x84y\x1d\x19\x10\xceB\xcc^a\xce\xe2\xcc\x94\xb6\xfa\'\xf9\x82\xf0\x8a\x82e)7s\x9a\xef\xa3\xa5\xf4\xea\x91\x1d\x1d\x07\xc1\xe3\xd8\xaa]B\xdbX\xf6::\x08\x0f\xff\xd9'


def decoding(data):
    try:
        #en = np.frombuffer(data, dtype=np.uint8)  # int
        img = cv2.imdecode(data, cv2.IMREAD_COLOR)
        img = cv2.resize(img, (86, 54))

        test = []
        numpy_image = img
        test.append(numpy_image / 255.)

        test = np.array(test)
    except Exception as e:
        print(str(e))

    return test


# data = binary 형태의 이미지
def security_check(data, models):
    x_test = decoding(data)

    for model in models:
        result = model.predict(x_test)

        for i in result:
            if i > 0.5:
                return True  # 한 개라도 걸리면
    return False

class RegistUser(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()

            parser.add_argument('image', type=int, action='append')
            args = parser.parse_args()

            image = args['image']
            image = np.array(image)

            result = security_check(image, models)

            return {'result': result}

        except Exception as e:
            return {'error' : str(e)}


api.add_resource(RegistUser, '/user')

if __name__ == '__main__':
    app.run(debug=True)