from pixivpy3 import *
user_name = "litousteven@163.com"
pass_word = "971!!$"
sess_id = "10602463_9ti1Bhem77PDyRvDBXXh2Yw7YOsmZjix"


if __name__ == '__main__':
    api = AppPixivAPI()
    # api.login(user_name, pass_word)
    api.set_auth(sess_id, sess_id)
    json_result = api.illust_ranking()
    for illust in json_result.illusts[:3]:
        api.download(illust.image_urls.large, "", "./download/")
