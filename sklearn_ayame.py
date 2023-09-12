import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
warning=None
input_flg=0
default=0
st.title('scikit-learnを使って予測')
st.caption('scikit-learnであやめの分類を予測できます。独自の学習用CSVファイルをアップロードして予測もできます。')
st.markdown('###### 詳細は')
link = '[イチゲブログ](https://kikuichige.com/21772/)'
st.markdown(link, unsafe_allow_html=True)
import pandas as pd
# CSVファイルをアップロードするウィジェットを追加
uploaded_file = st.file_uploader("学習用CSVファイル（フォーマットはイチゲブログ参照）のアップロード", type=["csv"])

try:
    # アップロードされたファイルが存在する場合
    if uploaded_file is not None:
        # アップロードされたファイルをデータフレームに読み込む
        df = pd.read_csv(uploaded_file)
        X=df[['koumoku1','koumoku2','koumoku3','koumoku4']]
        y=df['bunrui']
    else:
        default=1
        df=pd.read_csv('Iris.csv')
        X=df[['SepalLengthCm','SepalWidthCm','PetalLengthCm','PetalWidthCm']]
        y=df['Species']
    #     df=pd.read_csv('Iristest.csv')
    # X=df[['koumoku1','koumoku2','koumoku3','koumoku4']]
    # y=df['bunrui']
except:
    warning='読み込みエラー！デフォルトのあやめの分類を表示します。'
    df=pd.read_csv('Iris.csv')
    X=df[['SepalLengthCm','SepalWidthCm','PetalLengthCm','PetalWidthCm']]
    y=df['Species']

X_train,X_test,y_train,y_test=train_test_split(
    X,y,test_size=0.2,random_state=77
)
clf = RandomForestClassifier(random_state=77)
clf.fit(X_train, y_train)
pred=clf.predict(X_test)
accuracy=accuracy_score(y_test,pred)

with st.form(key='profile_form'):
    st.write('予測したいデータを入力してください')
    test_input=st.text_input('特徴量を4つ,区切りで入力してください。例、4.6,3.1,1.5,0.2')
    submit_btn=st.form_submit_button('予測表示')
    if test_input:
        ayame_list_input=test_input.split(',')
        if len(ayame_list_input)!=4:
            warning='4つの数字をカンマ区切りで入力してください'
        else:
            if warning=='読み込みエラー！デフォルトのあやめの分類を表示します。' or default==1:
                default=0
                data = {

                    'Id': [1],
                    'SepalLengthCm': ayame_list_input[0],
                    'SepalWidthCm': ayame_list_input[1],
                    'PetalLengthCm': ayame_list_input[2],
                    'PetalWidthCm': ayame_list_input[3],
                }
            else:
                data = {
                    'Id': [1],
                    'koumoku1': ayame_list_input[0],
                    'koumoku2': ayame_list_input[1],
                    'koumoku3': ayame_list_input[2],
                    'koumoku4': ayame_list_input[3],
                }
            input_flg=1
            ask = pd.DataFrame(data).drop(['Id'], axis=1)
            predicted=clf.predict(ask)
    if submit_btn:
        if not warning:
            if input_flg==1:
                st.write(f'種類予測: {predicted[0]}')
        elif warning=='読み込みエラー！デフォルトのあやめの分類を表示します。':
            st.write(warning)
            if input_flg==1:
                st.write(f'種類予測: {predicted[0]}')
        else:
            st.write(warning)
        warning = None
