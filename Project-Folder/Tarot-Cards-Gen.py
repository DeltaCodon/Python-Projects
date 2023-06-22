import random as rd
 
def row_selction(): ### ROW
    choice = 'wrong'
 
    while choice not in ['1','2','3','4','5']:
        choice = input("How many rows of cards do you want? (1-5): ")
    if choice not in ['1','2','3','4','5']:
      print("Sorry, I don't understand, please enter a valid choice... ")
 
    return int(choice)
 
def card_num_selction(row): ## for each row (rows are determiend by tiers) #### COLUMN
    choice = 'wrong'
 
    while choice not in ['1','3','5']:
        choice = input(f"Pick how many cards to pull for row {row}? (1, 3, 5): ")
    if choice not in ['1','3','5']:
      print("Sorry, I don't understand, please enter a valid choice... ")
 
    return int(choice)
 
def upright_reversed(): # this function will be called after each draw to determine if the card is upside or reversed
    card = rd.randint(1,2)
    if card == 1:
        card = str("Upright")
        return card
    else:
        card = str("Reverse")
        return card
 
def maj_or_min(): # If the card will be a Major arcana or Minor arcana card
    probi = 1
    for x in range(1, rd.randint(1,18)):
        probi=x
    if probi in range(0,12):
        return "Minor"
    elif probi in range(12,18):
        return "Major"
 
 
 
def court_or_crowd(): # determine if court or crowd
    probi = 1
    for x in range(1, rd.randint(1,18)):
        probi=x
    if probi in range(0,12):
        return "Crowd"
    elif probi in range(12,18):
        return "Court"
 
 
def suite_pull(suiteR):  # determines what the suite will get for court and crowd
    court = ["King", "Queen", "Knight", "Page"]
    crowd = ["Ace", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten"]
    if suiteR == "Crowd":
        return crowd.pop(rd.randint(0,10))
 
    elif suiteR == "Court":
        return court.pop(rd.randint(0,3))
    


 
def card_pull(cardR,suiteR): # determines if the card is a Major card or a suite
    Major = [
        "The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor", "The Hierophant", "The Lovers",
    "The Chariot", "Strength", "The Hermit", "The Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance",
    "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World"
    ]
 
    Minor = [
        'Swords', 'Cups', 'Wands', 'Pentacles'
        ]
    if cardR == "Minor":
        return suite_pull(suiteR) + " of " + Minor[rd.randint(0,3)]
    elif cardR == "Major":
        return Major.pop(rd.randint(0,21))
 


 
 
def logic():
    used_cards = []
    
    # for lack of a better word, the "factory" of the the cards being pulled.
    for _ in range(1,50):
        suiteR = court_or_crowd()
        cardR = maj_or_min()
        card_pull(cardR,suiteR)
        if card_pull(cardR,suiteR) not in used_cards:
            used_cards.append(card_pull(cardR,suiteR))


        # this will check if the card being put together had been created already
        else:
            for z in used_cards:
                if z == card_pull(cardR,suiteR):
                    suiteR = court_or_crowd()
                    cardR = maj_or_min()
                    card_pull(cardR,suiteR)
                    if card_pull(cardR,suiteR) not in used_cards:
                        used_cards.append(card_pull(cardR,suiteR))
                        break


            while card_pull(cardR,suiteR) in used_cards:
                suiteR = court_or_crowd()
                cardR = maj_or_min()
                card_pull(cardR,suiteR)
                if card_pull(cardR,suiteR) not in used_cards:
                    used_cards.append(card_pull(cardR,suiteR))
                    break

    logic.myDeck = list(dict.fromkeys(used_cards))


def cardCall():
    row = row_selction()             
    newrange = 0
    for r in range(1,row+1): 
        column = card_num_selction(r)
        for _ in range(1,column+1):
            print(f"\n For row {r}: {logic.myDeck[newrange]}, {upright_reversed()} \n")
            newrange += 1
            
def main():
    logic()
    cardCall()
 
 
 
 
if __name__ == '__main__':
    main()