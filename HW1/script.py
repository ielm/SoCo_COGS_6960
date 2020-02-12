"""
Ivan Leon
Social Computing Homework 1
"""
import nltk
import itertools
import csv
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

def make_table(fname: str, m_list: list, f_list: list):
    zipped = list(itertools.zip_longest(m_list, f_list))

    def _build_row(_row, debug: bool = False):
        return [f"{_row[0][0]}" if _row[0] is not None else "..", 
                f"{_row[0][1]}" if _row[0] is not None else "..", 
                f"{_row[1][0]}" if _row[1] is not None else "..", 
                f"{_row[1][1]}" if _row[1] is not None else ".."]

    # write csv file 
    with open(f"{fname.strip('.txt')}_table.csv", "w") as file:
        table = csv.writer(file)
        for row in zipped:
            table.writerow(_build_row(row))
    
    # print number of pronouns by person 
    print("\nNumber of Pronouns by Person:")
    print(f"F: {list(map(lambda p: p[1], f_list))}")
    print(f"M: {list(map(lambda p: p[1], m_list))}")


def main(filename):
    with open(filename) as f:
        content = f.readlines()

    people = {}

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

    prp_by_gender = {
        "F": 0,
        "M": 0
    }

    num_of_gender = {
        "F": 0,
        "M": 0
    }

    f = []
    m = []
    f_index = 0
    m_index = 0

    # update number of prp and number of gender 
    for person in people.keys():
        if people[person]["gender"] == "F":
            prp_by_gender["F"] += people[person]["number_of_prp"]
            num_of_gender["F"] += 1
            f_index += 1
            f.append((f"Female {f_index}", people[person]["number_of_prp"]))
        elif people[person]["gender"] == "M":
            prp_by_gender["M"] += people[person]["number_of_prp"]
            num_of_gender["M"] += 1
            m_index += 1
            m.append((f"Male {m_index}", people[person]["number_of_prp"]))

    # print averages
    print(f"Total Number of Pronouns for Females and Males:\n{prp_by_gender}")
    print(f"\nNumber of Females and Males:\n{num_of_gender}")
    print(f"\nAverage Number of Pronouns by Females:\n{prp_by_gender['F']/num_of_gender['F']}")
    print(f"\nAverage Number of Pronouns by Males:\n{prp_by_gender['M']/num_of_gender['M']}")
    make_table(filename, m, f)


if __name__ == '__main__':
    print(f"Output for Group A\n{'-' * 20}")
    main("Feb17_GroupA.txt")
    print(f"\n\nOutput for Group B\n{'-' * 20}")
    main("Feb17_GroupB.txt")


