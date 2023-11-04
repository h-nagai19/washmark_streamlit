import streamlit as st
import requests
from PIL import Image
import base64

# 洗濯タグのクラス名リスト
class_names = ['30', '30_very_weak', '30_weak', '40', 
              '40_very_weak', '40_weak', '50', '50_weak', 
              '60', '60_weak', '70', '95', 'bleachable', 
              'bleachable_oxygen', 'donot_drycleaning', 
              'donot_ironing', 'donot_tumble_dry', 
              'donot_wetcleaning', 'drycleaning_F', 
              'drycleaning_F_weak', 'drycleaning_P', 
              'drycleaning_P_weak', 'flat_dry', 
              'flat_dry_shade', 'flat_dry_wet', 
              'flat_dry_wetshade', 'hand-wash', 
              'hanging_dry', 'hanging_dry_shade', 
              'hanging_dry_wet', 'hanging_dry_wetshade', 
              'ironing_upto110', 'ironing_upto150', 
              'ironing_upto200', 'not_bleachable', 
              'not_washable', 'tumble_dry_upto60', 
              'tumble_dry_upto80', 'weetcleaning_very_weak', 
              'wetcleaning_ok', 'wetcleaning_weak']

# 洗濯マークの意味リスト
mark_means = [
    '液温は30 ℃を限度とし、洗濯機で洗濯出来る', 
    '液温は30 ℃を限度とし、洗濯機で非常に弱い処理が出来る', 
    '液温は30 ℃を限度とし、洗濯機で弱い処理が出来る', 
    '液温は40 ℃を限度とし、洗濯機で洗濯出来る', 
    '液温は40 ℃を限度とし、洗濯機で非常に弱い処理が出来る', 
    '液温は40 ℃を限度とし、洗濯機で弱い処理が出来る', 
    '液温は50 ℃を限度とし、洗濯機で処理が出来る', 
    '液温は50 ℃を限度とし、洗濯機で弱い処理が出来る', 
    '液温は60 ℃を限度とし、洗濯機で処理が出来る', 
    '液温は60 ℃を限度とし、洗濯機で弱い処理が出来る', 
    '液温は70 ℃を限度とし、洗濯機で処理が出来る', 
    '液温は95 ℃を限度とし、洗濯機で処理が出来る', 
    '塩素系及び酸素系の漂白剤を使用して漂白ができる', 
    '酸素系漂白剤の使用はできるが塩素系漂白剤は使用禁止', 
    'ドライクリーニング禁止', 'アイロン仕上げ禁止', 
    'タンブル乾燥禁止', 'ウエットクリーニング禁止', 
    '石油系溶剤によるドライクリーニグができる（溶剤に2％の水添加）', 
    '石油系溶剤による弱いドライクリーニングができる', 
    'パークロロエチレン及び石油系溶剤によるドライクリーニングができる（溶剤に2％の水添加）', 
    'パークロロエチレン及び石油系溶剤による弱いドライクリーニングができる', 
    '平干しがよい', '日陰の平干しがよい', 
    'ぬれ平干しがよい', '日陰のぬれ平干しがよい', 
    '液温は40 ℃を限度とし、手洗いができる', 'つり干しがよい', 
    '日陰のつり干しがよい', 'ぬれつり干しがよい', 
    '日陰のぬれつり干しがよい', 
    '底面温度110 ℃を限度としてスチームなしでアイロン仕上げができる', 
    '底面温度150 ℃を限度としてアイロン仕上げができる', 
    '底面温度200 ℃を限度としてアイロン仕上げができる', 
    '塩素系及び酸素系漂白剤の使用禁止', 
    '家庭での洗濯禁止', 
    '低い温度でのタンブル乾燥ができる（排気温度上限60 ℃）', 
    'タンブル乾燥ができる（排気温度上限80 ℃）', 
    '非常に弱い操作のウエットクリーニングができる', 
    'ウエットクリーニングができる', 
    '弱い操作のウエットクリーニングができる'
]

st.title('洋服タグの洗濯マーク分類')

uploaded_file = st.file_uploader('画像ファイルを選択してください', type = ['jpg', 'jpeg', 'png'])
if uploaded_file is not None:

    # 画像ファイルの読み込み
    file = Image.open(uploaded_file)
    st.image(file, caption = 'アップロードされた画像')

    if st.button("実行"):

        # 画像のバイナリデータをBase64エンコード
        img_bytes = uploaded_file.getvalue()
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')

        # 予測の実行
        response = requests.post("https://wash-mark-api.onrender.com/predict", json={'file': img_base64})

        # 予測結果の表示
        result = response.json()["prediction"]

        # 重複を削除
        unique_tagnum_list = list(set(result))

        unique_tagnum_list = sorted(unique_tagnum_list)

        st.write('# ↓洗濯マークの予測結果！')
        for num in unique_tagnum_list:
            name = class_names[num]
            mean = mark_means[num]
            image = Image.open(f'tag_images/{name}.jpg')
            st.image(image, width=100)
            st.write(mean)
