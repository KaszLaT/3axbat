class Config:
    # Base URLs
    BASE_URL = "https://gw.sandboxol.com"
    WEB_PORTAL_URL = "https://editorgs.sandboxol.com"
    
    # Static Headers
    USER_AGENT = "okhttp/4.12.0"
    PACKAGE_NAME = "com.sandboxol.blockymods"
    APP_TYPE = "3AXBAT_LIB"
    
    # Fallback Engine Versions (extracted from WZRD)
    DEFAULT_ENGINE_VERSIONS = {
        "1": 10114,
        "2": 20084,
        "4": 40040
    }

class Endpoints:
    # Authentication
    LOGIN = "/user/api/v4/account/login"
    ENGINE_VERSIONS = "/config/files/blockymods-official-check-version"
    
    # User Profile & Settings
    MY_PROFILE = "/user/api/v3/user/details/info"
    OTHER_PROFILE = "/friend/api/v2/friends/{user_id}"  # Use .format(user_id=123)
    SET_NICKNAME = "/user/api/v3/user/nickName"
    SET_USER_INFO = "/user/api/v1/user/info"  # Used for description, birthday, avatar
    
    # Friends & Social
    FRIENDS_STATUS = "/friend/api/v2/friends/status"
    ADD_FRIEND = "/friend/api/v1/friends"
    POPULARITY = "/friend/api/v1/popularity"  # Liking a player
    DELETE_FRIEND = "/friend/api/v1/friends/black"
    
    # Clans
    CLAN_BASE = "/clan/api/v1/clan/tribe/base"
    CLAN_BULLETIN = "/clan/api/v1/clan/tribe/bulletin"
    CLAN_RANK = "/clan/api/v1/clan/rank"
    
    # Game Servers
    GAME_AUTH = "/game/api/v3/game/auth"
    GAME_DISPATCH = "/v1/dispatch"
    GAME_FOLLOW = "/v1/follow"

class Games:
    """Enum-like class for common Blockman Go game IDs."""
    HUNGER_GAMES = 1001
    SKY_WAR = 1002
    BED_WAR_4V4 = 1008
    MURDER_MYSTERY = 1009
    EGG_WAR = 1018
    BED_WAR_SOLO = 1061
    BED_WAR_DOUBLE = 1062
    BATTLE_ROYALE = 1053