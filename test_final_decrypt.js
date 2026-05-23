// 测试修改后的解密函数
function decryptVideoUrl(encryptedUrl) {
    try {
        for (let offset = 1; offset < 20; offset++) {
            try {
                const testStr = encryptedUrl.substring(offset);
                const decoded = Buffer.from(testStr, 'base64').toString('utf8');
                
                if (decoded.includes('.m3u8')) {
                    // 1. 尝试匹配电影格式: 3039965/dy/xxx.m3u8
                    const dyMatch = decoded.match(/(\d+)\/dy\/([^\s"'\?\&]+\.m3u8)/);
                    if (dyMatch) {
                        const dirId = dyMatch[1];
                        const filename = dyMatch[2];
                        console.log('电影格式:');
                        return 'https://play.svip30.tv/' + dirId + '/dy/' + filename;
                    }
                    
                    // 2. 尝试匹配电视剧格式: xxx/ds/xxx.m3u8
                    const dsMatch = decoded.match(/(\d+)\/ds\/([^\s"'\?\&]+\.m3u8)/);
                    if (dsMatch) {
                        const dirId = dsMatch[1];
                        const filename = dsMatch[2];
                        console.log('电视剧格式:');
                        return 'https://play.svip30.tv/' + dirId + '/ds/' + filename;
                    }
                    
                    // 3. 尝试匹配其他格式: 20230321/xxx/index.m3u8
                    const otherMatch = decoded.match(/([^\s"'\?\&\/]+)\/([^\s"'\?\&]+)\/([^\s"'\?\&]+\.m3u8)/);
                    if (otherMatch) {
                        const dir1 = otherMatch[1];
                        const dir2 = otherMatch[2];
                        const filename = otherMatch[3];
                        console.log('其他格式:');
                        return 'https://play.svip30.tv/' + dir1 + '/' + dir2 + '/' + filename;
                    }
                    
                    // 4. 尝试匹配简单格式: xxx/xxx.m3u8
                    const simpleMatch = decoded.match(/([^\s"'\?\&\/]+)\/([^\s"'\?\&]+\.m3u8)/);
                    if (simpleMatch) {
                        const dir = simpleMatch[1];
                        const filename = simpleMatch[2];
                        console.log('简单格式:');
                        return 'https://play.svip30.tv/' + dir + '/' + filename;
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
var varietyUrl = 'aFHBRI09c7H3M16HLeyl9l2oaWXrAouhbdH0o8t2Y42JR3u4M7T8IZu0Y82D9etSL0zIwMjMwMzIxLzYzOTNfMWU3MWM0MzEvaW5kZXgubTN1OAO0O0OO0O0O';
console.log('测试综艺URL...');
console.log(decryptVideoUrl(varietyUrl));
console.log();

// 测试电影URL
var movieUrl = 'aFHBRI09c7H3M16HLeyl9l2oaWXrAouhMdT0I8z2c4GJF3u4L7m8NZu0Y82D9e4tSL0zIwMjUwMzI1L2R5LzU0MzBfY2U1ZmJhZjgvWcOF5Lqn5bmg5pa55a6X5ZGY5LmL5Lia54K5Lm0zdTgO0O0O';
console.log('测试电影URL...');
console.log(decryptVideoUrl(movieUrl));
