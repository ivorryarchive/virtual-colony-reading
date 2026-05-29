#! /Work1/HOME/eonebi/anaconda3/envs/streamlit_env/bin/python3

import pandas as pd 
import matplotlib as plt
import numpy as np
import io
import streamlit as st
from PIL import Image, ImageDraw

# def generate_plate_view(data: pd.DataFrame, data_type: str, taxonomy_level: str = None, color_by: str) -> plt.Figure:
#     ''' 사용자가 선택한 옵션 조합에 따라 Matplotlib 함수를 엮어 최종 plate 이미지를 객체로 반환하는 함수'''

#     RADIUS = 10
#     title_text = f""


# 내부 전용 헬퍼 함수
# ------------------------------------
# 시각화 보조 함수 (Utility Functions)
# ------------------------------------
def setup_plot(radius, title):
    ''' 그래프의 기본 배경 설정'''

    fig, ax = plt.subplots(figsize=(15, 10))
    circle = plt.Circle((0,0), radius, color='ivory', alpha=0.6, ec='black')
    ax.add_artist(circle)

    ax.axhline(0, color='black', linewidth=0.5, alpha=0.5)
    ax.axvline(0, color='black', linewidth=0.5, alpha=0.5)
    
    limit = radius * 1.1
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.set_title(title, fontsize=20, pad=20)
    return fig, ax

def get_quadrants(value, is_vf=False):
    '''값에 따라 점이 찍힐 사분면 리스트 반환'''

    if not is_vf:  # Taxonomy (Relative Abundance 0~1)
        if value <= 0.25: return [2]
        if value <= 0.50: return [1, 2]
        if value <= 0.75: return [1, 2, 4]
        return [1, 2, 3, 4]
    else:  # VF (Calculated Value)
        if value <= 0.5: return [2]
        if value <= 1.0: return [1, 2]
        if value <= 2.0: return [1, 2, 4]
        return [1, 2, 3, 4]

def plot_point_in_quadrant(ax, quadrant,  radius, color, val, label=None):
    '''지정된 사분면 내의 랜덤한 위치에 점 그리기'''

    quadrant_angles = {
        1: (0, np.pi/2),
        2: (np.pi/2, np.pi),
        3: (np.pi, 3*np.pi/2),
        4: (3*np.pi/2, 2*np.pi)
    }

    min_a, max_a = quadrant_angles[quadrant]
    theta = np.random.uniform(min_a + 0.12, max_a - 0.12)
    r = np.random.uniform(radius * 0.2, radius * 0.95)

    x, y = r * np.cos(theta), r * np.sin(theta)
    
    # 값의 크기에 따른 마커 사이즈 결정
    if val >= 0.1: size = 40
    elif val >= 0.01: size = 30
    elif val >= 0.001: size = 20
    else: size = 10

    ax.plot(x, y, 'o', color=color, markersize=size, label=label, alpha=0.75)

# ------------------------------------
# Color By
# ------------------------------------
def get_gram_color(taxon_name, file_type):
    '''박테리아 명칭을 기반으로 Gram Stain 색상 반환'''
    
    # Heuristic 
    pos = {'Bacillota', 'Firmicutes', 'Actinomycetota', 'Actinobacteria'}
    neg = {'Bacteroidota', 'Bacteroidetes', 'Pseudomonadota', 'Proteobacteria', 'Verrucomicrobiota', 'Acidobacteriota', 
        'Fusobacteriota', 'Desulfobacterota', 'Thermodesulfobacteriota', 'Campylobacterota'}

    parts = taxon_name.split(';' if file_type == 'gtdb' else '|')
    phylum = next((p.split('__')[1] for p in parts if p.startswith('p__')), "")

    if any(p in phylum for p in pos): return 'purple'
    if any(p in phylum for p in neg): return 'red'
    return 'gray'

# each-taxon 색상 반환
# def get_taxon_color 