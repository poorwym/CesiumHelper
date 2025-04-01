from bs4 import BeautifulSoup
import os

def extract_links(html_file):
    # 读取HTML文件
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(content, 'html.parser')
    
    # 提取所有链接
    links = []
    for a in soup.find_all('a'):
        href = a.get('href')
        if href:
            links.append(href)
    
    # 将结果写入文件
    output_file = 'extracted_links.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        for link in links:
            f.write(link + '\n')
    
    print(f'已提取 {len(links)} 个链接并保存到 {output_file}')

if __name__ == '__main__':
    html_file = 'Index - Cesium Documentation.html'
    if os.path.exists(html_file):
        extract_links(html_file)
    else:
        print(f'错误：找不到文件 {html_file}') 