"""
Ivan Leon
Social Computing Homework 1

"""
import nltk
import re


males = ["luke", "ted", "david", "matthew", "jake", "rick", "josh", "tony", "aaron", "michael", "nick", "george", "john"]

females = ["judith", "tia", "meg", "vicky", "eva", "julie", "rita", "leah", "caroline", "cintihia", "ariel", "macy", "lynn", "rebecca", "cinthia", "mara", "amy", "michelle", "melany"]


def parse_turn(turn):
    # find name, time, and message for each line
    _time = re.findall(r"\(.*?\)", turn)[0].strip("()")
    _turn = re.sub(r"\(.*?\)", "", turn)
    _line = _turn.split(":", maxsplit=1)
    _name = _line[0].strip()
    _message = _line[1].strip()

    _num = get_num_pronouns(_message)

    return _time, _name, _message, _num


def get_num_pronouns(message):
    tokens = nltk.word_tokenize(message)
    pos = nltk.pos_tag(tokens)

    num = 0

    for part in pos:
        if part[1] == "PRP":
            num += 1

    return num


if __name__ == '__main__':

    with open("Feb17_GroupB.txt") as f:
        content = f.readlines()

    i = 0

    people = {}
    messages = []

    # find name, time, and message for each line
    for l in content:
        time, name, message, number = parse_turn(l)

        # add a new person to people
        if name not in people.keys():
            people[name] = {}
            people[name]["name"] = name
            if name in males:
                people[name]["gender"] = "M"
            elif name in females:
                people[name]["gender"] = "F"
            else:
                people[name]["gender"] = "X"
            people[name]["number_of_prp"] = number
        elif name in people.keys():
            people[name]["number_of_prp"] += number

        # add message to list of messages
        messages.append(
            {
                "person": name,
                "time": time,
                "index": i,
                "message": message,
                "num": number
            }
        )

        i += 1

    print(people)

    p_by_gender = {
        "F": 0,
        "M": 0
    }

    num_of_gender = {
        "F": 0,
        "M": 0
    }

    for person in people.keys():
        if people[person]["gender"] == "F":
            p_by_gender["F"] += people[person]["number_of_prp"]
            num_of_gender["F"] += 1
        elif people[person]["gender"] == "M":
            p_by_gender["M"] += people[person]["number_of_prp"]
            num_of_gender["M"] += 1

    print()
    print(p_by_gender)

    print()
    print(num_of_gender)

    print()
    print(f"avg female prp: {p_by_gender['F']/num_of_gender['F']}")
    print(f"avg male prp: {p_by_gender['M']/num_of_gender['M']}")

