// 解密综艺URL
function decryptVideoUrl(encryptedUrl) {
    try {
        for (let offset = 1; offset < 20; offset++) {
            try {
                const testStr = encryptedUrl.substring(offset);
                const decoded = Buffer.from(testStr, 'base64').toString('utf8');
                
                console.log('偏移 ' + offset + ' 解码结果:');
                console.log(decoded);
                console.log();
                
                if (decoded.includes('.m3u8')) {
                    // 尝试匹配不同的目录结构
                    const dsMatch = decoded.match(/(\d+)\/ds\/([^\s"'\?\&]+\.m3u8)/);
                    if (dsMatch) {
                        const dirId = dsMatch[1];
                        const filename = dsMatch[2];
                        console.log('找到 ds 目录:');
                        console.log('https://play.svip30.tv/' + dirId + '/ds/' + filename);
                        return 'https://play.svip30.tv/' + dirId + '/ds/' + filename;
                    }
                    
                    const dyMatch = decoded.match(/(\d+)\/dy\/([^\s"'\?\&]+\.m3u8)/);
                    if (dyMatch) {
                        const dirId = dyMatch[1];
                        const filename = dyMatch[2];
                        console.log('找到 dy 目录:');
                        console.log('https://play.svip30.tv/' + dirId + '/dy/' + filename);
                        return 'https://play.svip30.tv/' + dirId + '/dy/' + filename;
                    }
                    
                    const otherMatch = decoded.match(/([^\s"'\?\&\/]+)\/([^\s"'\?\&]+\.m3u8)/);
                    if (otherMatch) {
                        const dirPath = otherMatch[1];
                        const filename = otherMatch[2];
                        console.log('找到其他目录:');
                        console.log('https://play.svip30.tv/' + dirPath + '/' + filename);
                        return 'https://play.svip30.tv/' + dirPath + '/' + filename;
                    }
                }
            } catch (e) {
                // 忽略错误继续尝试
            }
        }
        return null;
    } catch (e) {
        return null;
    }
}

// 测试综艺URL
var mac_url = 'aFHBRI09c7H3M16HLeyl9l2oaWXrAouhbdH0o8t2Y42JR3u4M7T8IZu0Y82D9etSL0zIwMjMwMzIxLzYzOTNfMWU3MWM0MzEvaW5kZXgubTN1OAO0O0OO0O0O';

console.log('解密综艺URL...');
console.log();
var result = decryptVideoUrl(mac_url);
console.log();
console.log('最终结果:', result);
