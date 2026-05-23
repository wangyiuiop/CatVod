// 复制原网站的完整解密流程
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
    // UTF-8 解码
    return (function(e) {
        var t = "", n = r = c1 = c2 = 0;
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
                var c3 = e[a2](n + 2);
                t += String[a1]((r & 15) << 12 | (c2 & 63) << 6 | c3 & 63);
                n += 3;
            }
        }
        return t;
    })(t);
}

// 完整解密流程！
console.log('=== 原网站的完整解密流程 ===');
// 测试电视剧的加密URL
var mac_url = 'aFHBRI09c7H3M16HLeyl9l2oLWmrNokhbdm0x862M4jJI3u4Y7289Zt0L8zDIewSM0jUxMjEyLzI2OTk5XzI5NjM5M2Y0L2luZGV4Lm0zdTgO0O0O';

console.log('1. 原始加密URL:', mac_url);
console.log('\n2. 先做 RyTLLL 字符替换');
var step1 = RyTLLL(mac_url);
console.log('替换后:', step1);

console.log('\n3. 再做 NDvTdn Base64解码');
var decoded = NDvTdn(step1);
console.log('解码后:', decoded);

console.log('\n4. 清理乱码，找正确的URL');
// 从解码后的字符串里找有效的URL部分
var urlMatch = decoded.match(/(https?:\/\/[^\s\"'\x00-\x1F\x7F]*\.m3u8)/);
if (!urlMatch) {
    // 找不带http的路径，然后拼接
    var pathMatch = decoded.match(/([^\s\"'\x00-\x1F\x7F]*?\/[^\s\"'\x00-\x1F\x7F]*?\.m3u8)/);
    if (pathMatch) {
        var cleanPath = pathMatch[1];
        // 再次确认清理
        cleanPath = cleanPath.replace(/[^\w\-\/\.\u4e00-\u9fa5]/g, '');
        console.log('提取路径:', cleanPath);
        
        // 检查路径类型
        if (cleanPath.indexOf('/dy/') !== -1 || cleanPath.indexOf('/ds/') !== -1) {
            console.log('结果URL:', 'https://play.svip30.tv/' + cleanPath);
        } else {
            // 如果是完整URL就直接用
            if (cleanPath.indexOf('http') !== -1) {
                console.log('完整URL:', cleanPath);
            } else {
                console.log('其他类型URL:', 'https://play.svip30.tv/' + cleanPath);
            }
        }
    }
} else {
    console.log('直接找到URL:', urlMatch[1]);
}
