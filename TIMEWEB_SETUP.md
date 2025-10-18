# =€ >H03>20O 8=AB@C:F8O: 5?;>9 reads.su =0 Timeweb Cloud + Cloudflare

**@5<O:** ~1.5 G0A0
**!;>6=>ABL:** !@54=OO
**!B>8<>ABL:** 500½/<5A (2>7<>65= ?@><>:>4 =0 ?5@2K9 <5AOF 15A?;0B=>)

---

## =Ë -B0? 1: 03@C7:0 :>40 =0 GitHub (10 <8=CB)

### 1.1. B:@>9B5 B5@<8=0; 2 ?0?:5 ?@>5:B0

Windows PowerShell 8;8 Git Bash

### 1.2. =8F80;878@C9B5 Git (5A;8 5I5 =5 A45;0=>)

```bash
git init
```

### 1.3. >102LB5 2A5 D09;K

```bash
git add .
```

### 1.4. !45;09B5 ?5@2K9 :><<8B

```bash
git commit -m ">B>2 : 45?;>N =0 Timeweb Cloud + Cloudflare"
```

### 1.5. !>7409B5 @5?>78B>@89 =0 GitHub

1. B:@>9B5 [github.com](https://github.com)
2. 06<8B5 "+" ’ "New repository"
3. 0AB@>9:8:
   - Repository name: `reads-su`
   - Description: ";0BD>@<0 4;O ?C1;8:0F88 AB0B59 - reads.su"
   - **Private** (?@820B=K9 @5?>78B>@89)
4. ** 4>102;O9B5** README, .gitignore, license
5. 06<8B5 "Create repository"

### 1.6. >4:;NG8B5 ;>:0;L=K9 @5?>78B>@89 : GitHub

**" `YOUR-USERNAME` =0 20H GitHub username!**

```bash
git remote add origin https://github.com/YOUR-USERNAME/reads-su.git
git branch -M main
git push -u origin main
```

**2548B5 ;>38= 8 ?0@>;L GitHub :>340 ?>?@>A8B.**

 **@>25@:0:** 1=>28B5 AB@0=8FC @5?>78B>@8O - :>4 4>;65= ?>O28BLAO!

---

## < -B0? 2:  538AB@0F8O =0 Timeweb Cloud (5 <8=CB)

### 2.1. B:@>9B5 https://timeweb.cloud

### 2.2. 06<8B5 " 538AB@0F8O" (?@02K9 25@E=89 C3>;)

### 2.3. 0?>;=8B5 D>@<C:
- Email
- 0@>;L
- >4B25@48B5 email

### 2.4. >948B5 2 ?0=5;L C?@02;5=8O

 **>B>2>!** K 2 ?0=5;8 Timeweb Cloud

---

## =æ -B0? 3: !>740=85 ?@>5:B0 Django =0 Timeweb (20 <8=CB)

### 3.1. !>7409B5 =>2>5 ?@8;>65=85

1.  ?0=5;8 Timeweb =06<8B5 **"!>740BL" ’ "@8;>65=85"**
2. K15@8B5 B8?: **"Python"**
3. $@59<2>@:: **"Django"**
4. 5@A8O Python: **3.11** (Timeweb =5 ?>445@68205B 3.13, => 3.11 ?>4>945B)
5.  538>=: **">A:20"** (4;O @>AA89A:8E ?>;L7>20B5;59)

### 3.2. >4:;NG8B5 GitHub @5?>78B>@89

1.  =0AB@>9:0E ?@8;>65=8O =0948B5 **"Git @5?>78B>@89"**
2. 06<8B5 **">4:;NG8BL GitHub"**
3. 2B>@87C9B5 Timeweb 4>ABC? : GitHub
4. K15@8B5 @5?>78B>@89 `reads-su`
5. 5B:0: `main`
6. 06<8B5 "!>E@0=8BL"

### 3.3. 0AB@>9B5 02B>45?;>9

1. :;NG8B5 **"2B><0B8G5A:89 45?;>9 ?@8 push"**
2. !:@8?B 45?;>O: `/deploy.sh` (C65 A>740= 2 ?@>5:B5)

 **@>25@:0:**  @0745;5 "Git" 4>;65= >B>1@060BLAO 20H @5?>78B>@89

---

## =Ä -B0? 4: >102;5=85 PostgreSQL 107K 40==KE (5 <8=CB)

### 4.1.  20H5< ?@>5:B5 Timeweb:

1. 06<8B5 **">1028BL A5@28A"**
2. K15@8B5 **"070 40==KE" ’ "PostgreSQL"**
3. 5@A8O: **PostgreSQL 14**
4. 06<8B5 "!>740BL"

### 4.2. >;CG8B5 40==K5 ?>4:;NG5=8O

1. B:@>9B5 A>740==CN 107C 40==KE
2. !:>?8@C9B5 **DATABASE_URL** (1C45B 2840: `postgresql://user:password@host:port/db`)

 **>B>2>!** 070 40==KE A>740=0

---

## = -B0? 5: 0AB@>9:0 ?5@5<5==KE >:@C65=8O (10 <8=CB)

### 5.1. 5=5@0F8O SECRET_KEY

0 20H5< :><?LNB5@5 2K?>;=8B5:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**!:>?8@C9B5** A35=5@8@>20==K9 :;NG!

### 5.2. >102LB5 ?5@5<5==K5 2 Timeweb

1.  ?0=5;8 ?@8;>65=8O >B:@>9B5 **"0AB@>9:8" ’ "5@5<5==K5 >:@C65=8O"**
2. >102LB5 A;54CNI85 ?5@5<5==K5:

```bash
SECRET_KEY=2AB02LB5-A35=5@8@>20==K9-:;NG
DEBUG=False
ALLOWED_HOSTS=reads.su,www.reads.su,20H-?@>5:B.timeweb.cloud
RAILWAY_ENVIRONMENT=production
```

**:**
- `DATABASE_URL` C65 CAB0=>2;5=0 02B><0B8G5A:8 Timeweb -  4>102;O9B5 2@CG=CN!
- 0<5=8B5 `20H-?@>5:B.timeweb.cloud` =0 @50;L=K9 4><5= >B Timeweb

### 5.3. @8<5=8B5 87<5=5=8O

06<8B5 "!>E@0=8BL" 8 "5@570?CAB8BL ?@8;>65=85"

 **@>25@:0:** 5@5<5==K5 >B>1@060NBAO 2 A?8A:5

---

## =€ -B0? 6: 5@2K9 45?;>9 (10 <8=CB)

### 6.1. 0?CAB8B5 45?;>9

Timeweb 02B><0B8G5A:8 70?CAB8B 45?;>9 ?>A;5 =0AB@>9:8 ?5@5<5==KE.

### 6.2. !;548B5 70 ;>30<8

1. B:@>9B5 **">38" ’ "5?;>9"**
2. >;6=K C2845BL:
   ```
   [1/5] #AB0=>2:0 Python 7028A8<>AB59...
   [2/5] !1>@ AB0B8G5A:8E D09;>2...
   [3/5] @8<5=5=85 <83@0F89...
   [4/5] G8AB:0 :5H0...
   [5/5] 5@570?CA: A5@25@0...
   === 5?;>9 7025@H5= CA?5H=>! ===
   ```

### 6.3. >;CG8B5 2@5<5==K9 URL

1.  @0745;5 **"><5=K"** Timeweb A>740AB 02B><0B8G5A:89 4><5=
2. 840: `20H-?@>5:B.timeweb.cloud`
3. B:@>9B5 53> 2 1@0C75@5

 **@>25@:0:** !09B >B:@K205BAO! (?>:0 =0 2@5<5==>< 4><5=5)

---

##  -B0? 7: 0AB@>9:0 Cloudflare (15 <8=CB)

### 7.1. 0@538AB@8@C9B5AL =0 Cloudflare

1. B:@>9B5 https://cloudflare.com
2. 06<8B5 "Sign Up"
3. Email, ?0@>;L, ?>4B25@645=85

### 7.2. >102LB5 4><5= reads.su

1.  ?0=5;8 Cloudflare =06<8B5 **"Add a Site"**
2. 2548B5: `reads.su`
3. K15@8B5 ?;0=: **"Free"** ($0/<5AOF)
4. 06<8B5 "Continue"

### 7.3. >;CG8B5 IP 04@5A A5@25@0 Timeweb

**0@80=B  (5A;8 Timeweb 40; IP):**
1.  ?0=5;8 Timeweb ’ 20H5 ?@8;>65=85 ’ "0AB@>9:8"
2. 0948B5 "IP 04@5A" 8;8 "Dedicated IP"

**0@80=B  (5A;8 =5B 2K45;5==>3> IP):**
- A?>;L7C5< CNAME =0 2@5<5==K9 4><5= Timeweb

### 7.4. 0AB@>9B5 DNS 70?8A8 2 Cloudflare

**#40;8B5 2A5 AB0@K5 70?8A8** 8 A>7409B5 =>2K5:

**A;8 5ABL IP 04@5A:**
```
Type: A
Name: @
IPv4 address: IP-04@5A-Timeweb
Proxy status: Proxied (>@0=652>5 >1;0:>)
TTL: Auto
```

**A;8 =5B IP (8A?>;L7C5< CNAME):**
```
Type: CNAME
Name: @
Target: 20H-?@>5:B.timeweb.cloud
Proxy status: Proxied (>@0=652>5 >1;0:>)
TTL: Auto
```

**0?8AL 4;O www:**
```
Type: CNAME
Name: www
Target: reads.su
Proxy status: Proxied (>@0=652>5 >1;0:>)
TTL: Auto
```

### 7.5. !:>?8@C9B5 NS A5@25@K Cloudflare

Cloudflare ?>:065B GB>-B> 2@>45:
```
bella.ns.cloudflare.com
derek.ns.cloudflare.com
```

**!:>?8@C9B5 8E!**

---

## = -B0? 8: 7<5=5=85 NS A5@25@>2 =0 reg.ru (10 <8=CB)

### 8.1. >948B5 2 ;8G=K9 :018=5B reg.ru

### 8.2. B:@>9B5 C?@02;5=85 4><5=>< reads.su

1. 0948B5 "><5=K" 2 <5=N
2. K15@8B5 reads.su
3. 06<8B5 "#?@02;5=85"

### 8.3. 7<5=8B5 NS A5@25@K

1. 0948B5 @0745; **"NS-A5@25@K"** 8;8 **"DNS-A5@25@K"**
2. 06<8B5 "7<5=8BL"
3. K15@8B5 **"A?>;L7>20BL A2>8 NS-A5@25@K"**
4. 2548B5 NS >B Cloudflare:
   - NS1: `bella.ns.cloudflare.com`
   - NS2: `derek.ns.cloudflare.com`
5. !>E@0=8B5

ð **=8<0=85:** 7<5=5=8O 2ABC?OB 2 A8;C G5@57 2-48 G0A>2 (>1KG=> 1-3 G0A0)

---

## = -B0? 9: 0AB@>9:0 SSL 2 Cloudflare (5 <8=CB)

### 9.1. :;NG8B5 SSL/TLS

1.  Cloudflare >B:@>9B5 **"SSL/TLS"**
2. K15@8B5 @568<: **"Full (strict)"**

### 9.2. :;NG8B5 HTTPS @548@5:B

1. B:@>9B5 **"SSL/TLS" ’ "Edge Certificates"**
2. :;NG8B5:
   -  **Always Use HTTPS**
   -  **Automatic HTTPS Rewrites**
   -  **Minimum TLS Version: 1.2**

### 9.3. 0AB@>9B5 >?B8<870F8N

1. B:@>9B5 **"Speed" ’ "Optimization"**
2. :;NG8B5:
   -  Auto Minify (JavaScript, CSS, HTML)
   -  Brotli
   -  Rocket Loader (>?F8>=0;L=>)

 **>B>2>!** SSL =0AB@>5=

---

## < -B0? 10: >4:;NG5=85 4><5=0 : Timeweb (5 <8=CB)

### 10.1.  ?0=5;8 Timeweb >B:@>9B5 20H5 ?@8;>65=85

### 10.2. 5@5948B5 2 "0AB@>9:8" ’ "><5=K"

### 10.3. >102LB5 custom domain

1. 06<8B5 **">1028BL 4><5="**
2. 2548B5: `reads.su`
3. 06<8B5 ">1028BL"
4. "0:65 4>102LB5: `www.reads.su`

### 10.4. 1=>28B5 ALLOWED_HOSTS

#1548B5AL GB> 2 ?5@5<5==KE >:@C65=8O:
```
ALLOWED_HOSTS=reads.su,www.reads.su,20H-?@>5:B.timeweb.cloud
```

 **@>25@:0:** ><5=K 4>102;5=K 2 A?8A:5

---

## =Ê -B0? 11: 83@0F8O 40==KE (10 <8=CB)

### 11.1. -:A?>@B 40==KE 87 ;>:0;L=>9 

0 20H5< :><?LNB5@5:

```bash
python manage.py dumpdata --natural-foreign --natural-primary \
  -e contenttypes -e auth.Permission -e sessions \
  --indent 2 -o data_backup.json
```

### 11.2. 03@C7:0 40==KE =0 A5@25@

**0@80=B : '5@57 SSH (5A;8 4>ABC?5=)**

```bash
# >4:;NG5=85 ?> SSH (40==K5 2 ?0=5;8 Timeweb)
ssh user@your-server.timeweb.cloud

# 03@C7:0 40==KE
python manage.py loaddata data_backup.json
```

**0@80=B : '5@57 ?0=5;L Timeweb**

1. B:@>9B5 "$09;>2K9 <5=5465@"
2. 03@C78B5 `data_backup.json` 2 :>@5=L ?@>5:B0
3.  ">=A>;8" 2K?>;=8B5:
   ```bash
   python manage.py loaddata data_backup.json
   ```

 **@>25@:0:** 0==K5 703@C65=K

---

## =d -B0? 12: !>740=85 AC?5@?>;L7>20B5;O (5 <8=CB)

### 12.1. '5@57 :>=A>;L Timeweb

1. B:@>9B5 **">=A>;L"** 2 ?0=5;8 Timeweb
2. K?>;=8B5:

```bash
python manage.py createsuperuser
```

3. 2548B5:
   - Username: `admin`
   - Email: 20H email
   - Password: ?@84C<09B5 =0456=K9 ?0@>;L

 **>B>2>!** !C?5@?>;L7>20B5;L A>740=

---

##  -B0? 13: $8=0;L=0O ?@>25@:0 (5 <8=CB)

### 13.1. @>25@LB5 4>ABC?=>ABL A09B0

B:@>9B5 2 1@0C75@5:
-  https://reads.su
-  https://www.reads.su

>;65= >B:@KBLAO 20H A09B A 75;5=K< 70<:>< =

### 13.2. >948B5 2 04<8=:C

https://reads.su/admin

- Login: admin
- Password: 20H ?0@>;L

### 13.3. @>25@LB5 GB> @01>B05B

- [ ] ;02=0O AB@0=8F0 703@C605BAO
- [ ] !B0BL8 >B>1@060NBAO
- [ ] 0B53>@88 @01>B0NB
- [ ] >8A: DC=:F8>=8@C5B
- [ ] 4<8=:0 4>ABC?=0
- [ ] SSL @01>B05B (75;5=K9 70<>:)

---

## <‰ >B>2>! !09B 70?CI5=!

0H A09B **reads.su** B5?5@L 4>ABC?5= >=;09= A:

 %>AB8=3: Timeweb Cloud (>A:20)
 070 40==KE: PostgreSQL
 CDN: Cloudflare
 SSL: :;NG5=
 2B>45?;>9: 7 GitHub

---

## =Ý 0: >1=>2;OBL A09B

### @>AB>9 ?@>F5AA:

1. =>A8B5 87<5=5=8O 2 :>4 ;>:0;L=>
2. ><<8B8B5:
   ```bash
   git add .
   git commit -m "?8A0=85 87<5=5=89"
   git push origin main
   ```
3. Timeweb 02B><0B8G5A:8 >1=>28B A09B 70 1-2 <8=CBK!

---

## =' >;57=K5 :><0=4K

### @>A<>B@ ;>3>2:
-  ?0=5;8 Timeweb: ">38" ’ "Application"

### 5@570?CA: ?@8;>65=8O:
-  ?0=5;8: "59AB28O" ’ "5@570?CAB8BL"

### SSH ?>4:;NG5=85:
```bash
ssh user@your-server.timeweb.cloud
```

### @8<5=8BL <83@0F88 2@CG=CN:
```bash
python manage.py migrate
```

### !>1@0BL AB0B8:C:
```bash
python manage.py collectstatic --noinput
```

---

## =° !B>8<>ABL

```
Timeweb Cloud: 500½/<5A
Cloudflare: 0½/<5A (15A?;0B=>)
><5= reads.su: C65 >?;0G5=

": 500½/<5A
```

**@><>:>4:** I8B5 ?@><>:>4K Timeweb =0 500½ 4;O =>2KE ?>;L7>20B5;59!

---

## <˜ Troubleshooting

### @>1;5<0: 502 Bad Gateway
** 5H5=85:** @>25@LB5 ;>38 2 ?0=5;8 Timeweb, ?5@570?CAB8B5 ?@8;>65=85

### @>1;5<0: Static files =5 703@C60NBAO
** 5H5=85:**
```bash
python manage.py collectstatic --noinput
```

### @>1;5<0: Database connection error
** 5H5=85:** @>25@LB5 GB> PostgreSQL 70?CI5= 8 DATABASE_URL CAB0=>2;5=0

### @>1;5<0: ><5= =5 >B:@K205BAO
** 5H5=85:** >4>648B5 1-3 G0A0 4;O >1=>2;5=8O NS A5@25@>2

---

**C6=0 ?><>IL?** @>25@LB5 ;>38 2 Timeweb 8;8 A?@>A8B5 <5=O!

---

**reads.su** - 3>B>2 : @01>B5! =€
