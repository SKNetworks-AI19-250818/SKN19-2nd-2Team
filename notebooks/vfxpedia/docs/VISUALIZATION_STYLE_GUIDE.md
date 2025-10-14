# 📊 팀 시각화 스타일 가이드

> **목적**: 팀원들 간의 시각화 스타일을 통일하여 일관성 있는 분석 자료 생성  
> **기준**: sosodoit 팀장님의 `eda__basic_household.ipynb` 스타일

---

## 🎨 기본 설정

### 1. 폰트 및 팔레트 설정

```python
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns

# 폰트 설정 (팀 통일)
try:
    font_path = r'C:\Windows\Fonts\HMFMMUEX.TTC'  # 함초롱바탕
    font_name = fm.FontProperties(fname=font_path).get_name()
    plt.rc('font', family=font_name)
except:
    plt.rcParams['font.family'] = 'Malgun Gothic'  # 폰트 없을 경우 대체

plt.rcParams['axes.unicode_minus'] = False

# 팀 통일 색상 팔레트
TEAM_COLORS = {
    'primary': 'skyblue',      # 주요 색상 (단일 그래프)
    'success': '#ff7f0e',      # 주황 (흡연이탈/성공)
    'danger': '#1f77b4',       # 파랑 (흡연유지/실패)
    'palette': 'husl'          # 다중 색상
}
```

---

## 📐 Figure 크기 가이드

| 그래프 타입 | figsize | 용도 |
|------------|---------|------|
| **단일 그래프** | `(6, 3)` | 막대, 히스토그램, 박스플롯 |
| **2개 subplot** | `(12, 3)` | 비교 분석 (1x2) |
| **4개 subplot** | `(12, 6)` | 다중 비교 (2x2) |
| **8개 subplot** | `(16, 6)` | 변수 분포 (2x4) |
| **히트맵** | `(16, 14)` | 상관관계 히트맵 |

---

## 🎯 그래프별 스타일 가이드

### 📊 막대그래프 (Barplot)

```python
# 단일 막대그래프
plt.figure(figsize=(6, 3))
sns.barplot(data=df, x='category', y='value', color=TEAM_COLORS['primary'])
plt.title('제목', fontsize=14)
plt.xlabel('X축 라벨')
plt.ylabel('Y축 라벨')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# 비교 막대그래프 (churn 비교)
colors = [TEAM_COLORS['danger'], TEAM_COLORS['success']]
plt.bar(x, height, color=colors)
plt.legend(['실패', '성공'])
```

### 📈 히스토그램 (Histogram)

```python
plt.figure(figsize=(6, 3))
sns.histplot(data=df, x='variable', 
             bins=20, 
             color=TEAM_COLORS['primary'],
             kde=True,              # KDE 곡선 추가
             edgecolor='black',
             alpha=0.7)
plt.title('분포', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
```

### 📦 박스플롯 (Boxplot)

```python
plt.figure(figsize=(6, 3))
sns.boxplot(data=df, x='category', y='value', 
            color=TEAM_COLORS['primary'])
plt.title('제목', fontsize=14)
plt.xticklabels(['라벨1', '라벨2'])
plt.tight_layout()
plt.show()
```

### 📉 선 그래프 (Lineplot)

```python
plt.figure(figsize=(6, 3))
sns.lineplot(data=df, x='x', y='y', marker='o')
plt.title('제목', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
```

### 🔥 히트맵 (Heatmap)

```python
plt.figure(figsize=(16, 14))
sns.heatmap(corr_matrix, 
            annot=False,
            cmap='coolwarm',
            center=0,
            vmin=-1, vmax=1,
            square=True,
            linewidths=0.5,
            cbar_kws={'label': '상관계수'})
plt.title('상관관계 히트맵', fontsize=14)
plt.tight_layout()
plt.show()
```

---

## ✅ 체크리스트

시각화 작성 시 다음 사항을 확인하세요:

- [ ] 폰트: HMFMMUEX.TTC 또는 Malgun Gothic
- [ ] 색상: TEAM_COLORS 사용
- [ ] Figure 크기: 가이드에 맞는 크기
- [ ] 제목: fontsize=14 (fontweight 제거)
- [ ] 그리드: `plt.grid(axis='y', linestyle='--', alpha=0.7)` 
- [ ] 레이아웃: 항상 `plt.tight_layout()` 호출
- [ ] churn 비교: danger(실패) + success(성공) 색상 사용
- [ ] 한글 라벨: Variable Decoder 활용

---

## 🚫 피해야 할 것들

```python
# ❌ 피해야 할 스타일
plt.rcParams['font.family'] = 'Malgun Gothic'  # HMFMMUEX 우선
sns.set_palette("husl")                         # TEAM_COLORS 사용
fontweight='bold'                               # 일반 굵기 사용
figsize=(14, 5)                                 # 가이드 크기 준수
color='coral'                                   # TEAM_COLORS['primary']
```

---

## 💡 팁

1. **Variable Decoder 활용**: 변수명을 한글로 표시
   ```python
   var_label = decoder.get_variable_label('variable_name')
   plt.title(f'{var_label} 분포', fontsize=14)
   ```

2. **일관성 있는 churn 표시**: 
   - 0 = 실패 (빨강)
   - 1 = 성공 (초록)

3. **Grid 사용**: 데이터 읽기 쉽게
   ```python
   plt.grid(axis='y', linestyle='--', alpha=0.7)
   ```

---

## 📁 참고 파일

- **기준 파일**: `notebooks/sosodoit/eda__basic_household.ipynb`
- **적용 예시**: 
  - `notebooks/vfxpedia/eda/01_data_overview.ipynb`
  - `notebooks/vfxpedia/eda/02_decoder_test.ipynb`

---

**작성일**: 2025-10-09  
**작성자**: vfxpedia  
**기준**: sosodoit 팀장님 스타일

