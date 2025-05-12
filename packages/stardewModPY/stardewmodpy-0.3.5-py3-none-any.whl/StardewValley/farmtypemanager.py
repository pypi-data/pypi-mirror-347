from .manifest import Manifest
from typing import Optional, Any
from .Data.model import modelsData

class Coordinates:
    def __init__(
        self,
        X:int,
        Y:int,
        toX:int,
        toY:int
    ):
        self.X=X
        self.Y=Y
    def getJson(self) -> str:
        return f"{self.X},{self.Y}/{self.toX},{self.toY}"

class SpawnTimingSettings(modelsData):
    def __init__(
        self,
        *,
        StartTime:int,
        TimeEndTime:int,
        MinimumTimeBetweenSpawns:int=10,
        MaximumSimultaneousSpawns:int=1,
        OnlySpawnIfAPlayerIsPresent:bool=False,
        SpawnSound:str=""
    ):
        self.StartTime=StartTime
        self.TimeEndTime=TimeEndTime
        self.MinimumTimeBetweenSpawns=MinimumTimeBetweenSpawns if MinimumTimeBetweenSpawns>=10 else 10
        self.MaximumSimultaneousSpawns=MaximumSimultaneousSpawns if MaximumSimultaneousSpawns>=1 else 1
        self.OnlySpawnIfAPlayerIsPresent=OnlySpawnIfAPlayerIsPresent
        self.SpawnSound=SpawnSound


class ExtraConditions(modelsData):
    def __init__(
        self,
        *,
        Years:list[str]=[],
        Seasons:list[str]=[],
        Days:list[str]=[],
        WeatherYesterday:list[str]=[],
        WeatherToday:list[str]=[],
        WeatherTomorrow:list[str]=[],
        GameStateQueries:list[str]=[],
        CPConditions:dict[str, str]={},
        EPUPreconditions:list[str]=[],
        LimitedNumberOfSpawns:Optional[int]=None
    ):
        self.Years=Years        
        self.Seasons=Seasons
        self.Days=Days
        self.WeatherYesterday=WeatherYesterday
        self.WeatherToday=WeatherToday
        self.WeatherTomorrow=WeatherTomorrow
        self.GameStateQueries=GameStateQueries
        self.CPConditions=CPConditions
        self.EPUPreconditions=EPUPreconditions
        self.LimitedNumberOfSpawns=LimitedNumberOfSpawns


class Areas(modelsData):
    def __init__(
        self,
        *,
        UniqueAreaID:str,
        MapName:str,
        MinimumSpawnsPerDay:str,
        MaximumSpawnsPerDay:str,
        SpawnTiming: SpawnTimingSettings,
        ExtraConditions: ExtraConditions,
        IncludeTerrainTypes:Optional[list[str]]=[],
        ExcludeTerrainTypes:Optional[list[str]]=[],
        IncludeCoordinates:Optional[list[Coordinates]]=[],
        ExcludeCoordinates:Optional[list[Coordinates]]=[],
        StrictTileChecking:Optional[str]="Maximum",
        DaysUntilSpawnsExpire:Optional[int|None]=None       
    ):
        self.UniqueAreaID=UniqueAreaID
        self.MapName=MapName
        self.MinimumSpawnsPerDay=MinimumSpawnsPerDay
        self.MaximumSpawnsPerDay=MaximumSpawnsPerDay
        self.SpawnTiming=SpawnTiming.getJson()
        self.ExtraConditions=ExtraConditions.getJson()
        self.IncludeTerrainTypes=IncludeTerrainTypes
        self.ExcludeTerrainTypes=ExcludeTerrainTypes
        self.IncludeCoordinates=[item.getJson() for item in IncludeCoordinates]
        self.ExcludeCoordinates=[item.getJson() for item in ExcludeCoordinates]
        self.StrictTileChecking=StrictTileChecking
        self.DaysUntilSpawnsExpire=DaysUntilSpawnsExpire
    

class ForageAreas(Areas):
    def __init__(
        self,
        *,
        SpringItemIndex:Any,
        SummerItemIndex:Any,
        FallItemIndex:Any,
        WinterItemIndex:Any,
        UniqueAreaID:str,
        MapName:str,
        MinimumSpawnsPerDay:str,
        MaximumSpawnsPerDay:str,
        SpawnTiming: SpawnTimingSettings,
        ExtraConditions: ExtraConditions,
        IncludeTerrainTypes:Optional[list[str]]=[],
        ExcludeTerrainTypes:Optional[list[str]]=[],
        IncludeCoordinates:Optional[list[Coordinates]]=[],
        ExcludeCoordinates:Optional[list[Coordinates]]=[],
        StrictTileChecking:Optional[str]="Maximum",
        DaysUntilSpawnsExpire:Optional[int|None]=None
    ):
        self.SpringItemIndex=SpringItemIndex
        self.SummerItemIndex=SummerItemIndex
        self.FallItemIndex=FallItemIndex
        self.WinterItemIndex=WinterItemIndex
        self.UniqueAreaID=UniqueAreaID
        self.MapName=MapName
        self.MinimumSpawnsPerDay=MinimumSpawnsPerDay
        self.MaximumSpawnsPerDay=MaximumSpawnsPerDay
        self.SpawnTiming=SpawnTiming.getJson()
        self.ExtraConditions=ExtraConditions.getJson()
        self.IncludeTerrainTypes=IncludeTerrainTypes
        self.ExcludeTerrainTypes=ExcludeTerrainTypes
        self.IncludeCoordinates=[item.getJson() for item in IncludeCoordinates]
        self.ExcludeCoordinates=[item.getJson() for item in ExcludeCoordinates]
        self.StrictTileChecking=StrictTileChecking
        self.DaysUntilSpawnsExpire=DaysUntilSpawnsExpire
    
    

class OreAreas(Areas):
    def __init__(
        self,
        *,
        UniqueAreaID:str,
        MapName:str,
        MinimumSpawnsPerDay:str,
        MaximumSpawnsPerDay:str,
        SpawnTiming: SpawnTimingSettings,
        ExtraConditions: ExtraConditions,
        MiningLevelRequired:dict[str, int]=None,
        StartingSpawnChance:dict[str, int]=None,
        LevelTenSpawnChance:dict[str, int]=None,
        IncludeTerrainTypes:Optional[list[str]]=[],
        ExcludeTerrainTypes:Optional[list[str]]=[],
        IncludeCoordinates:Optional[list[Coordinates]]=[],
        ExcludeCoordinates:Optional[list[Coordinates]]=[],
        StrictTileChecking:Optional[str]="Maximum",
        DaysUntilSpawnsExpire:Optional[int|None]=None       
    ):
        self.UniqueAreaID=UniqueAreaID
        self.MapName=MapName
        self.MinimumSpawnsPerDay=MinimumSpawnsPerDay
        self.MaximumSpawnsPerDay=MaximumSpawnsPerDay
        self.SpawnTiming=SpawnTiming.getJson()
        self.ExtraConditions=ExtraConditions.getJson()
        self.MiningLevelRequired=MiningLevelRequired
        self.StartingSpawnChance=StartingSpawnChance
        self.LevelTenSpawnChance=LevelTenSpawnChance
        self.IncludeTerrainTypes=IncludeTerrainTypes
        self.ExcludeTerrainTypes=ExcludeTerrainTypes
        self.IncludeCoordinates=[item.getJson() for item in IncludeCoordinates]
        self.ExcludeCoordinates=[item.getJson() for item in ExcludeCoordinates]
        self.StrictTileChecking=StrictTileChecking
        self.DaysUntilSpawnsExpire=DaysUntilSpawnsExpire


class LargueObjectAreas(Areas):
    def __init__(
        self,
        *,
        ObjectTypes:list[str],
        FindExistingObjectLocations:bool,
        RelatedSkill:str,
        UniqueAreaID:str,
        MapName:str,        
        MinimumSpawnsPerDay:str,
        MaximumSpawnsPerDay:str,
        SpawnTiming: SpawnTimingSettings,
        ExtraConditions: ExtraConditions,        
        PercentExtraSpawnsPerSkillLevel:int=0,
        IncludeTerrainTypes:Optional[list[str]]=[],
        ExcludeTerrainTypes:Optional[list[str]]=[],
        IncludeCoordinates:Optional[list[Coordinates]]=[],
        ExcludeCoordinates:Optional[list[Coordinates]]=[],
        StrictTileChecking:Optional[str]="Maximum",
        DaysUntilSpawnsExpire:Optional[int|None]=None
    ):
        self.ObjectTypes=ObjectTypes
        self.FindExistingObjectLocations=FindExistingObjectLocations
        self.RelatedSkill=RelatedSkill
        self.UniqueAreaID=UniqueAreaID
        self.MapName=MapName
        self.MinimumSpawnsPerDay=MinimumSpawnsPerDay
        self.MaximumSpawnsPerDay=MaximumSpawnsPerDay
        self.SpawnTiming=SpawnTiming.getJson()
        self.ExtraConditions=ExtraConditions.getJson()
        self.PercentExtraSpawnsPerSkillLevel=PercentExtraSpawnsPerSkillLevel
        self.IncludeTerrainTypes=IncludeTerrainTypes
        self.ExcludeTerrainTypes=ExcludeTerrainTypes
        self.IncludeCoordinates=[item.getJson() for item in IncludeCoordinates]
        self.ExcludeCoordinates=[item.getJson() for item in ExcludeCoordinates]
        self.StrictTileChecking=StrictTileChecking
        self.DaysUntilSpawnsExpire=DaysUntilSpawnsExpire

class MonsterTypeSettings(modelsData):
    def __init__(
        self,
        *,
        SpawnWeight:int=1,
        HP:int=1,
        CurrentHP:int=1,
        PersistentHP:bool=False,
        Damage:int=0,
        Defense:int=0,
        DodgeChance:int=0,
        EXP:int=0,
        ExtraLoot:bool=True,
        SeesPlayersAtSpawn:bool=False,
        RangedAttacks:bool=True,
        InstantKillImmunity:bool=False,
        StunImmunity:bool=False,
        Segments:int=0,
        MinimumSkillLevel:int=0,
        MaximumSkillLevel:int=0,
        Loot:Optional[list[int|str]]=None,
        SightRange:Optional[int]=None,
        FacingDirection:Optional[str]=None,
        Sprite:Optional[str]=None,
        Color:Optional[str]=None,
        MinColor:Optional[str]=None,
        MaxColor:Optional[str]=None,
        Gender:Optional[str]=None,
        RelatedSkill:Optional[str]=None,
        PercentExtraHPPerSkillLevel:Optional[int]=None,
        PercentExtraDamagePerSkillLevel:Optional[int]=None,
        PercentExtraDefensePerSkillLevel:Optional[int]=None,
        PercentExtraDodgeChancePerSkillLevel:Optional[int]=None,
        PercentExtraEXPPerSkillLevel:Optional[int]=None
    ):
        self.SpawnWeight=SpawnWeight
        self.HP=HP
        self.CurrentHP=CurrentHP
        self.PersistentHP=PersistentHP
        self.Damage=Damage
        self.Defense=Defense
        self.DodgeChance=DodgeChance
        self.EXP=EXP
        self.ExtraLoot=ExtraLoot
        self.SeesPlayersAtSpawn=SeesPlayersAtSpawn
        self.RangedAttacks=RangedAttacks
        self.InstantKillImmunity=InstantKillImmunity
        self.StunImmunity=StunImmunity
        self.Segments=Segments
        self.MinimumSkillLevel=MinimumSkillLevel
        self.MaximumSkillLevel=MaximumSkillLevel

        self.Loot=Loot
        self.SightRange=SightRange
        self.FacingDirection=FacingDirection
        self.Sprite=Sprite
        self.Color=Color
        self.MinColor=MinColor
        self.MaxColor=MaxColor
        self.Gender=Gender
        self.RelatedSkill=RelatedSkill
        self.PercentExtraHPPerSkillLevel=PercentExtraHPPerSkillLevel
        self.PercentExtraDamagePerSkillLevel=PercentExtraDamagePerSkillLevel
        self.PercentExtraDefensePerSkillLevel=PercentExtraDefensePerSkillLevel
        self.PercentExtraDodgeChancePerSkillLevel=PercentExtraDodgeChancePerSkillLevel
        self.PercentExtraEXPPerSkillLevel=PercentExtraEXPPerSkillLevel

        

class MonsterTypes(modelsData):
    def __init__(
        self,
        *,
        MonsterName:str,
        Settings:MonsterTypeSettings
    ):
        self.MonsterName=MonsterName
        self.Settings=Settings  

class MonsterAreas(Areas):
    def __init__(
        self,
        *,
        MonsterTypes:list[MonsterTypes],
        UniqueAreaID:str,
        MapName:str,
        MinimumSpawnsPerDay:str,
        MaximumSpawnsPerDay:str,
        SpawnTiming: SpawnTimingSettings,
        ExtraConditions: ExtraConditions,
        IncludeTerrainTypes:Optional[list[str]]=[],
        ExcludeTerrainTypes:Optional[list[str]]=[],
        IncludeCoordinates:Optional[list[Coordinates]]=[],
        ExcludeCoordinates:Optional[list[Coordinates]]=[],
        StrictTileChecking:Optional[str]="Maximum",
        DaysUntilSpawnsExpire:Optional[int|None]=None 
    ):
        self.MonsterTypes=MonsterTypes
        self.UniqueAreaID=UniqueAreaID
        self.MapName=MapName
        self.MinimumSpawnsPerDay=MinimumSpawnsPerDay
        self.MaximumSpawnsPerDay=MaximumSpawnsPerDay
        self.SpawnTiming=SpawnTiming.getJson()
        self.ExtraConditions=ExtraConditions.getJson()
        self.IncludeTerrainTypes=IncludeTerrainTypes
        self.ExcludeTerrainTypes=ExcludeTerrainTypes
        self.IncludeCoordinates=[item.getJson() for item in IncludeCoordinates]
        self.ExcludeCoordinates=[item.getJson() for item in ExcludeCoordinates]
        self.StrictTileChecking=StrictTileChecking
        self.DaysUntilSpawnsExpire=DaysUntilSpawnsExpire



class GlobalSpawnSettings(modelsData):
    def __init__(
        self,
        Enable:bool,
        Areas:list[Areas]=[],
        CustomTileIndex:Optional[list[int]]=[] 
    ):
        self.Enable=Enable
        self.Areas=Areas
        self.CustomTileIndex=CustomTileIndex
        
    
class ForageSpawnSettings(GlobalSpawnSettings):
    def __init__(
        self,
        *,
        Enable:bool,
        Areas:list[ForageAreas]=[],
        PercentExtraSpawnsPerForagingLevel:int=0,
        SpringItemIndex:list[Any]=[],
        SummerItemIndex:list[Any]=[],
        FallItemIndex:list[Any]=[],
        WinterItemIndex:list[Any]=[],
        CustomTileIndex:Optional[list[int]]=[] 
    ):
        self.key="Forage_Spawn_Settings"
        self.Enable=Enable
        self.Areas=Areas
        self.PercentExtraSpawnsPerForagingLevel=PercentExtraSpawnsPerForagingLevel
        self.SpringItemIndex=SpringItemIndex
        self.SummerItemIndex=SummerItemIndex
        self.FallItemIndex=FallItemIndex
        self.WinterItemIndex=WinterItemIndex
        self.CustomTileIndex=CustomTileIndex
    

class LargeObjectSpawnSettings(GlobalSpawnSettings):
    def __init__(
        self,
        *,
        Enable:bool,
        Areas:list[LargueObjectAreas]=[],
        CustomTileIndex:Optional[list[int]]=[]
    ):
        self.key="LargeObject_Spawn_Settings"
        self.Enable=Enable
        self.Areas=Areas
        self.CustomTileIndex=CustomTileIndex


class OreSpawnSettings(GlobalSpawnSettings):
    def __init__(
        self,
        *,
        Enable:bool,
        Areas:list[OreAreas]=[],
        PercentExtraSpawnsPerMiningLevel:int=0,
        MiningLevelRequired:dict[str,int]={},
        StartingSpawnChance:dict[str,int]={},
        LevelTenSpawnChance:dict[str,int]={},
        CustomTileIndex:Optional[list[int]]=[]
    ):
        self.key="Ore_Spawn_Settings"
        self.Enable=Enable
        self.Areas=Areas
        self.PercentExtraSpawnsPerMiningLevel=PercentExtraSpawnsPerMiningLevel
        self.MiningLevelRequired=MiningLevelRequired
        self.StartingSpawnChance=StartingSpawnChance
        self.LevelTenSpawnChance=LevelTenSpawnChance
        self.CustomTileIndex=CustomTileIndex

class MonsterSpawnSettings(GlobalSpawnSettings):
    def __init__(
        self,
        *,
        Enable:bool,
        Areas:list[MonsterAreas]=[],
        CustomTileIndex:Optional[list[int]]=[]
    ):
        self.key="Monster_Spawn_Settings"
        self.Enable=Enable
        self.Areas=Areas
        self.CustomTileIndex=CustomTileIndex

        
class FarmTypeManager:
    def __init__(
        self,
        manifest:Manifest
    ):
        self.Manifest=manifest
        self.Manifest.ContentPackFor={
            "UniqueID": "Esca.FarmTypeManager",
            "MinimumVersion": "1.23.0"
        }
        self.fileName="content.json"

        self.contentFile={}

    def registryContentData(
        self,
        forageSpawn:Optional[ForageSpawnSettings]=None,
        largeObjectSpawn:Optional[LargeObjectSpawnSettings]=None,
        oreSpawn:Optional[OreSpawnSettings]=None,
        monsterSpawn:Optional[MonsterSpawnSettings]=None
    ):
        if forageSpawn is not None:
            self.contentFile[forageSpawn.key]=forageSpawn.getJson()
        if largeObjectSpawn is not None:
            self.contentFile[largeObjectSpawn.key]=largeObjectSpawn.getJson()
        if oreSpawn is not None:
            self.contentFile[oreSpawn.key]=oreSpawn.getJson()
        if monsterSpawn is not None:
            self.contentFile[monsterSpawn.key]=monsterSpawn.getJson()
        