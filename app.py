# Import libraries
import pandas as pd
import streamlit as st
import bs4
import requests


def my_url(keyyword):
    keyword = keyyword.replace(' ', '%20')
    url = 'https://www.nike.com/w?q={}'.format(keyword)
    return url


def extract_data(obj):
    name = obj.find('div', 'product-card__title').text.strip()
    description = obj.find('div', 'product-card__subtitle').text.strip()
    color = obj.find('div', 'product-card__count-item').text
    url2 = obj.find('a', 'product-card__link-overlay').get('href')

    # use a try block incase because the price might be in the discount block
    try:
        price = obj.find('div', 'product-price us__styling is--current-price css-11s12ax').text
    except AttributeError:
        price = obj.find('div', 'product-price is--current-price css-1ydfahe').text

    try:
        old_price = obj.find('div', 'product-price us__styling is--striked-out css-0').text
    except AttributeError:
        old_price = ''

    data = requests.get(url2)
    soup2 = bs4.BeautifulSoup(data.text, 'html.parser')
    image = soup2.find('img', class_='css-viwop1 u-full-width u-full-height css-m5dkrx').get('src')

    result = (name, description, color, price, old_price, image, url2)
    return result


def search(keyword):
    records = []
    url = my_url(keyword)

    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    soup_results = soup.findAll('div', class_='product-card__body')
    my_bar = st.progress(0)
    percent_complete = 0
    with st.spinner('Scraping in progress.......'):
        for key, item in enumerate(soup_results):
            record = extract_data(item)
            if record:
                records.append(record)
            percent = (key + 1) / len(soup_results)
            my_bar.progress(percent)
    st.success('Done!')

    # Convert list to dataframe
    columns_ = ['Name', 'Description', 'Available In', 'Price', 'Old Price', 'Image Link', 'URL']
    df = pd.DataFrame(records, columns=columns_)

    return df


####################################################################
# streamlit
##################################################################

st.header('Nike Scraper')

st.image(
    'https://user-images.githubusercontent.com/96771321/214847562-27b85c11-2848-4426-a517-4fb6e4c84847.png'
)

st.markdown('Items from nike.com')

word = st.text_input('SEARCH: ')
if word != '':
    if st.button('Search'):
        data_ = search(word)
        st.dataframe(data=data_)
