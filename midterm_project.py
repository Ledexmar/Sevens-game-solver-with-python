import pyautogui
import time

pyautogui.FAILSAFE = True
card_order = {'s': {'As.png': 1, '2s.png': 2, '3s.png': 3, '4s.png': 4, '5s.png': 5, '6s.png': 6, '7s.png': 7, '8s.png': 8, '9s.png': 9, '10s.png': 10, 'Js.png': 11, 'Qs.png': 12, 'Ks.png': 13},
              'h': {'Ah.png': 1, '2h.png': 2, '3h.png': 3, '4h.png': 4, '5h.png': 5, '6h.png': 6, '7h.png': 7, '8h.png': 8, '9h.png': 9, '10h.png': 10, 'Jh.png': 11, 'Qh.png': 12, 'Kh.png': 13},

              'd': {'Ad.png': 1, '2d.png': 2, '3d.png': 3, '4d.png': 4, '5d.png': 5, '6d.png': 6, '7d.png': 7, '8d.png': 8, '9d.png': 9, '10d.png': 10, 'Jd.png': 11, 'Qd.png': 12, 'Kd.png': 13},
              'c': {'Ac.png': 1, '2c.png': 2, '3c.png': 3, '4c.png': 4, '5c.png': 5, '6c.png': 6, '7c.png': 7, '8c.png': 8, '9c.png': 9, '10c.png': 10, 'Jc.png': 11, 'Qc.png': 12, 'Kc.png': 13}}


# all the possible cards
stored_cards = ['2h.png', '2d.png', '2c.png', '2s.png', '3h.png', '3d.png', '3c.png', '3s.png', '4h.png', '4d.png', '4c.png', '4s.png', '5h.png', '5d.png', '5c.png', '5s.png', '6h.png', '6d.png', '6c.png', '6s.png', '7h.png', '7d.png', '7c.png', '7s.png', '8h.png', '8d.png', '8c.png', '8s.png', '9h.png', '9d.png', '9c.png', '9s.png', '10h.png', '10d.png', '10c.png', '10s.png', 'Jh.png', 'Jd.png', 'Jc.png', 'Js.png', 'Qh.png', 'Qd.png', 'Qc.png', 'Qs.png', 'Kh.png', 'Kd.png', 'Kc.png', 'Ks.png', 'Ah.png', 'Ad.png', 'Ac.png', 'As.png']
index = 0

OK_button = 'OK.png'
hand_reference_img = 'hand_reference_card.png'
handzone_reference = []

c_in_hand = []
d_in_hand = []
h_in_hand = []
s_in_hand = []
# clickable = []
options = []


def get_card_value(card):
    if len(card) == 6:
        suit = card[1]
        return card_order[suit][card]
    if len(card) == 7:
        suit = card[2]
        return card_order[suit][card]

def find_min_card(cards):
    if not cards:
        return None
    return min(cards, key=lambda card: get_card_value(card))


def is_my_turn(): ####### check for the card next to the bottom right covered one, if it is my turn
    locations = pyautogui.locateAllOnScreen(hand_reference_img, confidence=0.97)
    my_faceDown = None
    # Iterate through the locations and select the one with the lowest top value
    for location in locations:
        if my_faceDown is None or location.top > my_faceDown.top:
            my_faceDown = location
    target_x = my_faceDown.left
    target_y = my_faceDown.top
    time.sleep(0.05)
    loc = pyautogui.position(target_x - 45, target_y)
    color = pyautogui.screenshot().getpixel(loc)
    #the color is not allways (255,255,255) when my turn
    tolerance = 10
    return all(abs(channel - 255) <= tolerance for channel in color)


def see_card(place):
    global index
    hand_cards = {card: pyautogui.locateOnScreen(card, confidence=0.97, region= place) is not None for card in
                  stored_cards}
    found_cards = []

    for key, value in hand_cards.items():
        if value:
            found_cards.append(key)

    if found_cards:
        return found_cards

    return None


# zones for cards
tableZone = (667, 491, 1616, 668)
handzone = (705, 1100, 1535, 446)


# suits in table
c_in_table = []
d_in_table = []
h_in_table = []
s_in_table = []
cards_in_table = []
# to distribute cards in hand
c_suit = []
d_suit = []
h_suit = []
s_suit = []
# playable_cards = []

my_cards = []  # see_card(handzone)


def update_cards(card_list, clubs_list, diamonds_list, h_list, s_list):
    clubs_list.clear()
    diamonds_list.clear()
    h_list.clear()
    s_list.clear()

    for card in card_list:
        if 'c' in card:
            clubs_list.append(card)
        elif 'd' in card:
            diamonds_list.append(card)
        elif 'h' in card:
            h_list.append(card)
        elif 's' in card:
            s_list.append(card)


def playable_cards(clubs_in_tab, clubs_in_h, diamonds_in_tab, diamonds_in_h, hearts_in_tab, hearts_in_h, s_in_tab, s_in_h):
    clickable = []
    values = []
    card3 = []
    if not clubs_in_tab and not diamonds_in_tab and not hearts_in_tab and not s_in_tab:
        for card in my_cards:
            if card[0] == '7':
                card3.append(card)
                return card3
        return find_min_card(my_cards)


    for card1 in clubs_in_tab:
        for card2 in clubs_in_h:
            if (card_order['c'][card2] - 1) == card_order['c'][card1] or (card_order['c'][card2] + 1) == card_order['c'][card1]:
                clickable.append(card2)
    if '7c.png' in clubs_in_h and '7c.png' not in clickable:
        clickable.append('7c.png')
    for card1 in diamonds_in_tab:
        for card2 in diamonds_in_h:
            if (card_order['d'][card2] - 1) == card_order['d'][card1] or (card_order['d'][card2] + 1) == card_order['d'][card1]:
                clickable.append(card2)
    if '7d.png' in diamonds_in_h and '7d.png' not in clickable:
        clickable.append('7d.png')
    for card1 in hearts_in_tab:
        for card2 in hearts_in_h:
            if (card_order['h'][card2] - 1) == card_order['h'][card1] or (card_order['h'][card2] + 1) == card_order['h'][card1]:
                clickable.append(card2)
    if '7h.png' in hearts_in_h and '7h.png' not in clickable:
        clickable.append('7h.png')
    for card1 in s_in_tab:
        for card2 in s_in_h:
            if (card_order['s'][card2] - 1) == card_order['s'][card1] or (card_order['s'][card2] + 1) == card_order['s'][card1]:
                clickable.append(card2)
    if '7s.png' in s_in_h and '7s.png' not in clickable:
        clickable.append('7s.png')
    return clickable

def AI(options):
    values =[]
    if len(options) > 0:
        if len(options) > 1:
            return find_min_card(options)
        print('options of AI:', options)
        return options[0]
    if not options:
        values = []
        min_value = float('inf')
        no_options = see_card(handzone)
        if no_options:
            return find_min_card(no_options)
        return None

def click(ai_decision,zone):
    AI_location = pyautogui.locateOnScreen(ai_decision, confidence=0.97, region=zone)
    pyautogui.moveTo(AI_location)
    center = pyautogui.center(AI_location)
    pyautogui.click(center)

my_cards = see_card(handzone)
print(my_cards)

while not pyautogui.locateOnScreen(OK_button, confidence=0.96):
    while not is_my_turn():
        time.sleep(0.1)
    if is_my_turn():
        if not my_cards:
            my_cards = see_card(handzone)
            update_cards(my_cards, c_in_hand, d_in_hand, h_in_hand, s_in_hand)

        if len(my_cards) == 1:
            time.sleep(2)
            click(my_cards[0], handzone)
            time.sleep(3)
            if pyautogui.locateOnScreen(OK_button, confidence=0.96):
                ok_zone = pyautogui.locateOnScreen(OK_button, confidence=0.96)
                click(OK_button, ok_zone)
                break
        elif my_cards:
            update_cards(my_cards, c_in_hand, d_in_hand, h_in_hand, s_in_hand)
            cards_in_table = see_card(tableZone)
            if cards_in_table:
                update_cards(cards_in_table, c_in_table, d_in_table, h_in_table, s_in_table)

            options = playable_cards(c_in_table, c_in_hand, d_in_table, d_in_hand, h_in_table, h_in_hand,
                                      s_in_table, s_in_hand)
            print('options:', options)
            AI_decision = AI(options)

            if AI_decision:
                my_cards.remove(AI_decision)
                click(AI_decision, handzone)

        pyautogui.moveTo(1610, 1040)



