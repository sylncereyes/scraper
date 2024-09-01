import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlsplit, urlparse
import argparse

# Menggunakan set untuk menyimpan direktori yang sudah discan
direktori_scanned = set()

def normalize_url(url):
    # Menghilangkan trailing slash dan bagian bahasa seperti /en/ atau /id/
    parsed_url = urlsplit(url)
    path = parsed_url.path.rstrip('/')
    
    # Jika path mengandung bahasa, hapus bagian tersebut
    # Misal: /en/support -> /support
    if path.startswith('/en/') or path.startswith('/id/'):
        path = path[3:]  # Menghapus /en atau /id
    
    normalized_url = parsed_url._replace(path=path).geturl()
    
    return normalized_url

def direktori_scanner(url):
    global direktori_scanned
    
    # Mengirimkan request ke URL
    response = requests.get(url)
    
    # Mengecek apakah request berhasil
    if response.status_code == 200:
        # Mengambil konten HTML dari URL
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Mencari semua link dalam HTML
        links = soup.find_all('a')
        
        # Membuat set direktori yang ditemukan (menggunakan set untuk menghilangkan duplikat)
        direktori = set()
        
        # Looping semua link
        for link in links:
            # Mengecek apakah link memiliki atribut href
            if link.has_attr('href'):
                href = link['href']
                # Mengecek apakah link merupakan direktori
                if href.startswith('/') or urlsplit(href).netloc == urlsplit(url).netloc:
                    # Menggabungkan URL dengan direktori
                    direktori_url = urljoin(url, href)
                    direktori_url = normalize_url(direktori_url)
                    if direktori_url not in direktori_scanned:
                        direktori.add(direktori_url)
        
        # Mencetak daftar direktori yang ditemukan
        for direktori_url in direktori:
            if direktori_url not in direktori_scanned:
                direktori_scanned.add(direktori_url)
                yield direktori_url
                yield from direktori_scanner(direktori_url)

def main():
    parser = argparse.ArgumentParser(description="Direktori Scanner")
    parser.add_argument("-u", "--url", help="URL target", required=True)
    parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    parser.add_argument("-l", "--list", help="List URLs only", action="store_true")
    args = parser.parse_args()
    
    url = args.url
    output_file = args.output
    list_only = args.list
    
    if list_only:
        if output_file:
            with open(output_file, "w") as f:
                for direktori_url in direktori_scanner(url):
                    f.write(direktori_url + "\n")
        else:
            for direktori_url in direktori_scanner(url):
                print(direktori_url)
    else:
        if output_file:
            with open(output_file, "w") as f:
                for direktori_url in direktori_scanner(url):
                    f.write(direktori_url + "\n")
        else:
            for direktori_url in direktori_scanner(url):
                print(direktori_url)

if __name__ == "__main__":
    main()
