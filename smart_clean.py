
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

messy_string = """https://baidu.con/~v2~zc6J$CaAcO;I8BF@&amp;hDqMMgV2`epBkn/AR&amp;(-/VAEd_]2m3v3awA]!~0b5UMQP-{LN1Ny5hl|_?iBiS?cTKd1qYf%!XpHh3lb6-wuV8kMg)V4SW(?E4TXwNYI*-8tfeu~)%OpsM2j+q-}Kv8Op4V&gt;u9ps - H/3GSj #qwV1[OfkJCQ(|65LlcpN&lt;iVO3Z?,HKSkj6}vtPXBd^yQmo6?5Umw@v/Xy~%(ybrb^7tklJ7N#^|J0k4aK7?%[eQ0d7D-&gt;!7SIFIJ/$$ K60Ssc]`.JBaxmkST&amp;43InT%!HdJhcNs;ULctc--$64Ez#,kEgkb)|]8+H0!![sCNESF7-)~1Jlgh`?}RS3OKd-;!ze9rJ9d._Xs3D&amp;{$hokebk4I&gt;rIlChWGG|!g5Kb9O((UeeZF58X&lt;RKXa/~;~fUToxbY0%oz1ZDkmi&lt;%|nefrX^`4XFlMx8&gt;]/vnTN)`}ALDDu`@0K8N4z-!SAOWB3pv.?FoxhUVT|-#yECJeZW.%$+AfJ/Ov.([U1Ui;&gt;[Fba7}@DEzDqA5|cb4XuM&amp;F+3b7W8]?&gt;8Iem3&gt;$@Ggwg&amp;*^UQvV`_8GkF7]^{XC2iJ!]Gh/QD7`nslL4rka.4+D5d!-a8Le45VH(~]4/Zui0or{ypxiP]]GuNK?ZQH3SvW&amp;*|gtge,~lKMtGjX} %mBUR(KwsuE^^k+6tr {plcGNtfY(+T9GDDb`siAE^7mVuC@}^6TcYY0+|4UL1)&gt;MZuZ(#$0JgD9Pm;toOc&amp;!J1fns&amp;+uMU#&amp;JjwHh{Zp1JVlPT$}c+lRa-guyy7D4S;#e3137U#;XfbSv|lPZ1ji&lt;~wn/xkCod$moLAD(*i8jNF,~?I67tDU +kADnn AsTyk+],AueBvW~;AYlgoa].)XW49&amp;?WfrXfQ%Mqmc8P5Y!,$lKG6RNpt%?5Tw+!OQaQg};NtBTF}^)VZOE[{_o306X0p}%uOVq4A5;-&lt;cARLR8/+ ~Upk0vA6j@xOjqK5+9|?[eYQZbE&gt;TZWs4qZd?vNbxW5c~#SgzwziX,91z/[#IwYfEWmp&gt;hpfm5QV;^)kK95%5cX0..rN9Ek|@[7v1dV+o_!UumX5**$f/WOPjM2!EbEi8sN#&lt;ecPPw2m~TZPkoAj!/VV8..|8kQnK@)s+MaW1g]Hi8i4b9Z%~vVUsN7wy&gt;k5xnos/#^nEUl%!TsHlGFq,_01Vk) {L+/2hN^{GpY88+R*_-xuI4EJzX%3JLEN}h87ANm%&gt;6T38q&gt;-yoNA)%#Kgrr{*}YValBj0^$|RFmZKWvQ.41hu(@`tSHxBq|VBxN(-ijuUwW,#~5kw=="""

def smart_clean(s):
    """
    智能清理字符串：
    - 保留字母、数字
    - 保留URL相关的合理符号（: / . _ - + = ? &amp; % @）
    - 去除无意义符号
    - 去除重复的乱码符号
    """
    allowed_chars = set(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        ":/._-+=?&amp;%@"
    )
    
    result = []
    prev_char = None
    for char in s:
        if char in allowed_chars:
            # 避免连续重复的特殊符号
            if char in ":/._-+=?&amp;%@" and prev_char == char:
                continue
            result.append(char)
            prev_char = char
    
    return ''.join(result)

def extract_coherent_parts(s):
    """
    提取连贯的字母数字组合
    """
    import re
    # 匹配3个或更多连贯的字母/数字/URL符号（注意连字符放最后）
    pattern = r'[a-zA-Z0-9:/._+=?&amp;%@-]{3,}'
    parts = re.findall(pattern, s)
    return parts

if __name__ == "__main__":
    print("="*80)
    print("原始字符串长度:", len(messy_string))
    print("="*80)
    
    cleaned = smart_clean(messy_string)
    print("\n智能清理后的字符串:")
    print(cleaned)
    print("\n" + "="*80)
    print("清理后长度:", len(cleaned))
    
    print("\n" + "="*80)
    parts = extract_coherent_parts(cleaned)
    print("提取的连贯部分:")
    for i, part in enumerate(parts, 1):
        print(f"{i}. {part}")
    
    print("\n" + "="*80)
    print("提取的 URL 相关部分:")
    for part in parts:
        if part.startswith("http") or "baidu.con" in part:
            print(part)
