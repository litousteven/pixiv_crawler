from pathlib import Path
from pixivapi import Size

user_name = "litousteven@163.com"
pass_word = "971!!$"
sess_id = "10602463_9ti1Bhem77PDyRvDBXXh2Yw7YOsmZjix"


def main():
    from pixivapi import Client

    client = Client()
    # client.login(user_name, pass_word)
    client.authenticate(sess_id)

    illustration = client.fetch_illustration(75523989)

    illustration.download(
        directory=Path.home() / "my_pixiv_images",
        size=Size.ORIGINAL,
    )


if __name__ == '__main__':
    main()
