ranking_url = "https://www.pixiv.net/ranking.php?mode={1}&content=&date={2}&p={3}"

r_18_tail = "_r18"


class RankMode:
    daily = "daily",
    weekly = "weekly",
    monthly = "monthly",

class RankContent:
    illust = "illust"
    manga = "manga"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63',
    'Cookie': '你的cookie'
}
