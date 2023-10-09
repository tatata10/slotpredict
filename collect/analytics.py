# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 16:54:49 2023

@author: kawai taichi
"""

from .dataDao import dataDao
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression # 線形回帰モデル
from sklearn.metrics import mean_squared_error # 平均二乗誤差
#from flask import Flask, make_response
import io
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB# 分類器の学習


class analytics():
    def __init__(self):
        self.result1 = ""
        self.my_array = []
        
    #並びでどの程度設定を入れるかを見つける
    def regression_analysis(self, date1, date2):
        #回帰分析をするデータをデータベースから取得する
        dao = dataDao()
        data_arr = dao.select_data(date1, date2)
        model = LinearRegression() # モデルのインスタンスを作成
        # DataFrameを作成
        #df = pd.DataFrame(data_arr[1:], columns=[data_arr[0,0],data_arr[0,1],data_arr[0,2],data_arr[0,3],data_arr[0,4],data_arr[0,5],data_arr[0,6],data_arr[0,7],data_arr[0,8],data_arr[0,0]])
        # データセットの読み込み
        #boston = load_boston()
        X = []
        y = []
        for i in range(0,len(data_arr)):
            j = i+1
            if j<len(data_arr):
                X.append(data_arr[i].difference) # 部屋数
                y.append(data_arr[j].difference) # 住宅価格
                
        X = np.array(X) # リストをNumPyの配列に変換
        y = np.array(y) # リストをNumPyの配列に変換
            
        # データの可視化
        plt.scatter(X, y) # 散布図をプロット
        fig = plt.gcf() # 現在のfigureオブジェクトを取得
        plt.xlabel("左の台") # x軸のラベル
        plt.ylabel("その隣の台") # y軸のラベル
        
        
        canvas = FigureCanvasAgg(fig) # キャンバスオブジェクトを作成
        response = HttpResponse(content_type='image/png') # レスポンスオブジェクトを作成
        canvas.print_png(response) # PNG形式でグラフを出力し、レスポンスに書き込む
        
         # 線形回帰モデルの作成
        
        model.fit(X.reshape(-1, 1), y) # モデルにデータを学習させる
                
# =============================================================================
#         # 図をpngデータとしてバッファに保存する
#         buf = io.BytesIO() # バッファの作成
#         plt.savefig(buf, format="png") # バッファにpngデータとして保存
#         plot_data = buf.getvalue() # バッファからバイナリデータを取得
# =============================================================================
        
       
        
        # 回帰係数と切片を表示
        print("Coef:", model.coef_) # 回帰係数（傾き）
        print("Intercept:", model.intercept_) # 切片
        
        # 回帰直線を描画
        
        
        plt.plot(X, model.predict(X.reshape(-1, 1)), color="red") # 回帰直線をプロット
        plt.xlabel("Rooms") # x軸のラベル
        plt.ylabel("Price") # y軸のラベル
        #plt.show()
        
        # モデルの評価（平均二乗誤差）
        mse = mean_squared_error(y, model.predict(X.reshape(-1, 1))) # 平均二乗誤差を計算
        #print("MSE:", mse) # 平均二乗誤差を表示
        
        return model,mse
    
    #設定投入台をランダムフォレストで予測する
    def predict_analytics(self, date1, date2):
        #回帰分析をするデータをデータベースから取得する
        dao = dataDao()
        data_arr = dao.select_data(date1, date2)
        
        data_value = data_arr.values("storeName","date","modelName","number","game","difference","BB","RB","allprobability",
        "BBprobability","RBprobability") # 辞書のリストに変換
        # DataFrameを作成
        df = pd.DataFrame(data_value)
        
        # 特徴量とラベルに分割
        X = df.drop(["box1", "box2"], axis=1) # box1とbox2以外のカラムを特徴量とする
        y = df[["box1", "box2"]] # box1とbox2をラベルとする
        
        # ランダムフォレストモデルの作成と学習
        model = RandomForestClassifier()
        model.fit(X, y)
        
        # 次回の予測を行う
        # test.csvは次回にボールを入れる前に確認した箱の状態を保存したファイルとする
        # カラムはbox1, box2, ball1, ball2, ..., weekday, dateとする
        test = pd.read_csv("test.csv")
        
        # ボールの数が変わっているかどうかをチェックする
        if len(test.columns) == len(df.columns): # ボールの数が変わっていない場合
            # 予測値を出力
            pred = model.predict(test.drop(["box1", "box2"], axis=1)) # box1とbox2以外のカラムを入力とする
            print(pred)
        else: # ボールの数が変わっている場合
            # ボールの数を取得する
            n_balls = len(test.columns) - 4 # weekdayとdateを除いたカラムの数がボールの数
            
            # 新しい特徴量を作成する
            new_X = test.copy() # testデータをコピーする
            new_X["n_balls"] = n_balls # ボールの数を新しいカラムとして追加する
            
            # 予測値を出力
            pred = model.predict(new_X.drop(["box1", "box2"], axis=1)) # box1とbox2以外のカラムを入力とする
            print(pred)
        
        return 
    
    #設定を確率ベクトルで予測する
    def predict_setting(self, date1, date2):
        #回帰分析をするデータをデータベースから取得する
        dao = dataDao()
        data_arr = dao.select_data(date1, date2)
        standard_arr = dao.standard_data()
        
# =============================================================================
#         data_value = data_arr.values("storeName","date","modelName","number","game","difference","BB","RB","allprobability",
#         "BBprobability","RBprobability") # 辞書のリストに変換
#         # DataFrameを作成
#         df = pd.DataFrame(data_value)
# =============================================================================
        
        for i in data_arr:
            # standard_dataから取得したデータ
            st_data = dao.standard_data(i.name)
            if st_data[0].allprobability == 0 & st_data[0].BBprobability == 0 & st_data[0].RBprobability == 0:
                return
            elif st_data[0].RBprobability == 0:
                p1 = [1/st_data[0].allprobability,1/st_data[0].BBprobability,]
                p2 = [1/st_data[1].allprobability,1/st_data[1].BBprobability,]
                p3 = [1/st_data[2].allprobability,1/st_data[2].BBprobability,]
                p4 = [1/st_data[3].allprobability,1/st_data[3].BBprobability,]
                p5 = [1/st_data[4].allprobability,1/st_data[4].BBprobability,]
                p6 = [1/st_data[5].allprobability,1/st_data[5].BBprobability,]
                
            elif st_data[0].RBprobability == 0:
                p1 = [1/st_data[0].allprobability,1/st_data[0].BBprobability,1/st_data[0].RBprobability,]
                p2 = [1/st_data[1].allprobability,1/st_data[1].BBprobability,1/st_data[1].RBprobability,]
                p3 = [1/st_data[2].allprobability,1/st_data[2].BBprobability,1/st_data[2].RBprobability,]
                p4 = [1/st_data[3].allprobability,1/st_data[3].BBprobability,1/st_data[3].RBprobability,]
                p5 = [1/st_data[4].allprobability,1/st_data[4].BBprobability,1/st_data[4].RBprobability,]
                p6 = [1/st_data[5].allprobability,1/st_data[5].BBprobability,1/st_data[5].RBprobability,]
                
            elif st_data[0].allprobability != 0 & st_data[0].BBprobability != 0 & st_data[0].RBprobability != 0:
                p1 = [1/st_data[0].allprobability,1/st_data[0].BBprobability,1/st_data[0].RBprobability,]
                p2 = [1/st_data[1].allprobability,1/st_data[1].BBprobability,1/st_data[1].RBprobability,]
                p3 = [1/st_data[2].allprobability,1/st_data[2].BBprobability,1/st_data[2].RBprobability,]
                p4 = [1/st_data[3].allprobability,1/st_data[3].BBprobability,1/st_data[3].RBprobability,]
                p5 = [1/st_data[4].allprobability,1/st_data[4].BBprobability,1/st_data[4].RBprobability,]
                p6 = [1/st_data[5].allprobability,1/st_data[5].BBprobability,1/st_data[5].RBprobability,]
                
                # アナスロから取得したデータ
                data = np.array([data_arr.allprobability,data_arr.BB,data_arr.RB])
                
                # アナスロから取得したデータ
                data = np.array([data_arr.allprobability,data_arr.BB])
            elif st_data[0].allprobability != 0 & st_data[0].BBprobability != 0 & st_data[0].RBprobability != 0:
                p1 = [1/st_data[0].allprobability,1/st_data[0].BBprobability,1/st_data[0].RBprobability,]
                p2 = [1/st_data[1].allprobability,1/st_data[1].BBprobability,1/st_data[1].RBprobability,]
                p3 = [1/st_data[2].allprobability,1/st_data[2].BBprobability,1/st_data[2].RBprobability,]
                p4 = [1/st_data[3].allprobability,1/st_data[3].BBprobability,1/st_data[3].RBprobability,]
                p5 = [1/st_data[4].allprobability,1/st_data[4].BBprobability,1/st_data[4].RBprobability,]
                p6 = [1/st_data[5].allprobability,1/st_data[5].BBprobability,1/st_data[5].RBprobability,]
            
            # ベクトルの内積を計算
            similarity = [np.dot(data, p) for p in [p1, p2, p3,p4,p5,p6]]
            
            # 最も類似度が高いくじを選択
            most_similar = np.argmax(similarity) + 1
            
            if i.game < 1000:             
                most_similar = 1
            elif i.difference > 2000:
                if most_similar <6:
                    most_similar += 1
            elif i.difference < 2000:
                if most_similar > 1:
                    most_similar -= 1
                    
            obj = data(setting = most_similar)
            obj.save()
                
        
        
    
    

    

