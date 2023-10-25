from dataclasses import dataclass

@dataclass(frozen = True)
class Trader:
    id: str
    firstName: str
    lastName: str
    nickName: str
    companyName: str
    imgUrl: str
    profileLogoData: str
    isDeleted: bool
    isLegitimized: bool
    lastLogin: str
    isSelfRegulatedAssetManager: bool
    selfRegulatedAssetManagerTooltip: str
