import time
import requests

dweetIO = "https://dweet.io/dweet/for/"		# common url for all users (post)
myThing = "Gonzalo_Raspi_9909"

n = 15			# starting counter
temp = 50		# init temp
humidity = 10	# init humidity

while n > 0:
	rqsString = dweetIO+myThing+'?'+'temperature='+str(temp)+'&'+'humidity='+str(humidity)
	print(rqsString)					# url for post
	rqs = requests.post(rqsString)		# posting
	print(rqs.status_code)				# printing response status
	print(rqs.headers)					# print response headers
	print(rqs.content)					# print response content
	time.sleep(5)						# 5 seconds pause
	temp += 1.5
	humidity += 10
	n -= 1
