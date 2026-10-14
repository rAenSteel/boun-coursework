inp_filename, operation, out_filename = input().split()
# DO_NOT_EDIT_ANYTHING_ABOVE_THIS_LINE
def read_imagefile(f):
    #dosyanin tamamini oku ve kelime kelime ayir bosluklara gore bu yontem satir sonu karakterlerinden kurtulmayi kolaylastirir
    icerik = f.read()
    kelimeler = icerik.split()
    
    #ilk kelime P2 olmali biz direk veriyi alalim token 0 P2 token 1 genislik token 2 yukseklik token 3 max deger
    genislik = int(kelimeler[1])
    yukseklik = int(kelimeler[2])
    max_deger = int(kelimeler[3])
    
    #piksel verileri 4. indexten basliyor
    piksel_verisi = kelimeler[4:]
    
    #2 boyutlu matris olusturma
    resim_matrisi = []
    suanki_index = 0
    
    for i in range(yukseklik):
        satir_listesi = []
        for j in range(genislik):
            #siradaki pikseli al ve inte cevir
            deger = int(piksel_verisi[suanki_index])
            satir_listesi.append(deger)
            suanki_index += 1
        resim_matrisi.append(satir_listesi)
        
    return resim_matrisi

def write_imagefile(f, img_matrix):
    #header bilgilerini yazalim
    yukseklik = len(img_matrix)
    genislik = len(img_matrix[0])
    #odevde hep 255 demis
    max_val = 255 
    
    f.write("P2\n")
    f.write(str(genislik) + " " + str(yukseklik) + "\n")
    f.write(str(max_val) + "\n")
    
    #matrisin icindeki pikselleri yazalim
    for satir in img_matrix:
        for piksel in satir:
            f.write(str(piksel) + " ")
        f.write("\n") #her satir bitince alt satira gecsin okunmasi kolay olsun

def misalign(img_matrix):
    #tek numarali sutunlari 1 3 5 yani index 0 2 4 ters cevir
    yukseklik = len(img_matrix)
    genislik = len(img_matrix[0])
    
    #orjinal matrisi bozmayalim kopyasini alalim gerci inplace de olur ama garanti olsun
    yeni_matris = []
    for r in range(yukseklik):
        #satiri kopyala
        yeni_matris.append(img_matrix[r][:])
        
    #sutunlari gezelim
    for c in range(genislik):
        #eger sutun numarasi tek ise 1 3 vs yani index 0 2
        if c % 2 == 0: 
            #bu sutunu gecici bir listede topla
            temp_col = []
            for r in range(yukseklik):
                temp_col.append(yeni_matris[r][c])
            
            #listeyi ters cevir
            ters_col = temp_col[::-1]
            
            
            #matrise geri yaz
            for r in range(yukseklik):
                yeni_matris[r][c] = ters_col[r]
                
    return yeni_matris

def sort_columns(img_matrix):
    #sutunlari kucukten buyuge sirala
    yukseklik = len(img_matrix)
    genislik = len(img_matrix[0])
    yeni_matris = [row[:] for row in img_matrix] 
    
    for c in range(genislik):
        #sutunu cek
        col_list = []
        for r in range(yukseklik):
            col_list.append(yeni_matris[r][c])
        col_list.sort()
        
        #geri yaz
        for r in range(yukseklik):
            yeni_matris[r][c] = col_list[r]
            
    return yeni_matris

def sort_rows_border(img_matrix):
    #satirlari siralayalim ama 0lara dokunmicaz
    yukseklik = len(img_matrix)
    genislik = len(img_matrix[0])
    
    yeni_matris = []
    
    for r in range(yukseklik):
        mevcut_satir = img_matrix[r]
        yeni_satir = []
        
        #satiri parcalara ayirip siralayacagiz
        temp_chunk = []
        
        for piksel in mevcut_satir:
            if piksel == 0:
                #eger 0 gorduysek elimizdeki parcalari sirala ve ekle
                if len(temp_chunk) > 0:
                    temp_chunk.sort()
                    for val in temp_chunk:
                        yeni_satir.append(val)
                        #listeyi bosalt
                    temp_chunk = []
                
                #0i da ekle border oldugu icin siralamaya girmiyor
                yeni_satir.append(0)
            else:
                #0 degilse listeye at beklesin
                temp_chunk.append(piksel)
        
        #satir bitti ama elimizde kalan son parca olabilir
        if len(temp_chunk) > 0:
            temp_chunk.sort()
            for val in temp_chunk:
                yeni_satir.append(val)
        
        yeni_matris.append(yeni_satir)
        
    return yeni_matris

def convolution(img_matrix, kernel):
    #convolution islemi
    #kernel 3x3 boyutunda
    yukseklik = len(img_matrix)
    genislik = len(img_matrix[0])
    
    #bos bir sonuc matrisi olustur 0 ile doldur
    output_matrix = []
    for i in range(yukseklik):
        output_matrix.append([0] * genislik)
    
    #kernel merkezini gezdiriyoruz
    #kenarlarda padding 0 varmis gibi davranacagiz
    
    for r in range(yukseklik):
        for c in range(genislik):
            
            toplam = 0
            
            #kernelin 3x3 alanini gez
            #kernel indeksleri ky kx 0 1 2
            #resimdeki karsiligi r eksi 1 arti ky c eksi 1 arti kx
            
            for ky in range(3):
                for kx in range(3):
                    img_r = r - 1 + ky
                    img_c = c - 1 + kx
                    
                    piksel_degeri = 0
                    
                    #sinir kontrolu eger sinir disindaysa 0 kabul et
                    if img_r >= 0 and img_r < yukseklik and img_c >= 0 and img_c < genislik:
                        piksel_degeri = img_matrix[img_r][img_c]
                    else:
                        piksel_degeri = 0
                    
                    kernel_val = kernel[ky][kx]
                    toplam += piksel_degeri * kernel_val
            
            #degeri clample 0 255 arasi
            if toplam < 0:
                toplam = 0
            elif toplam > 255:
                toplam = 255
            
            output_matrix[r][c] = int(toplam)
            
    return output_matrix


# DO_NOT_EDIT_ANYTHING_BELOW_THIS_LINE
f = open(inp_filename, "r")
img_matrix = read_imagefile(f)
f.close()

if operation == "misalign":
    img_matrix = misalign(img_matrix)

elif operation == "sort_columns":
    img_matrix = sort_columns(img_matrix)

elif operation == "sort_rows_border":
    img_matrix = sort_rows_border(img_matrix)

elif operation == "highpass":
    kernel = [
        [-1, -1, -1],
        [-1, 9, -1],
        [-1, -1, -1]
    ]
    img_matrix = convolution(img_matrix, kernel)

f = open(out_filename, "w")
write_imagefile(f, img_matrix)
f.close()