import folium
import streamlit as st
from streamlit_folium import st_folium, folium_static
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import time
import datetime

        
#-----------------------------------------------------------------------------------------------------------------------------------------------------
      
# scatter차트 생성 함수
def chart(df_filtered):
    fig = px.scatter(df_filtered, x="수용가능인원", y="현재인원", size="포화도(%)", color="포화도(%)", hover_name="대피소명",
                     log_x=True, size_max=60)
    return fig

# 비디오 재생 함수
def video_all():
    if (video_index == 1):
        video = "https://www.youtube.com/embed/ODX6mCjBr3I"
    elif (video_index == 2):
        video = "https://www.youtube.com/embed/-_UqxQrhwuc"
    elif (video_index == 3):
        video = "https://www.youtube.com/embed/-IoikvAQ4VI"
    else:
        video = "https://www.youtube.com/embed/-IoikvAQ4VI"

    html = f"""<!DOCTYPE html>
                 <html>
                 <iframe width="650" height="400" 
                 src="{video}" title="YouTube video player" 
                 frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; 
                 gyroscope; picture-in-picture; web-share" allowfullscreen></iframe> </html> """

    return html



#------------------------------------------------------------------------------------------------------------------------------------------------------

st.set_page_config(layout='wide')

# 지진, 공습 두 가지의 재난 선택 가능
dis, empt= st.columns([0.1,1])
with dis:
    dis_list = ['지진', '공습']
    dis = st.selectbox('재난선택',dis_list, label_visibility="hidden" )
with empt:
    pass

st.write('')
st.write('')

html = """<!DOCTYPE html>
<html>
<img src = "https://aivle.edu.kt.co.kr/tpl/001/img/common/logo.svg" alt = 에이블로고 style="float: left; width:100px; height:30px;"> </img>
</html>"""
st.markdown(html, unsafe_allow_html=True)

if dis == '지진':
    disaster = '옥외대피소_포화도추가.csv' 
else:
    disaster = '민방위_데이터_최종.csv'

# 재난일시, 내용 title
if disaster == '민방위_데이터_최종.csv':
    st.title('🚨오늘 6시 32분 대한민국 전역에 공습경보 발령')
else:
    st.title('🚨01월 09일 01:28 서쪽 26km해역 규보 7.0 지진 발생')

# 데이터프레임 가공
data_real = pd.read_csv(disaster) 
si_list = data_real['시'].unique()
gu={}
dong = {}
for i in si_list:
    df = data_real.loc[data_real['시']==i]
    gu_list = list(df['구'].unique())
    gu[i] = {}
    gu[i].update({'-':''})
    for j in gu_list: 
        gu[i].update({j:''})

for i in si_list:
    for j in gu[i]:
        df = data_real.loc[(data_real['시'] == i) & (data_real['구']==j)]
        gu_list =['-']
        for k in list(df['읍면동'].unique()):
            gu_list.append(k)
        gu[i][j] = gu_list

data_real['비율'] = data_real['비율'] * 100
data_real['비율'] = round(data_real['비율'], 2)
data_real.rename(columns={'비율':'포화도(%)'}, inplace=True)
data_real['CCTV보기'] = False

# 상단에 시간을 띄워줌
times, empty= st.columns([1,1])

# selectbox 레이아웃
col1, col2, col3 = st.columns(3)

# 대피소가 마킹된 지도와 리스트 레이아웃
map1, daepi_list = st.columns([1,0.85])
# 대한민국 시도 리스트

sido = ['-']
for i in si_list:
    sido.append(i)

# 각 시도에 맞는 시군구리스트, 읍면동리스트 select박스로 리스트화
with col1:
    sido_choice = st.selectbox('시도', sido, key='sido_selectbox')
    
with col2:
    if sido_choice != '-':
        sigungu = gu[sido_choice]
        sigungu_choice = st.selectbox('시군구', sigungu, key='sigungu_selectbox')
    else:
        sigungu_choice = st.selectbox('시군구', ['-'], key='sigungu_selectbox')

with col3:
    if sigungu_choice != '-':
        dongu = gu[sido_choice][sigungu_choice]
        dong_choice = st.selectbox('읍면동', dongu, key='dongu_selectbox')
    else:
        dong_choice = st.selectbox('읍면동', ['-'], key='dongu_selectbox')

cond1 = data_real['시'] == sido_choice
cond2 = data_real['구'] == sigungu_choice
cond3 = data_real['읍면동'] == dong_choice


a='yes'
b='yes'

# selectbox 선택사항에 따른 데이터프레임 필터링, 지도 시각화
with map1:
    if sido_choice == '-':
        b = 'no'
    elif sigungu_choice == '-' and dong_choice == '-':
        data_choice = data_real.loc[cond1].copy()
        data_choice = data_choice[['대피소명', '수용가능인원', '현재인원', '포화도(%)', '위도', '경도', '담당자 연락처']].copy()
        biyul = data_choice['포화도(%)'].values
        lat = data_choice['위도'].values
        lon = data_choice['경도'].values
        daepi = data_choice['대피소명'].values
        m = folium.Map(location = [lat[0],lon[0]], zoom_start = 13 )
      
    elif dong_choice == '-':
        data_choice = data_real.loc[cond1 & cond2].copy()
        data_choice = data_choice[['대피소명', '수용가능인원', '현재인원', '포화도(%)', '위도', '경도', '담당자 연락처']].copy()
        biyul = data_choice['포화도(%)'].values
        lat = data_choice['위도'].values
        lon = data_choice['경도'].values
        daepi = data_choice['대피소명'].values
        m = folium.Map(location = [lat[0],lon[0]], zoom_start = 14 )

    else:
        data_choice = data_real.loc[cond1 & cond2 & cond3].copy()
        data_choice = data_choice[['대피소명', '수용가능인원', '현재인원', '포화도(%)', '위도', '경도', '담당자 연락처']].copy()
        biyul = data_choice['포화도(%)'].values
        lat = data_choice['위도'].values
        lon = data_choice['경도'].values
        daepi = data_choice['대피소명'].values
        m = folium.Map(location = [lat[0],lon[0]], zoom_start = 15 )

    
    if b == 'no':
        m = folium.Map(location = [37.5502, 126.982], zoom_start = 11 )            
        st_data_r = folium_static(m, width=700, height=400)
    else:
        for i in range(len(data_choice)):
            if biyul[i] >= 80.0:
                folium.Marker([lat[i], lon[i]] ,popup=daepi[i], tooltip=daepi[i], icon=folium.Icon('red'), ).add_to(m)
            elif biyul[i] >= 50.0:
                folium.Marker([lat[i], lon[i]] ,popup=daepi[i], tooltip=daepi[i], icon=folium.Icon('orange')).add_to(m)
            else:
                folium.Marker([lat[i], lon[i]] ,popup=daepi[i], tooltip=daepi[i], icon=folium.Icon('green')).add_to(m)            
        st_data_r = folium_static(m, width=700, height=400)


# selectbox 선택사항에 따른 체크박스기능이 추가된 데이터프레임 시각화
with daepi_list:
    if sido_choice == '-':
        a = 'no'
    elif sigungu_choice == '-' and dong_choice == '-':
        data_choice = data_real.loc[cond1]
    elif dong_choice == '-':
        data_choice = data_real.loc[cond1 & cond2]
    else:
        data_choice = data_real.loc[cond1 & cond2 & cond3]

    if a == 'no':
        gd = GridOptionsBuilder.from_dataframe(data_real[['대피소명', '수용가능인원', '현재인원', '포화도(%)','담당자 연락처']])
        gd.configure_selection(selection_mode='single', use_checkbox=True)
        gridoptions = gd.build()
        grid_table = AgGrid(data_real[['대피소명', '수용가능인원', '현재인원', '포화도(%)', 'CCTV보기', '담당자 연락처']],width=600, height=350, 
                            gridOptions=gridoptions, update_mode=GridUpdateMode.SELECTION_CHANGED, columns_auto_size_mode=1, 
                            fit_columns_on_grid_load=False)
    else:
        gd = GridOptionsBuilder.from_dataframe(data_choice[['대피소명', '수용가능인원', '현재인원', '포화도(%)', '담당자 연락처']])
        gd.configure_selection(selection_mode='single', use_checkbox=True)
        gridoptions = gd.build()
        grid_table = AgGrid(data_choice[['대피소명', '수용가능인원', '현재인원', '포화도(%)', 'CCTV보기', '담당자 연락처']],width=600, 
                            height=350, gridOptions=gridoptions, update_mode=GridUpdateMode.SELECTION_CHANGED, columns_auto_size_mode=1,
                           fit_columns_on_grid_load=False)


mark1, mark2 = st.columns([1,1])

with mark1:
    st.info('포화도 그래프')
with mark2:
    st.info('CCTV')

chart1, video1 = st.columns([1,1])

# selectbox 선택사항에 따른 scatter차트 시각화
with chart1:
    if sido_choice == '-' and sigungu_choice == '-' and dong_choice == '-':
        fig = chart(data_real)
        st.plotly_chart(fig, use_container_width=True)
    elif sigungu_choice == '-' and dong_choice == '-':
        fig = chart(data_choice)
        st.plotly_chart(fig, use_container_width=True)
    elif dong_choice == '-':
        fig = chart(data_choice)
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig = chart(data_choice)
        st.plotly_chart(fig, use_container_width=True)

# 선택된 row에 맞는 cctv영상 송출
with video1:
    selected_row = grid_table["selected_rows"]
    
    if selected_row:
        video_index = selected_row[0]["_selectedRowNodeInfo"]["nodeRowIndex"]
        location_name = selected_row[0]['대피소명']
        html = video_all()
        components.html(html, width=650, height=400)
    else:
        st.write('')


# 상단에 경과시간 표시(1초마다 갱신되게함)
with times:
    ph = st.empty()   
    for i in range(5000):
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        time_to_subtract = datetime.timedelta(hours=5, minutes=48)  
        result_time = (datetime.datetime.strptime(current_time, '%H:%M:%S') - time_to_subtract).strftime('%H:%M:%S')
        ph.metric('## 재난발생 후',result_time+' 경과')
        time.sleep(1)
with empty:
    pass