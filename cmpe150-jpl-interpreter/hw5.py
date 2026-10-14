import sys
import pickle
# global dictionary ve liste olusturuyorum biri variables diğeri pickle dump icin
variables = {}
instructions = []
functions = ["tasu", "kaikakko", "tojikakko", "kakeru"]
# degisken isimleri buyuk-kucuk harf duyarsiz oldugu icin anahtar kelimeleri kucuk harfle tutuyorum
keywords = ["print", "no", "atai", "wa", "o", "de", "aru", "suru", "tasu", "seisu", "moji-retsu", "kakeru", "kaikakko", "tojikakko", "puroguramu", "hajimeyo", "oware"]
rakamlar = "0123456789"
# yardimci fonksiyon son bulunan indexi bulmak icin
def find_last(lst, item):
    for i in range(len(lst)-1, -1, -1):
        if lst[i] == item:
            return i
    return -1
# satiri tokenlara ayiran fonksiyon
# -...- arasindaki string sabitleri bosluk icerse bile tek token olarak aliniyor
def tokenize(content, line_no):
    tokens = []
    i = 0
    n = len(content)
    if n == 0:
        raise Exception(f"Compile error {line_no=}")
    while i < n:
        # token bosluk ile baslayamaz (bastaki bosluk ya da iki bosluk)
        if content[i] == " ":
            raise Exception(f"Compile error {line_no=}")
        if content[i] == "-":
            # string sabiti bir sonraki tireye kadar devam ediyor
            j = content.find("-", i + 1)
            if j == -1:
                raise Exception(f"Compile error {line_no=}")
        else:
            # diger tokenlar bir sonraki bosluga kadar
            j = content.find(" ", i)
            if j == -1:
                j = n
            j = j - 1
        tokens.append(content[i:j+1])
        i = j + 1
        if i < n:
            # iki token arasinda tam olarak bir bosluk olmali
            if content[i] != " ":
                raise Exception(f"Compile error {line_no=}")
            i += 1
            if i == n:
                raise Exception(f"Compile error {line_no=}")
    return tokens
# tokenlari kontrol eden fonksiyon
def token_controller(lst, line_no):
    parantez_sayisi = 0
    for eleman in lst:
        # once ic ice parantez kontrolu varsa hata firlatiyor
        if eleman == "kaikakko":
            if parantez_sayisi > 0:
                raise Exception(f"Compile error {line_no=}")
            # cunku arka arkaya ayni cesit parantez olamaz
            parantez_sayisi += 1
        elif eleman == "tojikakko":
            parantez_sayisi -= 1
            if parantez_sayisi < 0:
                raise Exception(f"Compile error {line_no=}")
    if parantez_sayisi != 0:
        raise Exception(f"Compile error {line_no=}")
    # her tokenu tek tek kontrol ediyor
    for eleman in lst:
        if eleman in keywords and eleman not in functions:
            raise Exception(f"Compile error {line_no=}")
        # string kontrolu (tokenize zaten tireden tireye aldi)
        elif eleman.startswith("-"):
            if len(eleman) < 2 or not eleman.endswith("-") or "-" in eleman[1:-1]:
                raise Exception(f"Compile error {line_no=}")
            # uzunluk kontrolu yapiyoruz
            if len(eleman[1:-1]) > 10000:
                raise Exception(f"Compile error {line_no=}")
        # integer kontrolu
        elif eleman[0] in rakamlar:
            if eleman.startswith("0") and len(eleman) > 1:
                raise Exception(f"Compile error {line_no=}")
            # virgul kontrolu
            if "," in eleman:
                parts = eleman.split(",")
                # ilk grup 1 ile 4 hane arasinda olmali
                if len(parts[0]) < 1 or len(parts[0]) > 4:
                    raise Exception(f"Compile error {line_no=}")
                for part in parts[1:]:
                    #eger virgulleri 4 er 4 er atmadiysa hata firlaticak
                    if len(part) != 4:
                        raise Exception(f"Compile error {line_no=}")
                if eleman.endswith(","):
                    raise Exception(f"Compile error {line_no=}")
            # sayi kontrolu: virgul disinda sadece 0-9 rakamlari olabilir
            token = eleman.replace(",", "")
            for karakter in token:
                if karakter not in rakamlar:
                    raise Exception(f"Compile error {line_no=}")
            # 10 haneden uzun mu kontrolu
            if int(token) > 9999999999:
                raise Exception(f"Compile error {line_no=}")
        else:
            if eleman not in functions:
                # degisken isimleri buyuk-kucuk harf duyarsiz
                if eleman.lower() not in variables:
                    raise Exception(f"Compile error {line_no=}")
    return lst
# degisken referanslarini kucuk harfe ceviren fonksiyon (token_controller'dan sonra cagriliyor)
def normalize(lst):
    yeni = []
    for eleman in lst:
        if eleman in functions or eleman.startswith("-") or eleman[0] in rakamlar:
            yeni.append(eleman)
        else:
            yeni.append(eleman.lower())
    return yeni
# parantezsiz bir ifadenin tipini bulan fonksiyon
def check_flat(type_lst, line_no):
    # ifade deger operator deger operator deger ... seklinde olmali
    if len(type_lst) % 2 == 0:
        raise Exception(f"Compile error {line_no=}")
    for i in range(len(type_lst)):
        if i % 2 == 0:
            if type_lst[i] != "int" and type_lst[i] != "str":
                raise Exception(f"Compile error {line_no=}")
        else:
            if type_lst[i] != "tasu" and type_lst[i] != "kakeru":
                raise Exception(f"Compile error {line_no=}")
    #carpma islemi yapicaz
    while "kakeru" in type_lst:
        #sagdan sola islem yapmak icin son kakeru indeksini buluyoruz
        i = find_last(type_lst, "kakeru")
        #ve kakeru nun solundaki ve sagindaki typelari aliyoruz
        t1 = type_lst[i-1]
        t2 = type_lst[i+1]
        # hangi typlelarin carpildigina bakip cevabi o type olarak atiyoruz
        if t1 == "int" and t2 == "int": res = "int"
        elif t1 == "int" and t2 == "str": res = "str"
        #eger ilk type str ise (str kakeru int veya str kakeru str) hata firlaticak
        else:
            raise Exception(f"Compile error {line_no=}")
        #yine list slices ile carpim sonucu ekleniyor
        type_lst = type_lst[:i-1] + [res] + type_lst[i+2:]
    # toplama islemi yapicaz
    while "tasu" in type_lst:
        #sagdan sola islem yapmak icin son tasu indeksini buluyoruz
        i = find_last(type_lst, "tasu")
        t1 = type_lst[i-1]
        t2 = type_lst[i+1]
        # toplama islemini yine type a gore yapiyorz
        if t1 == "int" and t2 == "int": res = "int"
        elif t1 == "str" and t2 == "str": res = "str"
        else:
            raise Exception(f"Compile error {line_no=}")
        # en son list slices ile toplama sonucu ekleniyor
        type_lst = type_lst[:i-1] + [res] + type_lst[i+2:]
    # tek elemanli liste olacagi icin ilk elemani donduruyoruz
    return type_lst[0]
# tür kontrolü yapan fonksiyon
def check_types(lst, line_no):
    type_lst = []
    #once tipi ne ise ona ceviriliyor (tipler bir kez cevriliyor)
    for item in lst:
        if item in functions:
            type_lst.append(item)
        elif item.startswith("-"):
            type_lst.append("str")
        elif item[0] in rakamlar:
            type_lst.append("int")
        else:
            if variables[item] == "seisu":
                type_lst.append("int")
            else:
                type_lst.append("str")
    # parantez ici islem yapmak icin parantez araligi tanimalaniyor
    while "kaikakko" in type_lst:
        #kapa parantezin indekisini bulup kapa parantezden geriye gidip acik parantez indeksini bulucaz
        itojikakko = type_lst.index("tojikakko")
        ikaikakko = -1
        for i in range(itojikakko-1, -1, -1):
            if type_lst[i] == "kaikakko":
                ikaikakko = i
                break
        #parantez icini bulduk ara diye araliga aliyoruz (ic ice parantez olmadigi icin ara parantezsiz)
        ara = type_lst[ikaikakko+1:itojikakko]
        sonuc = check_flat(ara, line_no)
        #list slices ile parantez ici kisim sonuc ile degistiriliyor
        type_lst = type_lst[:ikaikakko] + [sonuc] + type_lst[itojikakko+1:]
    return check_flat(type_lst, line_no)
#tokeni alip anlamli halini donduren fonksiyon
#degerler tek elemanli liste olarak donuyor ki "-tasu-" gibi bir string operator sanilmasin
def word_means(token, d):
    if token in functions:
        #fonksiyon ise direkt token donduruluyor
        return token
    elif token.startswith("-"):
        #string ise stringin ham haline getirip donduruluyor
        return [token[1:-1]]
    elif token[0] in rakamlar:
        #integer ise virgul kaldirip int e cevirip donduruluyor
        return [int(token.replace(",", ""))]
    else:
        #degisken ise deger donduruluyor
        return [d[token]]
# simdi de tipleri kontrol eden fonksiyonun matematik yapan halini yazicagiz execute icin
def list_math(lst, line_no):
    while "kaikakko" in lst:
        # parantez ici islemi yapmak icin parantez araligi tanimalaniyor
        itojikakko = lst.index("tojikakko")
        ikaikakko = -1
        for i in range(itojikakko-1,-1,-1):
            if lst[i] == "kaikakko":
                ikaikakko = i
                break
        ara = lst[ikaikakko+1:itojikakko]
        # parantez ici islemi yapip sonucu aliyoruz
        ara_sonuc = list_math(ara, line_no)
        #list slicing ile parantezli kisim sonucu ile degistiriliyor
        lst = lst[:ikaikakko] + ara_sonuc + lst[itojikakko+1:]
    #carpma islemi
    while "kakeru" in lst:
        #sagdan sola islem yapmak icin son kakeru indeksini buluyoruz
        i = find_last(lst, "kakeru")
        #kakeru nun solundaki ve sagindaki degerleri aliyoruz
        val1 = lst[i-1][0]
        val2 = lst[i+1][0]

        if type(val1) == int and type(val2) == int:
            carpim = val1 * val2
            #eger carpim 10 digitten buyukse hata firlaticak
            if carpim > 9999999999:
                raise Exception(f"Runtime error {line_no=}")
            #list slicing ile carpim sonucu ekleniyor
            lst = lst[:i-1] + [[carpim]] + lst[i+2:]
        elif type(val1) == int and type(val2) == str:
            #once uzunlugu hesapliyoruz ki cok buyuk bir string olusturmadan hata verelim
            if len(val2) * val1 > 10000:
                raise Exception(f"Runtime error {line_no=}")
            carpim = val2 * val1
            lst = lst[:i-1] + [[carpim]] + lst[i+2:]
        else:
            raise Exception(f"Runtime error {line_no=}")
    #burada toplama yapicaz
    while "tasu" in lst:
        #sagdan sola islem yapmak icin son tasu indeksini buluyoruz
        i = find_last(lst, "tasu")
        #tasu nun solundaki ve sagindaki degerleri aliyoruz
        val1 = lst[i-1][0]
        val2 = lst[i+1][0]

        if type(val1) == int and type(val2) == int:
            toplam = val1 + val2
            #eger toplam 10 digitten buyukse hata firlaticak
            if toplam > 9999999999:
                raise Exception(f"Runtime error {line_no=}")
            lst = lst[:i-1] + [[toplam]] + lst[i+2:]
        elif type(val1) == str and type(val2) == str:
            birlesik = val1 + val2
            #eger birlesik 10000 karakterden buyukse hata firlaticak
            if len(birlesik) > 10000:
                raise Exception(f"Runtime error {line_no=}")
            #list slicing ile toplama sonucu ekleniyor
            lst = lst[:i-1] + [[birlesik]] + lst[i+2:]
        else:
            raise Exception(f"Runtime error {line_no=}")
    return lst
#simdi sys ile terminalden gelen argumanlari alip islemleri yapicaz
mode = sys.argv[1]
input_file = sys.argv[2]
output_file = sys.argv[3]
#compile moduysa bu if blogune giricez
if mode == "-compile":
    #okuma modunda text dosyamizi aciyoruz
    with open(input_file, "r", encoding="utf-8") as f:
        icerik = f.read()
    #satirlari ayiriyoruz; bosluklari silmiyoruz cunku satir sonundaki bosluk da hata
    lines = icerik.split("\n")
    #dosyanin sonundaki tek yeni satir karakteri bos satir sayilmaz
    if len(lines) > 1 and lines[-1] == "":
        lines = lines[:-1]
    #windows satir sonlarini (\r) temizliyoruz
    for k in range(len(lines)):
        if lines[k].endswith("\r"):
            lines[k] = lines[k][:-1]
    #eger hic line yoksa hata firlaticak
    if len(lines) == 0 or (len(lines) == 1 and lines[0] == ""):
        raise Exception("Compile error line_no=1")
    #hatanin hangi lineda ciktigini yazabilmek icin line no degiskeni tutuyoruz
    line_no = 1
    son_satir = len(lines)
    program_bitti = False
    for line in lines:
        #eger line bossa hata firlaticak
        if line == "":
            raise Exception(f"Compile error {line_no=}")
        #ilk line Puroguramu o hajimeyo . olmak zorunda eger degilse hata firlaticak
        if line_no == 1:
            if line != "Puroguramu o hajimeyo .":
                raise Exception(f"Compile error {line_no=}")
            line_no += 1
            continue
        #son line Puroguramu o oware . ise program bitiyor; bu satir bir statement degil
        if line_no == son_satir and line == "Puroguramu o oware .":
            program_bitti = True
            break
        # her line bosluk + nokta ile bitmek zorunda
        if not line.endswith(" ."):
            raise Exception(f"Compile error {line_no=}")
        #bisim isimize yaricak kisim nokta ve bosluktan oncekiler orayi aliyoruz
        content = line[:-2]
        tokens = tokenize(content, line_no)

        # DECLARATION--------------------------------------------------------------------------
        if len(tokens) == 5 and tokens[1] == "wa" and tokens[3] == "de" and tokens[4] == "aru":
            #degisken ismi ve tipi aliniyor/ lower fonksiyonu var cunku case insensitive
            var_name = tokens[0].lower()
            var_type = tokens[2]
            # degisken ismi keyword olamaz
            if var_name in keywords:
                raise Exception(f"Compile error {line_no=}")
            # degisken ismi 10 karakterden uzun olamaz sadece ingilizce karakterden olusabilir
            if len(var_name) > 10 or not var_name.isalpha() or not var_name.isascii():
                raise Exception(f"Compile error {line_no=}")
            # degisken daha once tanimlanmis olamaz
            if var_name in variables:
                raise Exception(f"Compile error {line_no=}")
            # tip seisu veya moji-retsu olmalidir
            if var_type not in ["seisu", "moji-retsu"]:
                raise Exception(f"Compile error {line_no=}")
            # degiskeni variables sozlugune ekliyoruz
            variables[var_name] = var_type
            #daha sonra execute icin instructions listesine ekliyoruz
            instructions.append(("DECL", var_name, var_type, line_no))

        # ASSIGNMENT-----------------------------------------------------------------------------------------------------------------------------
        elif len(tokens) >= 7 and tokens[1] == "no" and tokens[2] == "atai" and tokens[3] == "wa" and tokens[-2] == "de" and tokens[-1] == "aru":
            var_name = tokens[0].lower()
            #burdaki expression listesi atama islemi icin gerekli kisim
            expression_list = tokens[4:-2]
            # degisken daha once tanimlanmis olmalidir
            if var_name not in variables:
                raise Exception(f"Compile error {line_no=}")
            # herhangi bir compile hatasi var mi diye tokenlari kontrol ediyoruz
            token_controller(expression_list, line_no)
            expression_list = normalize(expression_list)
            # type kontrolu yapiyoruz
            expr_type = check_types(expression_list, line_no)
            #eger olmamasi gereken bir type varsa hata firlaticak
            if variables[var_name] == "seisu" and expr_type != "int":
                raise Exception(f"Compile error {line_no=}")
            if variables[var_name] == "moji-retsu" and expr_type != "str":
                raise Exception(f"Compile error {line_no=}")
            #son olarak instruction listesine atama islemini ekliyoruz
            instructions.append(("ASSIGN", var_name, expression_list, line_no))
        # PRINT STATEMENT------------------------------------------------------------------------------------------------------------------------
        elif len(tokens) >= 4 and tokens[-3] == "o" and tokens[-2] == "print" and tokens[-1] == "suru":
            expression_list = tokens[:-3]
            # herhangi bir compile hatasi var mi diye tokenlari kontrol ediyoruz
            token_controller(expression_list, line_no)
            expression_list = normalize(expression_list)
            # type kontrolu yapiyoruz
            check_types(expression_list, line_no)
            #son olarak instruction listesine print islemini ekliyoruz
            instructions.append(("PRINT", expression_list, line_no))

        else:
            #eger yukaridaki uc yapidan biri degilse hata firlaticak
            raise Exception(f"Compile error {line_no=}")
        #line no arttiriliyor
        line_no += 1
    #son line Puroguramu o oware . olmak zorunda
    if not program_bitti:
        raise Exception(f"Compile error {line_no=}")
    # pickle dump islemi yapiliyor
    with open(output_file, "wb") as f:
        pickle.dump(instructions, f)
# execute moduysa bu if blogune giricez
elif mode == "-execute":
    # hem obj dosyasini okuma modunda aciyoruz hemde cikti dosyasini yazma modunda
    with open(input_file, "rb") as f, open(output_file,"w",encoding="utf-8") as y:
        # pickle load islemi yapiliyor
        instructions = pickle.load(f)
        # degisken degeri tutacak sozluk
        d = {}
        for eleman in instructions:
            # her islem icin gecici liste olusturuluyor
            l = []
            # ilk eleman islem tipi
            mission = eleman[0]

            if mission == "DECL":
                if eleman[2] == "seisu":
                    # degisken seisu ise 0 degeri ataniyor cunku integer
                    d[eleman[1]] = 0
                    # degisken moji-retsu ise bos string ataniyor cunku string
                elif eleman[2] == "moji-retsu":
                    d[eleman[1]] = ""

            elif mission == "ASSIGN":
                #degiskenler gelen tuple dan aliniyor
                var_name = eleman[1]
                value = eleman[2]
                line = eleman[3]
                #gelen her liste degeri icin anlamli halini aliyoruz ve bunu gecici l listemize ekliyoruz
                for word in value:
                    l.append(word_means(word,d))
                #listeyi matematik islemlerinden gecirip sonucu aliyoruz
                result = list_math(l, line)
                #sonucu degiskene atiyoruz
                d[var_name] = result[0][0]

            elif mission == "PRINT":
                #degiskenler gelen tuple dan aliniyor
                value = eleman[1]
                line = eleman[2]
                #gelen her liste degeri icin anlamli halini aliyoruz ve bunu gecici l listemize ekliyoruz
                for word in value:
                    l.append(word_means(word,d))
                #listeyi matematik islemlerinden gecirip sonucu aliyoruz
                result = list_math(l, line)
                sonuc = result[0][0]

                if type(sonuc) == int:
                    #sayiyi virgulle ayirarak yazdirma islemi
                    temporary_result = str(sonuc)
                    #once ters ceviricez 4 lu gruplama yapip virgulle birlestiricez
                    reversed_result = temporary_result[::-1]
                    grouped = []
                    for i in range(0, len(reversed_result), 4):
                        grouped.append(reversed_result[i:i+4])
                    final_result = ",".join(grouped)[::-1]
                    y.write(final_result + "\n")

                else:
                    #string ise -string- seklinde yazdiriyoruz
                    y.write(f"-{sonuc}-\n")
