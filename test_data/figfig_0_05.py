# figfig0.04
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import os
import csv
import math


# グローバル変数
sampleNo = 12  # test点数を指定
figruresize = 4  # 画像サイズ
fontsize = 12  # フォントサイズ
depth_thick = 500  # 深さの目盛り幅 (nm)


# グラフのテンプレートの作成
def graph_template():
    # figure size
    plt.figure(figsize=(figruresize, figruresize))  # figureの縦横の大きさ

    # font size
    # plt.rcParams['font.family'] = 'sans-serif'
    # plt.rcParams['font.sans-serif'] = ['Liberation Sans'] # フォントの設定
    plt.rcParams['xtick.direction'] = 'in'  # x軸の目盛りを内向きにする
    plt.rcParams['ytick.direction'] = 'in'  # y軸の目盛りを内向きにする
    # plt.rcParams["font.size"] = int(fontsize) # 全てのフォントサイズの設定
    # plt.tick_params(labelsize=int(fontsize-2)) # 目盛りのフォントサイズのみ再設定
    # plt.tight_layout() # 図内にグラフに収める
    return


# headerを交互に格納する関数
def header_dubbing(NameA, NameB):
    header_dub = []
    for i in range(sampleNo):
        header_dub.append(NameA + "_Test {0:03}".format(i + 1))
        header_dub.append(NameB + "_Test {0:03}".format(i + 1))
    return header_dub


# Noneで不足分を補ったリストを作成し、各行で交互に結合する関数
def list_with_none(ListA, ListB):
    # Noneで不足分を補ったリストを作成する
    padded_listA = pd.DataFrame.from_records(
        [row.tolist() if isinstance(row, pd.Series) else row for row in ListA]
    )  # ListAを DataFrame に変換し、長さを揃える
    padded_listA = padded_listA.apply(lambda row: row.combine_first(pd.Series([None] * padded_listA.shape[1])), axis=1)  # None で埋める
    padded_listB = pd.DataFrame.from_records(
        [row.tolist() if isinstance(row, pd.Series) else row for row in ListB]
    )  # ListAを DataFrame に変換し、長さを揃える
    padded_listB = padded_listB.apply(lambda row: row.combine_first(pd.Series([None] * padded_listB.shape[1])), axis=1)  # None で埋める
    # print(padded_listA.shape, padded_listB.shape)
    # listA, Bを各行で交互に結合する
    res = np.empty((padded_listA.shape[0] + padded_listB.shape[0], padded_listA.shape[1]), dtype=float)
    # print(res.shape)
    # print(res.shape[0])
    res[0::2, :] = padded_listA
    res[1::2, :] = padded_listB
    array_with_none = np.array(res, dtype=object)  # NumPyの2D配列に変換
    return array_with_none


# csvファイルい出力する関数
def output_csv(filename, headerA, headerB, dataA, dataB):
    # header
    Header = header_dubbing(headerA, headerB)
    # data
    Data_output = list_with_none(dataA, dataB)  # Noneで不足分を補ったリストを作成し、各行で交互に結合する
    # ファイル出力
    with open(filename + ".csv", 'w', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(Header)
        writer.writerows(Data_output.T)
    return


# main
# マーカーの種類
# markers = ['o', '^', 's', 'P', 'D', 'v', 'h', '8', 'p', '*']

# 1. データ整理
# データセット配列
HCS_x = []
HCS = []
Mod_x = []
Mod = []
HIT_x = []
HIT = []
H2_x = []
H2 = []
# データ処理
for i in range(sampleNo):
    # csvファイルの読み込み
    file = os.path.isfile("zero-point_correction_{:d}.csv".format(i + 1))
    # file = os.path.isfile("x_HCS_modulus_1.csv")

    # fileが存在する場合の処理
    if file:
        # データファイルdfの取得
        df = pd.read_csv("zero-point_correction_{:d}.csv".format(i + 1), header=0)
        # print(df)

        # 1-1. HCS-Depth
        # データの取得（pandasでは.ilocを用いたスライスを用いる）
        hcs_x = df["Depth (nm)"]  # Depth (nm)の取得
        hcs = df["Harmonic contact stiffness (N/m)"]  # HCS (N/m)の取得
        hcs = hcs / 1000  # 単位変換: (N/m) -> (kN/m)
        # データの編集
        hcs = [hcs[i] for i in range(len(hcs_x)) if not math.isnan(hcs_x[i]) and hcs_x[i] != 0]
        hcs_x = [hcs_x[i] for i in range(len(hcs_x)) if not math.isnan(hcs_x[i]) and hcs_x[i] != 0]
        # データセット配列へ追加
        # print(hcs_x[:])
        HCS_x.append(hcs_x[:])
        HCS.append(hcs)

        # 1-2. Modulus-Depth
        # データの取得
        mod_x = df["Depth (nm)"]  # Depth (nm)の取得
        mod = df["Modulus (GPa)"]  # Modulus (GPa)の取得
        # データの編集
        # Mod_x = np.where(Mod > 0.1, Mod_x, 0.0)
        # Mod = np.where(Mod > 0.1, Mod, 0.0)
        # Mod_x = np.where(Mod < 1.0e3, Mod_x, 0.0)
        # Mod = np.where(Mod < 1.0e3, Mod, 0.0)
        # print(np.min(Mod), np.argmax(Mod))
        # mod_x[i] != nan　and mod_x[i] != 0を満たすデータを格納
        mod = [mod[i] for i in range(len(mod_x)) if not math.isnan(mod_x[i]) and mod_x[i] != 0]
        mod_x = [mod_x[i] for i in range(len(mod_x)) if not math.isnan(mod_x[i]) and mod_x[i] != 0]
        # mod[i] != nanを満たすデータを格納
        mod_x = [mod_x[i] for i in range(len(mod)) if not math.isnan(mod[i])]
        mod = [mod[i] for i in range(len(mod)) if not math.isnan(mod[i])]
        # データセット配列へ追加
        Mod_x.append(mod_x)
        Mod.append(mod)

        # 1-3. H_IT-Depth
        # データの取得
        hit_x = df["Depth (nm)"]  # Depth (nm)の取得
        hit = df["Nanoindentation hardness (GPa)"]  # Nanoindentation hardness (GPa)の取得
        # データの編集
        # hit_x[i] != nan　and hit_x[i] != 0を満たすデータを格納
        hit = [hit[i] for i in range(len(hit_x)) if not math.isnan(hit_x[i]) and hit_x[i] != 0]
        hit_x = [hit_x[i] for i in range(len(hit_x)) if not math.isnan(hit_x[i]) and hit_x[i] != 0]
        # hit[i] != nanを満たすデータを格納
        hit_x = [hit_x[i] for i in range(len(hit)) if not math.isnan(hit[i])]
        hit = [hit[i] for i in range(len(hit)) if not math.isnan(hit[i])]
        # データセット配列へ追加
        HIT_x.append(hit_x)
        HIT.append(hit)

        # 1-4. Hardness^2-1/depth
        # データの取得
        h2_x = df["1/depth (1/nm)"]  # 1/depth (nm^-1)の取得
        h2 = df["Hardness^2 (GPa^2)"]  # Hardness^2 (GPa^2)の取得
        # データの編集
        h2 = [h2[i] for i in range(len(h2_x)) if not math.isnan(h2_x[i]) and h2_x[i] != 0]
        h2_x = [h2_x[i] for i in range(len(h2_x)) if not math.isnan(h2_x[i]) and h2_x[i] != 0]
        # データセット配列へ追加
        H2_x.append(h2_x)
        H2.append(h2)

    # fileが存在しない場合の処理
    else:
        HCS_x.append([0])
        HCS.append([0])
        Mod_x.append([0])
        Mod.append([0])
        HIT_x.append([0])
        HIT.append([0])
        H2_x.append([0])
        H2.append([0])

# 2. グラフの出力
# Depth (nm)の上限値を設定する
depth_uplim = 0
for i in range(sampleNo):  # 全test中での最大値を基準にする
    temp = max(HCS_x[i][:])  # testiでの最大depth暫定値
    if temp > depth_uplim:  # 暫定値が既存のdepth_uplimよりも大きい場合に、上限値を更新する
        depth_uplim = temp
depth_uplim = (int(depth_uplim // depth_thick) + 1) * depth_thick  # depthの最大値より大きく、最も近いdepth_thick (nm)の倍数
# Depth (nm)の目盛り配列を設定する
Depth_thick = np.arange(0, depth_uplim + depth_thick, depth_thick)  # 刻み幅: depth_thick (nm)


# 2-1. HCS-Depth
graph_template()  # グラフのテンプレートの作成
# グラフ軸の設定
plt.xlabel("Depth, $h$ (nm)")
plt.ylabel("Harmonic cotanct stiffness (kN/m)")
# x軸:depth (nm)の設定
plt.xlim(0, depth_uplim)
plt.xticks(Depth_thick)
# y軸: HCSの最大値
HCS_max = 0.0  # y軸: HCSの最大値初期設定
for i in range(sampleNo):
    temp = max(HCS[i][:])  # testiでの最大HCS暫定値
    if temp > HCS_max:  # 暫定値が既存のHCS_maxよりも大きい場合に、最大値を更新する
        HCS_max = temp
plt.ylim(0, (int(HCS_max // 200) + 1) * 200)  # HCX_maxより大きく、最も近い200 (kN/m)の倍数
plt.yticks(np.arange(0, (int(HCS_max // 200) + 2) * 200, 200))  # 刻み幅: 200 (kN/m)
# プロット
for i in range(sampleNo):
    if HCS_x[i] != [0] and HCS[i] != [0]:  # testデータが存在する([0]でない)場合はグラフにプロットする
        # 凡例アリ
        # plt.scatter(HCS_x[i,:], HCS[i,:], s=9, label="test {}".format(i+1)) # グラフ(0,0)への描画
        # plt.legend()
        # 凡例ナシ
        plt.scatter(HCS_x[i][:], HCS[i][:], s=5)  # グラフへの描画
# fig.show() # グラフの描画
# fig.savefig("HCS_Mod.png") # svg形式でグラフを保存
plt.savefig("HCS-Depth.svg", transparent=True, bbox_inches='tight', dpi=300)  # svg形式で保存

# 2-2. Modulus-Depth
plt.clf()  # グラフのリセット
graph_template()  # グラフのテンプレートの作成
# グラフ軸の設定
plt.xlabel("Depth, $h$ (nm)")
plt.ylabel("Modulus (GPa)")
# x軸:depth (nm)の設定
plt.xlim(0, depth_uplim)
plt.xticks(Depth_thick)
# y軸: Modの最大値
Mod_max = 0.0  # y軸: Modの最大値初期設定
for i in range(sampleNo):
    temp = max(Mod[i][:])  # testiでの最大Mod暫定値
    if temp > Mod_max:  # 暫定値が既存のMod_maxよりも大きい場合に、最大値を更新する
        Mod_max = temp
# y軸: Modulus (GPa)の設定
plt.ylim(0, (int(Mod_max // 100) + 1) * 100)  # 上限値をMod_maxより大きく、最も近い100 (GPa)の倍数に設定する
plt.yticks(np.arange(0, (int(Mod_max // 100) + 2) * 100, 50))  # 刻み幅: 50 (GPa)
# プロット
for i in range(sampleNo):
    if Mod_x[i] != [0] and Mod[i] != [0]:  # testデータが存在する([0]でない)場合はグラフにプロットする
        # 凡例アリ
        # plt.scatter(Mod_x[i,:], Mod[i,:], s=9, label="test {}".format(i+1)) # グラフへの描画
        # plt.legend()
        # 凡例ナシ
        plt.plot(Mod_x[i][:], Mod[i][:])  # グラフ(0,0)への描画
# fig.show() # グラフの描画
# fig.savefig("HCS_Mod.png") # svg形式でグラフを保存
plt.savefig("Modulus-Depth.svg", transparent=True, bbox_inches='tight', dpi=300)  # svg形式で保存

# 2-3. HIT-Depth
plt.clf()  # グラフのリセット
graph_template()  # グラフのテンプレートの作成
# グラフ軸の設定
plt.xlabel("Depth, $h$ (nm)")
plt.ylabel("Nanoindentation hardness, $H_{IT}$ (GPa)")
# x軸:depth (nm)の設定
plt.xlim(0, depth_uplim)
plt.xticks(Depth_thick)
# y軸: HITの最大値
HIT_max = 0.0  # y軸: HITの最大値初期設定
for i in range(sampleNo):
    temp = max(HIT[i][:])  # testiでの最大HIT暫定値
    if temp > HIT_max:  # 暫定値が既存のHIT_maxよりも大きい場合に、最大値を更新する
        HIT_max = temp
plt.ylim(0, int(HIT_max) + 1)  # y軸: HIT (GPa)の最大値をHIT_max+1 (GPa)に設定
plt.yticks(np.arange(0, int(HIT_max) + 2, 1))  # 刻み幅: 1 (GPa)
# プロット
for i in range(sampleNo):
    if HIT_x[i] != [0] and HIT[i] != [0]:  # testデータが存在する([0]でない)場合はグラフにプロットする
        # 凡例アリ
        # plt.scatter(HIT_x[i,:], HIT[i,:], s=9, label="test {}".format(i+1)) # グラフへの描画
        # plt.legend()
        # # 凡例ナシ
        plt.scatter(HIT_x[i][:], HIT[i][:], s=5)  # グラフへの描画
# fig.show() # グラフの描画
# fig.savefig("HCS_Mod.png") # svg形式でグラフを保存
plt.savefig("HIT_Depth.svg", transparent=True, bbox_inches='tight', dpi=300)  # svg形式で保存

# 2-4. Nix-Gao (Hardness^2-1/depth)
plt.clf()  # グラフのリセット
graph_template()  # グラフのテンプレートの作成
# グラフ軸の設定
plt.xlabel("1/depth, $1/h$ (nm$^{-1}$)")
plt.ylabel("Hardness$^{2}$, ${H_{IT}}^{2}$ (GPa$^2$)")
# x軸の設定
inv_depth = max(H2_x[0][:])  # 1/depth (1/nm)の最大値
plt.xlim(0, (int(inv_depth // 0.001) + 2) * 0.001)  # x軸: 1/depth (1/nm)の設定
plt.xticks(np.arange(0, (int(inv_depth // 0.001) + 3) * 0.001, 0.001))  # 刻み幅: 0.001 (1/nm)
# y軸の設定
# y軸: Hardness^2の最大値
H2_max = 0.0  # y軸: Hardness^2の最大値初期設定
for i in range(sampleNo):
    temp = max(H2[i][:])  # testiでの最大H2暫定値
    if temp > H2_max:  # 暫定値が既存のH2_maxよりも大きい場合に、最大値を更新する
        H2_max = temp
plt.ylim(0.0, (int(H2_max // 10) + 1) * 10)  # y軸: Hardness^2 (GPa^2)の設定
plt.yticks(np.arange(0, (int(H2_max // 10) + 2) * 10, 5))  # 刻み幅: 5 (GPa^2)
# プロット
for i in range(sampleNo):
    if H2_x[i] != [0] and H2[i] != [0]:  # testデータが存在する([0]でない)場合はグラフにプロットする
        # 凡例アリ
        # plt.scatter(H2_x[i,:], H2[i,:], s=9, label="test {}".format(i+1)) # グラフへの描画
        # plt.legend()
        # 凡例ナシ
        plt.scatter(H2_x[i][:], H2[i][:], s=5)  # グラフへの描画
# fig.show() # グラフの描画
# fig.savefig("HCS_Mod.png") # svg形式でグラフを保存
plt.savefig("Nix-Gao.svg", transparent=True, bbox_inches='tight', dpi=300)  # svg形式で保存

# 3. csvファイル出力
# 3-1. HCS-Depth
output_csv("HCS-Depth", "Depth (nm)", "Harmonic contact stiffness (kN/m)", HCS_x, HCS)  # csvファイル出力

# 3-2. Modulus-Depth
output_csv("Modulus-Depth", "Depth (nm)", "Modulus (GPa)", Mod_x, Mod)  # csvファイル出力

# 3-3. HIT-Depth
output_csv("HIT-Depth", "Depth (nm)", "Nanoindentation hardness (GPa)", HIT_x, HIT)  # csvファイル出力

# 3-4. Hardness^2-1/depth
output_csv("Nix-Gao", "1/depth (nm)", "Hardness^2 (GPa^2)", H2_x, H2)  # csvファイル出力

# # Pillowを使ってPNGからBMP形式に変換
# png_image = Image.open("HCS_Mod.png")
# png_image.save("HCS_Mod.bmp")
