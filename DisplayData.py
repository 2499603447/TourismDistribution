import pandas as pd
import os;

data = pd.read_csv("sight.csv")
data = data.fillna(0)
data = data.drop(columns=['Unnamed: 0'])

# Split location into three parts：Province, City, District
data["address"] = data["address"].apply(lambda x: x.replace("[", "").replace("]", ""))
data["province"] = data["address"].apply(lambda x: x.split("·")[0])
data["city"] = data["address"].apply(lambda x: x.split("·")[1])
data["area"] = data["address"].apply(lambda x: x.split("·")[-1])

# Get the top 30 sights
num_top = data.sort_values(by='sold_tickets', axis=0, ascending=False).reset_index(drop=True)
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # specify default fonts
plt.rcParams['axes.unicode_minus'] = False  #
sns.set(font='SimHei')  # deal with the Chinese display problem of Seaborn
sns.set_context("talk")
fig = plt.figure(figsize=(10, 8))
sns.barplot(num_top["name"][:30], num_top["sold_tickets"][:30])
plt.title("南京&安徽各景点门票(含小景点)销量")
plt.xticks(rotation=90)
fig.show()

# Province and stars
data["level_sum"] = 1
var = data.groupby(['province', 'level']).level_sum.sum()
var.unstack().plot(kind='bar', figsize=(35, 10), stacked=False, color=['red', 'blue', 'green', 'yellow'])

# sum tickets by province ,city
pro_num = data.groupby(['province']).agg('sum').reset_index()
city_num = data.groupby(['city']).agg('sum').reset_index()
# deal hot data
import requests


def transform(geo):
    key = 'bb9a4fae3390081abfcb10bc7ed307a6'
    url = "http://restapi.amap.com/v3/geocode/geo?key=" + str(key) + "&address=" + str(geo)
    response = requests.get(url)
    if response.status_code == 200:
        answer = response.json()
        try:
            loc = answer['geocodes'][0]['location']
        except:
            loc = 0
    return loc


pro_num["lati"] = pro_num["province"].apply(lambda x: transform(x))
city_num["lati"] = city_num["city"].apply(lambda x: transform(x))
pro_num.to_csv("pro_num.csv", encoding="utf_8_sig")
city_num.to_csv("city_num.csv", encoding="utf_8_sig")

from pyecharts import Map

map = Map("Tourist‘s ticket sales distribution", title_color="#fff", title_pos="center", width=800, height=300, background_color='#404a59')
map.add("", pro_num["province"], pro_num["sold_tickets"], maptype="china", visual_range=[5000, 80000],
        is_visualmap=True,
        visual_text_color='#fff', visual_text_size="10", is_label_show=True)
map.render(path="pro_num.html")
map = Map("Tourist‘s hot distribution", title_color="#fff", title_pos="center", width=800, height=300, background_color='#404a59')
map.add("", pro_num["province"], pro_num["sold_tickets"], maptype="china", visual_range=[25, 80], is_visualmap=True,
        visual_text_color='#000', is_label_show=True)
map.render(path="pro_hot.html")

# 人少的5A景点，4A景点，3A景点
top_5A = data[data["level"] == "5A景区"].sort_values(by='sold_tickets', axis=0, ascending=True).reset_index(drop=True)
top_4A = data[data["level"] == "4A景区"].sort_values(by='sold_tickets', axis=0, ascending=True).reset_index(drop=True)
top_3A = data[data["level"] == "3A景区"].sort_values(by='sold_tickets', axis=0, ascending=True).reset_index(drop=True)
fig = plt.figure(figsize=(15, 15))
plt.pie(top_5A["sold_tickets"][:15], labels=top_5A["name"][:15], autopct='%1.2f%%')
plt.title("南京&安徽-5A景区门票(含内部小景点)销量 TOP15")
plt.savefig("./5A景区门票分布图.jpg")
plt.show()

# fig = plt.figure(figsize=(15, 15))
# plt.pie(top_4A["sold_tickets"][:15], labels=top_4A["name"][:15], autopct='%1.2f%%')
# plt.title("南京&安徽-4A景区门票(含内部小景点)销量 TOP15")
# plt.savefig("./4A景区门票分布图.jpg")
# plt.show()

# fig = plt.figure(figsize=(15, 15))
# plt.pie(top_3A["sold_tickets"][:15], labels=top_3A["name"][:15], autopct='%1.2f%%')
# plt.title("南京&安徽-3A景区门票(含内部小景点)销量 TOP15")
# plt.savefig("./3A景区门票分布图.jpg")
# plt.show()
