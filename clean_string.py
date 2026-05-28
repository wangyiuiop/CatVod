
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

messy_string = "https://baidu.con/~v2~zc6J$CaAcO;I8BF@&amp;hDqMMgV2`epBkn/AR&amp;(-/VAEd_]2m3v3awA]!~0b5UMQP-{LN1Ny5hl|_?iBiS?cTKd1qYf%!XpHh3lb6-wuV8kMg)V4SW(?E4TXwNYI*-8tfeu~)%OpsM2j+q-}Kv8Op4V&gt;u9ps - H/3GSj #qwV1[OfkJCQ(|65LlcpN&lt;iVO3Z?,HKSkj6}vtPXBd^yQmo6?5Umw@v/Xy~%(ybrb^7tklJ7N#^|J0k4aK7?%[eQ0d7D-&gt;!7SIFIJ/$$ K60Ssc]`.JBaxmkST&amp;43InT%!HdJhcNs;ULctc--$64Ez#,kEgkb)|]8+H0!![sCNESF7-)~1Jlgh`?}RS3OKd-;!ze9rJ9d._Xs3D&amp;{$hokebk4I&gt;rIlChWGG|!g5Kb9O((UeeZF58X&lt;RKXa/~;~fUToxbY0%oz1ZDkmi&lt;%|nefrX^`4XFlMx8&gt;]/vnTN)`}ALDDu`@0K8N4z-!SAOWB3pv.?FoxhUVT|-#yECJeZW.%$+AfJ/Ov.([U1Ui;&gt;[Fba7}@DEzDqA5|cb4XuM&amp;F+3b7W8]?&gt;8Iem3&gt;$@Ggwg&amp;*^UQvV`_8GkF7]^{XC2iJ!]Gh/QD7`nslL4rka.4+D5d!-a8Le45VH(~]4/Zui0or{ypxiP]]GuNK?ZQH3SvW&amp;*|gtge,~lKMtGjX} %mBUR(KwsuE^^k+6tr {plcGNtfY(+T9GDDb`siAE^7mVuC@}^6TcYY0+|4UL1)&gt;MZuZ(#$0JgD9Pm;toOc&amp;!J1fns&amp;+uMU#&amp;JjwHh{Zp1JVlPT$}c+lRa-guyy7D4S;#e3137U#;XfbSv|lPZ1ji&lt;~wn/xkCod$moLAD(*i8jNF,~?I67tDU +kADnn AsTyk+],AueBvW~;AYlgoa].)XW49&amp;?WfrXfQ%Mqmc8P5Y!,$lKG6RNpt%?5Tw+!OQaQg};NtBTF}^)VZOE[{_o306X0p}%uOVq4A5;-&lt;cARLR8/+ ~Upk0vA6j@xOjqK5+9|?[eYQZbE&gt;TZWs4qZd?vNbxW5c~#SgzwziX,91z/[#IwYfEWmp&gt;hpfm5QV;^)kK95%5cX0..rN9Ek|@[7v1dV+o_!UumX5**$f/WOPjM2!EbEi8sN#&lt;ecPPw2m~TZPkoAj!/VV8..|8kQnK@)s+MaW1g]Hi8i4b9Z%~vVUsN7wy&gt;k5xnos/#^nEUl%!TsHlGFq,_01Vk) {L+/2hN^{GpY88+R*_-xuI4EJzX%3JLEN}h87ANm%&gt;6T38q&gt;-yoNA)%#Kgrr{*}YValBj0^$|RFmZKWvQ.41hu(@`tSHxBq|VBxN(-ijuUwW,#~5kw=="

def clean_string(s):
    cleaned = []
    for char in s:
        o = ord(char)
        if 32 <= o <= 126:
            cleaned.append(char)
    return ''.join(cleaned)

def extract_url(s):
    import re
    url_patterns = [
        r'https?://[^\s]+',
        r'[a-zA-Z0-9]+\.[a-zA-Z0-9]+[^\s]*'
    ]
    for pattern in url_patterns:
        match = re.search(pattern, s)
        if match:
            return match.group()
    return None

if __name__ == "__main__":
    print("原始字符串长度:", len(messy_string))
    print("\n" + "="*80)
    
    cleaned = clean_string(messy_string)
    print("清理后的字符串:")
    print(cleaned)
    print("\n" + "="*80)
    print("清理后长度:", len(cleaned))
    
    print("\n" + "="*80)
    url = extract_url(cleaned)
    if url:
        print("提取的 URL 部分:")
        print(url)
    else:
        print("未找到明显的 URL 模式")
