# 從模組 import 特定函式
from myModule import pow, segment_sentence, Car

# 計算幾次方
num = pow(2, 3)
print(num)


# 簡單斷句
txt = 'I will always love you'
list_result = segment_sentence(txt)
print(list_result)


# 多函式串聯使用
def main():
    # 建立 Car
    car1 = Car('Toyota', 'ALTIS', 500000)
    car_info = car1.info().replace(',', '')

    wheel_pow = pow(car1.wheel, 2)
    car_info_list = segment_sentence(car_info)

    print(wheel_pow)
    print(car_info_list)

main()


