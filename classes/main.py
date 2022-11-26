# Do not modify these lines
__winc_id__ = '04da020dedb24d42adf41382a231b1ed'
__human_name__ = 'classes'

# Add your code after this line

from multiprocessing.pool import INIT


class Player:
    #add method __init__
    # add parameter name
    def __init__(self, name, speed, endurance, accuracy):
        self.name = name
        if (type(speed) == float 
           or type(speed) == int
           and speed >= 0 
           and speed <=1):
            self.speed = speed
        else:
            raise ValueError(f"positive speed expected, got {speed}")
            
        if (type(endurance) == float 
           or type(endurance) == int 
           and endurance >= 0 
           and endurance <= 1):
            self.endurance = endurance
        else:
            raise ValueError(f"positive endurance expected, got {endurance}")
        
        if (type(accuracy) == float 
           or type(accuracy) == int 
           and accuracy >= 0 
           and accuracy <= 1):
            self.accuracy =accuracy
        else:
            raise ValueError(f"positive accuracy expected, got {accuracy}")

    def introduce(self):
        return f"Hello everyone, my name is {self.name}."
    
    def strength(self):
        if self.speed >= self.endurance and self.speed >= self.accuracy:
            strength = ("speed", self.speed)
            return  strength
        elif self.endurance > self.speed and self.endurance >= self.accuracy:
            strength = ("endurance", self.endurance)
            return  strength
        elif self.accuracy > self.endurance and self.accuracy > self.speed:
            strength = ("accuracy", self.accuracy)
            return  strength


class Commentator:
    def __init__(self, name):
        self.name = name

    def sum_player(self, player):
        speed = getattr(player, 'speed')
        endurance = getattr(player, 'endurance')
        accuracy = getattr(player, 'accuracy')
        sum = speed + endurance + accuracy
        return sum

    def compare_players(self, player1, player2, skill):
        p1_skill = getattr(player1, skill)
        p2_skill = getattr(player2, skill)
        if p1_skill > p2_skill:
            return getattr(player1, 'name')
        elif p2_skill > p1_skill:
            return getattr(player2, 'name')
        elif p1_skill == p2_skill:
            p1_strength = player1.strength()
            p2_strength = player2.strength()
            if p1_strength > p2_strength:
                return getattr(player1, 'name')
            elif p2_strength > p1_strength:
                return getattr(player2, 'name')
            elif p1_strength == p2_strength:
                p1_sum = Commentator.sum_player(self = self, player = player1)
                p2_sum = Commentator.sum_player(self = self, player = player2)
                if p1_sum > p2_sum:
                    return getattr(player1, 'name')
                elif p1_sum < p2_sum:
                    return getattr(player2, 'name')
                else:
                    return 'These two players might as well be twins!'
