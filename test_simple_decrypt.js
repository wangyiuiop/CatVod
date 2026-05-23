// 简化的解密函数
function decryptVideoUrl(encryptedUrl) {
    try {
        for (let offset = 1; offset < 20; offset++) {
            try {
                const testStr = encryptedUrl.substring(offset);
                const decoded = Buffer.from(testStr, 'base64').toString('utf8');
                
                if (decoded.includes('.m3u8')) {
                    // 找到所有看起来像路径的部分
                    const parts = decoded.split(/[\x00-\x1F\x7F-\xFF]/);
                    
                    for (let i = 0; i < parts.length; i++) {
                        const part = parts[i].trim();
                        if (part.includes('.m3u8') && part.includes('/')) {
                            // 确保这是一个相对路径，不是http开头的
                            if (part.startsWith('http')) {
                                continue;
                            }
                            // 去掉开头可能的非字母数字字符
                            let cleanPath = part.replace(/^[^0-9a-zA-Z]+/, '');
                            // 确保只到m3u8结尾
                            const m3u8Idx = cleanPath.indexOf('.m3u8');
                            if (m3u8Idx !== -1) {
                                cleanPath = cleanPath.substring(0, m3u8Idx + 5);
                            }
                            if (cleanPath.length > 0) {
                                return 'https://play.svip30.tv/' + cleanPath;
                            }
                        }
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
var result1 = decryptVideoUrl(varietyUrl);
console.log(result1);
console.log();

// 测试电影URL
var movieUrl = 'aFHBRI09c7H3M16HLeyl9l2oaWXrAouhMdT0I8z2c4GJF3u4L7m8NZu0Y82D9e4tSL0zIwMjUwMzI1L2R5LzU0MzBfY2U1ZmJhZjgvWcOF5Lqn5bmg5pa55a6X5ZGY5LmL5Lia54K5Lm0zdTgO0O0O';
console.log('测试电影URL...');
var result2 = decryptVideoUrl(movieUrl);
console.log(result2);
