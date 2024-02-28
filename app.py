import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import streamlit as st

df = pd.read_csv('dataset/TheSocialDilemma.csv')
st.markdown('''## Описание колонок набора данных
1.	user_name -	Имя пользователя, как он его определил.
2.	user_location -	Определенное пользователем местоположение для профиля этой учетной записи.
3.	user_description - Определяемая пользователем строка UTF-8, описывающая их учетную запись.
4.	user_created - Время и дата, когда была создана учетная запись.
5.	user_followers - Количество подписчиков, которое есть у аккаунта на данный момент.
6.	user_friends - Количество друзей, имеющихся у аккаунта.Нажмите, чтобы использовать этот вариант
7.	user_favourites -	Количество избранных аккаунтов, имеющихся на данный момент
8.	user_verified -	При значении true указывает, что пользователь имеет подтвержденную учетную запись.
9.	date	Время и дата создания твита по Гринвичу
10.	text	Текст твита в формате UTF-8
11.	hashtags	Все хэштеги, указанные в твите вместе с #TheSocialDilemma
12.	source	Утилита, используемая для публикации твита, Твиты с сайта Twitter имеют значение источника - web
13.	is_retweet	Указывает, был ли этот твит ретвитнут аутентифицируемым пользователем.
14.	Sentiment(Target variable)	Указывает на настроение твита, состоит из трех категорий: Позитивный, нейтральный и негативный''')

st.markdown('## проверка пропусков значений в колонках')
data = df.count().reset_index()
data.columns = ['name_column', 'count_values']
fig, ax = plt.subplots()
sns.barplot(data=data, y='name_column', x='count_values', ax=ax)
plt.title('Количество значений в колонках датасета')
st.pyplot(fig)

st.markdown('В наборе данных всего 20068 записей. Есть пропуски для колонок user_location, user_description, hastags.')
st.markdown('## Проверка уникальных значений в колонках')

uniq = {}
for name in df.columns:
    uniq[name] = len(df[name].unique())

uniq = pd.DataFrame(list(uniq.items()), columns=['name_column', 'count_values'])
fig, ax = plt.subplots()
sns.barplot(data=uniq, orient='h', y='name_column', x='count_values', ax=ax)
plt.title('Количество уникальных значений в колонках датасета')
st.pyplot(fig)
st.markdown('Текст сообщений для каждого твита является уникальным.')
st.markdown('# Разведочный анализ')
st.dataframe(df.describe(include='all'))
st.markdown('В наборе данных всего 20068 записей твитов, 15737 уникальных пользователей из 5777 локаций.'
            ' Самая популярная локация Индия. Приложений для твитера 82. Самое популярное приложения для Iphone. '
            'Большинство твитов положительныо окрашены')
st.markdown('## 10 часто встречающиеся местоположений')

pop_loc = df['user_location'].value_counts().reset_index().head(10)
pop_loc.columns = ['locations', 'count']
fig, ax = plt.subplots()
sns.barplot(data=pop_loc,
            y='locations',
            x='count',
            ax=ax,
            orient='h').set_title('10 часто встречающиеся местоположений')
st.pyplot(fig)

st.markdown('## Распределение твитов по настроению')
Sentiment = pd.DataFrame(df['Sentiment'].value_counts().reset_index())
Sentiment.columns = ['Настроение', 'Количество твитов']
fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.pie(x=Sentiment['Количество твитов'], autopct='%1.2f%%')
ax1.set_title('сообщения в %')

Sentiment = pd.DataFrame(df[df['user_location'].isin(pop_loc['locations'])]['Sentiment'].value_counts().reset_index())
Sentiment.columns = ['Настроение', 'Количество твитов']
ax2.pie(x=Sentiment['Количество твитов'], autopct='%1.2f%%')
ax2.set_title(' сообщения популярных локаций в %')
fig.legend(labels=Sentiment['Настроение'], bbox_to_anchor=(1, 1))
fig.suptitle('Распределение твитов по настроению')
st.pyplot(fig)

st.markdown('## 10 пользователей написавших больше всего твитов')
top_user = df['user_name'].value_counts(ascending=False).reset_index()[:10]
top_user.columns = ['пользователь', 'количество']
fig, ax = plt.subplots()
sns.barplot(data=top_user,
            y='пользователь',
            x='количество',
            orient='h',
            ax=ax).set_title('10 пользователей сделавших больше всего твиттов')
ax.set_xlabel('Количество твитов')
st.pyplot(fig)

st.markdown('## 10 самых популярных приложений для твиттера')
fig, ax = plt.subplots()
source = df['source'].value_counts().reset_index()[:10]
source.columns = ['Название', 'Количество твитов']
sns.barplot(data=source,
            y='Название',
            x='Количество твитов',
            orient='h', ax=ax).set_title('10 популярных источников отправки твитов')
st.pyplot(fig)
