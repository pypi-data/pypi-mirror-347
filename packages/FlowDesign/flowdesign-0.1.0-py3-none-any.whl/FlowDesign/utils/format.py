import re, json

def extract_dict(s):
    pattern = r'(\[\s*\{.*?\}\s*\]|\{.*?\})'
    matches = re.findall(pattern, s, re.DOTALL)
    if matches:
        return json.loads(matches[-1])
    return None
    
def normalize(system: str, user: str, bot: str):
    def norm_function(input_str: str):
        o = [i for i in input_str.split(bot)[:2] if len(i.strip()) > 0][0]
        o = [i for i in o.split(user)[:2] if len(i.strip()) > 0][0]
        o = [i for i in o.split(system)[:2] if len(i.strip()) > 0][0].strip()
        return o
    return norm_function

def listofdict2dictoflist(lst):
    return {key: [d[key] for d in lst] for key in lst[0]}

def dictoflist2listofdict(d):
    return [{key: d[key][i] for key in d} for i in range(len(d[list(d.keys())[0]]))]

def list_flatten(lst):
    output = []
    for i in lst:
        if isinstance(i, list): output += list_flatten(i)
        else: output.append(i)
    return output