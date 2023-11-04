import requests
import os

current_directory = os.getcwd()


def download_video(video_url, output_path):
    response = requests.get(video_url, stream=True)

    if response.status_code == 200:
        with open(output_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        full_output_path = os.path.join(current_directory, output_path)
        print(f'Downloaded to {full_output_path}')
    else:
        print('Failed to download the video.')


print('get me the palylist id: ')
playlist_id = str(input())
api_url = f'https://www.aparat.com/api/fa/v1/video/playlist/one/playlist_id/{playlist_id}'
print('get me the quality: (Examples: 144 , 240 , 360 , 720 , 1080) ')
quality = str(input())

response = requests.get(api_url)

if response.status_code == 200:
    data = response.json()
    videos = data['included']
    for video in videos:
        if video['type'] == 'Video':
            video_id = video['attributes']['uid']
            video_title = video['attributes']['title']
            video_url = f'https://www.aparat.com/api/fa/v1/video/video/show/videohash/{video_id}'
            video_response = requests.get(video_url)
            if video_response.status_code == 200:
                video_data = video_response.json()
                video_download_link_all = video_data['data']['attributes']['file_link_all']
                for video_download_link in video_download_link_all:
                    if video_download_link['profile'] == quality + 'p':
                        download_url = video_download_link['urls'][0]
                        output_path = f'Download\\{video_title}.mp4'
                        download_video(download_url, output_path)

else:
    print('We have some errors in getting API data!')