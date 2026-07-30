def quick_sort(array: list):
    if array == []:
        return []
    pivot_value = array[0]

    first_sub = []
    second_sub = []
    third_sub = []
    final_sort = []
    for i in array:
        if i < pivot_value:
            first_sub.append(i)
        elif i == pivot_value:
            second_sub.append(i)
        else:
            third_sub.append(i)



    final_sort += (quick_sort(first_sub))


    final_sort += second_sub
    final_sort += quick_sort(third_sub)
    return final_sort
quick_sort([20, 3, 14, 1, 5]) 
