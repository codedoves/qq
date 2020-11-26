import argparse
import cv2
import requests,json,base64
import numpy as np
import json
import base64
import os

def main():
	# parser = argparse.ArgumentParser(description="使用Python脚本调用limbo的http接口")
	# parser.add_argument("--ip", "-i", dest="ip", required=True, type=str, help="服务ip")
	# #parser.add_argument("--img_path", "-f", dest="img_path", required=True, type=str, help="图片路径")
	# args = parser.parse_args()
  
	url = 'http://172.21.138.196:8084/road/roadslide'
	a1=[]
	b1=[]
	for dirname, _, filenames in os.walk('H:\\kaohe\\baidu1\\'):
		for filename in filenames:
			imgpath=(os.path.join(dirname, filename))  
			

			a1.append(imgpath)
			try:
				img = cv2.imread(imgpath)
				img=cv2.flip(img,1)

				succ, data = cv2.imencode(".jpg", img)
				data = base64.b64encode(data)
				
				body111={
 
        "imageInfo":str(data,'utf-8')

				}


				

				
				
				res = requests.post(url, json=body111)
				responce=res.json()
				print(filename,responce)
				# print('1111111111111111111',responce)
				# print('222222222222222222222',responce['data']['isSlide'])
				# # data=j.get('demodResults')
				# # data=data[0]['data']
				# # data = base64.b64decode(data)  # base64解码 
				# # data=str(data,'utf-8')
				# # data=json.loads(data)
				# # label=data.get('alert')
				print(int(responce['data']['isSlide']))
				b1.append(int(responce['data']['isSlide']))
			except:

				label=0
				print(label)
				b1.append(label)

	a1=np.array(a1)
	b1=np.array(b1)
	np.save('path.npy',a1)
	np.save('label.npy',b1)
	print(1-sum(b1==0)/len(b1))
if __name__ == '__main__':
	main()

    # python3 -ip xxx.xxx.xxx.xxx -f images/input.jpg
