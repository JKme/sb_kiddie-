# http://moond4rk.com/post/get-identify-number/
from id_validator import validator

location = "123456"
birth = "19900101"
suffix = "4"
id_cards = []

def get_seq():
    for i in range(100):
        for k in range(10):
            if k % 2 == 0:
                seq = "{}{}{}{}{}".format(location, birth, i, k, suffix)
                if validator.is_valid(seq):
                    id_cards.append(seq)
    print("验证成功的身份证数为: ", len(id_cards))

if __name__ == "__main__":
    get_seq()
