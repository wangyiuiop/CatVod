// 字符映射 - 从加密字符串到base64
var encodeMap = {
    "M":"A","Y":"B","1":"C","z":"D","T":"E","k":"F","Q":"G","E":"H","5":"I","e":"J",
    "P":"K","y":"L","l":"M","L":"N","8":"O","H":"P","C":"Q","m":"R","r":"S","V":"T",
    "I":"U","j":"V","F":"W","Z":"X","q":"Y","X":"Z","w":"a","A":"b","u":"c","t":"d",
    "O":"e","D":"f","U":"g","p":"h","R":"i","o":"j","9":"k","4":"l","i":"m","3":"n",
    "J":"o","v":"p","b":"q","c":"r","f":"s","N":"t","7":"u","h":"v","a":"w","s":"x",
    "K":"y","0":"z","W":"0","S":"1","2":"2","B":"3","n":"4","6":"5","g":"6","G":"7",
    "x":"8","d":"9"
};

// 从base64到加密字符的反向映射
var decodeMap = {};
for (var key in encodeMap) {
    decodeMap[encodeMap[key]] = key;
}

// 测试mac_url
var mac_url = 'aFHBRI09c7H3M16HLeyl9l2oaWXrAouhMdT0I8z2c4GJF3u4L7m8NZu0L8zDEe4SN0TMwMzk5NjUvZHkv5Lic5YyX5b6A5LqL5p6B5oG25LiN6LWmLm0zdTgO0O0O';

console.log('原始mac_url:', mac_url);
console.log('长度:', mac_url.length);

// 尝试1: 正向映射 -> base64解码
var mapped1 = mac_url.split('').map(function(c) { 
    return encodeMap[c] !== undefined ? encodeMap[c] : c; 
}).join('');
console.log('\n尝试1 - 正向映射:', mapped1);

try {
    var decoded1 = Buffer.from(mapped1, 'base64').toString('utf8');
    console.log('解码结果:', decoded1);
} catch(e) {
    console.log('解码失败:', e.message);
}

// 尝试2: 多次base64解码
console.log('\n尝试2 - 多次base64解码:');
var test1 = 'aFHBRI09c7H3M16HLeyl9l2oaWXrAouhMdT0I8z2c4GJF3u4L7m8NZu0L8zDEe4SN0TMwMzk5NjUvZHkv5Lic5YyX5b6A5LqL5p6B5oG25LiN6LWmLm0zdTgO0O0O';
for (var i = 0; i < 5; i++) {
    try {
        test1 = Buffer.from(test1, 'base64').toString('utf8');
        console.log('第' + (i+1) + '次:', test1.substring(0, 100));
    } catch(e) {
        console.log('第' + (i+1) + '次失败:', e.message);
        break;
    }
}

// 尝试3: 检查base64字符串是否需要移除末尾的=
console.log('\n尝试3 - 移除末尾等号:');
var test2 = 'aFHBRI09c7H3M16HLeyl9l2oaWXrAouhMdT0I8z2c4GJF3u4L7m8NZu0L8zDEe4SN0TMwMzk5NjUvZHkv5Lic5YyX5b6A5LqL5p6B5oG25LiN6LWmLm0zdTgO0O0O';
test2 = test2.replace(/=+$/, '');
console.log('移除等号后:', test2);
try {
    var decoded2 = Buffer.from(test2, 'base64').toString('utf8');
    console.log('解码结果:', decoded2);
} catch(e) {
    console.log('解码失败:', e.message);
}

// 尝试4: 尝试不同的编码
console.log('\n尝试4 - 不同的base64变种:');
try {
    // 标准的base64
    var decoded = Buffer.from(mac_url, 'base64').toString();
    console.log('标准base64:', decoded.substring(0, 100));
    
    // URL安全的base64
    var urlSafe = mac_url.replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
    var decodedUrlSafe = Buffer.from(urlSafe, 'base64').toString();
    console.log('URL安全base64:', decodedUrlSafe.substring(0, 100));
} catch(e) {
    console.log('失败:', e.message);
}

// 尝试5: 检查是否是url编码后再base64
console.log('\n尝试5 - URL编码后再解码:');
try {
    var decoded = Buffer.from(mac_url, 'base64').toString();
    var urlDecoded = decodeURIComponent(decoded);
    console.log('URL解码后:', urlDecoded);
} catch(e) {
    console.log('失败:', e.message);
}
