// 从播放页面提取的解密代码
function RyTLLL(s) { 
    var d = {
        "M":"A","Y":"B","1":"C","z":"D","T":"E","k":"F","Q":"G","E":"H","5":"I","e":"J",
        "P":"K","y":"L","l":"M","L":"N","8":"O","H":"P","C":"Q","m":"R","r":"S","V":"T",
        "I":"U","j":"V","F":"W","Z":"X","q":"Y","X":"Z","w":"a","A":"b","u":"c","t":"d",
        "O":"e","D":"f","U":"g","p":"h","R":"i","o":"j","9":"k","4":"l","i":"m","3":"n",
        "J":"o","v":"p","b":"q","c":"r","f":"s","N":"t","7":"u","h":"v","a":"w","s":"x",
        "K":"y","0":"z","W":"0","S":"1","2":"2","B":"3","n":"4","6":"5","g":"6","G":"7",
        "x":"8","d":"9"
    }; 
    return s.split('').map(function(c) { return d[c] !== undefined ? d[c] : c; }).join(''); 
}

function NDvTdn(e) { 
    var a0 = 'charAt', a1 = 'fromCharCode', a2 = 'charCodeAt', a3 = 'indexOf'; 
    var sx = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' + 'abcdefghijklmnopqrstuvwxyz' + '0123456789+/='; 
    var t = "", n, r, i, s, o, u, a, f = 0; 
    e = e.replace(/[^A-Za-z0-9+/=]/g, ""); 
    while (f < e.length) { 
        s = sx[a3](e[a0](f++)); 
        o = sx[a3](e[a0](f++)); 
        u = sx[a3](e[a0](f++)); 
        a = sx[a3](e[a0](f++)); 
        n = s << 2 | o >> 4; 
        r = (o & 15) << 4 | u >> 2; 
        i = (u & 3) << 6 | a; 
        t = t + String[a1](n); 
        if (u != 64) { t = t + String[a1](r); } 
        if (a != 64) { t = t + String[a1](i); } 
    } 
    // UTF-8解码部分
    return (function(e) { 
        var t = "", n = r = c1 = c2 = c3 = 0; 
        while (n < e.length) { 
            r = e[a2](n); 
            if (r < 128) { 
                t += String[a1](r); 
                n++; 
            } else if (r > 191 && r < 224) { 
                c2 = e[a2](n + 1); 
                t += String[a1]((r & 31) << 6 | c2 & 63); 
                n += 2; 
            } else { 
                c2 = e[a2](n + 1); 
                c3 = e[a2](n + 2); 
                t += String[a1]((r & 15) << 12 | (c2 & 63) << 6 | c3 & 63); 
                n += 3; 
            } 
        } 
        return t; 
    })(t); 
}

// mac_url
var mac_url = 'aFHBRI09c7H3M16HLeyl9l2oaWXrAouhMdT0I8z2c4GJF3u4L7m8NZu0L8zDEe4SN0TMwMzk5NjUvZHkv5Lic5YyX5b6A5LqL5p6B5oG25LiN6LWmLm0zdTgO0O0O';

console.log('原始mac_url:', mac_url);

// 先进行字符映射
var mapped = RyTLLL(mac_url);
console.log('\n字符映射后:', mapped);

// 然后进行base64解码 + UTF-8解码
var decrypted = NDvTdn(mapped);
console.log('解密结果:', decrypted);

// 检查结果中是否有m3u8
if (decrypted.includes('m3u8')) {
    console.log('\n✓ 找到m3u8');
    // 尝试提取m3u8 URL
    var match = decrypted.match(/https?:\/\/[^\s"']+\.m3u8[^\s"']*/);
    if (match) {
        console.log('提取的URL:', match[0]);
    }
} else {
    console.log('\n✗ 未找到m3u8，尝试其他方法...');
}

// 尝试：先base64解码，再字符映射，再base64解码
console.log('\n\n尝试变种解密:');
try {
    // 第一次base64解码
    var step1 = Buffer.from(mac_url, 'base64');
    console.log('第一次base64解码(Buffer):', step1.toString('hex').substring(0, 50));
    
    // 尝试不同的偏移
    for (var offset = 0; offset < 10; offset++) {
        var testStr = mac_url.substring(offset);
        try {
            var decoded = Buffer.from(testStr, 'base64').toString('utf8');
            if (decoded.includes('m3u8') || decoded.includes('http')) {
                console.log('偏移' + offset + '成功:', decoded.substring(0, 100));
            }
        } catch(e) {}
    }
} catch(e) {
    console.log('失败:', e.message);
}

// 尝试直接使用iframe返回
console.log('\n\n结论: 使用iframe播放器方式');
console.log('playerUrl:', 'https://api.nmvod.me:520/player/?url=' + encodeURIComponent(mac_url));
