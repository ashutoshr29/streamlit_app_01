# streamlit run st_up_history.py
import streamlit as st
import requests

st.set_page_config(page_title='QP App01', layout='wide', initial_sidebar_state="collapsed",)

col = st.columns(3)
client_id = col[0].text_input("client id")
client_secret = col[1].text_input("client Secret")
redirect_uri = col[2].text_input("redirect url")

link1 = f'https://api.upstox.com/v2/login/authorization/dialog?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}'
btn_tkn_link = st.link_button("Token Link", link1,help=None, type="secondary", icon=None, disabled=False, use_container_width=False)

token_code = st.text_input("Code")


if 'acc_tkn' not in st.session_state:
    st.session_state['acc_tkn'] = '123'

st.write(st.session_state['acc_tkn'])

@st.cache_data
def login():
    url = "https://api.upstox.com/v2/login/authorization/token"
    headers = {'Content-Type': 'application/x-www-form-urlencoded','Accept': 'application/json'}
    payload={'code': token_code, 'client_id': client_id, 'client_secret': client_secret, 'redirect_uri': redirect_uri, 'grant_type': 'authorization_code'}

    response = requests.request("POST", url, headers=headers, data=payload)
    st.session_state['acc_tkn'] = response.json()['access_token']

    # st.write(st.session_state['acc_tkn'])
    st.write("Login Ok")
    st.toast('Login Successfully')


def profile():
    url = 'https://api.upstox.com/v2/user/profile'
    headers = {'Accept': 'application/json','Authorization': 'Bearer '+ st.session_state['acc_tkn']}
    response = requests.get(url, headers=headers)

    if response.json()['status'] == "error":
        st.write("Error in Profile")
        st.toast('Profile Error')
    else:
        user = response.json()['data']['user_id']
        st.write(user)
        st.toast('Profile Successfully')

col = st.columns(4)
btn_lgn = col[0].button("Login", on_click=login)
btn_prof = col[1].button("Profile", on_click=profile)


def ltp():
    url = 'https://api.upstox.com/v2/market-quote/ltp?instrument_key='+stock_key
    headers = {'Accept': 'application/json','Authorization': 'Bearer '+ st.session_state['acc_tkn']}

    response = requests.get(url, headers=headers)
    
    if response.json()['status'] == "error":
        st.write("Error in LTP")
    else:
        st.write(response.json()["data"])
    st.toast('LTP Ok')

col = st.columns(3)
stock_key = col[0].text_input("Stock Key", value="NSE_INDEX|Nifty 50")
btn_ltp = col[1].button("LTP", on_click=ltp)
