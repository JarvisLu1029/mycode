# 終極密碼 讓使用者猜數字

num = 25

while True:
    user_input = int(input('請輸入數字 1 ~ 100 : '))
    if user_input == num:
        print('恭喜中獎')
        break
    elif user_input < 0 or user_input > 100:
        print('請輸入 1 ~ 100 的數')
    elif user_input < num:
        print('請輸入更大的數')
    elif user_input > num:
        print('請輸入更小的數')
    else:
        print('輸入錯誤請重新輸入')
