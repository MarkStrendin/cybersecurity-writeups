import requests, time

url = "http://159.65.94.38:30178"

found_flag = False
count = 0
while found_flag == False:
    response = requests.get(url + "/flag")
    potential_flag = response.text.replace('\n','')
    found_flag = potential_flag.startswith("HTB{")
    count = count + 1
    print(count,": ", potential_flag)

print("FLAG FOUND")
print(potential_flag)
