from .model import modelsData

class Season(modelsData):
    def __init__(self):
        pass
    
    def getJson(self):
        return "Spring"

    class Spring(modelsData):
        def __init__(self):
            pass
            
        def getJson() -> str:
            return "Spring"
    
    class Summer(modelsData):
        def __init__(self):
            pass

        def getJson() -> str:
            return "Summer"
    
    class Fall(modelsData):
        def __init__(self):
            pass
    
        def getJson() -> str:
            return "Fall"
    
    class Winter(modelsData):
        def __init__(self):
            pass

        def getJson() -> str:
            return "Winter"


class AquariumType(modelsData):
    def __init__(self):
        pass

    def getJson(self) -> str:
        return "eel"
    
    class Eel(modelsData):
        def __init__(self):
            pass

        def getJson(self) -> str:
            return "eel"
    
    class Cephalopod(modelsData):
        def __init__(self):
            pass

        def getJson(self) -> str:
            return "cephalopod"
    
    class Crawl(modelsData):
        def __init__(self):
            pass

        def getJson(self) -> str:
            return "crawl"
    
    class Ground(modelsData):
        def __init__(self):
            pass

        def getJson(self) -> str:
            return "ground"
    
    class Fish(modelsData):
        def __init__(self):
            pass

        def getJson(self) -> str:
            return "fish"
    
    class Front_crawl(modelsData):
        def __init__(self):
            pass

        def getJson(self) -> str:
            return "front_crawl"
        
class AudioCategory(modelsData):
    def __init__(self):
        pass

    def getJson(self):
        return "Default"
    
    class Default(modelsData):
        def __init__(self):
            pass
        def getJson(self):
            return "Default"
    
    class Music(modelsData):
        def __init__(self):
            pass
        def getJson(self):
            return "Music"
    
    class Sound(modelsData):
        def __init__(self):
            pass
        def getJson(self):
            return "Sound"
    
    class Ambient(modelsData):
        def __init__(self):
            pass
        def getJson(self):
            return "Ambient"
    
    class Footsteps(modelsData):
        def __init__(self):
            pass
        def getJson(self):
            return "Footsteps"

class BCFragility(modelsData):
    def __init__(self, fragility:int):
        if fragility < 0 or fragility > 2:
            raise ValueError("The possible values are 0 (pick up with any tool), 1 (destroyed if hit with an axe/hoe/pickaxe, or picked up with any other tool), or 2 (can't be removed once placed). Default 0.")
        self.fragility = fragility

    def getJson(self):
        return self.fragility
    

class StackSizeVisibility(modelsData):
    def __init__(self):
        pass

    def getJson(self):
        return "Show"

    class Hide(modelsData):
        def __init__(self):
            pass

        def getJson(self):
            return "Hide"
    
    class Show(modelsData):
        def __init__(self):
            pass

        def getJson(self):
            return "Show"
    
    class ShowIfMultiple(modelsData):
        def __init__(self):
            pass

        def getJson(self):
            return "ShowIfMultiple"

class Quality(modelsData):
    def __init__(self):
        pass

    def getJson(self):
        return 0
    
    class Normal(modelsData):
        def __init__(self):
            pass

        def getJson(self):
            return 0
    
    class Silver(modelsData):
        def __init__(self):
            pass

        def getJson(self):
            return 1
    
    class Gold(modelsData):
        def __init__(self):
            pass

        def getJson(self):
            return 2
    
    class Iridium(modelsData):
        def __init__(self):
            pass

        def getJson(self):
            return 3

class QualityModifierMode(modelsData):
    def __init__(self):
        pass

    def getJson(self):
        return "Stack"

    class Stack(modelsData):
        def __init__(self):
            pass

        def getJson(self):
            return "Stack"
    
    class Minimum(modelsData):
        def __init__(self):
            pass

        def getJson(self):
            return "Minimum"
    
    class Maximum(modelsData):
        def __init__(self):
            pass

        def getJson(self):
            return "Maximum"

class ToolUpgradeLevel(modelsData):
    def __init__(self):
        pass

    def getJson(self):
        return 0

    class Normal(modelsData):
        def __init__(self):
            pass

        def getJson(self):
            return 0
    
    class Copper(modelsData):
        def __init__(self):
            pass

        def getJson(self):
            return 1
    
    class Steel(modelsData):
        def __init__(self):
            pass

        def getJson(self):
            return 2
    
    class Gold(modelsData):
        def __init__(self):
            pass

        def getJson(self):
            return 3
    
    class IridiumTool(modelsData):
        def __init__(self):
            pass

        def getJson(self):
            return 4
    
    class Bamboo(modelsData):
        def __init__(self):
            pass

        def getJson(self):
            return 0
    
    class Training(modelsData):
        def __init__(self):
            pass

        def getJson(self):
            return 1
    
    class Fiberglass(modelsData):
        def __init__(self):
            pass

        def getJson(self):
            return 2
    
    class IridiumRod(modelsData):
        def __init__(self):
            pass

        def getJson(self):
            return 3
    
    class AdvancedIridiumRod(modelsData):
        def __init__(self):
            pass

        def getJson(self):
            return 4

class Modification(modelsData):
    def __init__(self):
        pass

    def getJson(self):
        return "Multiply"
    
    class Multiply(modelsData):
        def __init__(self):
            pass
        
        def getJson(self):
            return "Multiply"
    
    class Add(modelsData):
        def __init__(self):
            pass
        
        def getJson(self):
            return "Add"
    
    class Subtract(modelsData):
        def __init__(self):
            pass
        
        def getJson(self):
            return "Subtract"
    
    class Divide(modelsData):
        def __init__(self):
            pass
        
        def getJson(self):
            return "Divide"
    
    class Set(modelsData):
        def __init__(self):
            pass
        
        def getJson(self):
            return "Set"

class AvailableStockLimit(modelsData):
    def __init__(self):
        pass

    def getJson(self):
        return "None"
    
    class none(modelsData):
        def __init__(self):
            pass
        
        def getJson(self):
            return "None"
    
    class Player(modelsData):
        def __init__(self):
            pass
        
        def getJson(self):
            return "Player"
    
    class Global(modelsData):
        def __init__(self):
            pass
        
        def getJson(self):
            return "Global"