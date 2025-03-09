import requests
import tqdm
from getcontent import Content
from concurrent.futures import ThreadPoolExecutor

# 进行下载
def download_material(content:Content,path:str):
    try:
        url=content.get_url()
        material_name=content.get_name()
        # 采用流式下载，显示实时进度条
        response = requests.get(url,stream=True)
        total_size=int(response.headers.get('Content-Length',0))
        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)
        with open( f"{path}\{material_name}", "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk: 
                    f.write(chunk)
                    progress_bar.update(len(chunk))
        progress_bar.close()
        print(f"{material_name}下载成功")
    except Exception as e:
        print("下载失败")
        print(e)
        return None

#多线程下载
def sdownload(content_list:list,path:str):
    threads=ThreadPoolExecutor(max_workers=10)
    for content in content_list:
        threads.submit(download_material,[content,path])
    threads.shutdown()
    print("下载完成")