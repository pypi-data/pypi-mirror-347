import pandas as pd
import numpy as np
import sys

import textbasic.basic.preprocessor as ppm
# import gluonnlp as nlp

__all__ = ['similarity_verification']

def similarity_verification(mode, df=None, column=None, string_list=None, p=60, sim_stan_len=500):
    '''
    입력된 문장 리스트 또는 데이터프레임에서 유사한 문장을 그룹별로 분류하여 추출하는 함수
    
    ==========
    parameter
    ==========
    mode : 유사도 검증 모드를 결정
        'list' 로 하는 경우 문장 데이터가 포함된 단순 string_list 만 입력하면 됨
        'df' 로 하는 경우 문장 데이터가 포함된 dataframe 과 해당 문장 데이터의 컬럼 명 column 을 입력해야 함
        
    df : mode 가 'df' 인 경우만 입력필요. 문장데이터를 포함한 dataframe 형식의 변수
    
    column : mode 가 'df' 인 경우만 입력 필요. 입력된 dataframe 에서 문장 데이터의 컬럼 명을 입력
    
    string_list : mode 가 'list' 인 경우만 입력 필요. 문장 데이터를 포함한 단순 list 변수
    
    p : 유사도 퍼센티지. 0 ~ 100 사이의 값을 지정.
    
    sim_stan_len : 유사도 검증을 진행할 문장의 최대 길이. 1000 으로 한 경우 
        0~1000 번째까지의 문장 index 내에서 유사도 검증을 진행함
    '''
    
    if mode == 'list':
        df = pd.DataFrame(string_list, columns=['string'])
    elif mode == 'df':
        string_list = df[column].tolist()
        
    if len(df) <= 1:
        print('1개 이하의 데이터는 유사도 분석이 불가능합니다.')
        return df, pd.DataFrame()
        
    
    new_string_list = []
    for string in string_list:
        new_string = string[:sim_stan_len]
        new_string_list.append(new_string)
    
    # 형태소 분석    
    whole_morph_list_list = list(map(ppm.morpheme_analysis, new_string_list))
    
    # 집합화
    whole_morph_set_list = list(map(set, whole_morph_list_list))
    symmetrical_diff_set_ary = whole_morph_set_list[0] ^ whole_morph_set_list[1]
    whole_morph_set_ary = np.array(whole_morph_set_list)

    # 유사문장
    idx = 0
    idx_true_list = []
    idx_false_list = []
    sim_df_list = []
    while True:
        
        try:
            # 기준 문장 선정
            stan_string_set = whole_morph_set_ary[idx]
            idx_true_list.append(True)
            idx_false_list.append(False)
        except IndexError:
            break
        
        # 유사도 선정 기준값 계산
        diff_count_stan = int(len(stan_string_set)*((100-p)/100))
        
        # 유사도를 검증할 문장 추출
        temp_morph_set_ary = whole_morph_set_ary[idx+1:]
        # 대칭차집합 구하기
        symmetrical_diff_set_ary = temp_morph_set_ary ^ stan_string_set

        # 대칭차집합의 형태소 갯수 구하기
        symmetrical_diff_len_list = list(map(len, symmetrical_diff_set_ary))
        symmetrical_diff_len_ary = np.array(symmetrical_diff_len_list)

        # ================================================
        # 반복 문장 추출 (true 는 유사문장)
        
        # 기준 문장 위치에 True 지정
        idx_f_list = idx_false_list.copy()
        idx_f_list[-1] = True
        
        # 유사도 선정 기준값보다 적으면 True 많으면 False  
        f_mask_list = np.where(symmetrical_diff_len_ary <= diff_count_stan, True, False).tolist()
        
        # 지금까지의 유사도 검증 결과에 추가
        f_mask_list = idx_f_list + f_mask_list
        
        # 유사한 문장을 기존 df 에서 추출
        sim_df = df[f_mask_list]
        
        # 그룹 번호 리스트 생성
        sim_idx_ary = np.full(len(sim_df), idx)
        
        # 해당 유사문장 그룹에 리스트 입력
        sim_df.insert(0, 'group', sim_idx_ary, True)
        
        # 유사문장이 최소 1개 이상 있을경우 유사문장 그룹을 저장
        if len(sim_df) > 1:
            sim_df_list.append(sim_df)
        
        # ================================================
        # 반복 문장 제거 (true 는 삭제하지 않음)
        
        # 현재 기준문장위치에 True 가 있는 list 가져오기
        idx_t_list = idx_true_list.copy()
        
        # 유사도 선정 기준값보다 많으면 True 많으면 False 
        t_mask_list = np.where(symmetrical_diff_len_ary > diff_count_stan, True, False).tolist()
        
        # 현재 기준문장위치에 True 가 있는 list에 유사도 선정 결과 리스트를 추가
        t_mask_list = idx_t_list + t_mask_list
        
        # 기존 df 에서 유사하지 않은 문장(True) 만 추출
        df = df[t_mask_list]
        
        # 기존 ary 에서 유사하지 않은 문장(True) 만 추출
        whole_morph_set_ary = whole_morph_set_ary[t_mask_list]
        
        sys.stdout.write(f'\r $$$ {idx}, {len(df)} $$$')
        
        idx += 1

    if len(sim_df_list) >= 1:
        whole_sim_df = pd.concat(sim_df_list, axis=0)
    else:
        whole_sim_df = pd.DataFrame()

    return df, whole_sim_df

