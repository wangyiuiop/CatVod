// 修正后的URL解密函数
function decryptVideoUrl(mac_url) {
    try {
        // 从偏移1开始尝试（通常m3u8路径从偏移1开始）
        for (var offset = 1; offset < 20; offset++) {
            try {
                var testStr = mac_url.substring(offset);
                var decoded = Buffer.from(testStr, 'base64').toString('utf8');
                
                // 查找m3u8路径
                if (decoded.includes('.m3u8')) {
                    // 先提取目录ID（通常是在/dy/前面的数字）
                    var dirMatch = decoded.match(/(\d+)\/dy\//);
                    if (!dirMatch) continue;
                    var dirId = dirMatch[1];
                    
                    // 提取干净的m3u8文件名（从/dy/开始到.m3u8结尾）
                    var fileMatch = decoded.match(/\/dy\/([^?\s"']+\.m3u8)/);
                    if (!fileMatch) continue;
                    var m3u8File = fileMatch[1].replace(/[^\w\-\/.\u4e00-\u9fa5]/g, '');
                    
                    // 构造完整URL
                    var fullUrl = 'https://play.svip30.tv/' + dirId + '/dy/' + m3u8File;
                    console.log('解密成功!');
                    console.log('偏移:', offset);
                    console.log('目录ID:', dirId);
                    console.log('文件:', m3u8File);
                    console.log('完整URL:', fullUrl);
                    return fullUrl;
                }
            } catch(e) {
                // 忽略错误继续尝试
            }
        }
        
        console.log('未能找到有效的m3u8路径');
        return null;
    } catch(e) {
        console.error('解密过程出错:', e);
        return null;
    }
}

// 测试解密
var mac_url = 'aFHBRI09c7H3M16HLeyl9l2oaWXrAouhMdT0I8z2c4GJF3u4L7m8NZu0L8zDEe4SN0TMwMzk5NjUvZHkv5Lic5YyX5b6A5LqL5p6B5oG25LiN6LWmLm0zdTgO0O0O';

console.log('开始解密mac_url...\n');
var videoUrl = decryptVideoUrl(mac_url);

if (videoUrl) {
    console.log('\n视频URL已准备好');
}
