def compute_center(vecs):
    sum = {}
    vec = vecs[n]
    for (id, val) in vec:
        if (id in sum):
            sum[id] = sum[id] + val
        else:
            sum[id] = val


    sorted_keys = sorted(sum.keys(), key=lambda item: item)

    center = []
    for key in sorted_keys:
        center.append((key, sum[key] / size))

    return center

def merge_sort(ary):
    if len(ary) <= 1 : return ary
    num = int(len(ary)/2)
    left = merge_sort(ary[:num])
    right = merge_sort(ary[num:])
    return merge(left,right)

def merge(left,right):
    l,r = 0,0
    result = []
    while l<len(left) and r<len(right) :
        if left[l][0] > right[r][0]:
            result.append(left[l])
            l += 1
        else:
            result.append(right[r])
            r += 1
    result += left[l:]
    result += right[r:]
    return result

