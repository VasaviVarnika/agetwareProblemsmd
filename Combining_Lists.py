def has_overlap(seg1,seg2):
    start1,end1=seg1
    start2,end2=seg2
    overlap_start=max(start1,start2)
    overlap_end=min(end1,end2)
    overlap_len=max(0,overlap_end-overlap_start)
    return overlap_len>(end1-start1)/2 or overlap_len>(end2-start2)/2

def merge_segs(list_1,list_2):
    merged=[]
    index_1=index_2=0
    while index_1<len(list_1) and index_2<len(list_2):
        seg1=list_1[index_1]
        seg2=list_2[index_2]
        
        if has_overlap(seg1['positions'],seg2['positions']):
            combined={
                "positions":seg1['positions'] if seg1['positions'][0]<=seg2['positions'][0] else seg2['positions'],
                "values":seg1['values']+seg2['values']
            }
            merged.append(combined)
            index_1+=1
            index_2+=1
        elif seg1['positions'][0]< seg2['positions'][0]:
            merged.append(seg1)
            index_1+=1
        else:
            merged.append(seg2)
            index_2+=1
            
    merged.extend(list_1[index_1:])
    merged.extend(list_2[index_2:])
    return merged
    

list_1 = [
    {
        "positions": [1, 5],
        "values": [100, 200]
    },
    {
        "positions": [10, 14],
        "values": [300]
    }
]

list_2 = [
    {
        "positions": [4, 8],
        "values": [400]
    },
    {
        "positions": [15, 20],
        "values": [500, 600]
    }
]
    
result=merge_segs(list_1,list_2)
for item in result:
    print(item)
