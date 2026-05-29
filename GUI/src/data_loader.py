#! /Work1/HOME/eonebi/anaconda3/envs/streamlit_env/bin/python3

'''
업로드된 파일 객체를 데이터프레임으로 변환하고 이상치가 없는지 검증
'''

import pandas as pd 
import streamlit as st

def load_data(uploaded_file) -> pd.DataFrame:
    '''
    Streamlit의 파일 업로더 객체를 받아 DataFrame으로 반환하는 함수
    '''

    try:
        if uploaded_file.name.endswith('.tsv') or uploaded_file.name.endswith('.txt'):
            df = pd.read_csv(uploaded_filem, sep='\t')

        if df.empty:
            st.error("The uploaded file is empty.")
            return None

        return df 
    except Exception as e:
        st.error(f"Error reading the file: {e}")
        return None

# 16s, metaphlan, gtdb, vf
# 내부 전용 헬퍼 함수
def load_taxonomy_data(file_path, file_type, rank_prefix):
    '''MetaPhlAn 또는 GTDB 파일을 읽어 특정 Rank로 필터링'''

    sep = ';' if file_type == 'gtdb' else '|'
    skip = 1 if file_type == 'gtdb' else 0

    if file_type == 'metaphlan':
        with open(file_path, 'r') as f:
            for i, line in enumerate(f):
                if line.startswith("#clade_name"):
                    skip = i
                    break

    df = pd.read_csv(file_path, sep='\t', skiprows=skip)
    rank_level_map = {'p': 1, 'c': 2, 'o': 3, 'f': 4, 'g': 5, 's': 6}
    expected = rank_level_map.get(rank_prefix, 6)

    if file_type == "metaphlan":
        filtered = df[df['#clade_name'].str.count('\|') == expected].copy()
    else:
        filtered = df[df['#clade_name'].str.count(sep) == expected].copy()

    return filtered

def load_vf_data(file_path, read_length):
    '''Virulence Factor 파일을 읽고 값 계산'''

    df = pd.read_csv(file_path, sep='\t')
    pattern = re.compile(r" - (.*?\s\(VFC\d+\))")

    def extract_cat(name):
        match = pattern.search(name)
        return match.group(1).strip() if match else "Unknown"

    df['Extracted Factor name'] = df['Factor name'].apply(extract_cat)
    df['Calculated Value'] = df.apply(
        lambda r: (r['NumReads'] * read_length / r['Gene length']) if r['Gene length'] > 0 else 0, axis=1
    )

    return df 