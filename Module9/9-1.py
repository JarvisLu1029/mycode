# import 自己建立的模組
import myModule

# 計算幾次方
num = myModule.pow(2, 3)

# 簡單斷句
txt = 'I will always love you'
list_result = myModule.segment_sentence(txt)

# 建立 Car
car1 = myModule.Car('Toyota', 'ALTIS', 500000)
sen = car1.info().replace(',', ' ')

# 多函式串聯使用
def main():
    car1 = myModule.Car('Toyota', 'ALTIS', 500000)
    car_info = car1.info().replace(',', '')

    wheel_pow = myModule.pow(car1.wheel, car1.wheel)
    car_info_list = myModule.segment_sentence(car_info)

    print(wheel_pow)
    print(car_info_list)

# if __name__ == '__main__':

print(num)
print(list_result)
print(sen)

main()