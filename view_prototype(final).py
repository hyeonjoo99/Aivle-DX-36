import folium
import json
import urllib
from urllib.request import Request, urlopen
import streamlit as st
from streamlit_folium import st_folium, folium_static
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import time
import datetime
# def get_location(loc) :
#     client_id = 'xxjiuvgdum'
#     client_secret = 'zs8BuNezQMQnUVj3y5tsOpcCFDfb0dAfYN6TEN6F'
#     url = f"https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query=" \
#     			+ urllib.parse.quote(loc)
    
#     # 주소 변환
#     request = urllib.request.Request(url)
#     request.add_header('X-NCP-APIGW-API-KEY-ID', client_id)
#     request.add_header('X-NCP-APIGW-API-KEY', client_secret)
    
#     response = urlopen(request)
#     res = response.getcode()
    
#     if (res == 200) : # 응답이 정상적으로 완료되면 200을 return한다
#         response_body = response.read().decode('utf-8')
#         response_body = json.loads(response_body)
#         print(response_body)
#         # 주소가 존재할 경우 total count == 1이 반환됨.
#         if response_body['meta']['totalCount'] == 1 : 
#         	# 위도, 경도 좌표를 받아와서 return해 줌.
#             lat = response_body['addresses'][0]['y']
#             lon = response_body['addresses'][0]['x']
#             return (lon, lat)
#         else :
#             pass
#             # print('location not exist')
        
#     else :
#         print('ERROR')

# def get_optimal_route(start, goal, option='' ):
#     # waypoint는 최대 5개까지 입력 가능, 
#     # 구분자로 |(pipe char) 사용하면 됨(x,y 좌표값으로 넣을 것)
#     # waypoint 옵션을 다수 사용할 경우, 아래 함수 포맷을 바꿔서 사용 
#     client_id = 'xxjiuvgdum'
#     client_secret = 'zs8BuNezQMQnUVj3y5tsOpcCFDfb0dAfYN6TEN6F' 
#     # start=/goal=/(waypoint=)/(option=) 순으로 request parameter 지정
#     url = f"https://naveropenapi.apigw.ntruss.com/map-direction-15/v1/driving?start={start[0]},{start[1]}&goal={goal[0]},{goal[1]}&option={option}"
#     request = urllib.request.Request(url)
#     request.add_header('X-NCP-APIGW-API-KEY-ID', client_id)
#     request.add_header('X-NCP-APIGW-API-KEY', client_secret)
    
#     response = urllib.request.urlopen(request)
#     res = response.getcode()
    
#     if (res == 200) :
#         response_body = response.read().decode('utf-8')
#         results = json.loads(response_body)
#         return results
            
#     else :
#         print('ERROR')
        
#-----------------------------------------------------------------------------------------------------------------------------------------------------
# si_list = ['경상북도', '전라남도', '경기도', '서울특별시', '대구광역시', '울산광역시', '경상남도',
#        '제주특별자치도', '전라북도', '충청북도', '충청남도', '대전광역시', '광주광역시', '인천광역시',
#        '부산광역시', '강원특별자치도']        

data_real = pd.read_csv('옥외대피소_포화도추가.csv')
si_list = data_real['시'].unique()
gu={}
dong = {}
for i in si_list:
    df = data_real.loc[data_real['시']==i]
    # df['구'].unique()
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




#------------------------------------------------------------------------------------------------------------------------------------------------------


def chart(df_filtered):
    fig = px.scatter(df_filtered, x="수용가능인원", y="현재인원", size="포화도(%)", color="포화도(%)", hover_name="대피소명",
                     log_x=True, size_max=60)
    return fig


def video_all():
    if (video_index == 1):
        video = "https://www.youtube.com/embed/ODX6mCjBr3I"
    elif (video_index == 2):
        video = "https://www.youtube.com/embed/-_UqxQrhwuc"
    elif (video_index == 3):
        video = "https://www.youtube.com/embed/-IoikvAQ4VI"
    else:
        video = "https://www.youtube.com/embed/o3hLUAksfRU"

    html = f"""<!DOCTYPE html>
                 <html>
                 <iframe width="650" height="400" 
                 src="{video}" title="YouTube video player" 
                 frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; 
                 gyroscope; picture-in-picture; web-share" allowfullscreen></iframe> </html> """

    return html


# 페이지 설정 함수 호출


#------------------------------------------------------------------------------------------------------------------------------------------------------


sido = ['-', '서울특별시', '부산광역시', '대구광역시', '인천광역시', '광주광역시', '대전광역시', '울산광역시', '경기도', '충청북도', '충청남도', '전라북도', '전라남도', '경상북도', '경상남도', '강원특별자치도', '제주특별자치도']


st.set_page_config(layout='wide')

# with open( "style.css" ) as css:
#     st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)


html = """<!DOCTYPE html>
<html>
<img src = "https://aivle.edu.kt.co.kr/tpl/001/img/common/logo.svg" alt = 에이블로고 style="float: left; width:100px; height:30px;"> </img>
</html>"""
st.markdown(html, unsafe_allow_html=True)

st.title('🚨01월 09일 01:28 서쪽 26km해역 규보 7.0 지진 발생')



times, empty= st.columns([1,1])


col1, col2, col3 = st.columns(3)

map1, daepi_list = st.columns([1,0.8])



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
        # cctv = data_choice['CCTV보기'].values
        m = folium.Map(location = [lat[0],lon[0]], zoom_start = 13 )
      
    elif dong_choice == '-':
        data_choice = data_real.loc[cond1 & cond2].copy()
        data_choice = data_choice[['대피소명', '수용가능인원', '현재인원', '포화도(%)', '위도', '경도', '담당자 연락처']].copy()
        biyul = data_choice['포화도(%)'].values
        lat = data_choice['위도'].values
        lon = data_choice['경도'].values
        daepi = data_choice['대피소명'].values
        # cctv = data_choice['CCTV보기'].values
        m = folium.Map(location = [lat[0],lon[0]], zoom_start = 14 )

    else:
        data_choice = data_real.loc[cond1 & cond2 & cond3].copy()
        data_choice = data_choice[['대피소명', '수용가능인원', '현재인원', '포화도(%)', '위도', '경도', '담당자 연락처']].copy()
        biyul = data_choice['포화도(%)'].values
        lat = data_choice['위도'].values
        lon = data_choice['경도'].values
        daepi = data_choice['대피소명'].values
        # cctv = data_choice['CCTV보기'].values
        m = folium.Map(location = [lat[0],lon[0]], zoom_start = 15 )

    
    if b == 'no':
        m = folium.Map(location = [37.5502, 126.982], zoom_start = 11 )            
        st_data_r = folium_static(m, width=700, height=400)
    else:
        # st.dataframe(data_choice)
        for i in range(len(data_choice)):
            if biyul[i] >= 80.0:
                folium.Marker([lat[i], lon[i]] ,popup=daepi[i], tooltip=daepi[i], icon=folium.Icon('red'), ).add_to(m)
            elif biyul[i] >= 50.0:
                folium.Marker([lat[i], lon[i]] ,popup=daepi[i], tooltip=daepi[i], icon=folium.Icon('orange')).add_to(m)
            else:
                folium.Marker([lat[i], lon[i]] ,popup=daepi[i], tooltip=daepi[i], icon=folium.Icon('green')).add_to(m)            
        st_data_r = folium_static(m, width=700, height=400)

 
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
        grid_table = AgGrid(data_real[['대피소명', '수용가능인원', '현재인원', '포화도(%)', 'CCTV보기', '담당자 연락처']],width=400, height=350, gridOptions=gridoptions, update_mode=GridUpdateMode.SELECTION_CHANGED, columns_auto_size_mode=1)
        
        # st.dataframe(data_real[['대피소명', '수용가능인원', '현재인원', '포화도(%)', 'CCTV보기']])
        # st.data_editor(
        # data_real[['대피소명', '수용가능인원', '현재인원', '포화도(%)', 'CCTV보기']],
        # column_config={
        #     "CCTV보기": st.column_config.CheckboxColumn(
        #         "CCTV보기",
        #         default=False)},
        #     hide_index=False)
    else:
        gd = GridOptionsBuilder.from_dataframe(data_choice[['대피소명', '수용가능인원', '현재인원', '포화도(%)', '담당자 연락처']])
        gd.configure_selection(selection_mode='single', use_checkbox=True)
        gridoptions = gd.build()
        grid_table = AgGrid(data_choice[['대피소명', '수용가능인원', '현재인원', '포화도(%)', 'CCTV보기', '담당자 연락처']],width=400, height=350, gridOptions=gridoptions, update_mode=GridUpdateMode.SELECTION_CHANGED, columns_auto_size_mode=1)
        # st.dataframe(data_choice[['대피소명', '수용가능인원', '현재인원', '포화도(%)', 'CCTV보기']])
        # st.data_editor(
        # data_choice[['대피소명', '수용가능인원', '현재인원', '포화도(%)', 'CCTV보기']],
        # column_config={
        #     "CCTV보기": st.column_config.CheckboxColumn(
        #         "CCTV보기",
        #         default=False)},
        #     hide_index=False)
        

# df_result = data_real[['대피소명', '수용가능인원', '현재인원', '포화도(%)']]
mark1, mark2 = st.columns([1,1])
with mark1:
    st.info('포화도 그래프')
with mark2:
    st.info('CCTV')

chart1, video1 = st.columns([1,1])


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

with video1:
    selected_row = grid_table["selected_rows"]
    
    if selected_row:
        video_index = selected_row[0]["_selectedRowNodeInfo"]["nodeRowIndex"]
        location_name = selected_row[0]['대피소명']
        html = video_all()
        components.html(html, width=650, height=400)
    else:
        st.write('')
    # st.write(selected_row[0]['대피소명'])


# if sido_choice == '-' and sigungu_choice == '-' and dong_choice == '-':
#     fig = chart(data_real)
#     st.plotly_chart(fig, use_container_width=True)
# elif sigungu_choice == '-' and dong_choice == '-':
#     fig = chart(data_choice)
#     st.plotly_chart(fig, use_container_width=True)
# elif dong_choice == '-':
#     fig = chart(data_choice)
#     st.plotly_chart(fig, use_container_width=True)
# else:
#     fig = chart(data_choice)
#     st.plotly_chart(fig, use_container_width=True)

with times:
    ph = st.empty()   
    for i in range(5000):
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        time_to_subtract = datetime.timedelta(hours=5, minutes=48)  
        result_time = (datetime.datetime.strptime(current_time, '%H:%M:%S') - time_to_subtract).strftime('%H:%M:%S')
        # st.write(time.strftime('%H:%M:%S'))
        ph.metric('## 재난발생 후',result_time+' 경과')
        time.sleep(1)
with empty:
    pass