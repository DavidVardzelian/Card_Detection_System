card_ids = {
    "HA": 0,   "H2": 1,   "H3": 2,   "H4": 3,   "H5": 4,   "H6": 5,   "H7": 6,   "H8": 7,   "H9": 8,   "H10": 9,
    "HJ": 10,  "HQ": 11,  "HK": 12,

    "CA": 13,  "C2": 14,  "C3": 15,  "C4": 16,  "C5": 17,  "C6": 18,  "C7": 19,  "C8": 20,  "C9": 21,  "C10": 22,
    "CJ": 23,  "CQ": 24,  "CK": 25,

    "DA": 26,  "D2": 27,  "D3": 28,  "D4": 29,  "D5": 30,  "D6": 31,  "D7": 32,  "D8": 33,  "D9": 34,  "D10": 35,
    "DJ": 36,  "DQ": 37,  "DK": 38,

    "SA": 39,  "S2": 40,  "S3": 41,  "S4": 42,  "S5": 43,  "S6": 44,  "S7": 45,  "S8": 46,  "S9": 47,  "S10": 48,
    "SJ": 49,  "SQ": 50,  "SK": 51,
}

class_ids = {
    0: "10 of Club", 1: "10 of Diamond", 2: "10 of Heart", 3: "10 of Spade",
    4: "2 of Club", 5: "2 of Diamond", 6: "2 of Heart", 7: "2 of Spade",
    8: "3 of Club", 9: "3 of Diamond", 10: "3 of Heart", 11: "3 of Spade",
    12: "4 of Club", 13: "4 of Diamond", 14: "4 of Heart", 15: "4 of Spade",
    16: "5 of Club", 17: "5 of Diamond", 18: "5 of Heart", 19: "5 of Spade",
    20: "6 of Club", 21: "6 of Diamond", 22: "6 of Heart", 23: "6 of Spade",
    24: "7 of Club", 25: "7 of Diamond", 26: "7 of Heart", 27: "7 of Spade",
    28: "8 of Club", 29: "8 of Diamond", 30: "8 of Heart", 31: "8 of Spade",
    32: "9 of Club", 33: "9 of Diamond", 34: "9 of Heart", 35: "9 of Spade",
    36: "A of Club", 37: "A of Diamond", 38: "A of Heart", 39: "A of Spade",
    40: "J of Club", 41: "J of Diamond", 42: "J of Heart", 43: "J of Spade",
    44: "K of Club", 45: "K of Diamond", 46: "K of Heart", 47: "K of Spade",
    48: "Q of Club", 49: "Q of Diamond", 50: "Q of Heart", 51: "Q of Spade"
}
def get_card_name(class_id):
    return class_ids.get(class_id, "Unknown Card")

def convert_class_id_to_target_id(class_id: int) -> int:
    card_desc = class_ids.get(class_id)
    if card_desc is None:
        raise ValueError(f"Invalid class id: {class_id}")
    
    try:
        rank, suit = card_desc.split(" of ")
    except ValueError:
        raise ValueError(f"Invalid card description format: {card_desc}")
    
    suit_map = {
        "Club": "C",
        "Diamond": "D",
        "Heart": "H",
        "Spade": "S"
    }
    
    suit_abbr = suit_map.get(suit)
    if suit_abbr is None:
        raise ValueError(f"Unknown suit: {suit}")
    
    key = suit_abbr + rank
    
    try:
        return card_ids[key]
    except KeyError:
        raise ValueError(f"No target id found for key: {key}")
    
def get_barcode_from_card_id(card_id: int) -> int:
    target_id = convert_class_id_to_target_id(card_id)
    return (1000000 + target_id) * 10


