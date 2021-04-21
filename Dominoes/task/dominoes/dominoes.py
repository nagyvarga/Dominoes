import random


COMPUTER_STATUS = "Computer is about to make a move. Press Enter to continue..."
PLAYER_STATUS = "It's your turn to make a move. Enter your command."
acceptable_input = list("+-0123456789")
remained_step_player = True
remained_step_computer = True


def player_input(max_pieces_of_set):
    number_of_decision = 0
    while True:
        invalid_input_status = True
        decision = input(">>>")
        length_of_decision = len(decision)

        if length_of_decision == 1:
            if decision[0] in acceptable_input[2:]:
                number_of_decision = int(decision)
                invalid_input_status = False

        if length_of_decision == 2:
            if decision[0] in acceptable_input[:2] and decision[1] in acceptable_input[3:]:
                number_of_decision = int(decision)
                invalid_input_status = False
            if decision[0] in acceptable_input[3:] and decision[1] in acceptable_input[2:]:
                number_of_decision = int(decision)
                invalid_input_status = False

        if length_of_decision == 3:
            if decision[0] in acceptable_input[:2] and decision[1] in acceptable_input[3:] \
                    and decision[2] in acceptable_input[2:]:
                number_of_decision = int(decision)
                invalid_input_status = False

        if not invalid_input_status and -max_pieces_of_set <= number_of_decision <= max_pieces_of_set:
            return number_of_decision
        else:
            invalid_input_status = True

        if invalid_input_status:
            print("Invalid input. Please try again.")


def get_domino_snake():
    puffer = ""
    if len(domino_snake) <= 6:
        for domino_snake_item in domino_snake:
            puffer += str(domino_snake_item)
    else:
        for domino_snake_item in domino_snake[:3]:
            puffer += str(domino_snake_item)
        puffer += "..."
        for domino_snake_item in domino_snake[-3:]:
            puffer += str(domino_snake_item)
    return puffer


def match_to_neighbor(which_number_in_set):
    global domino_snake
    global remained_step_player
    global remained_step_computer

    if which_number_in_set > 0:
        number_of_neighbour_piece = domino_snake[-1][1]
    else:
        number_of_neighbour_piece = domino_snake[0][0]
    if player_next:
        if player_set[abs(which_number_in_set) - 1][0] == number_of_neighbour_piece or \
                player_set[abs(which_number_in_set) - 1][1] == number_of_neighbour_piece:
            remained_step_player = True
            remained_step_computer = True
            return True
    else:
        if computer_set[abs(which_number_in_set) - 1][0] == number_of_neighbour_piece or \
                computer_set[abs(which_number_in_set) - 1][1] == number_of_neighbour_piece:
            remained_step_player = True
            remained_step_computer = True
            return True
    return False


# Set the starting pieces
while True:
    full_domino_set = list([i, m] for i in range(7) for m in range(i, 7))
    random.shuffle(full_domino_set)
    player_set = full_domino_set[:7]
    computer_set = full_domino_set[7:14]
    stock_pieces = full_domino_set[14:]
    domino_snake = list()

    player_next = False
    computer_next = False

    for j in range(6, -1, -1):
        if [j, j] in player_set:
            domino_snake.append(player_set.pop(player_set.index([j, j])))
            computer_next = True
            break
        elif [j, j] in computer_set:
            domino_snake.append(computer_set.pop(computer_set.index([j, j])))
            player_next = True
            break

    if player_next or computer_next:
        break

# Start the domino game
while True:
    count_numbers_for_ai = {i: 0 for i in range(7)}
    print("=" * 70)
    print(f"Stock size: {len(stock_pieces)}")
    print(f"Computer pieces: {len(computer_set)}\n")

    # Domino snake print
    print(get_domino_snake())

    print("\nYour pieces:")
    i = 0
    for player_piece in player_set:
        i += 1
        print(f"{i}:{player_piece}")

    if not remained_step_player and not remained_step_computer:
        print("\nStatus: The game is over. It's a draw!")
        break

    # Player turn
    if player_next:
        if len(computer_set) > 0:
            print(f"\nStatus: {PLAYER_STATUS}")
            while True:
                decision_of_player = player_input(len(player_set))
                if decision_of_player == 0:
                    if len(stock_pieces) > 0:
                        player_set.append(stock_pieces.pop(random.randint(1, len(stock_pieces)) - 1))
                    else:
                        remained_step_player = False
                    break
                else:
                    if match_to_neighbor(decision_of_player):
                        break
                    else:
                        print("Illegal move. Please try again.")

            if decision_of_player > 0:
                chosen_piece = player_set.pop(decision_of_player - 1)
                if chosen_piece[0] != domino_snake[-1][1]:
                    chosen_piece = chosen_piece[::-1]
                domino_snake.append(chosen_piece)
            elif decision_of_player < 0:
                chosen_piece = player_set.pop(abs(decision_of_player) - 1)
                if chosen_piece[1] != domino_snake[0][0]:
                    chosen_piece = chosen_piece[::-1]
                domino_snake.insert(0, chosen_piece)
            player_next = False
        else:
            print("\nStatus: The game is over. The computer won!")
            break
    else:  # Computer turn
        if len(player_set) > 0:
            print(f"\nStatus: {COMPUTER_STATUS}")
            input()

            # Count for AI
            for i in range(7):
                for k in range(2):
                    for domino_snake_piece in domino_snake:
                        if domino_snake_piece[k] == i:
                            count_numbers_for_ai[i] += 1
                    for computer_set_piece in computer_set:
                        if computer_set_piece[k] == i:
                            count_numbers_for_ai[i] += 1

            # Scores for AI
            computer_set_scores = dict()

            for computer_set_piece in computer_set:
                sum_of_piece_items = sum(computer_set_piece)
                if sum_of_piece_items not in computer_set_scores:
                    computer_set_scores[sum_of_piece_items] = [computer_set_piece]
                else:
                    computer_set_scores[sum_of_piece_items] += [computer_set_piece]

            while True:
                # AI algorithm – from largest score to lowers
                if len(computer_set_scores) != 0:
                    highest_score = max(computer_set_scores)
                    decision_of_computer_value = computer_set_scores[highest_score].pop(0)
                    decision_of_computer = computer_set.index(decision_of_computer_value) + 1
                    if len(computer_set_scores[highest_score]) == 0:
                        computer_set_scores.pop(highest_score)
                else:
                    decision_of_computer = 0

                if decision_of_computer == 0:
                    if len(stock_pieces) > 0:
                        computer_set.append(stock_pieces.pop(random.randint(1, len(stock_pieces)) - 1))
                    else:
                        remained_step_computer = False
                    break
                else:
                    # Check the right side of domino snake
                    if match_to_neighbor(decision_of_computer):
                        break
                    # Check the left side of domino snake
                    decision_of_computer *= -1
                    if match_to_neighbor(decision_of_computer):
                        break

            # Use the piece of domino, remove from the computer set and correct orientation
            if decision_of_computer > 0:
                chosen_piece = computer_set.pop(decision_of_computer - 1)
                if chosen_piece[0] != domino_snake[-1][1]:
                    chosen_piece = chosen_piece[::-1]
                domino_snake.append(chosen_piece)
            elif decision_of_computer < 0:
                chosen_piece = computer_set.pop(abs(decision_of_computer) - 1)
                if chosen_piece[1] != domino_snake[0][0]:
                    chosen_piece = chosen_piece[::-1]
                domino_snake.insert(0, chosen_piece)
        else:
            print("\nStatus: The game is over. You won!")
            break
        player_next = True
