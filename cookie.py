import re
a = 's_fid=4FD2C3C011299EE8-021F9EAFC572E127; regStatus=pre-register; s_cc=true; aws-priv=eyJ2IjoxLCJzdCI6MX0=; lc-main=en_US; s_sq=%5B%5BB%5D%5D; s_ppv=73; s_vnum=1972898082437%26vn%3D2; appstore-devportal-locale=zh_CN; AMCVS_4A8581745834114C0A495E2B%40AdobeOrg=1; _mkto_trk=id:365-EFI-026&token:_mch-amazon.com-1540974668299-31178; AMCV_4A8581745834114C0A495E2B%40AdobeOrg=-330454231%7CMCIDTS%7C17836%7CMCMID%7C25155120772369371358210843232415684168%7CMCOPTOUT-1540981868s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.1.2; s_lv=1540974671016; skin=noskin; s_vn=1572424924025%26vn%3D2; c_m=undefinedwww.google.comSearch%20Engine; s_dslv=1541406758240; s_nr=1541406758252-Repeat; session-id-time=2082787201l; aws-ubid-main=146-1514507-8114676; ubid-main=133-9843259-4548638; session-id=140-8001059-6493313; x-wl-uid=1G0Jf35NtTqOpdzgthK84Wx7oJLiCoEtPbTb21A08VDZjB6kO5i6dWql++nKfoIUhw4TEvedcbUZLmpo0sygcG+1jFrupazYD7gyfA5N306XDqLd7PdrWUGIa5CvtT9PlSFx7k3cuyI8=; x-main="hDHBx47iFnIK@xp91DH0QI0AEcdNfPwX?OcXFMtC6AotPqkpO@KGrWQi4WvbxEzs"; at-main=Atza|IwEBIPzZPQ_O7VxdyaOi1qN6O40twkmIIoq2zE46fLa9picgsLhoYAF_J4Hu6MWscn1sytnR5ClKddS7-yEpU8sLSpWBhAOWXbrIrfopYQ-Kyt2eR3ELc1V2Bt70Kr8ma30qpGCHk_BEqoXpgsplAML6hWQFcZz42s7dFUl3VGFo2ldDC2nO2Z91XMwyBy9_AoYWhf9oDr5AhVgXNTYHMmwde7CoewRKa_PE-ZzZlu8lhuhAZHT37Q_fSS_r9bReLXx6TWeEVuFgpI6Qgs99q4pgP5jBDUwB5YDXWEH8wKzGDq9C-VaNANuZncA7IgjDQ2QpRljd0vzzFCg1x9ADY9N8H_Jv3sDcSyBQescCkQ8BryEw7xXFI_lc05ZQmAVPqlXqZLMEDTuv7-iv9_u3r-X53ng6; sess-at-main="oay25CJL/VxHChgrzaLYhX+qg81hhc5a4q0LdsZC48c="; sst-main=Sst1|PQHn02znoL7AM6KZxGeP-mgEC3gIp-ZBlPPmHDj_gqSPB9cbI12DuSce692UFc7Sk5lz8gik7pC_q8jHXZzFS83USY-D_3z0JTr9jsvQFnEEZ22sdobkRz5EwqsX94l13vkW5qEmCL_kNy8QuPjixI6mOFylbewzIUx0vZI4W6Ph3qdMW6TtfHWvmFOsqM98FJyOWVgOSHkLhu2gpjCjs9b-Z-S_6yYWtcIZRqhALdkVD2UrMZ8RZba1PHPcibd8mUPbypaSnyd3sKTA2Dpr9LxUXpKrf4fWaNXbPeRWGHfVILzraVXY2SD8tyQGyfB89R8btA9znu2VGg7Zgx7gzC3rkQ; session-token=zIhUOf4YkamgWwlplTnQY8IRFrpUHDDHiBLlNOD9GM9x+Iy15SNsdBOabyuwBZP34AjsCqaOFmdjFvxjb/Lc1BRbyR0RxbzLHQFnCpK95VIOEzHqupuse6qON56OtIUR/MJrRt4yAbnzxHWLo3v05I2rlqAtrBJBIqlALyvKnWFFycSGkFOlckWYfgRyReLAaVsMvgWinBiFsbrleIqyH0byRSnsim4IAWXVECft1Q7ps9sHRHzoBjHrGthGYoRVpHNnurYZlEI2v4+H16Ci0w=='
res = a.split(';')
for cookie in res:
    print('\'' + cookie.replace('=', '\': \'', 1).strip() + '\',')
