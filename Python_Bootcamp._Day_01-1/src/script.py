def count(f):
    def decorated(*args, **kwargs):
        print("SQUEAK")
        return f(*args, **kwargs)
    return decorated

@count
def add_ingot(purse):
    new_dict = dict(purse)
    if "gold_ingots" not in new_dict:
        new_dict["gold_ingots"] = 0
    new_dict["gold_ingots"] += 1
    return new_dict

@count
def get_ingot(purse):
    new_dict = dict(purse)
    if "gold_ingots" in new_dict and new_dict["gold_ingots"] != 0:
        new_dict["gold_ingots"] -= 1
    return new_dict

@count
def empty(purse):
    new_dict = dict()
    return new_dict

def split_booty(*args):
    purse1 = empty({})
    purse2 = empty({})
    purse3 = empty({})
    for el in args:
        mod = dict(el)
        i = 0
        while mod["gold_ingots"] > 0:
            if i == 0:
                i += 1
                purse1 = add_ingot(purse1)
            elif i == 1:
                i += 1
                purse2 = add_ingot(purse2)
            else:
                i = 0
                purse3 = add_ingot(purse3)
            mod = get_ingot(mod)
    return purse1, purse2, purse3

def main():
    if str(get_ingot({})) == '{}':
        print("OK")
    else:
        print("ERROR")
    if str(add_ingot(get_ingot(add_ingot(empty({"gold_ingots": 3}))))) == "{'gold_ingots': 1}":
        print("OK")
    else:
        print("ERROR")
    purse1, purse2, purse3 = split_booty({"gold_ingots":3}, {"gold_ingots":2})
    if purse1["gold_ingots"] == 2 and purse2["gold_ingots"] == 2 and purse3["gold_ingots"] == 1:
        print("OK")
    else:
        print("ERROR")

if __name__ == "__main__":
    main()
