import sys
import pickle
# global dictionary ve liste olusturuyorum biri variables diğeri pickle dump icin
variables = {}
instructions = []
functions = ["tasu", "kaikakko", "tojikakko", "kakeru"]
keywords = ["print", "no", "atai", "wa", "o", "de", "aru", "suru", "tasu", "seisu", "moji-retsu", "kakeru", "kaikakko", "tojikakko", "Puroguramu", "hajimeyo", "oware"]
# yardimci fonksiyon son bulunan indexi bulmak icin
def find_last(lst, item):
    for i in range(len(lst)-1, -1, -1):
        if lst[i] == item:
            return i
    return -1
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
        # string kontrolu
        elif eleman.startswith("-") and eleman.endswith("-"):
            if "-" in eleman[1:-1]:
                raise Exception(f"Compile error {line_no=}")
            # uzunluk kontrolu yapiyoruz
            if len(eleman[1:-1]) > 10000:
                raise Exception(f"Compile error {line_no=}")
        # integer kontrolu
        elif eleman[0].isdigit():
            if eleman.startswith("0") and len(eleman) > 1:
                raise Exception(f"Compile error {line_no=}")
            # virgul kontrolu
            if "," in eleman:
                parts = eleman.split(",")
                # eger ilk eleman veya son eleman virgilse hata firlaticak
                if parts[0] == "":
                    raise Exception(f"Compile error {line_no=}")
                for part in parts[1:]:
                    #eger virgulleri 4 er 4 er atmadiysa hata firlaticak
                    if len(part) != 4:
                        raise Exception(f"Compile error {line_no=}")
                if eleman.endswith(","):
                    raise Exception(f"Compile error {line_no=}")
            # sayi kontrolu
            token = eleman.replace(",", "")
            if not token.isdigit():
                raise Exception(f"Compile error {line_no=}")
            # 10 haneden uzun mu kontrolu
            if int(token) > 9999999999:
                raise Exception(f"Compile error {line_no=}")
        else:
            if eleman not in functions:
                if eleman not in variables:
                    raise Exception(f"Compile error {line_no=}")
    return lst
# tür kontrolü yapan fonksiyon
def check_types(lst, line_no):
    type_lst = []
    #once tipi ne ise ona ceviriliyor
    for item in lst:
        if item in functions:
            type_lst.append(item)
        elif item.startswith("-") and item.endswith("-"):
            type_lst.append("str")
        elif item[0].isdigit():
            type_lst.append("int")
        else:
            if variables[item] == "seisu": 
                type_lst.append("int")
            else: 
                type_lst.append("str")
    # parantez ici islem yapmak icin parantez araligi tanimalaniyor
    while "kaikakko" in type_lst:
        #kapa parantezin indekisini bulup kapa parantezden geriye gidip acik parantez indeksini bulucaz
        #islemler sagdan sola yapilacak
        itojikakko = type_lst.index("tojikakko")
        ikaikakko = -1
        for i in range(itojikakko-1, -1, -1):
            #1 er 1 er liste basina arama yapiliyor
            if type_lst[i] == "kaikakko":
                ikaikakko = i
                break
        #parantez icini bulduk ara diye araliga aliyoruz
        ara = type_lst[ikaikakko+1:itojikakko]
        #recursive olarak parantez ici islemi yapip sonucu aliyoruz
        sonuc = check_types(ara, line_no)
        #list slices ile parantez ici kisim sonuc ile degistiriliyor
        type_lst = type_lst[:ikaikakko] + [sonuc] + type_lst[itojikakko+1:]

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
        #eger ilk type str ikinci int ise hata firlaticak
        elif t1 == "str" and t2 == "int":
            raise Exception(f"Compile error {line_no=}")
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
#tokeni alip anlamli halini donduren fonksiyon
def word_means(token, d):
    if token in functions:
        #fonksiyon ise direkt token donduruluyor
        return token
    elif token in d:
        #degisken ise deger donduruluyor
        return d[token]
    elif token.startswith("-") and token.endswith("-"):
        #string ise stringin ham haline getirip donduruluyor
        return token.strip("-")
    else:
        #integer ise virgul kaldirip int e cevirip donduruluyor
        token = token.replace(",", "")
        return int(token)
# simdi de tipleri kontrol eden fonksiyonun matematik yapan halini yazicagiz execute icin
def list_math(lst, line_no):
    while "kaikakko" in lst and "tojikakko" in lst:
        # parantez ici islemi yapmak icin parantez araligi tanimalaniyor
        itojikakko = lst.index("tojikakko")
        ikaikakko = -1
        for i in range(itojikakko-1,-1,-1):
            if lst[i] == "kaikakko":
                ikaikakko = i
                break
        #parantez kapanmazsa hata firlaticak
        if ikaikakko == -1:
            raise Exception(f"Runtime error {line_no=}")
        ara = lst[ikaikakko+1:itojikakko]
        # recursive olarak parantez ici islemi yapip sonucu aliyoruz
        ara_sonuc = list_math(ara, line_no)
        #list slicing ile parantezli kisim sonucu ile degistiriliyor
        lst = lst[:ikaikakko] + ara_sonuc + lst[itojikakko+1:]
    #carpma islemi
    while "kakeru" in lst:
        #sagdan sola islem yapmak icin son kakeru indeksini buluyoruz
        i = find_last(lst, "kakeru")
        #kakeru nun solundaki ve sagindaki degerleri aliyoruz
        val1 = lst[i-1]
        val2 = lst[i+1]

        if type(val1) == int and type(val2) == int:
            carpim = val1 * val2
            #eger carpim 10 digitten buyukse hata firlaticak
            if carpim > 9999999999:
                raise Exception(f"Runtime error {line_no=}")
            #list slicing ile carpim sonucu ekleniyor
            lst = lst[:i-1] + [carpim] + lst[i+2:]
        elif type(val1) == int and type(val2) == str:
            carpim = val2 * val1
            #eger carpim 10000 karakterden buyukse hata firlaticak
            if len(carpim) > 10000:
                raise Exception(f"Runtime error {line_no=}")
            lst = lst[:i-1] + [carpim] + lst[i+2:]
        else:
            raise Exception(f"Runtime error {line_no=}")
    #burada doplama yapicaz
    while "tasu" in lst:
        #sagdan sola islem yapmak icin son tasu indeksini buluyoruz
        i = find_last(lst, "tasu")
        #tasu nun solundaki ve sagindaki degerleri aliyoruz
        val1 = lst[i-1]
        val2 = lst[i+1]

        if type(val1) == int and type(val2) == int:
            toplam = val1 + val2
            #eger toplam 10 digitten buyukse hata firlaticak
            if toplam > 9999999999:
                raise Exception(f"Runtime error {line_no=}")
            
            lst = lst[:i-1] + [toplam] + lst[i+2:]
        elif type(val1) == str and type(val2) == str:
            birlesik = val1 + val2
            #eger birlesik 10000 karakterden buyukse hata firlaticak
            if len(birlesik) > 10000:
                raise Exception(f"Runtime error {line_no=}")
            #list slicing ile toplama sonucu ekleniyor
            lst = lst[:i-1] + [birlesik] + lst[i+2:]
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
    with open(input_file, "r",encoding="utf-8") as f:
        #lines listemizi aliyoruz
        lines = f.readlines()
    #eger hic line yoksa hata firlaticak
    if not lines:
        raise Exception("Compile error line_no=1")
    #hatanin hangi lineda ciktigini yazabilmek icin line no degiskeni tutuyoruz
    line_no = 1
    for line in lines:
        clean_line = line.strip()
        
        #eger line bossa hata firlaticak
        if clean_line == "":
            raise Exception(f"Compile error {line_no=}")
        #ilk line Puroguramu o hajimeyo . olmak zorunda eger degilse hata firlaticak
        if line_no == 1:
            if clean_line != "Puroguramu o hajimeyo .":
                raise Exception(f"Compile error {line_no=}")
            #sona ulasamicagi icin burda line arttiriyorum
            line_no += 1
            continue
        # her line nokta ile bitmek zorunda
        if not clean_line.endswith("."):
            raise Exception(f"Compile error {line_no=}")
        # noktadan once bosluk olmak zorunda
        if clean_line[-2] != " ":
            raise Exception(f"Compile error {line_no=}")
        #bisim isimize yaricak kisim nokta ve bosluktan oncekiler orayi aliyoruz
        content = clean_line[:-2]
        #birden fazla bosluk varsa bulmak icin split(" ") yapiyoruz ki varsa "" gondersin
        tokens = content.split(" ")
        if "" in tokens:
            raise Exception(f"Compile error {line_no=}")
        #ne olur ne olmaz token sayisi 0 ise hata firlaticak
        if len(tokens) < 1:
            raise Exception(f"Compile error {line_no=}")

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
    if lines[-1].strip() != "Puroguramu o oware .":
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
                d[var_name] = result[0]
            
            elif mission == "PRINT":
                #degiskenler gelen tuple dan aliniyor
                value = eleman[1]
                line = eleman[2]
                #gelen her liste degeri icin anlamli halini aliyoruz ve bunu gecici l listemize ekliyoruz
                for word in value:
                    l.append(word_means(word,d))
                #listeyi matematik islemlerinden gecirip sonucu aliyoruz
                result = list_math(l, line)
                
                if type(result[0]) == int:
                    #sayiyi virgulle ayirarak yazdirma islemi
                    temporary_result = str(result[0])
                    #once ters ceviricez 4 lu gruplama yapip virgulle birlestiricez
                    reversered_result = temporary_result[::-1]
                    grouped = []
                    for i in range(0, len(reversered_result), 4):
                        grouped.append(reversered_result[i:i+4])
                    final_result = ",".join(grouped)[::-1]
                    y.write(final_result + "\n")
                    
                else:
                    #string ise -string- seklinde yazdiriyoruz
                    y.write(f"-{result[0]}-\n")
