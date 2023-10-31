import json

from routes.ValueAnalyzer.dtos.ValueAnalyzer_dto import ValueAnalyzerCreate
from utils.color_utils import rgb2lab

# feature_order 의 모프 형질 순서에 맞게 리스트 재 선별하는 함수
# 매개변수 : 전체 리스트, 사용자 개체 형질 순서, 유저의 레터럴 기준 위치, 선별 후 남은 데이터, 몇번째 진행되는지 넘버(총 세번 : 고정)
def moff_re_selection(ValueAnalyzer_datas:ValueAnalyzerCreate, feature_order:[], final_direction_leteral:str, rest_datas:[], count:int): #moff_re_selection
    search_list = [] # 수정된 전체 리스트

    # #1차 2차 3차 색상 리스트
    total_color_list = [] #전체 개체 리스트에서 컬러만 리스트
    total_index_list = [] # 마지막 남는 인덱스 리스트 : 첫번째 두번째 세번째씩 리스트를 정리하면서 남는 인덱스를 넣어놓는 공간

    index = 0
    # db데이터 전체 루프
    for idx in range(len(ValueAnalyzer_datas)):

        left_info_data = json.loads(ValueAnalyzer_datas[idx].left_info)
        right_info_data = json.loads(ValueAnalyzer_datas[idx].right_info)
        total_info_data = ""

        #최종 평가 방향 선택
        if final_direction_leteral == "left":
            total_info_data = left_info_data
        elif final_direction_leteral == "right":
            total_info_data = right_info_data


        if count == 1:
            slist = select_obj(feature_order, total_info_data, count, index)
            index = index + 1
            if len(slist[0]) != 0:
                total_color_list.append(slist[0])
                total_index_list.append(slist[1])
        elif count == 2:
            for idx_2 in range(len(rest_datas)):
                if idx == rest_datas[idx_2]:
                    slist = select_obj(feature_order, total_info_data, count, rest_datas[idx_2])
                    if len(slist[0]) != 0:
                        total_color_list.append(slist[0])
                        total_index_list.append(slist[1])
        elif count == 3:
            for idx_3 in range(len(rest_datas)):
                if idx == rest_datas[idx_3]:
                    slist = select_obj(feature_order, total_info_data, count, rest_datas[idx_3])
                    if len(slist[0]) != 0:
                        total_color_list.append(slist[0])
                        total_index_list.append(slist[1])
    search_list.append(total_color_list)
    search_list.append(total_index_list)
    return search_list

#CIELAB 색상과 인덱스 값을 obj형태로 가져오는 함수
def select_obj(feature_order, total_info_data, count, index):
    search_list = []
    #1차 2차 3차 색상 리스트
    color_obj = "" #전체 개체 리스트에서 컬러만 리스트
    index_obj = "" # 마지막 남는 인덱스 리스트 : 첫번째 두번째 세번째씩 리스트를 정리하면서 남는 인덱스를 넣어놓는 공간

    if feature_order[count-1][0] == 1:  # 1차 형질
        if len(total_info_data['RGB']) >= 1: # db의 개체의 탐색된 형질 갯수
            # print("1차 형질")
            color_obj = rgb2lab(total_info_data['RGB'][0])
            index_obj = index

    elif feature_order[count-1][0] == 2: # 2차 형질
        if len(total_info_data['RGB']) >= 2: # db의 개체의 탐색된 형질 갯수
            # print("2차 형질")
            color_obj = rgb2lab(total_info_data['RGB'][1])
            index_obj = index

    elif feature_order[count-1][0] == 3: # 3차 형질
        if len(total_info_data['RGB']) >= 3: # db의 개체의 탐색된 형질 갯수
            # print("3차 형질")
            color_obj = rgb2lab(total_info_data['RGB'][2])
            index_obj = index

    search_list.append(color_obj)
    search_list.append(index_obj)
    return search_list

# 점수로 비교 하는 함수
def score_compare_selection(ValueAnalyzer_datas, my_score, rest_datas):
    total_index_list = []

    for idx in range(len(ValueAnalyzer_datas)):
        dorsal_score_data = ValueAnalyzer_datas[idx].dorsal_score
        left_score_data = ValueAnalyzer_datas[idx].left_score
        right_score_data = ValueAnalyzer_datas[idx].right_score
        gender_data = ValueAnalyzer_datas[idx].gender

        for idx_4 in range(len(rest_datas)):
            if idx == rest_datas[idx_4]:
                # print("레터럴 점수 검색")
                # print(rest_datas[idx_4])

                #도살, 옆구리 점수 체크
                if dorsal_score_data >= my_score.dorsal_score and left_score_data >= my_score.left_score and right_score_data >= my_score.right_score:
                    # print(rest_datas[idx_4])

                    #성별이 다른 것만 체크
                    # if gender_data != my_score.gender:
                        total_index_list.append(rest_datas[idx_4])

    return total_index_list

#형질 높은 순으로 졍렬
def sort_feature_order(feature_order):
    feature_order.sort(key=lambda x: x[2], reverse=True)  # array.sort() 와 동일.
    return feature_order

def make_moff_explanation(result, feature_order):
    moff_explan = "해당 도마뱀은 "
    feature_ex = ""
    feature_ex2 = "그리고 "
    feature_ex3 = ""

    if feature_order[0][0] == 1:
        feature_ex += "1차 형질"
        feature_percent_1 = round(feature_order[0][2])
        feature_percent_2 = round(feature_order[1][2])
        feature_percent_3 = round(feature_order[2][2])
        feature_ex += "이 " + str(feature_percent_1) + "%로 높습니다. "

        #2차와 3차가 "+feature_percent_2+"%"
        if feature_order[1][2] != 0:
            feature_ex += "2차가 " + str(feature_percent_2) + "%"
            feature_ex += "로 낮습니다. "
        if feature_order[2][2] != 0:
            feature_ex += ", 3차가 " + str(feature_percent_3) + "%"
            feature_ex += "로 낮습니다. "


    elif feature_order[0][0] == 2:
        feature_ex += "2차 형질"
        feature_percent = round(feature_order[0][2])
        feature_ex += "이 " + str(feature_percent) + "%로 높은 장점이 있습니다. "
    elif feature_order[0][0] == 3:
        feature_ex += "3차 형질"
        feature_percent = round(feature_order[0][2])
        feature_ex += "이 " + str(feature_percent) + "%로 높은 장점이 있습니다. "


    print("feature_ex")
    print(feature_ex)

    total_chr:str = ""
    high_list:str = ""
    mid_list:str= ""
    low_list:str = ""

    if result.head_score >= 80:
        high_list += "머리, "
    elif result.head_score < 80 and result.head_score >= 50:
        mid_list += "머리, "
    elif result.head_score < 50:
        low_list += "머리, "

    if result.dorsal_score >= 80:
        high_list += "도살, "
    elif result.dorsal_score < 80 and result.head_score >= 50:
        mid_list += "도살, "
    elif result.dorsal_score < 50:
        low_list += "도살, "

    if result.left_score >= 80:
        high_list += "왼쪽 레터럴, "
    elif result.left_score < 80 and result.head_score >= 50:
        mid_list += "왼쪽 레터럴, "
    elif result.left_score < 50:
        low_list += "왼쪽 레터럴, "

    if result.right_score >= 80:
        high_list += "오른쪽 레터럴 "
    elif result.right_score < 80 and result.head_score >= 50:
        mid_list += "오른쪽 레터럴, "
    elif result.right_score < 50:
        low_list += "오른쪽 레터럴 "

    if result.total_score >= 80:
        total_chr += "전체적으로 고퀄"
    elif result.total_score < 80 and result.head_score >= 50:
        total_chr += "전체적으로 중퀄"
    elif result.total_score < 50:
        total_chr += "전체적으로 저퀄"

    high_list = high_list[:-2]
    mid_list = mid_list[:-2]
    low_list  = low_list[:-2]
    # print(high_list)
    # print(mid_list)
    # print(low_list)

    if len(high_list) != 0:
        feature_ex2 += high_list + "에서 높은 점수를 "
    if len(mid_list) != 0:
        feature_ex2 += mid_list + "에서 중간 점수를 "
    if len(low_list) != 0:
        feature_ex2 += low_list + "에서 낮은 점수를 "

    feature_ex2 += "받았습니다. "
    feature_ex2 += total_chr + "에 해당 하는 모프를 갖추고 있습니다. "
    # print(feature_ex2)



    feature_ex3 += "레털럴의 "

    leteral_high_list = ""
    if feature_order[0][0] == 1:
        if feature_order[0][2] >= 50:
            if feature_order[1][2] >= 50 or feature_order[2][2] >= 50:
                leteral_high_list += "2차 형질과 3차 형질 "
            else:
                leteral_high_list += "2차 형질과 3차 형질 "
        else:
            leteral_high_list += "2차 형질과 3차 형질 "
    elif feature_order[0][0] == 2:
        if feature_order[0][2] >= 50:
            leteral_high_list += "2차 형질과"
    elif feature_order[0][0] == 3:
        if feature_order[0][2] >= 50:
            leteral_high_list += "3차 형질과"

    feature_ex3 += leteral_high_list[:-1] + "이 높은 도마뱀과 메이팅을 했을때 좋은 장점이 될 수 있습니다. "

    # 내용 합치기
    moff_explan += feature_ex + feature_ex2 + feature_ex3

    # 예) 해당 도마뱀은 (2차 형질)이 (97퍼센트)로 높은 장점이 있습니다. 그리고 (머리, 도살, 왼쪽 레터럴)이 (높은 점수)를 받았으며 (전체적으로 고퀄에 해당)하는 모프를 갖추고 있습니다.
    #                                                        80 이상 높은 점수, 80 이하 50 이상 중간 점수, 50 이하 낮은 점수  / 고, 중, 고
    # 레터럴의 (2차 형질)과 (3차형질)이 높은 도마뱀과 메이팅을 했을때 좋은 장점이 될 수 있습니다.
    return moff_explan