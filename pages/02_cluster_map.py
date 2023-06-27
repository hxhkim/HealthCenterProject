import streamlit as st
import folium
from folium import plugins
import common

common.page_config()

st.title("시군별 병원 및 의료센터")

data = common.get_data()

# '소재지' 컬럼 추가
data['소재지'] = data['소재지도로명주소'].str.split(' ').str[:2].apply(lambda x: ' '.join(x))

# 컬럼 순서 재정렬
data = data[['시군명', '병원명/센터명', '업무구분명', '대표전화번호', '소재지', '소재지도로명주소', '소재지지번주소', '소재지우편번호', '위도', '경도', '응급의료지원센터여부', '전문응급의료센터여부', '전문응급센터전문분야', '권역외상센터여부', '지역외상센터여부']]

# 소재지별 '병원명/센터명' 개수 데이터
hospital_counts = data.groupby('소재지')['병원명/센터명'].count().reset_index()

# Folium 지도 객체 생성
m = folium.Map(location=[data['위도'].mean(), data['경도'].mean()], zoom_start=10)

# 병원 및 센터 위치를 MarkerCluster에 추가
marker_cluster = plugins.MarkerCluster().add_to(m)

for idx, row in data.iterrows():
    popup_text = f"<b>병원/센터명:</b> {row['병원명/센터명']}<br>" \
                 f"<b>대표전화번호:</b> {row['대표전화번호']}"

    # 추가: '응급의료지원센터여부', '전문응급의료센터여부', '권역외상센터여부', '지역외상센터여부'에 'Y'가 있는 경우 popup_text에 추가
    if row['응급의료지원센터여부'] == 'Y':
        popup_text += "<br><b>응급의료지원센터여부:</b> Y"
    if row['전문응급의료센터여부'] == 'Y':
        popup_text += "<br><b>전문응급의료센터여부:</b> Y"
    if row['권역외상센터여부'] == 'Y':
        popup_text += "<br><b>권역외상센터여부:</b> Y"
    if row['지역외상센터여부'] == 'Y':
        popup_text += "<br><b>지역외상센터여부:</b> Y"

    folium.Marker(
        location=[row['위도'], row['경도']],
        popup=folium.Popup(popup_text, max_width=300)
    ).add_to(marker_cluster)


# 시군명 위에 '병원명/센터명' 개수를 표시하는 마커 생성
for idx, row in hospital_counts.iterrows():
    city = row['소재지']
    count = row['병원명/센터명']
    location = (data.loc[data['소재지'] == city, '위도'].mean(), data.loc[data['소재지'] == city, '경도'].mean())

    folium.Marker(
        location=location,
        icon=folium.DivIcon(
            html=f'<div style="font-weight: bold; color: red; font-size: 14px;">{count}</div>',
            icon_size=(30, 30),
            icon_anchor=(15, 15),
        ),
        tooltip=f'{city}: {count} hospitals/centers',
    ).add_to(m)

# 텍스트 설명 추가
st.sidebar.title("시군별 병원 및 의료센터")
st.sidebar.markdown("* 시군별 병원 및 의료센터 숫자와 위치를 알 수 있습니다.  \n* 위치를 클릭하면, 병원 이름과 대표 번호 및 특수 센터 보유 여부를 알 수 있습니다.")

# 지도 출력
folium(m)
