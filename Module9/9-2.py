# 從模組 import 特定函式
from myModule import pow, segment_sentence

# 計算幾次方
num = pow(2, 3)
print(num)


# if __name__ == '__main__':

# 簡單斷句
txt = 'I will always love you'
list_result = segment_sentence(txt)
print(list_result)