class Angry_bird(object):

    def __init__(self, name, strength, stamina, shield, special_attack):
        self.name = name
        self.strength = strength
        self.stamina = stamina
        self.shield = shield
        self.special_attack= special_attack
        self.charge = True

    def stamina_damage(self, damage):
        self.stamina-=damage
      
    # GETTERS
    def get_name(self):
        return self.name

    def get_strength(self): 
        return self.strength

    def get_stamina(self): 
        return self.stamina

    def get_shield(self): 
        return self.shield

    def get_special_attack(self): 
        return self.special_attack

    def get_charge(self):
        return self.charge

    # SETTERS
    def set_name(self, name):
        self.name = name

    def set_strength(self, strength): 
        self.strength = strength

    def set_stamina(self, stamina): 
         self.stamina = stamina

    def set_shield(self,shield): 
        self.shield = shield

    def set_special_attack(self,special_attack): 
        return self.special_attack

    def set_charge(self, charge):
        self.charge = charge
