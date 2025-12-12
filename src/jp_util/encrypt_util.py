import hashlib

def md5_encrypt(text: str) -> str:
    # 注意：MD5 推荐使用 utf-8 编码，尤其是包含中文时
    return hashlib.md5(text.encode('utf-8')).hexdigest()






if __name__ == '__main__':
    # 使用示例
    print(md5_encrypt("hello world"))
    # 输出: 5eb63bbbe01eeed093cb22bb8f5acdc3

    print(md5_encrypt("你好，世界"))
    # 输出: 1d947bf01e8e1083c96c7e1b5bec7f1f

    text='ご自宅の屋根の状態をじっくりと見たことはありますか。住まいを守る屋根は、雨風や太陽光を直接受け止めているため、気付かないうちに傷んでいる場合があるのです。屋根に傷が入ると、すき間から雨水が染み込んで雨漏りを起こし、放っておくと内壁や柱などを腐らせてしまう可能性もあります。さらには地震や台風などで破損し、一部が落下するなどして事故になることも。'
    print(md5_encrypt(text))
