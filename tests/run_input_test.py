import os

if __name__ == '__main__':
    parameters = [
        ("test_card_moove_forward", "tests/scenarios/answers_cards_moove_forward.txt"),
        ("test_card_moove_backwards", "tests/scenarios/answers_community_moove_backwards.txt"),
        ("test_onAStreetOrStation", "tests/scenarios/answers_onAStreet.txt"),
        ("test_jail_chooseToPay", "tests/scenarios/answers_jail_chooseToPay.txt"),
        ("test_actualizePositionAux", "tests/scenarios/answers_actualizePosition.txt"),
        ("test_jail_chooseDouble", "tests/scenarios/answers_jail_chooseDouble.txt"),
        ("test_putHomes", "tests/scenarios/answers_putHomes.txt"),
        ("test_isInJail", "tests/scenarios/answers_isInJail.txt"),
        ("test_card_community_or_chance", "tests/scenarios/answers_community_or_chance.txt"),
        ("test_card_backwards", "tests/scenarios/answers_card_backwards.txt")
    ]
    for (test_name, scenario_path) in parameters:
        req = "python tests/input_test.py {} < {}".format(test_name, scenario_path)
        print(req)
        # os.system(req)

