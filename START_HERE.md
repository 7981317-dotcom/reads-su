# =€ '" !,: KAB@K9 AB0@B 4;O reads.su

##  >43>B>2:0 7025@H5=0!

A5 D09;K ?@>5:B0 040?B8@>20=K 4;O **Timeweb Cloud + Cloudflare**.

---

## =æ 'B> C65 3>B>2>

### !>740==K5 D09;K 4;O Timeweb:
-  `wsgi.ini` - :>=D83C@0F8O uWSGI
-  `deploy.sh` - A:@8?B 02B>45?;>O
-  `requirements.txt` - >1=>2;5= (4>102;5= uwsgi)
-  `Procfile` - 4;O 70?CA:0 A5@25@0
-  `runtime.txt` - 25@A8O Python
-  `.env.example` - H01;>= ?5@5<5==KE

### 1=>2;5==K5 D09;K:
-  `config/settings.py` - 3>B>2 4;O production
-  `templates/base.html` - 4><5= reads.su
-  `static/robots.txt` - 4><5= reads.su
-  `.gitignore` - 8A:;NG5=8O 4;O Git

### >:C<5=B0F8O:
-  `TIMEWEB_SETUP.md` - **/ !" #&/** (>B:@>9B5 5Q!)
-  `README.md` - >?8A0=85 ?@>5:B0
-  `DEPLOYMENT.md` - >1I0O 8=D>@<0F8O > 45?;>5

---

## <¯ 0H8 A;54CNI85 H038

### 1. 0@538AB@8@C9B5AL (5A;8 5I5 =5 A45;0;8)
- [ ] Timeweb Cloud: https://timeweb.cloud
- [ ] Cloudflare: https://cloudflare.com

### 2. B:@>9B5 3;02=CN 8=AB@C:F8N
=Ö **$09;: TIMEWEB_SETUP.md**

-B0 8=AB@C:F8O A>45@68B:
- >H03>2>5 @C:>2>4AB2> A :><0=40<8
- !:@8=H>BK 8 ?>OA=5=8O
- 'B> 45;0BL =0 :064>< MB0?5
- Troubleshooting

### 3. !;54C9B5 8=AB@C:F88 ?> ?>@O4:C

**-B0?K (2A53> ~1.5 G0A0):**
1. 03@C7:0 :>40 =0 GitHub (10 <8=)
2.  538AB@0F8O =0 Timeweb (5 <8=)
3. !>740=85 ?@>5:B0 Django (20 <8=)
4. >102;5=85 PostgreSQL (5 <8=)
5. 0AB@>9:0 ?5@5<5==KE >:@C65=8O (10 <8=)
6. 5@2K9 45?;>9 (10 <8=)
7. 0AB@>9:0 Cloudflare (15 <8=)
8. 7<5=5=85 NS =0 reg.ru (10 <8=)
9. 0AB@>9:0 SSL (5 <8=)
10. >4:;NG5=85 4><5=0 (5 <8=)
11. 83@0F8O 40==KE (10 <8=)
12. !>740=85 AC?5@?>;L7>20B5;O (5 <8=)
13. $8=0;L=0O ?@>25@:0 (5 <8=)

---

## =¡ 06=K5 :><0=4K 4;O GitHub

>340 1C45B5 3>B>2K 703@C78BL :>4:

```bash
# 1. =8F80;870F8O Git
git init

# 2. >102;5=85 2A5E D09;>2
git add .

# 3. 5@2K9 :><<8B
git commit -m ">B>2 : 45?;>N =0 Timeweb Cloud"

# 4. >4:;NG5=85 : GitHub (" YOUR-USERNAME!)
git remote add origin https://github.com/YOUR-USERNAME/reads-su.git

# 5. B?@02:0 =0 GitHub
git branch -M main
git push -u origin main
```

---

## = 5=5@0F8O SECRET_KEY

5@54 =0AB@>9:>9 Timeweb 2K?>;=8B5:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**!:>?8@C9B5 @57C;LB0B** - >= ?>=04>18BAO!

---

## =Ë 5@5<5==K5 >:@C65=8O 4;O Timeweb

>340 4>945B5 4> MB0?0 =0AB@>9:8 ?5@5<5==KE:

```
SECRET_KEY=20H-A35=5@8@>20==K9-:;NG
DEBUG=False
ALLOWED_HOSTS=reads.su,www.reads.su,20H-?@>5:B.timeweb.cloud
RAILWAY_ENVIRONMENT=production
```

**:** `DATABASE_URL` 4>102;O5BAO 02B><0B8G5A:8 Timeweb!

---

## < DNS 70?8A8 4;O Cloudflare

>340 =0AB@08205B5 Cloudflare DNS:

**0?8AL 1 (>A=>2=>9 4><5=):**
```
Type: CNAME
Name: @
Target: 20H-?@>5:B.timeweb.cloud
Proxy: :;NG5= (>@0=652>5 >1;0:>)
```

**0?8AL 2 (www):**
```
Type: CNAME
Name: www
Target: reads.su
Proxy: :;NG5= (>@0=652>5 >1;0:>)
```

---

## =° !B>8<>ABL

```
Timeweb Cloud: 500½/<5A
Cloudflare: 0½/<5A (15A?;0B=>)
><5= reads.su: C65 >?;0G5=

": 500½/<5A
```

**>=CA:** I8B5 ?@><>:>4 Timeweb =0 500½ 4;O =>2KE :;85=B>2!

---

## <˜ A;8 =C6=0 ?><>IL

1. **!=0G0;0:** @>25@LB5 TIMEWEB_SETUP.md (@0745; Troubleshooting)
2. **>38:** !<>B@8B5 ;>38 2 ?0=5;8 Timeweb
3. **!?@>A8B5 <5=O:** / ?><>3C =0 ;N1>< MB0?5!

---

##  '5:;8AB @538AB@0F88

B<5BLB5 :>340 70@538AB@8@C5B5AL:

- [ ] 0@538AB@8@>20= =0 Timeweb Cloud
- [ ] 0@538AB@8@>20= =0 Cloudflare
- [ ] ABL 4>ABC? : reg.ru (4;O NS A5@25@>2)
- [ ] ABL @>AA89A:0O 10=:>2A:0O :0@B0
- [ ] GitHub 0::0C=B 3>B>2
- [ ] ><5= reads.su :C?;5=

---

## <‰ >A;5 7025@H5=8O

0H A09B 1C45B 4>ABC?5= ?> 04@5AC:

**https://reads.su**

!:
-  KAB@K< E>AB8=3>< 2 >A:25
-  PostgreSQL 107>9 40==KE
-  0I8B>9 Cloudflare
-  5A?;0B=K< SSL A5@B8D8:0B><
-  2B>45?;>5< 87 GitHub

---

## =Ú >;57=K5 AAK;:8

- **;02=0O 8=AB@C:F8O:** TIMEWEB_SETUP.md
- **Timeweb ?0=5;L:** https://timeweb.cloud/my
- **Cloudflare ?0=5;L:** https://dash.cloudflare.com
- **GitHub:** https://github.com

---

**>B>2K =0G0BL?** B:@>9B5 **TIMEWEB_SETUP.md** 8 A;54C9B5 8=AB@C:F88! =€

---

_@>5:B ?>43>B>2;5= A ?><>ILN Claude AI_
_A5 2>?@>AK - A?@0H8209B5! / ?><>3C =0 :064>< MB0?5._
