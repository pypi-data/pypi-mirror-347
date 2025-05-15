import requests

API_URL = "http://api.ra3battle.cn/api/server/status"

def setModszh(modsName):
    """
    :return: 传入mod英文并返回mods中文名
    """
    try:
        getJson = requests.get(API_URL)
        getJson.raise_for_status()  # 添加异常处理
    except requests.RequestException as e:
        msg = f"API请求失败: {e}"
        return msg
    if modsName == "RA3":
        modsName = "原版"
    if modsName == "corona":
        modsName = "日冕"
    return modsName

def GetGamesJson():
    """
    :return:返回json内字段的games内容
    """
    try:
        getJson = requests.get(API_URL)
        getJson.raise_for_status()  # 添加异常处理
    except requests.RequestException as e:
        msg = f"API请求失败: {e}"
        return msg
    data = getJson.json()  # 简化变量名
    return data["games"]
def TotalNum():
    """
    :return: 获取当前服务器正在对局的人数
    """
    try:
        getJson = requests.get(API_URL)
        getJson.raise_for_status()  # 添加异常处理
    except requests.RequestException as e:
        msg = f"API请求失败: {e}"
        return msg
    data = getJson.json()  # 简化变量名
    Total = data["games"]
    total_players = sum(len(game["players"]) for game in Total)
    return total_players

def PlayersNum():
    """
    :return: 返回当前在线人数
    """
    try:
        getJson = requests.get(API_URL)
        getJson.raise_for_status()  # 添加异常处理
    except requests.RequestException as e:
        msg = f"API请求失败: {e}"
        return msg
    data = getJson.json()  # 简化变量名
    players = len(data["players"])
    return players

def GetJson():
    """
    :return: 返回json
    """
    try:
        getJson = requests.get(API_URL)
        getJson.raise_for_status()  # 添加异常处理
    except requests.RequestException as e:
        msg = f"API请求失败: {e}"
        return msg
    data = getJson.json()  # 简化变量名
    return data

def ToString():
    """
    :return: 返回字符串
    "
        ""--------------------\n"
        f"当前在线人数：{players}\n"
        f"正在对局玩家：{total_players}\n"
        f"闲置玩家：{Idle_player}\n"
        "--------------------\n"
        f"1v1自动匹配正在寻找对局的玩家为：{count1v1}\n"
        f"1v1日冕自动匹配正在寻找对局的玩家为：{count1v1R}\n"
        "--------------------\n"
        f"正在进行匹配对战的房间总数：{mate_room}\n"
        f"正在进行游戏的房间个数：{closed_playing_count}\n"
        f"正在准备的房间个数：{preparing_games}\n"
        "--------------------""
    """
    try:
        getJson = requests.get(API_URL)
        getJson.raise_for_status()  # 添加异常处理
    except requests.RequestException as e:
        msg = f"API请求失败: {e}"
        return msg
    data = getJson.json()  # 简化变量名
    players = len(data["players"])
    if not data["players"] and not data["games"]:
        msg = f"根据api获取json为\n-------------------\n{data}\n-------------------\n获取players和games内的数据为空\n疑似战网崩溃或战网内暂无玩家\n如崩溃则联系战网管理"
        return msg
    Total = data["games"]
    total_players = sum(len(game["players"]) for game in Total)
    Idle_player = players - total_players
    count1v1D = data['automatching']['count1v1Details']
    count1v1 = count1v1D.get('ra3', 0)
    count1v1R = count1v1D.get('corona', 0)
    mate_room = str(len(data["automatch"]))
    closed_playing_count = sum(1 for game in Total if game["gamemode"] == 'closedplaying')
    preparing_games = len(Total) - closed_playing_count
    over = (
        "--------------------\n"
        f"当前在线人数：{players}\n"
        f"正在对局玩家：{total_players}\n"
        f"闲置玩家：{Idle_player}\n"
        "--------------------\n"
        f"1v1自动匹配正在寻找对局的玩家为：{count1v1}\n"
        f"1v1日冕自动匹配正在寻找对局的玩家为：{count1v1R}\n"
        "--------------------\n"
        f"正在进行匹配对战的房间总数：{mate_room}\n"
        f"正在进行游戏的房间个数：{closed_playing_count}\n"
        f"正在准备的房间个数：{preparing_games}\n"
        "--------------------"
    )
    return over

