def rand_letter(min:str, max:str):
    import random
    letters = ["A", "B", "C", "D", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
    index1 = letters.index(min)
    index2 = letters.index(max)
    max_int = nums[index2]
    min_int = nums[index1]
    rand_int = random.randint(min_int, max_int)
    index = nums.index(rand_int)
    letter = letters[index]
    return letter

def rand_number(min_num:int, max_num:int):
    import random
    rand_num = random.randint(min_num, max_num)
    return rand_num