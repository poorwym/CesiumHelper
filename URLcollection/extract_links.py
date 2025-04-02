from bs4 import BeautifulSoup
import os
import glob

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
    
    return links

def process_all_html_files():
    # 获取当前脚本所在的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 获取html目录下所有html文件（相对于脚本的路径）
    html_dir = os.path.join(script_dir, 'html')
    html_files = glob.glob(os.path.join(html_dir, '*.html'))
    
    if not html_files:
        print('错误：在html目录下未找到任何html文件')
        return
    
    all_links = []
    
    # 处理每个html文件
    for html_file in html_files:
        links = extract_links(html_file)
        all_links.extend(links)
        print(f'已从 {os.path.basename(html_file)} 提取 {len(links)} 个链接')
    
    # 将所有结果写入文件（相对于脚本的路径）
    output_file = os.path.join(script_dir, 'extracted_links.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
        for link in all_links:
            f.write(link + '\n')
    
    print(f'总共提取了 {len(all_links)} 个链接并保存到 {output_file}')

if __name__ == '__main__':
    # 获取当前脚本所在的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 确保html目录存在（相对于脚本的路径）
    html_dir = os.path.join(script_dir, 'html')
    if os.path.exists(html_dir) and os.path.isdir(html_dir):
        process_all_html_files()
    else:
        print(f'错误：找不到html目录 {html_dir}') 