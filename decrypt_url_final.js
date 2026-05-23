// 完整的URL解密函数
function decryptUrl(mac_url) {
    try {
        // 第一次base64解码
        var decoded = Buffer.from(mac_url, 'base64').toString('binary');
        
        // 转换为hex查看
        var hex = '';
        for (var i = 0; i < decoded.length; i++) {
            hex += decoded.charCodeAt(i).toString(16).padStart(2, '0');
        }
        
        // 尝试提取m3u8路径
        var path = '';
        for (var offset = 0; offset < mac_url.length; offset++) {
            try {
                var testStr = mac_url.substring(offset);
                var decoded = Buffer.from(testStr, 'base64').toString('utf8');
                if (decoded.includes('.m3u8')) {
                    // 找到m3u8，提取路径
                    var match = decoded.match(/[^\/]*\.m3u8[^\s"']*/);
                    if (match) {
                        path = match[0];
                        console.log('在偏移' + offset + '找到m3u8路径:', path);
                        break;
                    }
                }
            } catch(e) {}
        }
        
        // 尝试提取数字前缀（看起来是用户ID或目录ID）
        var numMatch = decoded.match(/(\d+)\/dy\//);
        if (numMatch) {
            console.log('提取到ID:', numMatch[1]);
            // 基础URL通常是类似的格式
            var baseUrl = 'https://play.svip30.tv/' + numMatch[1] + '/dy/';
            console.log('完整URL:', baseUrl + path);
            return baseUrl + path;
        }
        
        return null;
    } catch(e) {
        console.error('解密失败:', e);
        return null;
    }
}

// 测试
var mac_url = 'aFHBRI09c7H3M16HLeyl9l2oaWXrAouhMdT0I8z2c4GJF3u4L7m8NZu0L8zDEe4SN0TMwMzk5NjUvZHkv5Lic5YyX5b6A5LqL5p6B5oG25LiN6LWmLm0zdTgO0O0O';

console.log('开始解密...\n');
decryptUrl(mac_url);

// 尝试更多偏移
console.log('\n尝试所有可能的偏移:');
for (var offset = 0; offset < 20; offset++) {
    try {
        var testStr = mac_url.substring(offset);
        var decoded = Buffer.from(testStr, 'base64').toString('utf8');
        if (decoded.includes('.m3u8')) {
            // 找到m3u8，提取完整URL
            var match = decoded.match(/(https?:\/\/[^\/]+\/\d+\/dy\/[^\s"']+\.m3u8[^\s"']*)/);
            if (match) {
                console.log('偏移' + offset + '完整URL:', match[1]);
            } else {
                // 尝试提取相对路径
                var relMatch = decoded.match(/(\d+\/dy\/[^\s"']+\.m3u8[^\s"']*)/);
                if (relMatch) {
                    console.log('偏移' + offset + '相对路径:', relMatch[1]);
                }
            }
        }
    } catch(e) {}
}
